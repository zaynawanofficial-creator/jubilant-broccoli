<?php
/**
 * [sb_packages] — data-driven package groups (tabs) + package cards for Elementor/any page.
 *
 * Usage: [sb_packages service="off-page-seo"]  (service = product_cat slug)
 *        [sb_packages service="off-page-seo" group="premium-links"]
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

/**
 * Renders packages straight from WooCommerce data. No prices live in page content.
 */
class SB_Shortcode {

	public static function init(): void {
		add_shortcode( 'sb_packages', array( __CLASS__, 'render' ) );
		add_action( 'wp_enqueue_scripts', array( __CLASS__, 'register_assets' ) );
	}

	public static function register_assets(): void {
		wp_register_style( 'sb-packages', SB_CORE_URL . 'assets/sb-packages.css', array(), SB_CORE_VERSION );
		wp_register_script( 'sb-packages', SB_CORE_URL . 'assets/sb-packages.js', array(), SB_CORE_VERSION, array( 'strategy' => 'defer', 'in_footer' => true ) );
	}

	/**
	 * Published packages for a service, grouped by package group.
	 *
	 * @return array<int,array{term:WP_Term,products:WC_Product[]}>
	 */
	public static function grouped( string $service, string $group = '' ): array {
		$args = array(
			'status'   => 'publish',
			'limit'    => 100,
			'category' => array( $service ),
			'return'   => 'objects',
		);
		$products = wc_get_products( $args );
		$out      = array();
		foreach ( $products as $product ) {
			if ( ! SB_Packages::is_package( $product ) || 'hidden' === $product->get_catalog_visibility() ) {
				continue;
			}
			$terms = wp_get_post_terms( $product->get_id(), SB_Packages::TAX );
			if ( is_wp_error( $terms ) || ! $terms ) {
				continue;
			}
			$term = $terms[0];
			if ( $group && $term->slug !== $group ) {
				continue;
			}
			if ( ! isset( $out[ $term->term_id ] ) ) {
				$out[ $term->term_id ] = array( 'term' => $term, 'products' => array() );
			}
			$out[ $term->term_id ]['products'][] = $product;
		}
		foreach ( $out as &$g ) {
			usort(
				$g['products'],
				static fn( $a, $b ) => (int) $a->get_meta( '_sb_sort' ) <=> (int) $b->get_meta( '_sb_sort' )
			);
		}
		unset( $g );
		uasort(
			$out,
			static fn( $a, $b ) => (int) get_term_meta( $a['term']->term_id, '_sb_group_sort', true ) <=> (int) get_term_meta( $b['term']->term_id, '_sb_group_sort', true )
		);
		return array_values( $out );
	}

