<?php
/** Dynamic blocks used inside imported page content. */
defined( 'ABSPATH' ) || exit;

/** Compact package card: price, top features, Order now (→ brief form) + View details (→ package page). */
function rrm_package_card( $product, $current_id = 0, $i = 0, $show_service = false ) {
	$featured = (int) rrm_pkg_meta( $product, 'featured', 0 );
	$price    = $product->get_regular_price();
	$unit     = rrm_pkg_meta( $product, 'unit', '' );
	$is_cur   = ( $current_id && $current_id === $product->get_id() );
	$features = rrm_pkg_features( $product );
	$show     = array_slice( $features, 0, 4 );
	$more     = count( $features ) - count( $show );
	$detail   = get_permalink( $product->get_id() );
	$quote    = ( '' === $price );
	$svc      = $show_service ? rrm_service( rrm_pkg_meta( $product, 'service' ) ) : null;
	$classes  = 'pk reveal d' . ( $i % 3 ) . ( $featured ? ' pk-hot' : '' ) . ( $is_cur ? ' pk-current' : '' );
	ob_start();
	?>
	<article class="<?php echo esc_attr( $classes ); ?>">
		<?php if ( $is_cur ) : ?><span class="pk-badge pk-badge-cur">You're viewing</span><?php elseif ( $featured ) : ?><span class="pk-badge">Recommended</span><?php endif; ?>
		<?php if ( $svc ) : ?><span class="pk-svc"><?php echo rrm_icon( $svc['icon'] ); // phpcs:ignore ?><?php echo esc_html( $svc['short_name'] ); ?></span><?php endif; ?>
		<h3 class="pk-name"><a href="<?php echo esc_url( $detail ); ?>"><?php echo esc_html( rrm_pkg_meta( $product, 'short', $product->get_name() ) ); ?></a></h3>
		<p class="pk-tag"><?php echo esc_html( rrm_pkg_meta( $product, 'tagline' ) ); ?></p>
		<p class="pk-price"><?php if ( $quote ) : ?><b>Custom</b><span>tailored quote</span><?php else : ?><b><?php echo esc_html( rrm_money( $price ) ); ?></b><span><?php echo esc_html( '/month' === $unit ? '/month' : 'one-off' ); ?></span><?php endif; ?></p>
		<ul class="pk-list">
			<?php foreach ( $show as $f ) : ?><li><?php echo rrm_icon( 'i-check' ); // phpcs:ignore ?><span><?php echo esc_html( $f ); ?></span></li><?php endforeach; ?>
		</ul>
		<?php if ( $more > 0 ) : ?><a class="pk-more" href="<?php echo esc_url( $detail ); ?>">+ <?php echo (int) $more; ?> more included</a><?php endif; ?>
		<div class="pk-cta">
			<a class="btn <?php echo ( $featured || $is_cur ) ? 'btn-primary' : 'btn-soft'; ?> btn-block" href="<?php echo esc_url( rrm_order_url( $product ) ); ?>"><?php echo $quote ? 'Get a quote' : 'Order now'; ?> <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a>
			<a class="pk-link" href="<?php echo esc_url( $detail ); ?>">View details</a>
		</div>
	</article>
	<?php
	return ob_get_clean();
}

/** Featured ("Most popular") package from each service — used on the home page. */
add_shortcode(
	'rrm_featured_packages',
	function () {
		if ( ! function_exists( 'wc_get_products' ) ) {
			return '';
		}
		$cards = '';
		$i     = 0;
		foreach ( array( 'seo', 'website-development', 'link-building' ) as $key ) {
			foreach ( rrm_packages( $key ) as $p ) {
				if ( rrm_pkg_meta( $p, 'featured', 0 ) ) {
					$cards .= rrm_package_card( $p, 0, $i++, true );
					break;
				}
			}
		}
		return '<div class="pricing">' . $cards . '</div><p class="swipe-hint">Swipe to compare →</p>';
	}
);

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
		$out  = '<div class="pricing">' . $cards . '</div><p class="swipe-hint">Swipe to compare all ' . count( $packages ) . ' packages →</p>';
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
