<?php
/**
 * Order flow: /order/?package=SKU
 *   Package (chosen) → Project brief (this form) → Secure checkout → Kick-off
 * The brief is stored as cart item data, shown in cart/checkout, and saved on the order line item.
 */
defined( 'ABSPATH' ) || exit;

function rrm_order_url( $product ) {
	if ( '' === $product->get_regular_price() ) {
		return add_query_arg( 'package', strtolower( $product->get_sku() ), home_url( '/contact-us/' ) ) . '#enquiry';
	}
	return add_query_arg( 'package', strtolower( $product->get_sku() ), home_url( '/order/' ) );
}

/** Brief fields per service: key => [label, type, required, options/placeholder]. */
function rrm_brief_fields( $service ) {
	$common_start = array(
		'business' => array( 'Business / brand name', 'text', true, 'e.g. Bright Smile Dental' ),
		'website'  => array( 'Website URL', 'url', 'website-development' !== $service, 'https://' ),
	);
	$by = array(
		'seo'                    => array(
			'keywords'  => array( 'Target keywords or services you want to rank for', 'textarea', true, 'e.g. emergency dentist London, teeth whitening' ),
			'locations' => array( 'Target locations', 'text', false, 'e.g. London, UK-wide, USA' ),
			'competitors' => array( 'Main competitors (optional)', 'text', false, 'competitor.com, another.com' ),
		),
		'link-building'          => array(
			'target_urls' => array( 'Page(s) you want links pointing to', 'textarea', true, 'https://yoursite.com/service-page' ),
			'anchors'     => array( 'Preferred keywords / anchor text', 'text', false, 'Leave blank and we’ll choose natural anchors' ),
			'niche'       => array( 'Your industry / niche', 'text', true, 'e.g. home improvement, SaaS, fashion' ),
		),
		'website-development'    => array(
			'platform' => array( 'Preferred platform', 'select', true, array( 'Not sure — please advise', 'WordPress', 'WooCommerce', 'Shopify', 'Custom code' ) ),
			'pages'    => array( 'Pages or features you need', 'textarea', true, 'e.g. Home, About, Services, Contact, booking form' ),
			'examples' => array( 'Websites you like (optional)', 'text', false, 'Links to sites with a style you like' ),
			'assets'   => array( 'Do you have a logo and content?', 'select', false, array( 'Logo and content ready', 'Logo only', 'Need help with both' ) ),
		),
		'content-writing'        => array(
			'topics'   => array( 'Pages or topics to write', 'textarea', true, 'e.g. Home page, About page, 3 blog posts about…' ),
			'keywords' => array( 'Target keywords (optional)', 'text', false, 'We can research these for you' ),
			'tone'     => array( 'Tone of voice', 'select', false, array( 'Friendly & conversational', 'Professional & authoritative', 'Bold & persuasive', 'Match my existing content' ) ),
		),
		'ppc'                    => array(
			'platforms' => array( 'Ad platforms', 'select', true, array( 'Google Ads', 'Meta (Facebook & Instagram)', 'Google + Meta', 'TikTok Ads', 'Not sure — please advise' ) ),
			'budget'    => array( 'Monthly ad budget (paid to the platform)', 'select', true, array( 'Under $1,000', '$1,000–$2,000', '$2,000–$5,000', '$5,000–$10,000', '$10,000+' ) ),
			'goal'      => array( 'Main goal and target locations', 'textarea', true, 'e.g. More calls for boiler repairs in Manchester' ),
		),
		'social-media-marketing' => array(
			'platforms' => array( 'Platforms to manage', 'text', true, 'e.g. Instagram, Facebook, LinkedIn' ),
			'handles'   => array( 'Your social handles / page links', 'textarea', false, '@yourbrand, facebook.com/yourbrand' ),
			'goal'      => array( 'Main goal', 'select', true, array( 'More enquiries & sales', 'Brand awareness', 'Grow followers & engagement', 'Launch a new product/service' ) ),
		),
	);
	$common_end = array(
		'notes' => array( 'Anything else we should know?', 'textarea', false, 'Deadlines, priorities, login details to follow, etc.' ),
	);
	return array_merge( $common_start, isset( $by[ $service ] ) ? $by[ $service ] : array(), $common_end );
}

