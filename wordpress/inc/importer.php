<?php
/**
 * Idempotent, batched content importer.
 *
 * Runs automatically when wordpress/data/site.json has a new "version". Each request processes
 * work for up to ~15 seconds, then resumes on the next request, so it never times out.
 * Everything is upserted by slug / SKU / file hash, so re-running never duplicates content.
 * Status: /wp-json/rrm/v1/status
 */
defined( 'ABSPATH' ) || exit;

add_action( 'init', 'rrm_maybe_import', 99 );
add_action( 'rest_api_init', function () {
	register_rest_route(
		'rrm/v1',
		'/status',
		array(
			'methods'             => 'GET',
			'permission_callback' => '__return_true',
			'callback'            => function () {
				$state = get_option( 'rrm_import_state', array() );
				return array(
					'data_version'     => rrm_data( 'version' ),
					'imported_version' => get_option( 'rrm_imported_version' ),
					'step'             => isset( $state['step'] ) ? $state['step'] : null,
					'theme'            => get_stylesheet(),
					'woocommerce'      => class_exists( 'WooCommerce' ),
					'rank_math'        => class_exists( 'RankMath' ),
					'log'              => array_slice( (array) get_option( 'rrm_import_log', array() ), -15 ),
					'last_fatal'       => get_option( 'rrm_last_fatal' ),
					'template_dir'     => get_template_directory(),
					'template_exists'  => file_exists( get_template_directory() . '/index.php' ),
					'theme_errors'     => is_wp_error( wp_get_theme()->errors() ) ? wp_get_theme()->errors()->get_error_messages() : array(),
					'php'              => PHP_VERSION,
				);
			},
		)
	);
} );

register_shutdown_function(
	function () {
		$e = error_get_last();
		if ( $e && in_array( $e['type'], array( E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR, E_RECOVERABLE_ERROR ), true ) ) {
			update_option( 'rrm_last_fatal', gmdate( 'c' ) . ' ' . substr( $e['message'], 0, 600 ) . ' @ ' . str_replace( WP_CONTENT_DIR, '', $e['file'] ) . ':' . $e['line'], false );
		}
	}
);

function rrm_log( $msg ) {
	$log   = (array) get_option( 'rrm_import_log', array() );
	$log[] = gmdate( 'H:i:s' ) . ' ' . $msg;
	update_option( 'rrm_import_log', array_slice( $log, -80 ), false );
}

function rrm_maybe_import() {
	if ( get_option( 'rrm_flush_rewrite' ) ) {
		delete_option( 'rrm_flush_rewrite' );
		flush_rewrite_rules( false );
	}
	$version = rrm_data( 'version' );
	if ( ! $version || get_option( 'rrm_imported_version' ) === $version ) {
		return;
	}
	// Atomic lock: add_option() is an INSERT on a unique key, so only one request can win.
	$lock = get_option( 'rrm_import_lock' );
	if ( $lock && ( time() - (int) $lock ) > 180 ) {
		delete_option( 'rrm_import_lock' ); // stale lock from a crashed request
	}
	if ( ! add_option( 'rrm_import_lock', time(), '', 'no' ) ) {
		return;
	}
	@set_time_limit( 120 ); // phpcs:ignore
	wp_raise_memory_limit( 'admin' );

	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	require_once ABSPATH . 'wp-admin/includes/post.php';
	kses_remove_filters(); // our bundled content contains inline SVG; it is trusted, not user input.

	$steps = array( 'settings', 'cleanup', 'media', 'pages', 'products', 'posts', 'finalize' );
	$state = get_option( 'rrm_import_state', array() );
	if ( empty( $state['version'] ) || $state['version'] !== $version ) {
		$state = array( 'version' => $version, 'step' => 0, 'cursor' => 0 );
		rrm_log( "Import {$version} started" );
	}
	$deadline = microtime( true ) + 15;

	try {
		while ( $state['step'] < count( $steps ) && microtime( true ) < $deadline ) {
			$fn   = 'rrm_step_' . $steps[ $state['step'] ];
			$done = call_user_func_array( $fn, array( &$state, $deadline ) );
			if ( $done ) {
				rrm_log( 'Step done: ' . $steps[ $state['step'] ] );
				$state['step']++;
				$state['cursor'] = 0;
			}
			update_option( 'rrm_import_state', $state, false );
		}
		if ( $state['step'] >= count( $steps ) ) {
			update_option( 'rrm_imported_version', $version );
			rrm_log( "Import {$version} complete" );
		}
	} catch ( Throwable $e ) {
		rrm_log( 'ERROR: ' . $e->getMessage() . ' @' . basename( $e->getFile() ) . ':' . $e->getLine() );
	}
	kses_init_filters();
	delete_option( 'rrm_import_lock' );
}

