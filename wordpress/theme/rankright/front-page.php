<?php
/**
 * Pages. Pages imported with "_rrm_raw" render their designed sections directly (no wpautop);
 * normal pages (legal, WooCommerce cart/checkout/account, anything the client adds) use a clean layout.
 */
defined( 'ABSPATH' ) || exit;
get_header();
while ( have_posts() ) :
	the_post();
	if ( get_post_meta( get_the_ID(), '_rrm_raw', true ) ) {
		echo do_shortcode( rrm_placeholders( get_the_content() ) ); // phpcs:ignore -- trusted imported markup
	} else {
		$hero = json_decode( (string) get_post_meta( get_the_ID(), '_rrm_hero', true ), true );
		$crumbs = array( array( 'Home', home_url( '/' ) ), array( get_the_title(), get_permalink() ) );
		rrm_page_hero( get_the_title(), $hero['sub'] ?? '', $hero['eyebrow'] ?? '', $crumbs );
		$wc = function_exists( 'is_woocommerce' ) && ( is_cart() || is_checkout() || is_account_page() );
		?>
		<section class="section"><div class="container <?php echo $wc ? 'wc-wrap' : 'narrow prose legal'; ?>">
			<?php the_content(); ?>
		</div></section>
		<?php
	}
endwhile;
get_footer();
