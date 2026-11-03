<?php
/**
 * RankRight Media — contact form handler (PHP 8+, no dependencies).
 * Security: POST-only, same-origin check, honeypot + time-trap, strict validation,
 * header-injection safe, per-IP rate limit, no user data echoed back.
 *
 * SETUP: set MAIL_TO to the inbox that should receive enquiries.
 *        On Hostinger, MAIL_FROM must be a mailbox on this domain (create it in hPanel > Emails).
 */
declare(strict_types=1);

const MAIL_TO      = 'CHANGE-ME@rankrightmedia.uk';   // TODO: real inbox
const MAIL_FROM    = 'no-reply@rankrightmedia.uk';    // TODO: mailbox on this domain
const SITE_ORIGIN  = 'https://rankrightmedia.uk';
const MIN_SECONDS  = 3;      // faster than this = bot
const MAX_PER_HOUR = 5;      // per IP

header('X-Robots-Tag: noindex');
header('Cache-Control: no-store');

function back(string $to): never { header('Location: ' . $to, true, 303); exit; }
function clean(string $v, int $max): string {
    $v = trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v));
    return mb_substr(strip_tags($v), 0, $max);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { back('/contact-us/'); }

// Same-origin only (blocks cross-site form posts)
$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
if ($origin !== '' && strpos($origin, SITE_ORIGIN) !== 0) { back('/contact-us/?sent=0'); }

// Honeypot + time trap: pretend success so bots learn nothing
$ts = (int)($_POST['ts'] ?? 0);
if (!empty($_POST['company']) || ($ts > 0 && (time() - $ts) < MIN_SECONDS)) { back('/thank-you/'); }

// Simple per-IP rate limit (file based, outside web root where possible)
$ip   = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$dir  = sys_get_temp_dir() . '/rrm-rate';
@mkdir($dir, 0700, true);
$file = $dir . '/' . hash('sha256', $ip);
$hits = array_filter(array_map('intval', @file($file, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > time() - 3600);
if (count($hits) >= MAX_PER_HOUR) { back('/contact-us/?sent=0'); }
$hits[] = time();
@file_put_contents($file, implode("\n", $hits), LOCK_EX);

// Validate
$name    = clean((string)($_POST['name'] ?? ''), 100);
$email   = filter_var(trim((string)($_POST['email'] ?? '')), FILTER_VALIDATE_EMAIL) ?: '';
$phone   = preg_replace('/[^0-9+()\s-]/', '', clean((string)($_POST['phone'] ?? ''), 40));
$website = filter_var(trim((string)($_POST['website'] ?? '')), FILTER_VALIDATE_URL) ?: '';
$package = preg_replace('/[^a-z0-9-]/', '', strtolower((string)($_POST['package'] ?? '')));
$message = mb_substr(strip_tags(trim((string)($_POST['message'] ?? ''))), 0, 5000);
$consent = ($_POST['consent'] ?? '') === 'yes';

if ($name === '' || $email === '' || $message === '' || !$consent) { back('/contact-us/?sent=0#enquiry'); }

$body = "New enquiry from rankrightmedia.uk\n\n"
      . "Name:    {$name}\nEmail:   {$email}\nPhone:   {$phone}\nWebsite: {$website}\nPackage: {$package}\n\n"
      . "Message:\n{$message}\n\n--\nIP: {$ip}\nTime: " . gmdate('c') . "\n";

$headers = [
    'From'         => 'RankRight Media Website <' . MAIL_FROM . '>',
    'Reply-To'     => $email,
    'Content-Type' => 'text/plain; charset=UTF-8',
    'X-Mailer'     => 'rrm-site',
];
$subject = '=?UTF-8?B?' . base64_encode('New enquiry: ' . ($package ?: 'general') . ' — ' . $name) . '?=';

$ok = @mail(MAIL_TO, $subject, $body, $headers, '-f' . MAIL_FROM);
back($ok ? '/thank-you/' : '/contact-us/?sent=0#enquiry');