function rrm_order_product() {
	$sku = isset( $_GET['package'] ) ? sanitize_text_field( wp_unslash( $_GET['package'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
	$id  = $sku ? wc_get_product_id_by_sku( $sku ) : 0;
	return $id ? wc_get_product( $id ) : null;
}

/* Never cache the order page (it holds a nonce and cart state). */
add_action(
	'template_redirect',
	function () {
		if ( is_page( 'order' ) ) {
			if ( ! defined( 'DONOTCACHEPAGE' ) ) {
				define( 'DONOTCACHEPAGE', true );
			}
			if ( function_exists( 'wc_nocache_headers' ) ) {
				wc_nocache_headers();
			}
			$p = function_exists( 'wc_get_product' ) ? rrm_order_product() : null;
			if ( $p && '' === $p->get_regular_price() ) {
				wp_safe_redirect( rrm_order_url( $p ) ); // quote-only packages go to the contact form
				exit;
			}
		}
	},
	5
);

/* Handle the brief submission: add package + brief to cart, go to checkout. */
add_action(
	'template_redirect',
	function () {
		if ( empty( $_POST['rrm_order'] ) || ! function_exists( 'WC' ) ) {
			return;
		}
		if ( ! isset( $_POST['_rrm_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['_rrm_nonce'] ) ), 'rrm_order' ) ) {
			wp_safe_redirect( add_query_arg( 'err', 'expired', wp_get_referer() ? wp_get_referer() : home_url( '/order/' ) ) );
			exit;
		}
		$product = wc_get_product( absint( $_POST['rrm_order'] ) );
		if ( ! $product || ! $product->is_purchasable() ) {
			wp_safe_redirect( home_url( '/shop/' ) );
			exit;
		}
		$service = $product->get_meta( '_rrm_service', true );
		$brief   = array();
		$missing = false;
		foreach ( rrm_brief_fields( $service ) as $key => $f ) {
			$raw = isset( $_POST[ 'b_' . $key ] ) ? wp_unslash( $_POST[ 'b_' . $key ] ) : ''; // phpcs:ignore
			$val = 'textarea' === $f[1] ? sanitize_textarea_field( $raw ) : ( 'url' === $f[1] ? esc_url_raw( $raw ) : sanitize_text_field( $raw ) );
			$val = mb_substr( $val, 0, 1500 );
			if ( $f[2] && '' === trim( $val ) ) {
				$missing = true;
			}
			if ( '' !== $val ) {
				$brief[ $f[0] ] = $val;
			}
		}
		$back = add_query_arg( 'package', strtolower( $product->get_sku() ), home_url( '/order/' ) );
		if ( $missing ) {
			WC()->session && WC()->session->set( 'rrm_brief_draft', $brief );
			wp_safe_redirect( add_query_arg( 'err', 'missing', $back ) . '#brief' );
			exit;
		}
		// One brief per package: replace an existing line for the same package.
		foreach ( WC()->cart->get_cart() as $k => $item ) {
			if ( (int) $item['product_id'] === $product->get_id() ) {
				WC()->cart->remove_cart_item( $k );
			}
		}
		$added = WC()->cart->add_to_cart( $product->get_id(), 1, 0, array(), array( 'rrm_brief' => $brief ) );
		if ( ! $added ) {
			wp_safe_redirect( add_query_arg( 'err', 'cart', $back ) );
			exit;
		}
		wc_clear_notices();
		WC()->session && WC()->session->set( 'rrm_brief_draft', null );
		wp_safe_redirect( wc_get_checkout_url() );
		exit;
	},
	20
);

/* Show the brief in cart / checkout (classic and block checkout via Store API). */
add_filter(
	'woocommerce_get_item_data',
	function ( $data, $item ) {
		if ( ! empty( $item['rrm_brief'] ) && is_array( $item['rrm_brief'] ) ) {
			foreach ( $item['rrm_brief'] as $label => $value ) {
				$data[] = array( 'key' => $label, 'value' => $value );
			}
		}
		return $data;
	},
	10,
	2
);

/* Save the brief on the order line item (visible in admin, emails and My Account). */
add_action(
	'woocommerce_checkout_create_order_line_item',
	function ( $line, $cart_key, $values ) {
		if ( ! empty( $values['rrm_brief'] ) && is_array( $values['rrm_brief'] ) ) {
			foreach ( $values['rrm_brief'] as $label => $value ) {
				$line->add_meta_data( $label, $value, true );
			}
		}
	},
	10,
	3
);

/* Direct ?add-to-cart without a brief (e.g. old links) → send to the brief form instead. */
add_filter(
	'woocommerce_add_to_cart_validation',
	function ( $ok, $product_id ) {
		if ( ! empty( $_POST['rrm_order'] ) || is_admin() || wp_doing_ajax() || defined( 'REST_REQUEST' ) ) { // phpcs:ignore
			return $ok;
		}
		$p = wc_get_product( $product_id );
		if ( $p && $p->get_meta( '_rrm_service', true ) ) {
			wp_safe_redirect( rrm_order_url( $p ) );
			exit;
		}
		return $ok;
	},
	10,
	2
);

/* [rrm_order_form] */
add_shortcode(
	'rrm_order_form',
	function () {
		if ( ! function_exists( 'wc_get_product' ) ) {
			return '';
		}
		$product = rrm_order_product();
		if ( ! $product ) {
			return '<section class="section"><div class="container narrow center"><h1>Choose a package to order</h1><p class="lead">Pick a package first, then tell us about your project.</p><a class="btn btn-primary" href="' . esc_url( home_url( '/shop/' ) ) . '">Browse packages ' . rrm_icon( 'i-arrow' ) . '</a></div></section>';
		}
		$service = $product->get_meta( '_rrm_service', true );
		$svc     = rrm_service( $service );
		$unit    = rrm_pkg_meta( $product, 'unit' );
		$err     = isset( $_GET['err'] ) ? sanitize_key( wp_unslash( $_GET['err'] ) ) : ''; // phpcs:ignore
		$draft   = ( function_exists( 'WC' ) && WC()->session ) ? (array) WC()->session->get( 'rrm_brief_draft', array() ) : array();
		ob_start();
		?>
		<section class="order-hero"><div class="aurora"></div><div class="container rel">
			<ol class="order-steps" aria-label="Order progress">
				<li class="done"><span><?php echo rrm_icon( 'i-check' ); // phpcs:ignore ?></span><span class="lbl">Package</span></li>
				<li class="now"><span>2</span>Project brief</li>
				<li><span>3</span><span class="lbl">Secure checkout</span></li>
				<li><span>4</span><span class="lbl">Kick-off</span></li>
			</ol>
			<h1>Tell us about your project</h1>
			<p class="lead">Takes about 2 minutes. Your brief is attached to your order so our team can start straight away.</p>
		</div></section>
		<section class="section order-wrap" id="brief"><div class="container order-grid">
			<form class="form order-form" method="post" action="">
				<?php wp_nonce_field( 'rrm_order', '_rrm_nonce' ); ?>
				<input type="hidden" name="rrm_order" value="<?php echo esc_attr( $product->get_id() ); ?>">
				<?php if ( $err ) : ?>
					<p class="notice" role="alert"><?php echo 'missing' === $err ? 'Please complete the required fields marked *.' : 'Something went wrong — please try again or call us on ' . esc_html( rrm_data( 'settings' )['phone_display'] ) . '.'; ?></p>
				<?php endif; ?>
				<h2 class="h3"><?php echo esc_html( $svc ? $svc['short_name'] : 'Project' ); ?> brief</h2>
				<div class="brief-fields">
				<?php
				foreach ( rrm_brief_fields( $service ) as $key => $f ) :
					$id   = 'b-' . $key;
					$val  = isset( $draft[ $f[0] ] ) ? $draft[ $f[0] ] : '';
					$req  = $f[2] ? ' required' : '';
					$wide = ( 'textarea' === $f[1] ) ? ' field-wide' : '';
					?>
					<div class="field<?php echo esc_attr( $wide ); ?>"><label for="<?php echo esc_attr( $id ); ?>"><?php echo esc_html( $f[0] ); ?><?php echo $f[2] ? ' <span aria-hidden="true">*</span>' : ''; ?></label>
					<?php if ( 'textarea' === $f[1] ) : ?>
						<textarea id="<?php echo esc_attr( $id ); ?>" name="b_<?php echo esc_attr( $key ); ?>" rows="3" placeholder="<?php echo esc_attr( $f[3] ); ?>"<?php echo $req; // phpcs:ignore ?>><?php echo esc_textarea( $val ); ?></textarea>
					<?php elseif ( 'select' === $f[1] ) : ?>
						<select id="<?php echo esc_attr( $id ); ?>" name="b_<?php echo esc_attr( $key ); ?>"<?php echo $req; // phpcs:ignore ?>>
							<?php foreach ( $f[3] as $opt ) : ?><option<?php selected( $val, $opt ); ?>><?php echo esc_html( $opt ); ?></option><?php endforeach; ?>
						</select>
					<?php else : ?>
						<input id="<?php echo esc_attr( $id ); ?>" type="<?php echo 'url' === $f[1] ? 'url' : 'text'; ?>" name="b_<?php echo esc_attr( $key ); ?>" value="<?php echo esc_attr( $val ); ?>" placeholder="<?php echo esc_attr( $f[3] ); ?>"<?php echo $req; // phpcs:ignore ?>>
					<?php endif; ?>
					</div>
				<?php endforeach; ?>
				</div>
				<button class="btn btn-primary btn-block btn-lg" type="submit">Continue to secure checkout <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></button>
				<p class="fine center"><?php echo rrm_icon( 'i-shield' ); // phpcs:ignore ?> Your details are only used to deliver your order. You can edit anything later with our team.</p>
			</form>

			<aside class="order-summary" aria-label="Order summary">
				<div class="os-card">
					<span class="eyebrow">Your package</span>
					<div class="os-head">
						<?php echo $product->get_image_id() ? wp_get_attachment_image( $product->get_image_id(), 'thumbnail', false, array( 'class' => 'os-thumb' ) ) : ''; // phpcs:ignore ?>
						<div><h2 class="h3"><?php echo esc_html( $product->get_name() ); ?></h2><p class="os-price"><b><?php echo esc_html( rrm_money( $product->get_regular_price() ) ); ?></b> <span><?php echo esc_html( $unit ); ?></span></p></div>
					</div>
					<ul class="buy-list"><?php foreach ( rrm_pkg_features( $product ) as $feat ) : ?><li><?php echo rrm_icon( 'i-check' ); // phpcs:ignore ?><?php echo esc_html( $feat ); ?></li><?php endforeach; ?></ul>
					<?php $others = rrm_packages( $service ); if ( count( $others ) > 1 ) : ?>
						<label class="os-switch"><span>Switch package</span>
							<select data-nav>
								<?php foreach ( $others as $o ) : if ( '' === $o->get_regular_price() ) { continue; } ?>
									<option value="<?php echo esc_url( rrm_order_url( $o ) ); ?>"<?php selected( $o->get_id(), $product->get_id() ); ?>><?php echo esc_html( rrm_pkg_meta( $o, 'short', $o->get_name() ) . ' — ' . rrm_money( $o->get_regular_price() ) . ( '/month' === rrm_pkg_meta( $o, 'unit' ) ? '/mo' : '' ) ); ?></option>
								<?php endforeach; ?>
							</select></label>
					<?php endif; ?>
					<ul class="assure">
						<li><?php echo rrm_icon( 'i-shield' ); // phpcs:ignore ?>Secure, encrypted checkout</li>
						<li><?php echo rrm_icon( 'i-clipboard' ); // phpcs:ignore ?>Covered by our <a href="<?php echo esc_url( home_url( '/refund-returns/' ) ); ?>">refund policy</a></li>
						<li><?php echo rrm_icon( 'i-phone' ); // phpcs:ignore ?>Questions? <a href="tel:<?php echo esc_attr( rrm_data( 'settings' )['phone_e164'] ); ?>"><?php echo esc_html( rrm_data( 'settings' )['phone_display'] ); ?></a></li>
					</ul>
				</div>
				<div class="os-next"><h2 class="h3">What happens next</h2><ol>
					<li><b>Pay securely</b> at checkout.</li>
					<li><b>We review your brief</b> and confirm any questions.</li>
					<li><b>Work starts</b> and you get progress updates.</li>
					<li><b>Delivery &amp; report</b> — <?php echo esc_html( strtolower( rrm_pkg_meta( $product, 'delivery', 'as agreed' ) ) ); ?>.</li>
				</ol></div>
			</aside>
		</div></section>
		<?php
		return ob_get_clean();
	}
);

/* Services need no postal address: slim checkout to name, email, (optional) phone/company, country. */
add_filter(
	'woocommerce_checkout_fields',
	function ( $fields ) {
		if ( ! function_exists( 'WC' ) || ! WC()->cart || WC()->cart->needs_shipping() ) {
			return $fields;
		}
		foreach ( array( 'billing_address_1', 'billing_address_2', 'billing_city', 'billing_state', 'billing_postcode' ) as $k ) {
			unset( $fields['billing'][ $k ] );
		}
		unset( $fields['order']['order_comments'] );
		if ( isset( $fields['billing']['billing_email'] ) ) {
			$fields['billing']['billing_email']['priority'] = 5;
		}
		return $fields;
	},
	99
);
add_filter( 'woocommerce_enable_order_notes_field', '__return_false' );
add_filter( 'woocommerce_order_button_text', function () { return 'Pay securely & start my project'; } );

add_filter( 'body_class', function ( $c ) { if ( is_page( 'order' ) ) { $c[] = 'rrm-order'; } return $c; } );
