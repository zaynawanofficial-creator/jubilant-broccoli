<?php
/**
 * Plugin Name:       SEO Booster Core
 * Description:       Service packages, package groups, post-purchase project briefs and service order workflow for SEO Booster (WooCommerce).
 * Version:           0.1.1
 * Requires at least: 6.5
 * Requires PHP:      8.1
 * Requires Plugins:  woocommerce
 * Author:            SEO Booster
 * Text Domain:       seo-booster-core
 * License:           GPL-2.0-or-later
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

define( 'SB_CORE_VERSION', '0.1.1' );
define( 'SB_CORE_FILE', __FILE__ );
define( 'SB_CORE_DIR', plugin_dir_path( __FILE__ ) );
define( 'SB_CORE_URL', plugin_dir_url( __FILE__ ) );

require_once SB_CORE_DIR . 'includes/class-sb-packages.php';
require_once SB_CORE_DIR . 'includes/class-sb-shortcode.php';
require_once SB_CORE_DIR . 'includes/class-sb-orders.php';
require_once SB_CORE_DIR . 'includes/class-sb-brief.php';
require_once SB_CORE_DIR . 'includes/class-sb-importer.php';

// Declare HPOS + cart/checkout blocks compatibility.
add_action(
	'before_woocommerce_init',
	static function () {
		if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
			\Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility( 'custom_order_tables', SB_CORE_FILE, true );
			\Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility( 'cart_checkout_blocks', SB_CORE_FILE, true );
		}
	}
);

add_action(
	'plugins_loaded',
	static function () {
		if ( ! class_exists( 'WooCommerce' ) ) {
			add_action(
				'admin_notices',
				static function () {
					echo '<div class="notice notice-error"><p>' . esc_html__( 'SEO Booster Core requires WooCommerce.', 'seo-booster-core' ) . '</p></div>';
				}
			);
			return;
		}
		SB_Packages::init();
		SB_Shortcode::init();
		SB_Orders::init();
		SB_Brief::init();
		SB_Importer::init();
	}
);

register_activation_hook(
	__FILE__,
	static function () {
		SB_Packages::register_taxonomy();
		SB_Brief::add_endpoint();
		SB_Brief::protect_upload_dir();
		flush_rewrite_rules();
	}
);

register_deactivation_hook( __FILE__, 'flush_rewrite_rules' );
