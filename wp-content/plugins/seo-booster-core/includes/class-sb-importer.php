<?php
/**
 * Imports SERVICE_CATALOG.csv into WooCommerce products (upsert by SKU).
 * Admin: Tools → SEO Booster catalog. CLI: wp sb import-catalog [--file=path] [--dry-run].
 *
 * Status rules: fixed price + both approvals + price > 0 + publish=READY → publish;
 *               pricing_model=quote + scope approved + publish=QUOTE → publish (quote button);
 *               everything else → draft.
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

/**
 * Catalog importer.
 */
class SB_Importer {

	public static function init(): void {
		add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
		if ( defined( 'WP_CLI' ) && WP_CLI ) {
			WP_CLI::add_command( 'sb import-catalog', array( __CLASS__, 'cli' ) );
		}
	}

	public static function default_file(): string {
		return SB_CORE_DIR . 'data/SERVICE_CATALOG.csv';
	}

	public static function menu(): void {
		add_management_page( __( 'SEO Booster catalog', 'seo-booster-core' ), __( 'SEO Booster catalog', 'seo-booster-core' ), 'manage_woocommerce', 'sb-catalog', array( __CLASS__, 'page' ) );
	}

	public static function page(): void {
		if ( ! current_user_can( 'manage_woocommerce' ) ) {
			return;
		}
		$report = null;
		if ( isset( $_POST['sb_import'] ) && check_admin_referer( 'sb_import' ) ) {
			$report = self::import( self::default_file(), ! empty( $_POST['sb_dry_run'] ) );
		}
		echo '<div class="wrap"><h1>' . esc_html__( 'SEO Booster catalog', 'seo-booster-core' ) . '</h1>';
		echo '<p>' . esc_html__( 'Creates or updates service packages from the bundled SERVICE_CATALOG.csv, matched by SKU. Prices you change later in wp-admin are overwritten only if you import again.', 'seo-booster-core' ) . '</p>';
		echo '<form method="post">';
		wp_nonce_field( 'sb_import' );
		echo '<p><label><input type="checkbox" name="sb_dry_run" value="1" checked> ' . esc_html__( 'Dry run (show what would change)', 'seo-booster-core' ) . '</label></p>';
		submit_button( __( 'Run import', 'seo-booster-core' ), 'primary', 'sb_import' );
		echo '</form>';
		if ( $report ) {
			echo '<h2>' . esc_html__( 'Result', 'seo-booster-core' ) . '</h2><pre style="background:#fff;padding:12px;max-height:480px;overflow:auto">' . esc_html( implode( "\n", $report ) ) . '</pre>';
		}
		echo '</div>';
	}

	/**
	 * WP-CLI handler.
	 *
	 * @param array $args       Positional.
	 * @param array $assoc_args Assoc.
	 */
	public static function cli( array $args, array $assoc_args ): void {
		$file = $assoc_args['file'] ?? self::default_file();
		foreach ( self::import( $file, isset( $assoc_args['dry-run'] ) ) as $line ) {
			WP_CLI::log( $line );
		}
	}

