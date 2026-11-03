<?php
/**
 * Contact form handler. Every enquiry is saved as a private "Lead" (so nothing is lost if email fails)
 * and emailed to the site admin address. Spam defence: honeypot, time-trap, per-IP rate limit.
 * No nonce on purpose: pages are cacheable and nonces in cached HTML expire.
 */
defined( 'ABSPATH' ) || exit;

add_action(
	'init',
	function () {
		register_post_type(
			'rrm_lead',
			array(
				'labels'          => array( 'name' => 'Leads', 'singular_name' => 'Lead' ),
				'public'          => false,
				'show_ui'         => true,
				'show_in_menu'    => true,
				'menu_icon'       => 'dashicons-email-alt',
				'supports'        => array( 'title', 'editor' ),
				'capability_type' => 'post',
				'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
				'map_meta_cap'    => true,
			)
		);
	}
);

add_action( 'admin_post_nopriv_rrm_contact', 'rrm_handle_contact' );
add_action( 'admin_post_rrm_contact', 'rrm_handle_contact' );

function rrm_handle_contact() {
	$back = home_url( '/contact-us/' );
	$ok   = home_url( '/thank-you/' );
	// phpcs:disable WordPress.Security.NonceVerification
	$p = wp_unslash( $_POST );
	// phpcs:enable
	$ts = isset( $p['ts'] ) ? (int) $p['ts'] : 0;
	if ( ! empty( $p['company'] ) || ( $ts > 0 && ( time() - $ts ) < 3 ) ) {
		wp_safe_redirect( $ok, 303 );
		exit;
	}
	$ip_key = 'rrm_rl_' . md5( isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '' );
	$hits   = (int) get_transient( $ip_key );
	if ( $hits >= 5 ) {
		wp_safe_redirect( add_query_arg( 'sent', '0', $back ) . '#enquiry', 303 );
		exit;
	}
	set_transient( $ip_key, $hits + 1, HOUR_IN_SECONDS );

	$name    = sanitize_text_field( isset( $p['name'] ) ? $p['name'] : '' );
	$email   = sanitize_email( isset( $p['email'] ) ? $p['email'] : '' );
	$company = sanitize_text_field( isset( $p['company_name'] ) ? $p['company_name'] : '' );
	$phone   = preg_replace( '/[^0-9+()\s-]/', '', sanitize_text_field( isset( $p['phone'] ) ? $p['phone'] : '' ) );
	$website = esc_url_raw( isset( $p['website'] ) ? $p['website'] : '' );
	$package = sanitize_key( isset( $p['package'] ) ? $p['package'] : '' );
	$message = sanitize_textarea_field( isset( $p['message'] ) ? $p['message'] : '' );
	$consent = isset( $p['consent'] ) && 'yes' === $p['consent'];

	if ( '' === $name || ! is_email( $email ) || '' === $message || ! $consent ) {
		wp_safe_redirect( add_query_arg( 'sent', '0', $back ) . '#enquiry', 303 );
		exit;
	}
	$body = "Name: {$name}\nCompany: {$company}\nEmail: {$email}\nPhone: {$phone}\nWebsite: {$website}\nPackage: {$package}\n\nMessage:\n{$message}\n";
	wp_insert_post(
		array(
			'post_type'    => 'rrm_lead',
			'post_status'  => 'private',
			'post_title'   => sprintf( '%s — %s', $name, $package ? $package : 'general' ),
			'post_content' => $body,
		)
	);
	wp_mail(
		get_option( 'admin_email' ),
		sprintf( 'New enquiry: %s — %s', $package ? $package : 'general', $name ),
		$body . "\n--\nSent from " . home_url(),
		array( 'Reply-To: ' . $name . ' <' . $email . '>' )
	);
	wp_safe_redirect( $ok, 303 );
	exit;
}
