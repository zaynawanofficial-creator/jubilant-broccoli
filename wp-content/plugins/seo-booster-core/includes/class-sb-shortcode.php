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
			echo self::selector( $g['products'], $pid ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in selector().
			echo '</section>';
		}
		echo '</div>';
		return (string) ob_get_clean();
	}

	/** "£0.85 per link" style unit price, when the package has a countable quantity. */
	public static function unit_price( WC_Product $p ): string {
		$qty  = (int) $p->get_meta( '_sb_quantity' );
		$unit = (string) $p->get_meta( '_sb_unit' );
		$map  = array( 'links' => __( 'per link', 'seo-booster-core' ), 'articles' => __( 'per article', 'seo-booster-core' ), 'graphics' => __( 'per graphic', 'seo-booster-core' ), 'pages' => __( 'per page', 'seo-booster-core' ), 'words' => __( 'per 100 words', 'seo-booster-core' ) );
		if ( $qty < 2 || ! isset( $map[ $unit ] ) || 'quote' === $p->get_meta( '_sb_pricing_model' ) || ! (float) $p->get_price() ) {
			return '';
		}
		$each = (float) $p->get_price() / $qty * ( 'words' === $unit ? 100 : 1 );
		return wp_strip_all_tags( wc_price( $each ) ) . ' ' . $map[ $unit ];
	}

	private static function short_price( WC_Product $p ): string {
		if ( 'quote' === $p->get_meta( '_sb_pricing_model' ) || ! $p->is_purchasable() ) {
			return esc_html__( 'Quote', 'seo-booster-core' );
		}
		$v = (float) $p->get_price();
		return esc_html( wp_strip_all_tags( wc_price( $v, array( 'decimals' => floor( $v ) == $v ? 0 : 2 ) ) ) ); // phpcs:ignore Universal.Operators.StrictComparisons.LooseEqual
	}

	/**
	 * Compact package picker: tier list (left) + one detail panel (right).
	 *
	 * @param WC_Product[] $products Group products, sorted.
	 */
	public static function selector( array $products, string $uid ): string {
		$default = 0;
		foreach ( $products as $i => $p ) {
			if ( '1' === $p->get_meta( '_sb_featured' ) ) {
				$default = $i;
				break;
			}
		}
		ob_start();
		echo '<div class="sb-pk" data-sb-pk>';
		echo '<div class="sb-pk__tiers" role="radiogroup" aria-label="' . esc_attr__( 'Choose a package', 'seo-booster-core' ) . '">';
		foreach ( $products as $i => $p ) {
			$on    = $i === $default;
			$ideal = (string) $p->get_meta( '_sb_ideal_for' );
			printf(
				'<button type="button" role="radio" class="sb-pk__tier%1$s" aria-checked="%2$s" tabindex="%3$s" aria-controls="%4$s" data-panel="%4$s"><span class="sb-pk__radio" aria-hidden="true"></span><span class="sb-pk__name">%5$s%6$s</span>%7$s<span class="sb-pk__tprice">%8$s</span></button>',
				'1' === $p->get_meta( '_sb_featured' ) ? ' is-featured' : '',
				$on ? 'true' : 'false',
				$on ? '0' : '-1',
				esc_attr( $uid . '-p' . $i ),
				esc_html( $p->get_name() ),
				$ideal ? '<small>' . esc_html( $ideal ) . '</small>' : '',
				'1' === $p->get_meta( '_sb_featured' ) ? '<span class="sb-pk__pop">' . esc_html__( 'Popular', 'seo-booster-core' ) . '</span>' : '',
				self::short_price( $p ) // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in short_price().
			);
		}
		echo '</div><div class="sb-pk__panels">';
		foreach ( $products as $i => $p ) {
			$quote = 'quote' === $p->get_meta( '_sb_pricing_model' ) || ! $p->is_purchasable();
			$items = SB_Packages::lines( $p, '_sb_deliverables' );
			$excl  = SB_Packages::lines( $p, '_sb_exclusions' );
			$unit  = self::unit_price( $p );
			$facts = array_filter(
				array(
					__( 'Delivery', 'seo-booster-core' )  => (string) $p->get_meta( '_sb_turnaround' ),
					__( 'Revisions', 'seo-booster-core' ) => (string) $p->get_meta( '_sb_revisions' ),
				)
			);
			echo '<div class="sb-pk__panel" id="' . esc_attr( $uid . '-p' . $i ) . '" role="region" aria-label="' . esc_attr( $p->get_name() ) . '"' . ( $i === $default ? '' : ' hidden' ) . '>';
			echo '<div class="sb-pk__head"><div><h3 class="sb-pk__title">' . esc_html( $p->get_name() ) . '</h3>';
			if ( $p->get_meta( '_sb_ideal_for' ) ) {
				echo '<p class="sb-pk__ideal">' . esc_html__( 'Ideal for:', 'seo-booster-core' ) . ' ' . esc_html( (string) $p->get_meta( '_sb_ideal_for' ) ) . '</p>';
			}
			echo '</div><div class="sb-pk__price">' . ( $quote ? esc_html__( 'Custom quote', 'seo-booster-core' ) : wp_kses_post( $p->get_price_html() ) );
			if ( $unit ) {
				echo '<span>' . esc_html( $unit ) . '</span>';
			}
			echo '</div></div>';
			if ( $facts ) {
				echo '<ul class="sb-pk__facts">';
				foreach ( $facts as $k => $v ) {
					echo '<li><span>' . esc_html( $k ) . '</span>' . esc_html( $v ) . '</li>';
				}
				echo '</ul>';
			}
			if ( $items ) {
				echo '<ul class="sb-pk__list">' . implode( '', array_map( static fn( $x ) => '<li>' . esc_html( $x ) . '</li>', $items ) ) . '</ul>';
			}
			echo '<div class="sb-pk__cta">';
			if ( $quote ) {
				echo '<a class="sb-btn sb-btn--primary" href="' . esc_url( SB_Packages::quote_url( $p ) ) . '">' . esc_html__( 'Get a quote', 'seo-booster-core' ) . '</a>';
			} else {
				/* translators: %s: package name */
				echo '<a class="sb-btn sb-btn--primary" href="' . esc_url( $p->get_permalink() . '#order' ) . '" aria-label="' . esc_attr( sprintf( __( 'Choose %s', 'seo-booster-core' ), $p->get_name() ) ) . '">' . esc_html__( 'Choose this package', 'seo-booster-core' ) . ' →</a>';
			}
			echo '<a class="sb-pk__more" href="' . esc_url( $p->get_permalink() ) . '">' . esc_html__( 'Full details', 'seo-booster-core' ) . '</a></div>';
			if ( $excl ) {
				echo '<details class="sb-pk__excl"><summary>' . esc_html__( 'Not included', 'seo-booster-core' ) . '</summary><ul>' . implode( '', array_map( static fn( $x ) => '<li>' . esc_html( $x ) . '</li>', $excl ) ) . '</ul></details>';
			}
			echo '</div>';
		}
		echo '</div></div>';
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
		if ( $product->get_image_id() ) {
			echo '<a class="sb-pkcard__media" href="' . esc_url( $product->get_permalink() ) . '" tabindex="-1" aria-hidden="true">' . wp_get_attachment_image( $product->get_image_id(), 'medium_large', false, array( 'loading' => 'lazy', 'alt' => '' ) ) . '</a>';
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
			/* translators: %s: package name */
			echo '<a class="sb-btn sb-btn--primary" href="' . esc_url( $product->get_permalink() . '#order' ) . '" aria-label="' . esc_attr( sprintf( __( 'Choose %s', 'seo-booster-core' ), $product->get_name() ) ) . '">' . esc_html__( 'Choose package', 'seo-booster-core' ) . ' →</a>';
		}
		echo '<a class="sb-pkcard__details" href="' . esc_url( $product->get_permalink() ) . '">' . esc_html__( 'Full package details', 'seo-booster-core' ) . '</a>';
		echo '</div></li>';
		return (string) ob_get_clean();
	}
}
