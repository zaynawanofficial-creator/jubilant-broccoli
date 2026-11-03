<?php
/**
 * Appearance → SEO Booster Setup: builds the whole site from the theme's patterns in one click.
 *
 * Every step is optional and idempotent:
 *  - Pages are created from patterns/page-*.php. Existing pages are only overwritten when they were created
 *    by this screen AND "Overwrite" is ticked. Pages you created yourself are never touched.
 *  - Old WoodMart demo pages are moved to Draft (never deleted).
 *
 * @package SEOBoosterTheme
 */

defined( 'ABSPATH' ) || exit;

/**
 * Site builder.
 */
final class SBT_Setup {

	const META   = '_sbt_generated';
	const DEMO   = array( 'home-corporate-2', 'about-us-3', 'contact-us', 'portfolio', 'wishlist', 'compare', 'blog' );
	const ACTION = 'sbt_setup';

	public static function init(): void {
		add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
		add_action( 'admin_notices', array( __CLASS__, 'nudge' ) );
	}

	public static function menu(): void {
		add_theme_page( __( 'SEO Booster Setup', 'seo-booster' ), __( 'SEO Booster Setup', 'seo-booster' ), 'manage_options', 'sbt-setup', array( __CLASS__, 'page' ) );
	}

	/** One-time hint after activating the theme. */
	public static function nudge(): void {
		if ( get_option( 'sbt_setup_done' ) || ! current_user_can( 'manage_options' ) ) {
			return;
		}
		$screen = get_current_screen();
		if ( $screen && 'appearance_page_sbt-setup' === $screen->id ) {
			return;
		}
		echo '<div class="notice notice-info"><p><strong>SEO Booster theme:</strong> ' . esc_html__( 'build all pages, menus, logo and starter articles in one click.', 'seo-booster' ) . ' <a class="button button-primary" href="' . esc_url( admin_url( 'themes.php?page=sbt-setup' ) ) . '">' . esc_html__( 'Open setup', 'seo-booster' ) . '</a></p></div>';
	}

	private static function manifest(): array {
		return require get_theme_file_path( 'inc/site-manifest.php' );
	}

	/** Pattern markup (PHP already evaluated, so image URLs are absolute). */
	private static function pattern( string $slug ): string {
		$reg = WP_Block_Patterns_Registry::get_instance();
		$p   = $reg->get_registered( $slug );
		if ( $p && ! empty( $p['content'] ) ) {
			return $p['content'];
		}
		// Fallback: render the pattern file directly.
		$file = get_theme_file_path( 'patterns/' . substr( $slug, strlen( 'seo-booster/' ) ) . '.php' );
		if ( ! is_readable( $file ) ) {
			return '';
		}
		ob_start();
		include $file;
		return (string) ob_get_clean();
	}

