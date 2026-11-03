<?php
/**
 * Service details page parts for a package (product) page:
 * [sb_service_hero], [sb_service_body], [sb_service_more]. The theme's single-product template lays them out
 * around [sb_order_form].
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

/**
 * Package detail page.
 */
class SB_Service_Page {

	public static function init(): void {
		add_shortcode( 'sb_service_hero', array( __CLASS__, 'hero' ) );
		add_shortcode( 'sb_service_body', array( __CLASS__, 'body' ) );
		add_shortcode( 'sb_service_more', array( __CLASS__, 'more' ) );
		add_action( 'wp_enqueue_scripts', array( __CLASS__, 'assets' ), 20 );
	}

	public static function assets(): void {
		if ( function_exists( 'is_product' ) && ( is_product() || is_cart() || is_checkout() ) ) {
			wp_enqueue_style( 'sb-packages' );
		}
	}

	private static function product(): ?WC_Product {
		$p = wc_get_product( get_the_ID() );
		return $p && SB_Packages::is_package( $p ) ? $p : null;
	}

	/** Service (category) name and its service page URL. */
	public static function service( WC_Product $p ): array {
		$cats = get_the_terms( $p->get_id(), 'product_cat' );
		if ( ! $cats || is_wp_error( $cats ) ) {
			return array( '', '', '' );
		}
		$page = get_page_by_path( 'services/' . $cats[0]->slug );
		return array( $cats[0]->name, $page ? get_permalink( $page ) : home_url( '/services/' ), $cats[0]->slug );
	}

	private static function group( WC_Product $p ): ?WP_Term {
		$g = wp_get_post_terms( $p->get_id(), SB_Packages::TAX );
		return ( $g && ! is_wp_error( $g ) ) ? $g[0] : null;
	}