/* ---------------------------------------------------------------- settings */
function rrm_step_settings( &$state, $deadline ) {
	$s = rrm_data( 'settings' );
	update_option( 'blogname', $s['name'] );
	update_option( 'blogdescription', $s['tagline'] );
	update_option( 'timezone_string', 'Europe/London' );
	update_option( 'date_format', 'j F Y' );
	update_option( 'permalink_structure', '/%postname%/' );
	update_option( 'default_comment_status', 'closed' );
	update_option( 'default_ping_status', 'closed' );
	update_option( 'blog_public', ! empty( $s['indexable'] ) ? 1 : 0 );
	update_option( 'posts_per_page', 9 );
	update_option( 'thumbnail_size_w', 480 );
	update_option( 'thumbnail_size_h', 300 );

	if ( class_exists( 'WooCommerce' ) ) {
		$wc = array(
			'woocommerce_currency'                   => $s['currency_code'],
			'woocommerce_currency_pos'               => 'left',
			'woocommerce_price_num_decimals'         => 2,
			'woocommerce_default_country'            => 'GB',
			'woocommerce_calc_taxes'                 => 'no',
			'woocommerce_enable_reviews'             => 'no',
			'woocommerce_cart_redirect_after_add'    => 'yes',
			'woocommerce_enable_ajax_add_to_cart'    => 'no',
			'woocommerce_enable_guest_checkout'      => 'yes',
			'woocommerce_coming_soon'                => 'no',
			'woocommerce_store_pages_only'           => 'no',
			'woocommerce_ship_to_countries'          => 'disabled',
			'woocommerce_manage_stock'               => 'no',
			'woocommerce_allow_tracking'             => 'no',
			'woocommerce_show_marketplace_suggestions' => 'no',
			'woocommerce_checkout_company_field'     => 'optional',
			'woocommerce_checkout_address_2_field'   => 'hidden',
			'woocommerce_checkout_phone_field'       => 'optional',
			'woocommerce_enable_signup_and_login_from_checkout' => 'yes',
			'woocommerce_registration_generate_password' => 'yes',
		);
		foreach ( $wc as $k => $v ) {
			update_option( $k, $v );
		}
		// Classic (shortcode) cart & checkout: reliable with every gateway and our slim service checkout.
		foreach ( array( 'checkout' => '[woocommerce_checkout]', 'cart' => '[woocommerce_cart]' ) as $pg => $sc ) {
			$pid = wc_get_page_id( $pg );
			if ( $pid > 0 ) {
				wp_update_post( array( 'ID' => $pid, 'post_content' => '<!-- wp:shortcode -->' . $sc . '<!-- /wp:shortcode -->' ) );
				update_post_meta( $pid, 'rank_math_robots', array( 'noindex', 'follow' ) );
			}
		}
		update_option(
			'woocommerce_permalinks',
			array(
				'product_base'           => '/package',
				'category_base'          => 'packages',
				'tag_base'               => 'package-tag',
				'attribute_base'         => '',
				'use_verbose_page_rules' => false,
			)
		);
	}
	if ( class_exists( 'RankMath' ) ) {
		rrm_configure_rank_math( $s );
	}
	update_option( 'rrm_flush_rewrite', 1 );
	return true;
}

