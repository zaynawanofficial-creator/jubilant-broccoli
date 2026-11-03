<?php
defined( 'ABSPATH' ) || exit;
$s = rrm_data( 'settings' );
?>
</main>
<footer class="site-footer">
	<div class="container">
		<div class="foot-grid">
			<div class="foot-brand">
				<img src="<?php echo esc_url( rrm_assets_url( 'img/logo-rankright-media.webp' ) ); ?>" alt="<?php echo esc_attr( $s['name'] ); ?>" width="232" height="73" loading="lazy">
				<p>RankRight Media is your trusted digital partner, offering SEO, web development, content writing &amp; more — all under one roof, for clients in the UK and worldwide.</p>
				<div class="foot-contact">
					<a href="tel:<?php echo esc_attr( $s['phone_e164'] ); ?>"><?php echo rrm_icon( 'i-phone' ); // phpcs:ignore ?><?php echo esc_html( $s['phone_display'] ); ?></a>
					<a href="mailto:<?php echo esc_attr( $s['email'] ); ?>"><?php echo rrm_icon( 'i-mail' ); // phpcs:ignore ?><?php echo esc_html( $s['email'] ); ?></a>
					<span><?php echo rrm_icon( 'i-pin' ); // phpcs:ignore ?><?php echo esc_html( $s['address']['street'] . ', ' . $s['address']['locality'] . ' ' . $s['address']['postcode'] ); ?></span>
				</div>
			</div>
			<div><h2>Services</h2><ul>
				<?php foreach ( (array) rrm_data( 'service_order' ) as $k ) : $sv = rrm_service( $k ); ?>
					<li><a href="<?php echo esc_url( home_url( '/' . $sv['slug'] . '/' ) ); ?>"><?php echo esc_html( $sv['name'] ); ?></a></li>
				<?php endforeach; ?>
			</ul></div>
			<div><h2>Support</h2><ul>
				<li><a href="<?php echo esc_url( home_url( '/faqs/' ) ); ?>">FAQs</a></li>
				<li><a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">Privacy Policy</a></li>
				<li><a href="<?php echo esc_url( home_url( '/refund-policy/' ) ); ?>">Refund Policy</a></li>
				<li><a href="<?php echo esc_url( home_url( '/terms-and-conditions/' ) ); ?>">Terms &amp; Conditions</a></li>
			</ul></div>
			<div><h2>Company</h2><ul>
				<li><a href="<?php echo esc_url( home_url( '/about-us/' ) ); ?>">About us</a></li>
				<li><a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>">Blog</a></li>
				<li><a href="<?php echo esc_url( function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/shop/' ) ); ?>">All packages</a></li>
				<li><a href="<?php echo esc_url( home_url( '/contact-us/' ) ); ?>">Contact us</a></li>
			</ul></div>
		</div>
		<div class="foot-bottom"><p>Copyright &copy; <?php echo esc_html( gmdate( 'Y' ) ); ?> <?php echo esc_html( $s['legal_name'] ); ?>. All rights reserved.</p><p>UK-based digital marketing agency serving clients worldwide</p></div>
	</div>
</footer>
<div class="mobile-cta"><a class="btn btn-ghost" href="tel:<?php echo esc_attr( $s['phone_e164'] ); ?>"><?php echo rrm_icon( 'i-phone' ); // phpcs:ignore ?>Call</a><a class="btn btn-primary" href="<?php echo esc_url( home_url( '/contact-us/' ) ); ?>">Get a quote</a></div>
<?php wp_footer(); ?>
</body>
</html>
