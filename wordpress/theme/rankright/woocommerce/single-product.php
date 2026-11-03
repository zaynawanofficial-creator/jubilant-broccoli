<?php
/**
 * Service package details page (WooCommerce product).
 * Layout: hero + sticky buy box → what's included → package details → process → compare tiers →
 * reviews → FAQs → related services → CTA.
 */
defined( 'ABSPATH' ) || exit;
get_header();

while ( have_posts() ) :
	the_post();
	global $product;
	$product  = wc_get_product( get_the_ID() );
	$key      = rrm_pkg_meta( $product, 'service' );
	$svc      = rrm_service( $key );
	$price    = $product->get_regular_price();
	$unit     = rrm_pkg_meta( $product, 'unit' );
	$features = rrm_pkg_features( $product );
	$delivery = rrm_pkg_meta( $product, 'delivery' );
	$short    = rrm_pkg_meta( $product, 'short', $product->get_name() );
	$svc_url  = $svc ? home_url( '/' . $svc['slug'] . '/' ) : home_url( '/' );
	$quote    = ( '' === $price );
	$contact  = add_query_arg( 'package', strtolower( $product->get_sku() ), home_url( '/contact-us/' ) ) . '#enquiry';
	?>
	<section class="page-hero product-hero"><div class="aurora"></div><div class="gridlines"></div>
		<div class="container rel product-hero-grid">
			<div>
				<nav aria-label="Breadcrumb"><ol class="crumbs">
					<li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a></li>
					<?php if ( $svc ) : ?><li><a href="<?php echo esc_url( $svc_url ); ?>"><?php echo esc_html( $svc['short_name'] ); ?></a></li><?php endif; ?>
					<li><a href="<?php echo esc_url( $svc_url . '#pricing' ); ?>">Packages</a></li>
					<li aria-current="page"><?php echo esc_html( $short ); ?></li>
				</ol></nav>
				<span class="eyebrow"><?php echo esc_html( $svc ? $svc['short_name'] . ' package' : 'Package' ); ?></span>
				<h1><?php the_title(); ?></h1>
				<p class="lead"><?php echo esc_html( wp_strip_all_tags( $product->get_short_description() ) ); ?></p>
				<ul class="trust-row">
					<li><?php echo rrm_icon( 'i-clock' ); // phpcs:ignore ?><?php echo esc_html( $delivery ? $delivery : 'Fast turnaround' ); ?></li>
					<li><?php echo rrm_icon( 'i-shield' ); // phpcs:ignore ?>White-hat &amp; transparent</li>
					<li><?php echo rrm_icon( 'i-clipboard' ); // phpcs:ignore ?>Clear reporting</li>
				</ul>
				<figure class="product-figure"><?php echo $product->get_image_id() ? wp_get_attachment_image( $product->get_image_id(), 'large', false, array( 'loading' => 'eager', 'fetchpriority' => 'high' ) ) : ''; // phpcs:ignore ?></figure>
			</div>

			<aside class="buy-box" aria-labelledby="buy-h">
				<?php if ( rrm_pkg_meta( $product, 'featured', 0 ) ) : ?><span class="ribbon">Recommended</span><?php endif; ?>
				<h2 id="buy-h" class="h3"><?php echo esc_html( $short ); ?></h2>
				<p class="tagline"><?php echo esc_html( rrm_pkg_meta( $product, 'tagline' ) ); ?></p>
				<p class="amount"><?php if ( $quote ) : ?><b>Custom</b><span>tailored quote</span><?php else : ?><b><?php echo esc_html( rrm_money( $price ) ); ?></b><span><?php echo esc_html( $unit ); ?></span><?php endif; ?></p>
				<ul class="buy-list">
					<?php foreach ( $features as $f ) : ?><li><?php echo rrm_icon( 'i-check' ); // phpcs:ignore ?><?php echo esc_html( $f ); ?></li><?php endforeach; ?>
				</ul>
				<?php if ( $quote || ! $product->is_purchasable() ) : ?>
					<a class="btn btn-primary btn-block" href="<?php echo esc_url( $contact ); ?>">Request a quote <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a>
				<?php else : ?>
					<a class="btn btn-primary btn-block btn-lg" href="<?php echo esc_url( rrm_order_url( $product ) ); ?>">Order now — 2-minute brief <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a>
					<a class="btn btn-ghost btn-block" href="<?php echo esc_url( $contact ); ?>">Ask a question first</a>
				<?php endif; ?>
				<?php if ( '/month' === $unit ) : ?><p class="fine">Monthly plan — price shown is per month.</p><?php endif; ?>
				<ul class="assure">
					<li><?php echo rrm_icon( 'i-shield' ); // phpcs:ignore ?>Secure checkout</li>
					<li><?php echo rrm_icon( 'i-message' ); // phpcs:ignore ?>Short project brief, then checkout</li>
					<li><?php echo rrm_icon( 'i-phone' ); // phpcs:ignore ?>UK support team</li>
				</ul>
			</aside>
		</div>
	</section>

	<section class="section"><div class="container split split-60">
		<div class="prose reveal">
			<?php echo apply_filters( 'the_content', $product->get_description() ); // phpcs:ignore ?>
		</div>
		<aside class="sidebar">
			<div class="facts">
				<h2><?php echo rrm_icon( 'i-clipboard' ); // phpcs:ignore ?>At a glance</h2>
				<dl>
					<dt>Package</dt><dd><?php echo esc_html( $short ); ?></dd>
					<dt>Service</dt><dd><?php echo esc_html( $svc ? $svc['name'] : '' ); ?></dd>
					<dt>Price</dt><dd><?php echo esc_html( $quote ? 'Custom quote' : rrm_money( $price ) . ' ' . $unit ); ?></dd>
					<?php if ( $delivery ) : ?><dt>Delivery</dt><dd><?php echo esc_html( $delivery ); ?></dd><?php endif; ?>
					<dt>Best for</dt><dd><?php echo esc_html( rrm_pkg_meta( $product, 'audience' ) ); ?></dd>
				</dl>
			</div>
			<?php if ( $svc ) : ?>
				<div class="side-card"><h2>Explore <?php echo esc_html( $svc['short_name'] ); ?></h2><p><?php echo esc_html( $svc['card'] ); ?></p><a class="text-link" href="<?php echo esc_url( $svc_url ); ?>">Full service overview <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a></div>
			<?php endif; ?>
		</aside>
	</div></section>

	<?php if ( $svc ) : ?>
		<section class="section spot" aria-labelledby="proc-h"><div class="container rel">
			<div class="section-head center"><span class="eyebrow">How it works</span><h2 id="proc-h">From checkout to results in 4 steps</h2></div>
			<ol class="steps" role="list">
				<?php foreach ( $svc['process'] as $i => $st ) : ?>
					<li class="step reveal d<?php echo (int) $i; ?>"><span class="ico"><?php echo rrm_icon( $st[0] ); // phpcs:ignore ?></span><h3><?php echo esc_html( $st[1] ); ?></h3><p><?php echo esc_html( $st[2] ); ?></p></li>
				<?php endforeach; ?>
			</ol>
		</div></section>

		<section class="section" id="compare" aria-labelledby="cmp-h"><div class="container">
			<div class="section-head center"><span class="eyebrow">Compare</span><h2 id="cmp-h">All <?php echo esc_html( $svc['short_name'] ); ?> packages</h2><p class="lead">Need more (or less)? Every package lists exactly what's included.</p></div>
			<div class="pricing">
				<?php foreach ( rrm_packages( $key ) as $i => $p ) { echo rrm_package_card( $p, $product->get_id(), $i ); } // phpcs:ignore ?>
			</div>
		</div></section>

		<?php echo rrm_placeholders( isset( $svc['testimonials_html'] ) ? $svc['testimonials_html'] : '' ); // phpcs:ignore ?>

		<section class="section" aria-labelledby="pfaq-h"><div class="container narrow">
			<div class="section-head center"><span class="eyebrow">FAQ</span><h2 id="pfaq-h">Questions about <?php echo esc_html( $svc['short_name'] ); ?></h2></div>
			<div class="faq">
				<?php foreach ( $svc['faqs'] as $i => $f ) : ?>
					<details<?php echo 0 === $i ? ' open' : ''; ?>><summary><?php echo esc_html( $f[0] ); ?><span class="pm"><?php echo rrm_icon( 'i-chevron' ); // phpcs:ignore ?></span></summary><div class="a"><?php echo wp_kses_post( rrm_placeholders( $f[1] ) ); ?></div></details>
				<?php endforeach; ?>
			</div>
		</div></section>
	<?php endif; ?>
	<?php
	rrm_partial( 'cta' );
endwhile;
get_footer();
