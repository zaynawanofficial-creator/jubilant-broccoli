<?php
/**
 * Plugin Name:       RankRight Site
 * Description:       RankRight Media site plugin: registers the RankRight theme, imports pages, service packages (WooCommerce), blog posts and media, and adds the contact form, schema and security hardening.
 * Version:           1.0.0
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            RankRight Media
 * License:           GPL-2.0-or-later
 * Text Domain:       rankright
 */

defined( 'ABSPATH' ) || exit;

define( 'RRM_FILE', __FILE__ );
define( 'RRM_DIR', __DIR__ );
define( 'RRM_WP', __DIR__ . '/wordpress' );

// The theme ships inside this plugin so one Git deploy updates both.
register_theme_directory( RRM_WP . '/theme' );

// Keep the stored theme root pointing at this plugin's real location (it changes if the plugin folder is moved/renamed).
add_action(
	'plugins_loaded',
	function () {
		$root = str_replace( wp_normalize_path( WP_CONTENT_DIR ), '', wp_normalize_path( RRM_WP . '/theme' ) );
		foreach ( array( 'stylesheet', 'template' ) as $k ) {
			if ( 'rankright' === get_option( $k ) && get_option( $k . '_root' ) !== $root ) {
				update_option( $k . '_root', $root );
				delete_site_transient( 'theme_roots' );
			}
		}
	},
	0
);

require_once RRM_WP . '/inc/helpers.php';
require_once RRM_WP . '/inc/security.php';
require_once RRM_WP . '/inc/importer.php';
require_once RRM_WP . '/inc/shortcodes.php';
require_once RRM_WP . '/inc/contact.php';
require_once RRM_WP . '/inc/seo.php';
require_once RRM_WP . '/inc/order.php';

register_activation_hook( __FILE__, 'rrm_activate' );
function rrm_activate() {
	delete_option( 'rrm_import_state' );
	if ( get_stylesheet() !== 'rankright' ) {
		switch_theme( 'rankright' );
	}
	update_option( 'rrm_flush_rewrite', 1 );
}
