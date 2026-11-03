<?php
/** "All Packages" shop page and package categories: every service's packages, grouped. */
defined( 'ABSPATH' ) || exit;
get_header();

$only = '';
if ( is_product_category() ) {
	$term = get_queried_object();
	foreach ( (array) rrm_data( 'service_order' ) as $k ) {
		if ( rrm_service( $k )['cat_slug'] === $term->slug ) {
			$only = $k;
		}
	}
}
rrm_page_hero(
	$only ? rrm_service( $only )['heading'] : 'Digital Marketing Packages & Prices',
	'Clear, fixed prices with every deliverable listed. Pick a package, check out securely, and we start straight away.',
	'All packages',
	array( array( 'Home', home_url( '/' ) ), array( 'Packages', wc_get_page_permalink( 'shop' ) ) )
);
?>
<nav class="container chip-row chip-row-center" aria-label="Jump to service">
	<?php foreach ( (array) rrm_data( 'service_order' ) as $k ) : $sv = rrm_service( $k ); ?>
		<a class="chip" href="<?php echo esc_url( $only ? home_url( '/' . $sv['slug'] . '/#pricing' ) : '#pk-' . $k ); ?>"><?php echo rrm_icon( $sv['icon'] ); // phpcs:ignore ?><?php echo esc_html( $sv['short_name'] ); ?></a>
	<?php endforeach; ?>
</nav>
<?php
foreach ( (array) rrm_data( 'service_order' ) as $k ) :
	if ( $only && $only !== $k ) {
		continue;
	}
	$sv = rrm_service( $k );
	$pk = rrm_packages( $k );
	if ( ! $pk ) {
		continue;
	}
	?>
	<section class="section" id="pk-<?php echo esc_attr( $k ); ?>" aria-labelledby="h-<?php echo esc_attr( $k ); ?>"><div class="container">
		<div class="section-head pk-head">
			<span class="ico"><?php echo rrm_icon( $sv['icon'] ); // phpcs:ignore ?></span>
			<div><h2 id="h-<?php echo esc_attr( $k ); ?>"><?php echo esc_html( $sv['heading'] ); ?></h2><p><?php echo esc_html( $sv['card'] ); ?></p></div>
			<a class="text-link" href="<?php echo esc_url( home_url( '/' . $sv['slug'] . '/' ) ); ?>">About this service <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a>
		</div>
		<div class="pricing"><?php foreach ( $pk as $i => $p ) { echo rrm_package_card( $p, 0, $i ); } // phpcs:ignore ?></div>
	</div></section>
	<?php
endforeach;
rrm_partial( 'cta' );
get_footer();