	public static function hero(): string {
		$p = self::product();
		if ( ! $p ) {
			return '';
		}
		list( $svc ) = self::service( $p );
		$group       = self::group( $p );
		$ideal       = (string) $p->get_meta( '_sb_ideal_for' );
		$facts       = array_filter(
			array(
				__( 'Delivery', 'seo-booster-core' )  => (string) $p->get_meta( '_sb_turnaround' ),
				__( 'Revisions', 'seo-booster-core' ) => (string) $p->get_meta( '_sb_revisions' ),
				__( 'Group', 'seo-booster-core' )     => $group ? $group->name : '',
			)
		);
		ob_start();
		echo '<div class="sb-svc-hero"><div class="sb-svc-hero__text">';
		echo SB_Site::breadcrumbs(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped inside.
		echo '<p class="sb-eyebrow">' . esc_html( $svc ) . '</p>';
		echo '<h1 class="sb-svc-hero__title">' . esc_html( $p->get_name() ) . '</h1>';
		if ( $p->get_short_description() ) {
			echo '<p class="sb-lead">' . esc_html( wp_strip_all_tags( $p->get_short_description() ) ) . '</p>';
		}
		echo '<div class="sb-svc-hero__buy"><span class="sb-svc-hero__price">';
		echo 'quote' === $p->get_meta( '_sb_pricing_model' ) ? esc_html__( 'Custom quote', 'seo-booster-core' ) : wp_kses_post( $p->get_price_html() );
		echo '</span><a class="wp-element-button sb-btn sb-btn--primary" href="#order">' . esc_html__( 'Start your order', 'seo-booster-core' ) . '</a></div>';
		if ( $ideal ) {
			echo '<p class="sb-svc-hero__ideal"><strong>' . esc_html__( 'Ideal for:', 'seo-booster-core' ) . '</strong> ' . esc_html( $ideal ) . '</p>';
		}
		if ( $facts ) {
			echo '<dl class="sb-svc-hero__facts">';
			foreach ( $facts as $k => $v ) {
				echo '<div><dt>' . esc_html( $k ) . '</dt><dd>' . esc_html( $v ) . '</dd></div>';
			}
			echo '</dl>';
		}
		echo '</div><div class="sb-svc-hero__media">';
		echo $p->get_image_id() ? wp_get_attachment_image( $p->get_image_id(), 'large', false, array( 'fetchpriority' => 'high', 'alt' => $p->get_name() ) ) : ''; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core function.
		echo '</div></div>';
		return (string) ob_get_clean();
	}

	private static function list_html( string $title, array $items, string $cls ): string {
		if ( ! $items ) {
			return '';
		}
		return '<section class="sb-svc-block"><h2>' . esc_html( $title ) . '</h2><ul class="' . esc_attr( $cls ) . '">' . implode( '', array_map( static fn( $i ) => '<li>' . esc_html( $i ) . '</li>', $items ) ) . '</ul></section>';
	}

	public static function body(): string {
		$p = self::product();
		if ( ! $p ) {
			return '';
		}
		$steps = array(
			array( __( 'Order', 'seo-booster-core' ), __( 'Add your project details and check out securely.', 'seo-booster-core' ) ),
			array( __( 'Kick-off', 'seo-booster-core' ), __( 'We review your details and confirm anything unclear within one working day.', 'seo-booster-core' ) ),
			array( __( 'Delivery', 'seo-booster-core' ), __( 'Work is done by hand and checked before it reaches you.', 'seo-booster-core' ) ),
			array( __( 'Report', 'seo-booster-core' ), __( 'You receive the report or files, with revisions where included.', 'seo-booster-core' ) ),
		);
		ob_start();
		echo '<div class="sb-svc-body">';
		echo self::list_html( __( "What's included", 'seo-booster-core' ), SB_Packages::lines( $p, '_sb_deliverables' ), 'sb-ticks' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in list_html().
		echo '<div class="sb-svc-body__two">';
		echo self::list_html( __( 'What we need from you', 'seo-booster-core' ), SB_Packages::lines( $p, '_sb_requirements' ), 'sb-ticks sb-ticks--blue' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in list_html().
		echo self::list_html( __( 'Not included', 'seo-booster-core' ), SB_Packages::lines( $p, '_sb_exclusions' ), 'sb-crosses' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in list_html().
		echo '</div>';
		echo '<section class="sb-svc-block"><h2>' . esc_html__( 'How your order works', 'seo-booster-core' ) . '</h2><ol class="sb-svc-steps">';
		foreach ( $steps as $i => $s ) {
			echo '<li><span class="sb-svc-steps__n">' . esc_html( str_pad( (string) ( $i + 1 ), 2, '0', STR_PAD_LEFT ) ) . '</span><strong>' . esc_html( $s[0] ) . '</strong><span>' . esc_html( $s[1] ) . '</span></li>';
		}
		echo '</ol></section>';
		echo '<section class="sb-svc-block sb-svc-faq"><h2>' . esc_html__( 'Good to know', 'seo-booster-core' ) . '</h2>';
		$faq = array(
			__( 'When does delivery start?', 'seo-booster-core' )  => __( 'The delivery time starts once we have your project details. If you add everything in the form on this page, we can start straight after payment.', 'seo-booster-core' ),
			__( 'Can I send files?', 'seo-booster-core' )          => __( 'Yes. After checkout you can upload logos, brand guides and documents securely from your account.', 'seo-booster-core' ),
			__( 'Do you guarantee rankings?', 'seo-booster-core' ) => __( 'No. We guarantee the deliverables listed above. Rankings depend on Google and your competitors, so no honest provider can promise them.', 'seo-booster-core' ),
			__( 'What if I need changes?', 'seo-booster-core' )    => __( 'Revisions are included as shown above. For anything beyond the package scope we quote before doing extra work.', 'seo-booster-core' ),
		);
		foreach ( $faq as $q => $a ) {
			echo '<details><summary>' . esc_html( $q ) . '</summary><p>' . esc_html( $a ) . '</p></details>';
		}
		echo '</section></div>';
		return (string) ob_get_clean();
	}

	public static function more(): string {
		$p = self::product();
		if ( ! $p ) {
			return '';
		}
		list( $svc, $url, $slug ) = self::service( $p );
		$group                    = self::group( $p );
		ob_start();
		echo '<div class="sb-svc-more"><div class="sb-svc-more__head"><div><p class="sb-eyebrow">' . esc_html__( 'Compare', 'seo-booster-core' ) . '</p><h2>' . esc_html( sprintf( /* translators: %s: service */ __( 'Other %s packages', 'seo-booster-core' ), $svc ) ) . '</h2></div>';
		echo '<a class="sb-card__more" href="' . esc_url( $url ) . '">' . esc_html__( 'About this service', 'seo-booster-core' ) . ' →</a></div>';
		echo SB_Shortcode::render( array( 'service' => $slug, 'group' => $group ? $group->slug : '' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped inside.
		echo '</div>';
		return (string) ob_get_clean();
	}
}
