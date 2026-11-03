<?php
/**
 * Smoke test for SB_Importer::import() against the real SERVICE_CATALOG.csv,
 * using minimal in-memory stubs for the WordPress/WooCommerce functions it calls.
 * Run: php tests/importer-smoke.php
 */
define( 'ABSPATH', __DIR__ );
define( 'SB_CORE_DIR', dirname( __DIR__ ) . '/wp-content/plugins/seo-booster-core/' );
$GLOBALS['terms'] = array(); $GLOBALS['products'] = array(); $GLOBALS['obj_terms'] = array(); $GLOBALS['term_meta'] = array();
function sanitize_title( $s ) { return trim( preg_replace( '/[^a-z0-9]+/', '-', strtolower( str_replace( '&', 'and', $s ) ) ), '-' ); }
function __( $s ) { return $s; }
function esc_html__( $s ) { return $s; }
function esc_html( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function esc_url( $s ) { return $s; }
function home_url( $p = '' ) { return 'https://example.test' . $p; }
function get_term_by( $f, $slug, $tax ) { return $GLOBALS['terms'][ $tax ][ $slug ] ?? false; }
function wp_insert_term( $name, $tax, $a ) { $id = count( $GLOBALS['terms'], COUNT_RECURSIVE ) + 1; $GLOBALS['terms'][ $tax ][ $a['slug'] ] = (object) array( 'term_id' => $id, 'name' => $name, 'parent' => $a['parent'] ); return array( 'term_id' => $id ); }
function is_wp_error( $x ) { return false; }
function update_term_meta( $id, $k, $v ) { $GLOBALS['term_meta'][ $id ][ $k ] = $v; }
function wp_update_term( $id, $tax, $a ) { foreach ( $GLOBALS['terms'][ $tax ] as $t ) { if ( $t->term_id === $id && isset( $a['parent'] ) ) { $t->parent = $a['parent']; } } }
function wc_get_product_id_by_sku( $sku ) { foreach ( $GLOBALS['products'] as $id => $p ) { if ( $p->sku === $sku ) { return $id; } } return 0; }
function wc_get_product( $id ) { return $GLOBALS['products'][ $id ]; }
function get_post_thumbnail_id( $id ) { return 0; }
function wp_upload_bits() { return array( 'error' => 'stub' ); }
function wp_set_object_terms( $id, $t, $tax ) { $GLOBALS['obj_terms'][ $id ] = $t; }
class SB_Packages { const TAX = 'sb_package_group'; public static bool $bypass_gate = false; }
class WC_Product_Simple {
	public $id = 0, $description = '', $name, $sku, $status, $price, $virtual, $downloadable, $meta = array(), $cats;
	function __call( $m, $a ) { $map = array( 'set_description' => 'description', 'set_name' => 'name', 'set_sku' => 'sku', 'set_status' => 'status', 'set_regular_price' => 'price', 'set_virtual' => 'virtual', 'set_downloadable' => 'downloadable', 'set_category_ids' => 'cats' ); if ( isset( $map[ $m ] ) ) { $this->{$map[ $m ]} = $a[0]; } }
	function update_meta_data( $k, $v ) { $this->meta[ $k ] = $v; }
	function save() { if ( ! $this->id ) { $this->id = count( $GLOBALS['products'] ) + 1; } $GLOBALS['products'][ $this->id ] = $this; return $this->id; }
}
require SB_CORE_DIR . 'includes/class-sb-importer.php';

$fail = 0;
function check( $cond, $msg ) { global $fail; echo ( $cond ? "PASS " : "FAIL " ) . $msg . "\n"; if ( ! $cond ) { $fail++; } }

$csv = dirname( __DIR__ ) . '/SERVICE_CATALOG.csv';
// Simulate a pre-existing top-level category (as found on the live site).
wp_insert_term( 'Content Writing', 'product_cat', array( 'slug' => 'content-writing', 'parent' => 0 ) );
$dry = SB_Importer::import( $csv, true );
check( count( $GLOBALS['products'] ) === 0, 'dry run saves nothing' );
SB_Importer::import( $csv );
$rows = SB_Importer::read_csv( $csv );
check( count( $GLOBALS['products'] ) === count( $rows ), 'one product per CSV row (' . count( $rows ) . ')' );
SB_Importer::import( $csv );
check( count( $GLOBALS['products'] ) === count( $rows ), 're-import upserts by SKU (no duplicates)' );

$by = array(); foreach ( $GLOBALS['products'] as $p ) { $by[ $p->sku ] = $p; }
$p = $by['off-page-seo-profiles-and-citations-1'];
check( 'publish' === $p->status && '5' === $p->price, '5 links: published at $5' );
check( true === $p->virtual && false === $p->downloadable, 'packages are virtual, not downloadable' );
check( '' === $by['off-page-seo-profiles-and-citations-2']->meta['_sb_featured'] && '1' === $by['off-page-seo-profiles-and-citations-4']->meta['_sb_featured'], 'featured by quantity (20 links)' );
$g = array_filter( $by, fn( $p ) => str_starts_with( $p->sku, 'off-page-seo-premium-links-' ) );
check( 1 === count( array_filter( $g, fn( $p ) => '1' === $p->meta['_sb_featured'] ) ), 'exactly one featured premium link (index rule)' );
check( '49' === $by['off-page-seo-premium-links-3']->price && '1' === $by['off-page-seo-premium-links-3']->meta['_sb_featured'], 'DR30+ is $49 and featured' );
check( str_contains( $by['graphic-design-branding-1']->meta['_sb_deliverables'], '2 logo concepts' ) && ! str_contains( $by['graphic-design-branding-1']->meta['_sb_deliverables'], 'Full Brand' ), 'branding cards get their own deliverables' );
$q = $by['seo-audit-audit-packages-3'];
check( 'publish' === $q->status && '' === $q->price && 'quote' === $q->meta['_sb_pricing_model'], 'quote package published without a price' );
check( 'draft' === $by['ppc-management-ppc-packages-1']->status, 'planned services stay draft' );
check( 'draft' === $by['marketing-automation-automation-packages-3']->status, 'draft quote package stays draft' );
foreach ( $by as $sku => $p ) {
	if ( 'publish' === $p->status && 'fixed' === $p->meta['_sb_pricing_model'] && ! ( (float) $p->price > 0 ) ) { check( false, "published fixed package without price: $sku" ); }
	if ( 'publish' === $p->status && empty( $p->meta['_sb_deliverables'] ) ) { check( false, "published package without deliverables: $sku" ); }
}
check( true, 'no published fixed package lacks a price or deliverables' );
$cw = $GLOBALS['terms']['product_cat']['content-writing']; $fam = $GLOBALS['terms']['product_cat']['content'];
check( $cw->parent === $fam->term_id, 'pre-existing service category is moved under its family' );
check( str_contains( $by['off-page-seo-profiles-and-citations-1']->description, '<li>Manually created' ) && str_contains( $by['off-page-seo-profiles-and-citations-1']->description, '/services/off-page-seo/' ), 'product description lists deliverables and links back to the service page' );
check( false === SB_Packages::$bypass_gate, 'publish gate bypass reset after import' );
echo $fail ? "\n$fail FAILED\n" : "\nALL PASSED\n";
exit( $fail ? 1 : 0 );
