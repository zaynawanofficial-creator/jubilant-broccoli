<?php
/**
 * Site helpers that must survive a theme change:
 * [sb_from], [sb_year], [sb_breadcrumbs], basic SEO head tags, product quote button.
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

/**
 * Site-wide helpers.
 */
class SB_Site {

	public static function init(): void {
		add_shortcode( 'sb_from', array( __CLASS__, 'from_price' ) );
		add_shortcode( 'sb_year', static fn() => esc_html( wp_date( 'Y' ) ) );
		add_shortcode( 'sb_breadcrumbs', array( __CLASS__, 'breadcrumbs' ) );
		add_action( 'save_post_product', array( __CLASS__, 'flush_prices' ) );
		add_action( 'woocommerce_update_product', array( __CLASS__, 'flush_prices' ) );
		add_filter( 'wp_robots', array( __CLASS__, 'robots' ) );
		add_action( 'wp_head', array( __CLASS__, 'head' ), 2 );
		add_filter( 'render_block_woocommerce/add-to-cart-form', array( __CLASS__, 'quote_button_block' ), 10, 2 );
		add_filter( 'render_block_woocommerce/add-to-cart-with-options', array( __CLASS__, 'quote_button_block' ), 10, 2 );
		add_action( 'woocommerce_single_product_summary', array( __CLASS__, 'quote_button_classic' ), 31 );
	}

	/* ------------------------------------------------------------------ prices */

	/**
	 * Lowest published price for a service (product_cat slug), optionally one package group.
	 * [sb_from] alone = lowest price in the whole catalogue.
	 */
	public static function from_price( $atts ): string {
		$atts = shortcode_atts( array( 'service' => '', 'group' => '' ), $atts, 'sb_from' );
		$key  = 'sb_from_' . md5( $atts['service'] . '|' . $atts['group'] );
		$min  = get_transient( $key );
		if ( false === $min ) {
			$args = array( 'status' => 'publish', 'limit' => 200, 'return' => 'objects' );
			if ( $atts['service'] ) {
				$args['category'] = array( sanitize_title( $atts['service'] ) );
			}
			$min = '';
			foreach ( wc_get_products( $args ) as $p ) {
				if ( ! SB_Packages::is_package( $p ) || 'quote' === $p->get_meta( '_sb_pricing_model' ) ) {
					continue;
				}
				if ( $atts['group'] && ! has_term( sanitize_title( $atts['group'] ), SB_Packages::TAX, $p->get_id() ) ) {
					continue;
				}
				$price = (float) $p->get_price();
				if ( $price > 0 && ( '' === $min || $price < (float) $min ) ) {
					$min = (string) $price;
				}
			}
			set_transient( $key, $min, DAY_IN_SECONDS );
		}
		if ( '' === $min ) {
			return esc_html__( 'quote', 'seo-booster-core' );
		}
		return wp_strip_all_tags( wc_price( (float) $min, array( 'decimals' => floor( (float) $min ) == (float) $min ? 0 : 2 ) ) ); // phpcs:ignore Universal.Operators.StrictComparisons.LooseEqual
	}

	public static function flush_prices(): void {
		global $wpdb;
		$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '\\_transient\\_sb\\_from\\_%' OR option_name LIKE '\\_transient\\_timeout\\_sb\\_from\\_%'" ); // phpcs:ignore WordPress.DB.DirectDatabaseQuery
	}

	/* ------------------------------------------------------------------ breadcrumbs */

	/** @return array<int,array{0:string,1:string}> [label, url] */
	public static function trail(): array {
		$trail = array( array( __( 'Home', 'seo-booster-core' ), home_url( '/' ) ) );
		if ( is_front_page() ) {
			return array();
		}
		if ( function_exists( 'is_product' ) && is_product() ) {
			$trail[] = array( __( 'Packages', 'seo-booster-core' ), home_url( '/packages/' ) );
			$cats    = get_the_terms( get_the_ID(), 'product_cat' );
			if ( $cats && ! is_wp_error( $cats ) ) {
				$page = get_page_by_path( 'services/' . $cats[0]->slug );
				if ( $page ) {
					$trail[] = array( get_the_title( $page ), get_permalink( $page ) );
				}
			}
			$trail[] = array( get_the_title(), '' );
		} elseif ( is_page() ) {
			foreach ( array_reverse( get_post_ancestors( get_the_ID() ) ) as $a ) {
				$trail[] = array( get_the_title( $a ), get_permalink( $a ) );
			}
			$trail[] = array( get_the_title(), '' );
		} elseif ( is_singular( 'post' ) ) {
			$posts_page = (int) get_option( 'page_for_posts' );
			if ( $posts_page ) {
				$trail[] = array( get_the_title( $posts_page ), get_permalink( $posts_page ) );
			}
			$trail[] = array( get_the_title(), '' );
		} elseif ( is_home() ) {
			$trail[] = array( single_post_title( '', false ), '' );
		} elseif ( is_category() || is_tag() || is_tax() ) {
			$trail[] = array( single_term_title( '', false ), '' );
		} elseif ( is_search() ) {
			$trail[] = array( __( 'Search', 'seo-booster-core' ), '' );
		}
		return $trail;
	}