	public static function render( $atts ): string {
		$atts = shortcode_atts( array( 'service' => '', 'group' => '' ), $atts, 'sb_packages' );
		$service = sanitize_title( $atts['service'] );
		if ( ! $service ) {
			return '';
		}
		$groups = self::grouped( $service, sanitize_title( $atts['group'] ) );
		if ( ! $groups ) {
			return '<div class="sb-packages sb-packages--empty"><p>' . esc_html__( 'Packages for this service are being finalised. Tell us what you need and we will send a tailored proposal.', 'seo-booster-core' ) . '</p><p><a class="sb-btn sb-btn--primary" href="' . esc_url( home_url( '/get-a-quote/' ) ) . '">' . esc_html__( 'Get a proposal', 'seo-booster-core' ) . '</a></p></div>';
		}
		wp_enqueue_style( 'sb-packages' );
		wp_enqueue_script( 'sb-packages' );

		$uid = 'sbp-' . wp_unique_id();
		ob_start();
		echo '<div class="sb-packages" id="' . esc_attr( $uid ) . '">';
		if ( count( $groups ) > 1 ) {
			echo '<div class="sb-tabs" role="tablist" aria-label="' . esc_attr__( 'Package groups', 'seo-booster-core' ) . '">';
			foreach ( $groups as $i => $g ) {
				$tid = $uid . '-tab-' . $i;
				$pid = $uid . '-panel-' . $i;
				printf(
					'<button type="button" class="sb-tab" role="tab" id="%1$s" aria-controls="%2$s" aria-selected="%3$s" tabindex="%4$s">%5$s</button>',
					esc_attr( $tid ),
					esc_attr( $pid ),
					0 === $i ? 'true' : 'false',
					0 === $i ? '0' : '-1',
					esc_html( $g['term']->name )
				);
			}
			echo '</div>';
		}
		foreach ( $groups as $i => $g ) {
			$tid   = $uid . '-tab-' . $i;
			$pid   = $uid . '-panel-' . $i;
			$multi = count( $groups ) > 1;
			printf(
				'<section class="sb-pkpanel" id="%1$s" %2$s %3$s>',
				esc_attr( $pid ),
				$multi ? 'role="tabpanel" aria-labelledby="' . esc_attr( $tid ) . '" tabindex="0"' : 'aria-label="' . esc_attr( $g['term']->name ) . '"',
				( $multi && $i > 0 ) ? 'hidden' : ''
			);
			if ( $g['term']->description ) {
				echo '<p class="sb-pkpanel__intro">' . esc_html( $g['term']->description ) . '</p>';
			}
			echo '<ul class="sb-pkgrid" role="list">';
			foreach ( $g['products'] as $product ) {
				echo self::card( $product ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in card().
			}
			echo '</ul></section>';
		}
		echo '</div>';
		return (string) ob_get_clean();
	}

	public static function card( WC_Product $product ): string {
		$model    = $product->get_meta( '_sb_pricing_model' );
		$featured = '1' === $product->get_meta( '_sb_featured' );
		$items    = SB_Packages::lines( $product, '_sb_deliverables' );
		$excl     = SB_Packages::lines( $product, '_sb_exclusions' );
		$ideal    = $product->get_meta( '_sb_ideal_for' );
		$turn     = $product->get_meta( '_sb_turnaround' );
		$rev      = $product->get_meta( '_sb_revisions' );

		ob_start();
		echo '<li class="sb-pkcard' . ( $featured ? ' sb-pkcard--featured' : '' ) . '">';
		if ( $featured ) {
			echo '<span class="sb-pkcard__badge">' . esc_html__( 'Most popular', 'seo-booster-core' ) . '</span>';
		}
		echo '<h3 class="sb-pkcard__title">' . esc_html( $product->get_name() ) . '</h3>';
		if ( $ideal ) {
			echo '<p class="sb-pkcard__ideal">' . esc_html( $ideal ) . '</p>';
		}
		echo '<div class="sb-pkcard__price">';
		if ( 'quote' === $model ) {
			echo '<span class="sb-pkcard__quote">' . esc_html__( 'Priced per publisher', 'seo-booster-core' ) . '</span>';
		} else {
			echo wp_kses_post( $product->get_price_html() );
		}
		echo '</div>';
		echo '<dl class="sb-pkcard__facts">';
		if ( $turn ) {
			echo '<div><dt>' . esc_html__( 'Delivery', 'seo-booster-core' ) . '</dt><dd>' . esc_html( $turn ) . '</dd></div>';
		}
		if ( $rev ) {
			echo '<div><dt>' . esc_html__( 'Revisions', 'seo-booster-core' ) . '</dt><dd>' . esc_html( $rev ) . '</dd></div>';
		}
		echo '</dl>';
		if ( $items ) {
			echo '<ul class="sb-pkcard__list">';
			foreach ( $items as $line ) {
				echo '<li>' . esc_html( $line ) . '</li>';
			}
			echo '</ul>';
		}
		if ( $excl ) {
			echo '<details class="sb-pkcard__excl"><summary>' . esc_html__( 'Not included', 'seo-booster-core' ) . '</summary><ul>';
			foreach ( $excl as $line ) {
				echo '<li>' . esc_html( $line ) . '</li>';
			}
			echo '</ul></details>';
		}
		echo '<div class="sb-pkcard__cta">';
		if ( 'quote' === $model || ! $product->is_purchasable() ) {
			echo '<a class="sb-btn sb-btn--primary" href="' . esc_url( SB_Packages::quote_url( $product ) ) . '">' . esc_html__( 'Get a quote', 'seo-booster-core' ) . '</a>';
		} else {
			printf(
				'<a class="sb-btn sb-btn--primary add_to_cart_button ajax_add_to_cart" href="%1$s" data-quantity="1" data-product_id="%2$d" data-product_sku="%3$s" rel="nofollow" aria-label="%4$s">%5$s</a>',
				esc_url( $product->add_to_cart_url() ),
				(int) $product->get_id(),
				esc_attr( $product->get_sku() ),
				/* translators: %s: package name */
				esc_attr( sprintf( __( 'Add %s to cart', 'seo-booster-core' ), $product->get_name() ) ),
				esc_html__( 'Add to cart', 'seo-booster-core' )
			);
		}
		echo '<a class="sb-btn sb-btn--ghost" href="' . esc_url( $product->get_permalink() ) . '">' . esc_html__( 'View details', 'seo-booster-core' ) . '</a>';
		echo '</div></li>';
		return (string) ob_get_clean();
	}
}