function rrm_configure_rank_math( $s ) {
	update_option( 'rank_math_wizard_completed', true );
	update_option( 'rank_math_is_configured', true );
	$modules = (array) get_option( 'rank_math_modules', array() );
	update_option( 'rank_math_modules', array_values( array_unique( array_merge( $modules, array( 'rich-snippet', 'sitemap', 'woocommerce', 'redirections', 'image-seo', 'local-seo', 'seo-analysis', 'link-counter', '404-monitor' ) ) ) ) );

	$titles = (array) get_option( 'rank-math-options-titles', array() );
	$titles = array_merge(
		$titles,
		array(
			'knowledgegraph_type'   => 'company',
			'knowledgegraph_name'   => $s['legal_name'],
			'website_name'          => $s['name'],
			'website_alternate_name'=> 'RankRight',
			'knowledgegraph_logo'   => rrm_assets_url( 'img/logo-rankright-media.png' ),
			'local_business_type'   => 'ProfessionalService',
			'local_address'         => array(
				'streetAddress'   => $s['address']['street'],
				'addressLocality' => $s['address']['locality'],
				'addressRegion'   => $s['address']['region'],
				'postalCode'      => $s['address']['postcode'],
				'addressCountry'  => 'GB',
			),
			'local_address_format'  => '{address} {locality}, {region} {postalcode}',
			'phone'                 => $s['phone_e164'],
			'email'                 => $s['email'],
			'url'                   => home_url( '/' ),
			'open_graph_image'      => rrm_assets_url( 'img/og-default.png' ),
			'title_separator'       => '|',
			'pt_post_default_rich_snippet'    => 'article',
			'pt_post_default_article_type'    => 'BlogPosting',
			'pt_product_default_rich_snippet' => 'product',
			'pt_page_default_rich_snippet'    => 'off',
			'noindex_empty_taxonomies'        => 'on',
			'disable_author_archives'         => 'off',
		)
	);
	update_option( 'rank-math-options-titles', $titles );

	$general = (array) get_option( 'rank-math-options-general', array() );
	$general = array_merge(
		$general,
		array(
			'breadcrumbs'               => 'on',
			'strip_category_base'       => 'on',
			'attachment_redirect_urls'  => 'on',
			'nofollow_external_links'   => 'off',
			'new_window_external_links' => 'on',
			'add_img_alt'               => 'on',
			'img_alt_format'            => '%filename%',
			'wc_remove_product_base'    => 'off',
			'wc_remove_generator'       => 'on',
		)
	);
	update_option( 'rank-math-options-general', $general );

	$sitemap = (array) get_option( 'rank-math-options-sitemap', array() );
	$sitemap = array_merge(
		$sitemap,
		array(
			'pt_attachment_sitemap' => 'off',
			'pt_product_sitemap'    => 'on',
			'pt_post_sitemap'       => 'on',
			'pt_page_sitemap'       => 'on',
		)
	);
	update_option( 'rank-math-options-sitemap', $sitemap );
}

/* ---------------------------------------------------------------- cleanup */
function rrm_step_cleanup( &$state, $deadline ) {
	// Remove leftover copies created by Hostinger's plugin deploy (rankright-site-old-*, rrm-src).
	foreach ( (array) glob( WP_PLUGIN_DIR . '/{rankright-site-old-*,rrm-src}', GLOB_BRACE | GLOB_ONLYDIR ) as $dir ) {
		if ( $dir && realpath( $dir ) !== realpath( RRM_DIR ) ) {
			rrm_rmdir( $dir );
			rrm_log( 'Removed stale copy ' . basename( $dir ) );
		}
	}
	foreach ( array( 'hello-world' ) as $slug ) {
		$p = get_page_by_path( $slug, OBJECT, 'post' );
		if ( $p ) {
			wp_delete_post( $p->ID, true );
		}
	}
	foreach ( array( 'sample-page' ) as $slug ) {
		$p = get_page_by_path( $slug, OBJECT, 'page' );
		if ( $p ) {
			wp_delete_post( $p->ID, true );
		}
	}
	$priv = get_page_by_path( 'privacy-policy', OBJECT, 'page' );
	if ( $priv && 'draft' === $priv->post_status && ! get_post_meta( $priv->ID, '_rrm_managed', true ) ) {
		wp_delete_post( $priv->ID, true );
	}
	return true;
}

/* ---------------------------------------------------------------- media */
function rrm_media_id( $rel ) {
	$map = (array) get_option( 'rrm_media_map', array() );
	return isset( $map[ $rel ] ) ? (int) $map[ $rel ] : 0;
}

