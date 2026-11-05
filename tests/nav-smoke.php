<?php
/**
 * Smoke test for the theme navigation (inc/nav.php) with minimal WordPress stubs.
 * Run: php tests/nav-smoke.php
 */
define( 'ABSPATH', '/' );
define( 'SBT_VERSION', 'test' );
$_SERVER['REQUEST_URI'] = '/services/local-seo/';
function __( $s ) { return $s; }
function esc_html__( $s ) { return htmlspecialchars( $s ); }
function esc_attr__( $s ) { return htmlspecialchars( $s ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s ); }
function esc_url_raw( $s ) { return $s; }
function wp_unslash( $s ) { return $s; }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function home_url( $p = '/' ) { return 'https://example.test' . $p; }
function trailingslashit( $s ) { return rtrim( $s, '/' ) . '/'; }
function apply_filters( $h, $v ) { return $v; }
function is_singular( $t = '' ) { return false; }
function is_category() { return false; }
function is_tag() { return false; }
function add_action( ...$a ) {}
function add_shortcode( ...$a ) {}
function has_custom_logo() { return false; }
function get_bloginfo( $k ) { return 'SEO Booster'; }
function wc_get_page_permalink( $p ) { return 'https://example.test/my-account/'; }
require __DIR__ . '/../wp-content/themes/seo-booster/inc/nav.php';

$fail = 0;
function check( string $name, bool $ok ): void {
	global $fail;
	echo ( $ok ? 'PASS ' : 'FAIL ' ) . $name . "\n";
	$fail += $ok ? 0 : 1;
}

$nav = sbt_unraw( sbt_nav_shortcode() );
$tog = sbt_unraw( '<p>' . sbt_nav_toggle_shortcode() . '</p>' );
ob_start();
sbt_drawer();
$drawer = ob_get_clean();

check( 'desktop menu has 7 top-level items', 7 === substr_count( $nav, 'class="sb-nav__item' ) );
check( 'mega panel lists all 20 service pages', 20 === substr_count( $nav, 'class="sb-mega__link"' ) );
check( 'drawer lists all 20 service pages', 20 === substr_count( $drawer, 'class="sb-drawer__sublink"' ) );
check( 'current page marked aria-current', str_contains( $nav, 'href="https://example.test/services/local-seo/" aria-current="page"' ) );
check( 'Services marked active on a service page', str_contains( $nav, 'has-mega is-active' ) );
check( 'Services group open in drawer on a service page', str_contains( $drawer, '<details open>' ) );
check( 'toggle unwrapped from <p> after wpautop', str_starts_with( $tog, '<div class="sb-burger-wrap">' ) );
check( 'drawer starts hidden and is a modal dialog', str_contains( $drawer, 'role="dialog" aria-modal="true"' ) && str_contains( $drawer, ' hidden>' ) );
check( 'no placeholder left behind', ! str_contains( $nav . $tog, 'sbt-raw' ) );

echo $fail ? "\n{$fail} FAILED\n" : "\nALL PASSED\n";
exit( $fail ? 1 : 0 );
