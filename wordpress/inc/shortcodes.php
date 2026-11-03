<?php
/** Dynamic blocks used inside imported page content. */
defined( 'ABSPATH' ) || exit;

/** One package card (used by pricing tables, the shop page and "other packages" on product pages). */
function rrm_package_card( $product, $current_id = 0, $i = 0 ) {
	$featured = (int) rrm_pkg_meta( $product, 'featured', 0 );
	$price    = $product->get_regular_price();
	$unit     = rrm_pkg_meta( $product, 'unit', '' );
	$is_cur   = ( $current_id && $current_id === $product->get_id() );
	$classes  = 'price reveal d' . ( $i % 3 ) . ( $featured ? ' featured' : '' ) . ( $is_cur ? ' current' : '' );
	$ribbon   = $is_cur ? '<span class="ribbon">You\'re viewing</span>' : ( $featured ? '<span class="ribbon">Recommended</span>' : '' );
	$img      = $product->get_image_id() ? wp_get_attachment_image( $product->get_image_id(), 'rrm-card', false, array( 'class' => 'price-img', 'loading' => 'lazy' ) ) : '';
	$amount   = '' === $price
		? '<b>' . esc_html__( 'Custom', 'rankright' ) . '</b><span>quote</span>'
		: '<b>' . esc_html( rrm_money( $price ) ) . '</b><span>' . esc_html( $unit ) . '</span>';
	$lis      = '';
	foreach ( rrm_pkg_features( $product ) as $f ) {
		$lis .= '<li>' . rrm_icon( 'i-check' ) . esc_html( $f ) . '</li>';
	}
	$url = get_permalink( $product->get_id() );
	ob_start();
	?>
	<article class="<?php echo esc_attr( $classes ); ?>">
		<?php echo $ribbon; // phpcs:ignore ?>
		<a class="price-media" href="<?php echo esc_url( $url ); ?>" tabindex="-1" aria-hidden="true"><?php echo $img; // phpcs:ignore ?></a>
		<h3><a href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( rrm_pkg_meta( $product, 'short', $product->get_name() ) ); ?></a></h3>
		<p class="tagline"><?php echo esc_html( rrm_pkg_meta( $product, 'tagline' ) ); ?></p>
		<p class="amount"><?php echo $amount; // phpcs:ignore ?></p>
		<ul><?php echo $lis; // phpcs:ignore ?></ul>
		<a class="btn <?php echo $featured ? 'btn-primary' : 'btn-ghost'; ?> btn-block" href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( '' === $price ? __( 'View & request a quote', 'rankright' ) : __( 'View package', 'rankright' ) ); ?> <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a>
	</article>
	<?php
	return ob_get_clean();
}

add_shortcode(
	'rrm_pricing',
	function ( $atts ) {
		$a        = shortcode_atts( array( 'service' => '' ), $atts );
		$svc      = rrm_service( $a['service'] );
		$packages = rrm_packages( $a['service'] );
		if ( ! $svc || ! $packages ) {
			return '<p class="price-note">' . esc_html__( 'Packages are being updated — contact us for a quote.', 'rankright' ) . '</p>';
		}
		$cards = '';
		$rows  = '';
		foreach ( $packages as $i => $p ) {
			$cards .= rrm_package_card( $p, 0, $i );
			$price  = $p->get_regular_price();
			$rows  .= '<tr><th scope="row"><a href="' . esc_url( get_permalink( $p->get_id() ) ) . '">' . esc_html( rrm_pkg_meta( $p, 'short', $p->get_name() ) ) . '</a></th><td>' . esc_html( rrm_money( $price ) . ( '' === $price ? '' : ' ' . rrm_pkg_meta( $p, 'unit' ) ) ) . '</td><td>' . esc_html( implode( '; ', rrm_pkg_features( $p ) ) ) . '</td></tr>';
		}
		$out  = '<div class="pricing">' . $cards . '</div>';
		$out .= '<p class="price-note">' . esc_html( $svc['note'] ) . ' ' . esc_html__( 'Prices in USD. Secure checkout.', 'rankright' ) . '</p>';
		$out .= '<details class="compare"><summary>' . esc_html( sprintf( __( 'Compare all %s packages side by side', 'rankright' ), $svc['short_name'] ) ) . rrm_icon( 'i-chevron' ) . '</summary><div class="table-wrap"><table><caption class="sr-only">' . esc_html( $svc['heading'] ) . '</caption><thead><tr><th scope="col">Package</th><th scope="col">Price</th><th scope="col">What\'s included</th></tr></thead><tbody>' . $rows . '</tbody></table></div></details>';
		return $out;
	}
);

