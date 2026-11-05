<?php
/**
 * Main navigation: desktop menu with a Services mega panel, and a slide-in drawer for tablets and phones.
 *
 * Why custom: the core Navigation overlay is position:fixed inside the sticky header, so any header effect
 * (blur, transform) traps it in a 64px strip ("only Home shows"). It also switches to the toggle at 600px,
 * when the full menu no longer fits from about 1024px. This version controls both.
 *
 * Edit the links in sbt_nav_items() or with the 'sbt_nav_items' filter.
 *
 * @package SEOBoosterTheme
 */

defined( 'ABSPATH' ) || exit;

/**
 * Menu structure. Top-level items with 'groups' render as the mega panel.
 *
 * @return array<int, array<string, mixed>>
 */
function sbt_nav_items(): array {
	$items = array(
		array(
			'label' => __( 'Home', 'seo-booster' ),
			'url'   => '/',
		),
		array(
			'label'  => __( 'Services', 'seo-booster' ),
			'url'    => '/services/',
			'groups' => array(
				array(
					'label' => __( 'SEO services', 'seo-booster' ),
					'links' => array(
						array( __( 'Monthly SEO', 'seo-booster' ), '/services/monthly-seo/' ),
						array( __( 'Local SEO', 'seo-booster' ), '/services/local-seo/' ),
						array( __( 'Link Building', 'seo-booster' ), '/services/off-page-seo/' ),
						array( __( 'SEO Audit', 'seo-booster' ), '/services/seo-audit/' ),
						array( __( 'Technical SEO', 'seo-booster' ), '/services/technical-seo/' ),
						array( __( 'On-Page SEO', 'seo-booster' ), '/services/on-page-seo/' ),
						array( __( 'Ecommerce SEO', 'seo-booster' ), '/services/ecommerce-seo/' ),
						array( __( 'AI SEO', 'seo-booster' ), '/services/ai-seo/' ),
						array( __( 'White Label SEO', 'seo-booster' ), '/services/white-label-seo/' ),
						array( __( 'SEO Consultancy', 'seo-booster' ), '/services/seo-consultancy/' ),
					),
				),
				array(
					'label' => __( 'Websites', 'seo-booster' ),
					'links' => array(
						array( __( 'Website Development', 'seo-booster' ), '/services/website-development/' ),
						array( __( 'Ecommerce Websites', 'seo-booster' ), '/services/ecommerce-website-development/' ),
						array( __( 'Website Maintenance', 'seo-booster' ), '/services/website-maintenance/' ),
						array( __( 'Website Migration', 'seo-booster' ), '/services/website-migration/' ),
					),
				),
				array(
					'label' => __( 'Ads & social', 'seo-booster' ),
					'links' => array(
						array( __( 'PPC Management', 'seo-booster' ), '/services/ppc-management/' ),
						array( __( 'Facebook Ads', 'seo-booster' ), '/services/facebook-ads/' ),
						array( __( 'TikTok Ads', 'seo-booster' ), '/services/tiktok-ads/' ),
						array( __( 'Social Media Management', 'seo-booster' ), '/services/social-media-management/' ),
					),
				),
				array(
					'label' => __( 'Content & design', 'seo-booster' ),
					'links' => array(
						array( __( 'Content Writing', 'seo-booster' ), '/services/content-writing/' ),
						array( __( 'Graphic Design & Branding', 'seo-booster' ), '/services/graphic-design/' ),
					),
				),
			),
		),
		array(
			'label' => __( 'Packages', 'seo-booster' ),
			'url'   => '/packages/',
		),
		array(
			'label' => __( 'How it works', 'seo-booster' ),
			'url'   => '/how-it-works/',
		),
		array(
			'label' => __( 'About', 'seo-booster' ),
			'url'   => '/about/',
		),
		array(
			'label' => __( 'Insights', 'seo-booster' ),
			'url'   => '/insights/',
		),
		array(
			'label' => __( 'Contact', 'seo-booster' ),
			'url'   => '/contact/',
		),
	);
	return (array) apply_filters( 'sbt_nav_items', $items );
}

/** Current request path, e.g. "/services/local-seo/". */
function sbt_nav_path(): string {
	$path = (string) wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? esc_url_raw( wp_unslash( $_SERVER['REQUEST_URI'] ) ) : '/', PHP_URL_PATH );
	$home = (string) wp_parse_url( home_url( '/' ), PHP_URL_PATH );
	if ( '' !== $home && '/' !== $home && str_starts_with( $path, rtrim( $home, '/' ) ) ) {
		$path = substr( $path, strlen( rtrim( $home, '/' ) ) );
	}
	return trailingslashit( '/' . ltrim( $path, '/' ) );
}