	public static function breadcrumbs(): string {
		$trail = self::trail();
		if ( count( $trail ) < 2 ) {
			return '';
		}
		$items = array();
		$ld    = array();
		foreach ( $trail as $i => $t ) {
			$label   = esc_html( wp_strip_all_tags( $t[0] ) );
			$items[] = $t[1] && $i < count( $trail ) - 1 ? '<li><a href="' . esc_url( $t[1] ) . '">' . $label . '</a></li>' : '<li aria-current="page">' . $label . '</li>';
			$ld[]    = array_filter(
				array(
					'@type'    => 'ListItem',
					'position' => $i + 1,
					'name'     => wp_strip_all_tags( $t[0] ),
					'item'     => $t[1] ? $t[1] : null,
				)
			);
		}
		$json = wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $ld ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		return '<nav class="sb-breadcrumbs" aria-label="' . esc_attr__( 'Breadcrumb', 'seo-booster-core' ) . '"><ol>' . implode( '', $items ) . '</ol></nav>'
			. ( self::seo_plugin_active() ? '' : '<script type="application/ld+json">' . $json . '</script>' );
	}

	/* ------------------------------------------------------------------ SEO head */

	public static function seo_plugin_active(): bool {
		return defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'AIOSEO_VERSION' ) || class_exists( 'SEOPress' ) || defined( 'THE_SEO_FRAMEWORK_VERSION' );
	}

	/** Keep transactional and thin pages out of the index. */
	public static function robots( array $robots ): array {
		$noindex = is_search() || ( function_exists( 'is_cart' ) && ( is_cart() || is_checkout() || is_account_page() ) ) || ( function_exists( 'is_product' ) && is_product() ) || ( function_exists( 'is_shop' ) && ( is_shop() || is_product_taxonomy() ) );
		if ( $noindex ) {
			$robots['noindex'] = true;
			$robots['follow']  = true;
		}
		return $robots;
	}

	private static function description(): string {
		$d = '';
		if ( is_front_page() || is_singular() ) {
			$id = is_front_page() && get_option( 'page_on_front' ) ? (int) get_option( 'page_on_front' ) : get_queried_object_id();
			$d  = has_excerpt( $id ) ? get_the_excerpt( $id ) : '';
		} elseif ( is_home() ) {
			$id = (int) get_option( 'page_for_posts' );
			$d  = $id && has_excerpt( $id ) ? get_the_excerpt( $id ) : '';
		} elseif ( is_category() || is_tax() ) {
			$d = term_description();
		}
		if ( '' === $d ) {
			$d = get_bloginfo( 'description' );
		}
		return trim( wp_html_excerpt( wp_strip_all_tags( $d ), 158, '…' ) );
	}

	public static function head(): void {
		if ( self::seo_plugin_active() || is_admin() ) {
			return;
		}
		$desc  = self::description();
		$title = wp_get_document_title();
		$url   = is_singular() ? get_permalink() : home_url( add_query_arg( array() ) );
		$logo  = (int) get_theme_mod( 'custom_logo' );
		$img   = get_site_icon_url( 512 );
		if ( is_singular() && has_post_thumbnail() ) {
			$img = get_the_post_thumbnail_url( null, 'large' );
		}
		if ( $desc ) {
			echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
		}
		if ( is_singular() || is_front_page() ) {
			echo '<link rel="canonical" href="' . esc_url( is_front_page() ? home_url( '/' ) : get_permalink() ) . '">' . "\n";
		}
		printf( '<meta property="og:type" content="%s">' . "\n", is_singular( 'post' ) ? 'article' : 'website' );
		printf( '<meta property="og:site_name" content="%s">' . "\n", esc_attr( get_bloginfo( 'name' ) ) );
		printf( '<meta property="og:title" content="%s">' . "\n", esc_attr( $title ) );
		if ( $desc ) {
			printf( '<meta property="og:description" content="%s">' . "\n", esc_attr( $desc ) );
		}
		printf( '<meta property="og:url" content="%s">' . "\n", esc_url( $url ) );
		if ( $img ) {
			printf( '<meta property="og:image" content="%s">' . "\n", esc_url( $img ) );
		}
		echo '<meta name="twitter:card" content="summary_large_image">' . "\n";

		if ( is_front_page() ) {
			$org = array(
				'@context' => 'https://schema.org',
				'@graph'   => array(
					array_filter(
						array(
							'@type' => 'Organization',
							'@id'   => home_url( '/#organization' ),
							'name'  => get_bloginfo( 'name' ),
							'url'   => home_url( '/' ),
							'logo'  => $logo ? wp_get_attachment_image_url( $logo, 'full' ) : null,
							'email' => apply_filters( 'sb_public_email', 'hello@seobooster.uk' ),
						)
					),
					array(
						'@type'     => 'WebSite',
						'@id'       => home_url( '/#website' ),
						'url'       => home_url( '/' ),
						'name'      => get_bloginfo( 'name' ),
						'publisher' => array( '@id' => home_url( '/#organization' ) ),
					),
				),
			);
			echo '<script type="application/ld+json">' . wp_json_encode( $org, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . '</script>' . "\n";
		}
	}

	/* ------------------------------------------------------------------ product page quote button */

	private static function quote_html( WC_Product $product ): string {
		return '<p class="sb-product-quote"><a class="wp-element-button sb-btn sb-btn--primary" href="' . esc_url( SB_Packages::quote_url( $product ) ) . '">' . esc_html__( 'Get a quote for this package', 'seo-booster-core' ) . '</a></p>';
	}

	public static function quote_button_block( string $html ): string {
		$product = wc_get_product( get_the_ID() );
		if ( $product && 'quote' === $product->get_meta( '_sb_pricing_model' ) ) {
			return $html . self::quote_html( $product );
		}
		return $html;
	}

	public static function quote_button_classic(): void {
		global $product;
		if ( $product instanceof WC_Product && 'quote' === $product->get_meta( '_sb_pricing_model' ) && ! wp_is_block_theme() ) {
			echo self::quote_html( $product ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in quote_html().
		}
	}
}