function rrm_step_media( &$state, $deadline ) {
	$media = (array) rrm_data( 'media' );
	$map   = (array) get_option( 'rrm_media_map', array() );
	$reset = (string) rrm_data( 'media_reset' );
	if ( 0 === $state['cursor'] && $reset && get_option( 'rrm_media_reset' ) !== $reset ) {
		foreach ( get_posts( array( 'post_type' => 'attachment', 'numberposts' => -1, 'fields' => 'ids', 'meta_key' => '_rrm_hash' ) ) as $aid ) {
			wp_delete_attachment( $aid, true );
		}
		$map = array();
		update_option( 'rrm_media_reset', $reset, false );
		rrm_log( 'Media library reset ' . $reset );
	}
	for ( $i = $state['cursor']; $i < count( $media ); $i++ ) {
		if ( microtime( true ) > $deadline ) {
			$state['cursor'] = $i;
			update_option( 'rrm_media_map', $map, false );
			return false;
		}
		$m    = $media[ $i ];
		$file = RRM_WP . '/data/media/' . $m['file'];
		if ( ! file_exists( $file ) ) {
			continue;
		}
		$hash = md5_file( $file );
		if ( ! empty( $map[ $m['file'] ] ) && get_post( $map[ $m['file'] ] ) && get_post_meta( $map[ $m['file'] ], '_rrm_hash', true ) === $hash ) {
			continue;
		}
		if ( ! empty( $map[ $m['file'] ] ) && get_post( $map[ $m['file'] ] ) ) {
			wp_delete_attachment( $map[ $m['file'] ], true ); // file changed: replace it
		}
		$tmp = wp_tempnam( $m['file'] );
		copy( $file, $tmp );
		$id = media_handle_sideload(
			array( 'name' => basename( $m['file'] ), 'tmp_name' => $tmp ),
			0,
			$m['title'],
			array( 'post_title' => $m['title'], 'post_excerpt' => isset( $m['caption'] ) ? $m['caption'] : '' )
		);
		if ( is_wp_error( $id ) ) {
			@unlink( $tmp ); // phpcs:ignore
			rrm_log( 'Media failed ' . $m['file'] . ': ' . $id->get_error_message() );
			continue;
		}
		update_post_meta( $id, '_wp_attachment_image_alt', $m['alt'] );
		update_post_meta( $id, '_rrm_hash', $hash );
		$map[ $m['file'] ] = $id;
	}
	update_option( 'rrm_media_map', $map, false );
	// Remove orphaned copies (e.g. from an interrupted run).
	$keep = array_map( 'intval', array_values( $map ) );
	foreach ( get_posts( array( 'post_type' => 'attachment', 'numberposts' => -1, 'fields' => 'ids', 'meta_key' => '_rrm_hash' ) ) as $aid ) {
		if ( ! in_array( (int) $aid, $keep, true ) ) {
			wp_delete_attachment( $aid, true );
		}
	}
	return true;
}

/* ---------------------------------------------------------------- shared */
function rrm_set_seo_meta( $post_id, $item ) {
	foreach ( array( 'rm_title' => 'rank_math_title', 'rm_desc' => 'rank_math_description', 'rm_focus' => 'rank_math_focus_keyword' ) as $k => $meta ) {
		if ( ! empty( $item[ $k ] ) ) {
			update_post_meta( $post_id, $meta, $item[ $k ] );
		}
	}
	if ( ! empty( $item['noindex'] ) ) {
		update_post_meta( $post_id, 'rank_math_robots', array( 'noindex', 'follow' ) );
	} else {
		delete_post_meta( $post_id, 'rank_math_robots' );
	}
}

function rrm_upsert_post( $type, $item, $extra = array() ) {
	$existing = get_page_by_path( $item['slug'], OBJECT, $type );
	$args     = array_merge(
		array(
			'post_type'    => $type,
			'post_status'  => 'publish',
			'post_title'   => $item['title'],
			'post_name'    => $item['slug'],
			'post_content' => $item['content'],
			'post_excerpt' => isset( $item['excerpt'] ) ? $item['excerpt'] : '',
			'menu_order'   => isset( $item['order'] ) ? (int) $item['order'] : 0,
		),
		$extra
	);
	if ( $existing ) {
		$args['ID'] = $existing->ID;
		$id         = wp_update_post( wp_slash( $args ), true );
	} else {
		$id = wp_insert_post( wp_slash( $args ), true );
	}
	if ( is_wp_error( $id ) ) {
		rrm_log( "Upsert {$type} {$item['slug']} failed: " . $id->get_error_message() );
		return 0;
	}
	update_post_meta( $id, '_rrm_managed', 1 );
	rrm_set_seo_meta( $id, $item );
	if ( ! empty( $item['image'] ) && rrm_media_id( $item['image'] ) ) {
		set_post_thumbnail( $id, rrm_media_id( $item['image'] ) );
	}
	return $id;
}

