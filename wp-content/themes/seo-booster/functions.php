<?php
/**
 * SEO Booster theme bootstrap.
 *
 * @package SEOBoosterTheme
 */

defined( 'ABSPATH' ) || exit;

define( 'SBT_VERSION', '1.2.0' );

add_action(
	'after_setup_theme',
	static function () {
		add_theme_support( 'wp-block-styles' );
		add_theme_support( 'editor-styles' );
		add_theme_support( 'woocommerce' );
		add_theme_support( 'responsive-embeds' );
		add_editor_style( 'style.css' );
	}
);

add_action(
	'wp_enqueue_scripts',
	static function () {
		wp_enqueue_style( 'seo-booster', get_stylesheet_uri(), array(), SBT_VERSION );
	}
);

// Preload the two variable fonts used above the fold.
add_action(
	'wp_head',
	static function () {
		foreach ( array( 'manrope-latin-wght.woff2', 'inter-latin-wght.woff2' ) as $font ) {
			printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( get_theme_file_uri( 'assets/fonts/' . $font ) ) );
		}
	},
	1
);

add_action(
	'init',
	static function () {
		register_block_pattern_category( 'seo-booster-pages', array( 'label' => __( 'SEO Booster: full pages', 'seo-booster' ) ) );
		register_block_pattern_category( 'seo-booster-sections', array( 'label' => __( 'SEO Booster: sections', 'seo-booster' ) ) );
	}
);

// Fallback year shortcode if the companion plugin is inactive.
add_action(
	'init',
	static function () {
		if ( ! shortcode_exists( 'sb_year' ) ) {
			add_shortcode( 'sb_year', static fn() => esc_html( wp_date( 'Y' ) ) );
		}
		if ( ! shortcode_exists( 'sb_currency' ) ) {
			add_shortcode( 'sb_currency', static fn() => function_exists( 'get_woocommerce_currency' ) ? esc_html( get_woocommerce_currency() ) : 'USD' );
		}
		if ( ! shortcode_exists( 'sb_breadcrumbs' ) ) {
			add_shortcode( 'sb_breadcrumbs', '__return_empty_string' );
		}
	},
	20
);

// Site icon fallback before a Site Icon is set in WordPress.
add_action(
	'wp_head',
	static function () {
		if ( ! has_site_icon() ) {
			echo '<link rel="icon" href="' . esc_url( get_theme_file_uri( 'assets/images/favicon.svg' ) ) . '" type="image/svg+xml">' . "\n";
		}
	}
);

/**
 * Tables with the "sb-table" class: copy header labels onto cells so they can stack on phones.
 * Front-end only (saved block markup stays untouched, so the editor keeps validating).
 */
add_filter(
	'render_block_core/table',
	static function ( string $html, array $block ): string {
		if ( empty( $block['attrs']['className'] ) || ! str_contains( $block['attrs']['className'], 'sb-table' ) || ! class_exists( 'WP_HTML_Tag_Processor' ) ) {
			return $html;
		}
		if ( ! preg_match( '#<thead>(.*?)</thead>#s', $html, $m ) || ! preg_match_all( '#<th[^>]*>(.*?)</th>#s', $m[1], $th ) ) {
			return $html;
		}
		$labels = array_map( static fn( $t ) => trim( wp_strip_all_tags( $t ) ), $th[1] );
		$p      = new WP_HTML_Tag_Processor( $html );
		$i      = 0;
		while ( $p->next_tag() ) {
			$tag = $p->get_tag();
			if ( 'TR' === $tag ) {
				$i = 0;
			} elseif ( 'TD' === $tag ) {
				if ( isset( $labels[ $i ] ) && '' !== $labels[ $i ] ) {
					$p->set_attribute( 'data-label', $labels[ $i ] );
				}
				++$i;
			}
		}
		return $p->get_updated_html();
	},
	10,
	2
);

require_once get_theme_file_path( 'inc/setup.php' );
