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
		if ( function_exists( 'is_checkout' ) && is_checkout() && ! is_wc_endpoint_url( 'order-received' ) ) {
			$sd = rrm_data( 'settings' );
			?>
			<section class="order-hero checkout-hero"><div class="aurora"></div><div class="container rel">
				<ol class="order-steps" aria-label="Order progress">
					<li class="done"><span><?php echo rrm_icon( 'i-check' ); // phpcs:ignore ?></span><span class="lbl">Package</span></li>
					<li class="done"><span><?php echo rrm_icon( 'i-check' ); // phpcs:ignore ?></span><span class="lbl">Project brief</span></li>
					<li class="now"><span>3</span>Secure checkout</li>
					<li><span>4</span><span class="lbl">Kick-off</span></li>
				</ol>
				<h1>Secure checkout</h1>
				<p class="lead">Almost done — add your details and pay securely. Our team starts as soon as your order is confirmed.</p>
			</div></section>
			<section class="section checkout-wrap"><div class="container wc-wrap rrm-checkout">
				<?php the_content(); ?>
				<ul class="trust-strip" aria-label="Why it's safe to order">
					<li><?php echo rrm_icon( 'i-shield' ); // phpcs:ignore ?><span><b>Secure payment</b>Encrypted, PCI-compliant checkout</span></li>
					<li><?php echo rrm_icon( 'i-clipboard' ); // phpcs:ignore ?><span><b>Clear deliverables</b>Everything listed in your package</span></li>
					<li><?php echo rrm_icon( 'i-award' ); // phpcs:ignore ?><span><b>1K+ projects delivered</b>500+ happy clients</span></li>
					<li><?php echo rrm_icon( 'i-phone' ); // phpcs:ignore ?><span><b>Real people</b><a href="tel:<?php echo esc_attr( $sd['phone_e164'] ); ?>"><?php echo esc_html( $sd['phone_display'] ); ?></a></span></li>
				</ul>
			</div></section>
			<?php
			continue;
		}
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