/* ---------------------------------------------------------------- pages */
function rrm_step_pages( &$state, $deadline ) {
	$ids = array();
	foreach ( (array) rrm_data( 'pages' ) as $p ) {
		$id = rrm_upsert_post( 'page', $p );
		if ( ! $id ) {
			continue;
		}
		$ids[ $p['slug'] ] = $id;
		update_post_meta( $id, '_rrm_raw', empty( $p['raw'] ) ? 0 : 1 );
		update_post_meta( $id, '_rrm_schema', isset( $p['schema'] ) ? wp_slash( wp_json_encode( $p['schema'] ) ) : '' );
		update_post_meta( $id, '_rrm_hero', isset( $p['hero'] ) ? wp_slash( wp_json_encode( $p['hero'] ) ) : '' );
		update_post_meta( $id, '_wp_page_template', 'default' );
	}
	update_option( 'rrm_page_ids', $ids, false );
	if ( isset( $ids['home'] ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $ids['home'] );
	}
	if ( isset( $ids['blog'] ) ) {
		update_option( 'page_for_posts', $ids['blog'] );
	}
	if ( isset( $ids['privacy-policy'] ) ) {
		update_option( 'wp_page_for_privacy_policy', $ids['privacy-policy'] );
	}
	if ( isset( $ids['terms-and-conditions'] ) ) {
		update_option( 'woocommerce_terms_page_id', $ids['terms-and-conditions'] );
	}
	return true;
}