	public static function page(): void {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}
		$log = array();
		if ( isset( $_POST[ self::ACTION ] ) && check_admin_referer( self::ACTION ) ) {
			$opt = array_map( 'sanitize_key', array_keys( (array) wp_unslash( $_POST['sbt'] ?? array() ) ) );
			$log = self::run( array_fill_keys( $opt, true ) );
			update_option( 'sbt_setup_done', gmdate( 'c' ) );
		}
		$m = self::manifest();
		echo '<div class="wrap"><h1>' . esc_html__( 'SEO Booster Setup', 'seo-booster' ) . '</h1>';
		echo '<p>' . esc_html( sprintf( /* translators: 1: pages, 2: posts */ __( 'Builds %1$d pages and %2$d starter articles from the theme patterns. Take a backup first. Everything created here can be edited in the block editor afterwards.', 'seo-booster' ), count( $m['pages'] ) + 1, count( $m['posts'] ) ) ) . '</p>';
		if ( ! class_exists( 'SB_Shortcode' ) ) {
			echo '<div class="notice notice-warning inline"><p>' . esc_html__( 'The SEO Booster Core plugin is not active. Activate it so package cards, prices, forms and breadcrumbs appear on the pages.', 'seo-booster' ) . '</p></div>';
		}
		echo '<form method="post">';
		wp_nonce_field( self::ACTION );
		$opts = array(
			'pages'     => array( true, __( 'Create pages (Home, Services and 7 service pages, Packages, How it works, About, Contact, Get a quote, FAQ, Insights, 5 policy drafts)', 'seo-booster' ) ),
			'overwrite' => array( false, __( 'Overwrite pages previously created by this screen with the latest design (tick this when updating the theme; your own pages are never touched)', 'seo-booster' ) ),
			'posts'     => array( true, __( 'Create 3 starter Insights articles', 'seo-booster' ) ),
			'reading'   => array( true, __( 'Set Home as the front page and Insights as the posts page', 'seo-booster' ) ),
			'brand'     => array( true, __( 'Upload the logo and site icon, set the site title and tagline', 'seo-booster' ) ),
			'demo'      => array( true, __( 'Move old WoodMart demo pages to Draft: ', 'seo-booster' ) . implode( ', ', self::DEMO ) ),
			'woo'       => array( true, __( 'WooCommerce for services: require an account at checkout (needed for the project brief), USD currency, link Terms page at checkout', 'seo-booster' ) ),
			'bacs'      => array( false, __( 'Enable "Direct bank transfer" as a payment method so test orders can be placed (orders stay On hold until you confirm payment). Connect Stripe / PayPal separately.', 'seo-booster' ) ),
		);
		echo '<table class="form-table" role="presentation"><tbody>';
		foreach ( $opts as $key => $o ) {
			echo '<tr><td><label><input type="checkbox" name="sbt[' . esc_attr( $key ) . ']" value="1"' . checked( $o[0], true, false ) . '> ' . esc_html( $o[1] ) . '</label></td></tr>';
		}
		echo '</tbody></table>';
		submit_button( __( 'Build the site', 'seo-booster' ), 'primary', self::ACTION );
		echo '</form>';
		if ( $log ) {
			echo '<h2>' . esc_html__( 'Result', 'seo-booster' ) . '</h2><pre style="background:#fff;padding:12px;max-height:520px;overflow:auto;white-space:pre-wrap">' . esc_html( implode( "\n", $log ) ) . '</pre>';
			echo '<p><a class="button button-primary" href="' . esc_url( home_url( '/' ) ) . '" target="_blank" rel="noopener">' . esc_html__( 'View site', 'seo-booster' ) . '</a></p>';
		}
		echo '</div>';
	}

	/**
	 * @param array<string,bool> $o Options.
	 * @return string[] Log lines.
	 */
	public static function run( array $o ): array {
		$log = array();
		$m   = self::manifest();
		$ids = array();

		if ( ! empty( $o['pages'] ) ) {
			$pages   = $m['pages'];
			$pages[] = array( 'slug' => 'insights', 'title' => 'Insights', 'parent' => '', 'template' => '', 'excerpt' => 'Practical guides on SEO, link building, websites and content.', 'pattern' => '', 'order' => 9 );
			// Parents first.
			usort( $pages, static fn( $a, $b ) => ( '' === $a['parent'] ? 0 : 1 ) <=> ( '' === $b['parent'] ? 0 : 1 ) );
			foreach ( $pages as $p ) {
				$parent_id = $p['parent'] ? ( $ids[ $p['parent'] ] ?? self::page_id( $p['parent'] ) ) : 0;
				$existing  = self::page_id( $p['slug'], $parent_id );
				$content   = $p['pattern'] ? self::pattern( $p['pattern'] ) : '';
				if ( $p['pattern'] && '' === $content ) {
					$log[] = "SKIP  {$p['slug']}: pattern {$p['pattern']} not found";
					continue;
				}
				if ( $existing && ! get_post_meta( $existing, self::META, true ) ) {
					$ids[ $p['slug'] ] = $existing;
					$log[]             = "KEEP  /{$p['slug']}/ already exists and was not created here, left unchanged";
					continue;
				}
				if ( $existing && empty( $o['overwrite'] ) ) {
					$ids[ $p['slug'] ] = $existing;
					$log[]             = "KEEP  /{$p['slug']}/ exists (tick Overwrite to rebuild it)";
					continue;
				}
				$data = array(
					'post_type'    => 'page',
					'post_status'  => 'publish',
					'post_title'   => $p['title'],
					'post_name'    => $p['slug'],
					'post_parent'  => $parent_id,
					'post_excerpt' => $p['excerpt'],
					'post_content' => wp_slash( $content ),
					'menu_order'   => (int) $p['order'],
				);
				if ( $existing ) {
					$data['ID'] = $existing;
				}
				$id = wp_insert_post( $data, true );
				if ( is_wp_error( $id ) ) {
					$log[] = "ERROR {$p['slug']}: " . $id->get_error_message();
					continue;
				}
				update_post_meta( $id, self::META, SBT_VERSION );
				update_post_meta( $id, '_wp_page_template', $p['template'] ? $p['template'] : 'default' );
				$ids[ $p['slug'] ] = $id;
				$log[]             = ( $existing ? 'UPDATE ' : 'CREATE ' ) . wp_make_link_relative( get_permalink( $id ) );
			}
		}

		if ( ! empty( $o['posts'] ) ) {
			foreach ( $m['posts'] as $p ) {
				if ( get_page_by_path( $p['slug'], OBJECT, 'post' ) ) {
					$log[] = "KEEP  article {$p['slug']} exists";
					continue;
				}
				$cat = term_exists( $p['category'], 'category' );
				$cat = $cat ? (int) $cat['term_id'] : (int) wp_insert_term( $p['category'], 'category' )['term_id'];
				$id  = wp_insert_post(
					array(
						'post_type'     => 'post',
						'post_status'   => 'publish',
						'post_title'    => $p['title'],
						'post_name'     => $p['slug'],
						'post_excerpt'  => $p['excerpt'],
						'post_content'  => wp_slash( self::pattern( $p['pattern'] ) ),
						'post_category' => array( $cat ),
					),
					true
				);
				if ( ! is_wp_error( $id ) ) {
					update_post_meta( $id, self::META, SBT_VERSION );
					$log[] = 'CREATE article ' . wp_make_link_relative( get_permalink( $id ) );
				}
			}
		}

		if ( ! empty( $o['reading'] ) ) {
			$home     = $ids['home'] ?? self::page_id( 'home' );
			$insights = $ids['insights'] ?? self::page_id( 'insights' );
			if ( $home ) {
				update_option( 'show_on_front', 'page' );
				update_option( 'page_on_front', $home );
				$log[] = 'SET   front page = Home';
			}
			if ( $insights ) {
				update_option( 'page_for_posts', $insights );
				$log[] = 'SET   posts page = Insights';
			}
			if ( '' === get_option( 'permalink_structure' ) ) {
				update_option( 'permalink_structure', '/%postname%/' );
				$log[] = 'SET   permalinks = /%postname%/';
			}
		}

		if ( ! empty( $o['brand'] ) ) {
			update_option( 'blogname', 'SEO Booster' );
			update_option( 'blogdescription', 'Fixed-price SEO, web, content and design services' );
			$logo = self::attach( 'logo.png', 'SEO Booster logo' );
			if ( $logo ) {
				set_theme_mod( 'custom_logo', $logo );
				update_option( 'site_logo', $logo );
				$log[] = 'SET   logo';
			}
			$icon = self::attach( 'site-icon.png', 'SEO Booster site icon' );
			if ( $icon ) {
				update_option( 'site_icon', $icon );
				$log[] = 'SET   site icon';
			}
		}

		if ( ! empty( $o['demo'] ) ) {
			foreach ( self::DEMO as $slug ) {
				$id = self::page_id( $slug );
				if ( $id && 'publish' === get_post_status( $id ) && ! get_post_meta( $id, self::META, true ) && (int) get_option( 'page_on_front' ) !== $id ) {
					wp_update_post( array( 'ID' => $id, 'post_status' => 'draft' ) );
					$log[] = "DRAFT old demo page /{$slug}/";
				}
			}
		}

		if ( ! empty( $o['woo'] ) && class_exists( 'WooCommerce' ) ) {
			update_option( 'woocommerce_enable_guest_checkout', 'no' );
			update_option( 'woocommerce_enable_checkout_login_reminder', 'yes' );
			update_option( 'woocommerce_enable_signup_and_login_from_checkout', 'yes' );
			update_option( 'woocommerce_registration_generate_password', 'yes' );
			update_option( 'woocommerce_currency', 'USD' );
			$terms = $ids['terms'] ?? self::page_id( 'terms' );
			if ( $terms ) {
				update_option( 'woocommerce_terms_page_id', $terms );
			}
			$privacy = $ids['privacy-policy'] ?? self::page_id( 'privacy-policy' );
			if ( $privacy ) {
				update_option( 'wp_page_for_privacy_policy', $privacy );
			}
			$log[] = 'SET   WooCommerce: account required at checkout, USD, terms + privacy pages linked';
		}

		if ( ! empty( $o['bacs'] ) && class_exists( 'WooCommerce' ) ) {
			$bacs                = (array) get_option( 'woocommerce_bacs_settings', array() );
			$bacs['enabled']     = 'yes';
			$bacs['title']       = $bacs['title'] ?? __( 'Bank transfer', 'seo-booster' );
			$bacs['description'] = $bacs['description'] ?? __( 'Pay by bank transfer. Use your order number as the reference. Work starts once payment is received.', 'seo-booster' );
			update_option( 'woocommerce_bacs_settings', $bacs );
			$log[] = 'SET   Direct bank transfer enabled (add your bank details in WooCommerce → Settings → Payments)';
		}

		flush_rewrite_rules();
		$log[] = 'Done.';
		return $log;
	}

	private static function page_id( string $slug, int $parent = -1 ): int {
		$args = array(
			'post_type'      => 'page',
			'name'           => $slug,
			'post_status'    => array( 'publish', 'draft', 'private', 'pending' ),
			'posts_per_page' => 1,
			'fields'         => 'ids',
			'no_found_rows'  => true,
		);
		if ( $parent >= 0 ) {
			$args['post_parent'] = $parent;
		}
		$q = get_posts( $args );
		return $q ? (int) $q[0] : 0;
	}

	/** Copy a theme image into the media library once; returns attachment ID. */
	private static function attach( string $file, string $title ): int {
		$existing = get_posts(
			array(
				'post_type'   => 'attachment',
				'meta_key'    => '_sbt_asset', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
				'meta_value'  => $file, // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_value
				'fields'      => 'ids',
				'numberposts' => 1,
			)
		);
		if ( $existing ) {
			return (int) $existing[0];
		}
		$src = get_theme_file_path( 'assets/images/' . $file );
		if ( ! is_readable( $src ) ) {
			return 0;
		}
		$up = wp_upload_bits( 'seo-booster-' . $file, null, (string) file_get_contents( $src ) ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
		if ( ! empty( $up['error'] ) ) {
			return 0;
		}
		$id = wp_insert_attachment(
			array(
				'post_title'     => $title,
				'post_mime_type' => 'image/png',
				'post_status'    => 'inherit',
			),
			$up['file']
		);
		if ( is_wp_error( $id ) || ! $id ) {
			return 0;
		}
		require_once ABSPATH . 'wp-admin/includes/image.php';
		wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $up['file'] ) );
		update_post_meta( $id, '_wp_attachment_image_alt', $title );
		update_post_meta( $id, '_sbt_asset', $file );
		return (int) $id;
	}
}

SBT_Setup::init();