/** Package select options for the contact form. */
function rrm_package_options( $selected = '' ) {
	$out = '<option value="">' . esc_html__( 'Not sure yet — please advise', 'rankright' ) . '</option>';
	foreach ( (array) rrm_data( 'service_order' ) as $key ) {
		$svc = rrm_service( $key );
		$out .= '<optgroup label="' . esc_attr( $svc['name'] ) . '"><option value="' . esc_attr( $key ) . '"' . selected( $selected, $key, false ) . '>' . esc_html( $svc['name'] ) . ' — general enquiry</option>';
		foreach ( rrm_packages( $key ) as $p ) {
			$sku  = $p->get_sku();
			$out .= '<option value="' . esc_attr( $sku ) . '"' . selected( $selected, $sku, false ) . '>' . esc_html( rrm_pkg_meta( $p, 'short', $p->get_name() ) . ' — ' . rrm_money( $p->get_regular_price() ) ) . '</option>';
		}
		$out .= '</optgroup>';
	}
	return $out;
}

add_shortcode(
	'rrm_contact_form',
	function () {
		$sel  = isset( $_GET['package'] ) ? sanitize_key( wp_unslash( $_GET['package'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
		$sent = isset( $_GET['sent'] ) ? sanitize_key( wp_unslash( $_GET['sent'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
		ob_start();
		?>
		<form class="form reveal" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" method="post" accept-charset="UTF-8">
			<input type="hidden" name="action" value="rrm_contact">
			<h2 class="h3"><?php esc_html_e( 'Send us a message', 'rankright' ); ?></h2>
			<p><?php esc_html_e( 'Please feel free to send us any questions, feedback or suggestions you might have.', 'rankright' ); ?></p>
			<?php if ( '0' === $sent ) : ?>
				<p class="notice" role="alert"><?php esc_html_e( 'Sorry — your message didn\'t send. Please check the required fields and try again.', 'rankright' ); ?></p>
			<?php endif; ?>
			<div class="form-row">
				<div class="field"><label for="f-name">Name <span aria-hidden="true">*</span></label><input id="f-name" name="name" type="text" autocomplete="name" required maxlength="100"></div>
				<div class="field"><label for="f-company">Company</label><input id="f-company" name="company_name" type="text" autocomplete="organization" maxlength="120"></div>
			</div>
			<div class="form-row">
				<div class="field"><label for="f-email">Email <span aria-hidden="true">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
				<div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="40"></div>
			</div>
			<div class="field"><label for="f-website">Website</label><input id="f-website" name="website" type="url" inputmode="url" placeholder="https://" maxlength="200"></div>
			<div class="field"><label for="f-package">Service or package</label><select id="f-package" name="package"><?php echo rrm_package_options( $sel ); // phpcs:ignore ?></select></div>
			<div class="field"><label for="f-message">How can we help? <span aria-hidden="true">*</span></label><textarea id="f-message" name="message" required maxlength="5000" placeholder="Your goals, timeline and anything else we should know"></textarea></div>
			<div class="hp" aria-hidden="true"><label for="f-hp">Leave this field empty</label><input id="f-hp" name="company" type="text" tabindex="-1" autocomplete="off"></div>
			<input id="f-ts" name="ts" type="hidden" value="0">
			<label class="consent"><input type="checkbox" name="consent" value="yes" required><span>I agree to RankRight Media contacting me about this enquiry, as described in the <a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">Privacy Policy</a>.</span></label>
			<button class="btn btn-primary" type="submit"><?php esc_html_e( 'Send message', 'rankright' ); ?> <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></button>
			<small><?php esc_html_e( 'We reply within one working day. Your details are never shared or sold.', 'rankright' ); ?></small>
		</form>
		<?php
		return ob_get_clean();
	}
);