/* ---------------------------------------------------------------- products */
function rrm_step_products( &$state, $deadline ) {
	if ( ! class_exists( 'WC_Product_Simple' ) ) {
		rrm_log( 'WooCommerce not active: products skipped' );
		return true;
	}
	$shop = wc_get_page_id( 'shop' );
	if ( $shop > 0 ) {
		wp_update_post( array( 'ID' => $shop, 'post_title' => 'All Packages' ) );
		update_post_meta( $shop, 'rank_math_title', 'Digital Marketing Packages & Prices | From $3.49' );
		update_post_meta( $shop, 'rank_math_description', 'Compare 36 fixed-price packages for SEO, link building, websites, content, PPC and social media. Every deliverable listed, secure checkout, start today.' );
	}
	$items = (array) rrm_data( 'products' );
	if ( 0 === $state['cursor'] ) {
		// Delete managed products that are not the canonical SKU holder (duplicates / removed packages).
		$skus = wp_list_pluck( $items, 'sku' );
		foreach ( get_posts( array( 'post_type' => 'product', 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids', 'meta_key' => '_rrm_managed' ) ) as $pid ) {
			$sku = get_post_meta( $pid, '_sku', true );
			if ( ! $sku || ! in_array( $sku, $skus, true ) || (int) wc_get_product_id_by_sku( $sku ) !== (int) $pid ) {
				wp_delete_post( $pid, true );
			}
		}
	}
	for ( $i = $state['cursor']; $i < count( $items ); $i++ ) {
		if ( microtime( true ) > $deadline ) {
			$state['cursor'] = $i;
			return false;
		}
		$it   = $items[ $i ];
		$term = term_exists( $it['cat_slug'], 'product_cat' );
		if ( ! $term ) {
			$term = wp_insert_term( $it['cat_name'], 'product_cat', array( 'slug' => $it['cat_slug'], 'description' => $it['cat_desc'] ) );
		}
		$term_id = is_array( $term ) ? (int) $term['term_id'] : (int) $term;
		if ( $term_id && ! empty( $it['cat_image'] ) && rrm_media_id( $it['cat_image'] ) ) {
			update_term_meta( $term_id, 'thumbnail_id', rrm_media_id( $it['cat_image'] ) );
		}

		$pid     = wc_get_product_id_by_sku( $it['sku'] );
		$product = $pid ? wc_get_product( $pid ) : new WC_Product_Simple();
		$product->set_name( $it['name'] );
		$product->set_slug( $it['slug'] );
		$product->set_sku( $it['sku'] );
		$product->set_status( 'publish' );
		$product->set_catalog_visibility( 'visible' );
		$product->set_virtual( true );
		$product->set_sold_individually( true );
		$product->set_regular_price( null === $it['price'] ? '' : (string) $it['price'] );
		$product->set_sale_price( '' );
		$product->set_short_description( $it['short_desc'] );
		$product->set_description( $it['description'] );
		$product->set_menu_order( (int) $it['order'] );
		$product->set_featured( ! empty( $it['featured'] ) );
		$product->set_reviews_allowed( false );
		$product->set_category_ids( $term_id ? array( $term_id ) : array() );
		if ( ! empty( $it['image'] ) && rrm_media_id( $it['image'] ) ) {
			$product->set_image_id( rrm_media_id( $it['image'] ) );
		}
		foreach ( array( 'service', 'short', 'tagline', 'unit', 'delivery', 'tier', 'audience' ) as $k ) {
			$product->update_meta_data( '_rrm_' . $k, isset( $it[ $k ] ) ? $it[ $k ] : '' );
		}
		$product->update_meta_data( '_rrm_features', wp_json_encode( $it['features'] ) );
		$product->update_meta_data( '_rrm_featured', empty( $it['featured'] ) ? 0 : 1 );
		$id = $product->save();
		update_post_meta( $id, '_rrm_managed', 1 );
		rrm_set_seo_meta( $id, $it );
	}
	return true;
}

/* ---------------------------------------------------------------- posts */
function rrm_step_posts( &$state, $deadline ) {
	$author = get_users( array( 'role' => 'administrator', 'number' => 1, 'fields' => 'ID' ) );
	$author = $author ? (int) $author[0] : 1;
	$a      = rrm_data( 'author' );
	if ( $a ) {
		wp_update_user(
			array(
				'ID'           => $author,
				'display_name' => $a['name'],
				'first_name'   => $a['first'],
				'last_name'    => $a['last'],
				'description'  => $a['bio'],
				'nickname'     => $a['name'],
			)
		);
	}
	$items = (array) rrm_data( 'posts' );
	for ( $i = $state['cursor']; $i < count( $items ); $i++ ) {
		if ( microtime( true ) > $deadline ) {
			$state['cursor'] = $i;
			return false;
		}
		$p   = $items[ $i ];
		$cat = term_exists( $p['category_slug'], 'category' );
		if ( ! $cat ) {
			$cat = wp_insert_term( $p['category'], 'category', array( 'slug' => $p['category_slug'] ) );
		}
		$cat_id = is_array( $cat ) ? (int) $cat['term_id'] : (int) $cat;
		$id     = rrm_upsert_post(
			'post',
			$p,
			array(
				'post_author'   => $author,
				'post_date'     => $p['date'],
				'post_category' => array( $cat_id ),
				'comment_status'=> 'closed',
			)
		);
		if ( $id ) {
			wp_set_post_tags( $id, $p['tags'], false );
			update_post_meta( $id, '_rrm_faqs', wp_slash( wp_json_encode( $p['faqs'] ) ) );
			update_post_meta( $id, '_rrm_takeaways', wp_slash( wp_json_encode( $p['takeaways'] ) ) );
			update_post_meta( $id, '_rrm_service', $p['service'] );
		}
	}
	// Remove the default "Uncategorized" from view by renaming it.
	$unc = get_term_by( 'slug', 'uncategorized', 'category' );
	if ( $unc ) {
		wp_update_term( $unc->term_id, 'category', array( 'name' => 'Insights', 'slug' => 'insights' ) );
	}
	return true;
}

/* ---------------------------------------------------------------- finalize */
function rrm_step_finalize( &$state, $deadline ) {
	update_option( 'rrm_flush_rewrite', 1 );
	if ( function_exists( 'wc_delete_product_transients' ) ) {
		wc_delete_product_transients();
	}
	return true;
}

function rrm_rmdir( $dir ) {
	$it = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $dir, FilesystemIterator::SKIP_DOTS ), RecursiveIteratorIterator::CHILD_FIRST );
	foreach ( $it as $f ) {
		$f->isDir() ? @rmdir( $f->getPathname() ) : @unlink( $f->getPathname() ); // phpcs:ignore
	}
	@rmdir( $dir ); // phpcs:ignore
}