	/**
	 * Product page description built from the package fields, so the single product page explains the package.
	 *
	 * @param array<string,string> $meta Package meta.
	 */
	public static function description( array $meta, string $service, string $service_slug ): string {
		$list = static function ( string $title, string $lines ): string {
			$items = array_filter( array_map( 'trim', preg_split( '/\r\n|\r|\n/', $lines ) ) );
			if ( ! $items ) {
				return '';
			}
			return '<h3>' . esc_html( $title ) . '</h3><ul>' . implode( '', array_map( static fn( $i ) => '<li>' . esc_html( $i ) . '</li>', $items ) ) . '</ul>';
		};
		$html  = '<div class="sb-product-info">';
		$html .= ! empty( $meta['_sb_ideal_for'] ) ? '<p><strong>' . esc_html__( 'Ideal for:', 'seo-booster-core' ) . '</strong> ' . esc_html( $meta['_sb_ideal_for'] ) . '</p>' : '';
		$html .= $list( __( "What's included", 'seo-booster-core' ), $meta['_sb_deliverables'] ?? '' );
		$html .= $list( __( 'Not included', 'seo-booster-core' ), $meta['_sb_exclusions'] ?? '' );
		$html .= $list( __( 'What we need from you', 'seo-booster-core' ), $meta['_sb_requirements'] ?? '' );
		$facts = array_filter(
			array(
				__( 'Delivery', 'seo-booster-core' )  => $meta['_sb_turnaround'] ?? '',
				__( 'Revisions', 'seo-booster-core' ) => $meta['_sb_revisions'] ?? '',
			)
		);
		if ( $facts ) {
			$html .= '<h3>' . esc_html__( 'Delivery & revisions', 'seo-booster-core' ) . '</h3><ul>';
			foreach ( $facts as $k => $v ) {
				$html .= '<li><strong>' . esc_html( $k ) . ':</strong> ' . esc_html( $v ) . '</li>';
			}
			$html .= '</ul>';
		}
		$html .= '<p>' . esc_html__( 'After checkout you will complete a short project brief in your account. The delivery time starts when the brief is complete.', 'seo-booster-core' ) . '</p>';
		$html .= '<p><a href="' . esc_url( home_url( '/services/' . $service_slug . '/' ) ) . '">' . esc_html( sprintf( /* translators: %s: service */ __( 'Compare all %s packages', 'seo-booster-core' ), $service ) ) . ' →</a></p>';
		return $html . '</div>';
	}