/** Is this URL the current page (exact) or a parent section (prefix)? */
function sbt_nav_state( string $url, bool $prefix = false ): string {
	$path = sbt_nav_path();
	if ( $path === $url ) {
		return 'page';
	}
	if ( $prefix && '/' !== $url && str_starts_with( $path, $url ) ) {
		return 'section';
	}
	return '';
}

/** Insights posts live at the root, so treat single posts as part of Insights. */
function sbt_nav_is_active( array $item ): bool {
	if ( ! empty( $item['groups'] ) ) {
		return '' !== sbt_nav_state( '/services/', true ) || ( function_exists( 'is_product' ) && is_product() );
	}
	if ( '/insights/' === $item['url'] && ( is_singular( 'post' ) || is_category() || is_tag() ) ) {
		return true;
	}
	return '' !== sbt_nav_state( $item['url'], '/' !== $item['url'] );
}

function sbt_nav_link( string $label, string $url, string $class ): string {
	$current = 'page' === sbt_nav_state( $url ) ? ' aria-current="page"' : '';
	return '<a class="' . esc_attr( $class ) . '" href="' . esc_url( home_url( $url ) ) . '"' . $current . '>' . esc_html( $label ) . '</a>';
}

function sbt_chevron(): string {
	return '<svg class="sb-nav__chev" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M2 4.25 6 8l4-3.75" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}

/**
 * Shortcode output is swapped in after the Shortcode block's wpautop, so the markup is never split by <p>/<br>.
 */
function sbt_raw( string $html ): string {
	static $n = 0;
	++$n;
	$GLOBALS['sbt_raw'][ $n ] = $html;
	return '<!--sbt-raw:' . $n . '-->';
}

function sbt_unraw( string $html ): string {
	if ( ! str_contains( $html, '<!--sbt-raw:' ) ) {
		return $html;
	}
	return (string) preg_replace_callback(
		'#(?:<p>\s*)?<!--sbt-raw:(\d+)-->(?:\s*(?:<br\s*/?>\s*)?</p>)?#',
		static fn( $m ) => $GLOBALS['sbt_raw'][ (int) $m[1] ] ?? '',
		$html
	);
}

/** [sb_nav] desktop menu (hidden below 1024px by CSS). */
function sbt_nav_shortcode(): string {
	$out = '<nav class="sb-nav" aria-label="' . esc_attr__( 'Main', 'seo-booster' ) . '"><ul class="sb-nav__list">';
	foreach ( sbt_nav_items() as $i => $item ) {
		$active = sbt_nav_is_active( $item ) ? ' is-active' : '';
		if ( empty( $item['groups'] ) ) {
			$out .= '<li class="sb-nav__item' . $active . '">' . sbt_nav_link( $item['label'], $item['url'], 'sb-nav__link' ) . '</li>';
			continue;
		}
		$id   = 'sb-mega-' . $i;
		$out .= '<li class="sb-nav__item has-mega' . $active . '">';
		$out .= '<button type="button" class="sb-nav__link sb-nav__trigger" aria-expanded="false" aria-controls="' . esc_attr( $id ) . '">' . esc_html( $item['label'] ) . sbt_chevron() . '</button>';
		$out .= '<div class="sb-mega" id="' . esc_attr( $id ) . '"><div class="sb-mega__inner"><div class="sb-mega__cols">';
		foreach ( $item['groups'] as $g ) {
			$out .= '<div class="sb-mega__col"><p class="sb-mega__h">' . esc_html( $g['label'] ) . '</p><ul>';
			foreach ( $g['links'] as $l ) {
				$out .= '<li>' . sbt_nav_link( $l[0], $l[1], 'sb-mega__link' ) . '</li>';
			}
			$out .= '</ul></div>';
		}
		$out .= '</div><div class="sb-mega__foot"><p>' . esc_html__( 'Fixed prices, clear scope and a report you can check on every order.', 'seo-booster' ) . '</p>';
		$out .= '<div class="sb-mega__actions">' . sbt_nav_link( __( 'All services', 'seo-booster' ), $item['url'], 'sb-mega__more' ) . sbt_nav_link( __( 'Compare packages', 'seo-booster' ), '/packages/', 'sb-mega__more' ) . sbt_nav_link( __( 'Get a free quote', 'seo-booster' ), '/get-a-quote/', 'sb-mega__btn' ) . '</div>';
		$out .= '</div></div></div></li>';
	}
	$out .= '</ul></nav>';
	return sbt_raw( $out );
}

/** [sb_nav_toggle] menu button for tablets and phones; the drawer prints in the footer. */
function sbt_nav_toggle_shortcode(): string {
	$GLOBALS['sbt_drawer'] = true;
	return sbt_raw(
		'<div class="sb-burger-wrap"><button type="button" class="sb-burger" aria-expanded="false" aria-controls="sb-drawer" aria-label="' . esc_attr__( 'Open menu', 'seo-booster' ) . '">'
		. '<span class="sb-burger__lines" aria-hidden="true"><span></span><span></span><span></span></span><span class="sb-burger__txt">' . esc_html__( 'Menu', 'seo-booster' ) . '</span></button></div>'
	);
}

function sbt_drawer(): void {
	if ( empty( $GLOBALS['sbt_drawer'] ) ) {
		return;
	}
	$logo = has_custom_logo() ? get_custom_logo() : '<a class="sb-drawer__brand" href="' . esc_url( home_url( '/' ) ) . '">' . esc_html( get_bloginfo( 'name' ) ) . '</a>';
	$out  = '<div class="sb-drawer" id="sb-drawer" role="dialog" aria-modal="true" aria-label="' . esc_attr__( 'Site menu', 'seo-booster' ) . '" hidden>';
	$out .= '<div class="sb-drawer__scrim" data-sb-close></div><div class="sb-drawer__panel">';
	$out .= '<div class="sb-drawer__top"><div class="sb-drawer__logo">' . $logo . '</div><button type="button" class="sb-drawer__close" data-sb-close aria-label="' . esc_attr__( 'Close menu', 'seo-booster' ) . '"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>';
	$out .= '<div class="sb-drawer__body">';
	$out .= '<form class="sb-drawer__search" role="search" method="get" action="' . esc_url( home_url( '/' ) ) . '"><label class="screen-reader-text" for="sb-drawer-s">' . esc_html__( 'Search', 'seo-booster' ) . '</label><input id="sb-drawer-s" type="search" name="s" placeholder="' . esc_attr__( 'Search services and guides', 'seo-booster' ) . '"><button type="submit" aria-label="' . esc_attr__( 'Search', 'seo-booster' ) . '"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></form>';
	$out .= '<nav aria-label="' . esc_attr__( 'Mobile', 'seo-booster' ) . '"><ul class="sb-drawer__list">';
	foreach ( sbt_nav_items() as $item ) {
		if ( empty( $item['groups'] ) ) {
			$out .= '<li>' . sbt_nav_link( $item['label'], $item['url'], 'sb-drawer__link' ) . '</li>';
			continue;
		}
		$open = sbt_nav_is_active( $item ) ? ' open' : '';
		$out .= '<li class="sb-drawer__services"><details' . $open . '><summary class="sb-drawer__link">' . esc_html( $item['label'] ) . sbt_chevron() . '</summary><div class="sb-drawer__groups">';
		foreach ( $item['groups'] as $g ) {
			$out .= '<div class="sb-drawer__group"><p class="sb-drawer__h">' . esc_html( $g['label'] ) . '</p><ul>';
			foreach ( $g['links'] as $l ) {
				$out .= '<li>' . sbt_nav_link( $l[0], $l[1], 'sb-drawer__sublink' ) . '</li>';
			}
			$out .= '</ul></div>';
		}
		$out .= '<p class="sb-drawer__all">' . sbt_nav_link( __( 'View all services', 'seo-booster' ), $item['url'], '' ) . '</p></div></details></li>';
	}
	$out .= '</ul></nav></div>';
	$account = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'myaccount' ) : wp_login_url();
	$out    .= '<div class="sb-drawer__foot"><a class="sb-drawer__btn is-primary" href="' . esc_url( home_url( '/get-a-quote/' ) ) . '">' . esc_html__( 'Get a free quote', 'seo-booster' ) . '</a><a class="sb-drawer__btn" href="' . esc_url( home_url( '/packages/' ) ) . '">' . esc_html__( 'Explore packages', 'seo-booster' ) . '</a>';
	$out    .= '<p class="sb-drawer__meta"><a href="' . esc_url( $account ) . '">' . esc_html__( 'My account', 'seo-booster' ) . '</a><a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a></p></div>';
	$out    .= '</div></div>';
	echo $out; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- built from escaped parts above.
}

add_action(
	'init',
	static function () {
		add_shortcode( 'sb_nav', 'sbt_nav_shortcode' );
		add_shortcode( 'sb_nav_toggle', 'sbt_nav_toggle_shortcode' );
	}
);
add_action( 'wp_footer', 'sbt_drawer', 5 );
add_action(
	'wp_enqueue_scripts',
	static function () {
		$file = get_theme_file_path( 'assets/js/nav.js' );
		wp_enqueue_script( 'seo-booster-nav', get_theme_file_uri( 'assets/js/nav.js' ), array(), SBT_VERSION . '.' . (string) filemtime( $file ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
	}
);