	/** @return array<int,array<string,string>> */
	public static function read_csv( string $file ): array {
		$rows = array();
		$fh   = fopen( $file, 'r' ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_fopen
		if ( ! $fh ) {
			return $rows;
		}
		$head = fgetcsv( $fh, 0, ',', '"', '\\' );
		while ( ( $r = fgetcsv( $fh, 0, ',', '"', '\\' ) ) !== false ) { // phpcs:ignore Generic.CodeAnalysis.AssignmentInCondition.FoundInWhileCondition
			if ( count( $r ) === count( $head ) ) {
				$rows[] = array_combine( $head, $r );
			}
		}
		fclose( $fh ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_fclose
		return $rows;
	}

	private static function term( string $name, string $tax, int $parent = 0 ): int {
		$slug  = sanitize_title( $name );
		$found = get_term_by( 'slug', $slug, $tax );
		if ( $found ) {
			// Pre-existing term (e.g. created by hand or a theme demo): make sure it sits under the right parent.
			if ( (int) $found->parent !== $parent ) {
				wp_update_term( (int) $found->term_id, $tax, array( 'parent' => $parent ) );
			}
			return (int) $found->term_id;
		}
		$res = wp_insert_term( $name, $tax, array( 'slug' => $slug, 'parent' => $parent ) );
		return is_wp_error( $res ) ? 0 : (int) $res['term_id'];
	}

	public static function import( string $file, bool $dry = false ): array {
		$rows = self::read_csv( $file );
		if ( ! $rows ) {
			return array( 'No rows read from ' . $file );
		}
		$content = require SB_CORE_DIR . 'data/group-content.php';
		$log     = array();
		$sort    = array();
		$gsort   = 0;
		foreach ( $rows as $row ) {
			$sku      = sanitize_title( $row['package_code'] );
			$group    = sanitize_title( $row['group'] );
			$gc       = $content[ $group ] ?? array();
			$model    = 'quote' === ( $row['pricing_model'] ?? '' ) ? 'quote' : 'fixed';
			$price    = is_numeric( $row['price'] ) ? (string) (float) $row['price'] : '';
			$approved = 'YES' === $row['price_approved'] && 'YES' === $row['scope_approved'];
			$status   = 'draft';
			if ( 'fixed' === $model && $approved && $price && 'READY' === $row['publish'] ) {
				$status = 'publish';
			} elseif ( 'quote' === $model && 'YES' === $row['scope_approved'] && 'QUOTE' === $row['publish'] ) {
				$status = 'publish';
			}
			$existing = wc_get_product_id_by_sku( $sku );
			$log[]    = sprintf( '%s %-55s %-8s %s', $existing ? 'UPDATE' : 'CREATE', $sku, $price ? '$' . $price : $model, $status );
			if ( $dry ) {
				continue;
			}

			$family_id  = self::term( $row['category'], 'product_cat' );
			$service_id = self::term( $row['service'], 'product_cat', $family_id );
			$group_id   = self::term( $row['group'], SB_Packages::TAX );
			if ( ! isset( $sort[ $group ] ) ) {
				$sort[ $group ] = 0;
				update_term_meta( $group_id, '_sb_group_sort', ++$gsort );
				if ( ! empty( $gc['intro'] ) ) {
					wp_update_term( $group_id, SB_Packages::TAX, array( 'description' => $gc['intro'] ) );
				}
			}
			$sort[ $group ] += 10;
			$idx             = (int) ( $sort[ $group ] / 10 ); // 1-based position within the group.

			$product = $existing ? wc_get_product( $existing ) : new WC_Product_Simple();
			$product->set_name( $row['package_title'] );
			$product->set_sku( $sku );
			$product->set_virtual( true );
			$product->set_downloadable( false );
			$product->set_sold_individually( false );
			$product->set_tax_status( 'taxable' );
			$product->set_regular_price( 'fixed' === $model ? $price : '' );
			$product->set_category_ids( array( $service_id ) );
			$product->set_status( $status );
			$qty = (int) $row['quantity'];
			$product->set_short_description( $gc['intro'] ?? '' );
			$meta = array(
				'_sb_pricing_model'  => $model,
				'_sb_quantity'       => $qty ? (string) $qty : '',
				'_sb_unit'           => $row['unit'],
				'_sb_turnaround'     => 'TBD' === $row['turnaround'] ? '' : $row['turnaround'],
				'_sb_revisions'      => 'TBD' === $row['revisions'] ? '' : $row['revisions'],
				'_sb_brief_profile'  => $gc['brief'] ?? 'generic',
				'_sb_terms_version'  => '2026-11-draft',
				'_sb_sort'           => (string) $sort[ $group ],
				'_sb_price_approved' => 'YES' === $row['price_approved'] ? '1' : '',
				'_sb_scope_approved' => 'YES' === $row['scope_approved'] ? '1' : '',
				'_sb_featured'       => ( in_array( $qty, $gc['featured'] ?? array(), true ) || in_array( $idx, $gc['featured_index'] ?? array(), true ) ) ? '1' : '',
			);
			foreach ( array( 'deliverables', 'exclusions', 'requirements' ) as $k ) {
				if ( isset( $gc[ $k ] ) ) {
					$meta[ '_sb_' . $k ] = $gc[ $k ];
				}
			}
			if ( isset( $gc['deliverables_by_index'][ $idx ] ) ) {
				$meta['_sb_deliverables'] = $gc['deliverables_by_index'][ $idx ];
			}
			if ( isset( $gc['ideal_for'][ $qty ] ) ) {
				$meta['_sb_ideal_for'] = $gc['ideal_for'][ $qty ];
			} elseif ( isset( $gc['ideal_for_index'][ $idx ] ) ) {
				$meta['_sb_ideal_for'] = $gc['ideal_for_index'][ $idx ];
			}
			foreach ( $meta as $k => $v ) {
				$product->update_meta_data( $k, $v );
			}
			$product->set_description( self::description( $meta, $row['service'], sanitize_title( $row['service'] ) ) );
			SB_Packages::$bypass_gate = true;
			$id                       = $product->save();
			SB_Packages::$bypass_gate = false;
			wp_set_object_terms( $id, array( $group_id ), SB_Packages::TAX );
		}
		$log[] = $dry ? 'Dry run — nothing saved.' : 'Done.';
		return $log;
	}
}
