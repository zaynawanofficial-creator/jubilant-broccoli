<?php
/**
 * Order flow: Package → Project details → Checkout → Kick-off.
 *
 * [sb_order_form] renders the project-details form on the service details (product) page.
 * The answers travel with the cart item, are saved on the order line, pre-fill the project brief,
 * and mark the brief complete when every required field was answered, so the customer is not asked twice.
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

/**
 * Pre-checkout project details.
 */
class SB_Order_Flow {

	const NONCE = 'sb_order';

	public static function init(): void {
		add_shortcode( 'sb_order_form', array( __CLASS__, 'render' ) );
		add_filter( 'woocommerce_add_to_cart_validation', array( __CLASS__, 'validate' ), 10, 3 );
		add_filter( 'woocommerce_add_cart_item_data', array( __CLASS__, 'cart_item_data' ), 10, 2 );
		add_filter( 'woocommerce_get_item_data', array( __CLASS__, 'item_data' ), 10, 2 );
		add_action( 'woocommerce_checkout_create_order_line_item', array( __CLASS__, 'save_line' ), 20, 3 );
		add_action( 'woocommerce_checkout_order_processed', array( __CLASS__, 'prefill_brief' ), 20, 1 );
		add_action( 'woocommerce_store_api_checkout_order_processed', array( __CLASS__, 'prefill_brief' ), 20, 1 );
		add_filter( 'woocommerce_add_to_cart_redirect', array( __CLASS__, 'redirect' ), 20 );
		add_filter( 'wc_add_to_cart_message_html', array( __CLASS__, 'quiet_message' ), 20 );
	}

	private static function posted_for( int $product_id ): bool {
		// phpcs:ignore WordPress.Security.NonceVerification.Missing -- nonce checked in validate().
		return isset( $_POST['sb_order_product'] ) && absint( $_POST['sb_order_product'] ) === $product_id;
	}

	/** Fields for a product: its brief profile minus the free-text "anything else" (kept as optional). */
	public static function fields( WC_Product $product ): array {
		$id      = $product->get_parent_id() ? $product->get_parent_id() : $product->get_id();
		$profile = (string) get_post_meta( $id, '_sb_brief_profile', true );
		$all     = SB_Brief::profiles();
		return $all[ $profile ] ?? $all['generic'];
	}

	public static function render(): string {
		$product = wc_get_product( get_the_ID() );
		if ( ! $product || ! SB_Packages::is_package( $product ) ) {
			return '';
		}
		if ( ! defined( 'DONOTCACHEPAGE' ) ) {
			define( 'DONOTCACHEPAGE', true );
		}
		do_action( 'litespeed_control_set_nocache', 'sb order form' );

		$turn = (string) $product->get_meta( '_sb_turnaround' );
		ob_start();
		echo '<div class="sb-order" id="order">';
		echo '<div class="sb-order__price"><span class="sb-order__label">' . esc_html__( 'Package price', 'seo-booster-core' ) . '</span>';
		if ( 'quote' === $product->get_meta( '_sb_pricing_model' ) || ! $product->is_purchasable() ) {
			echo '<strong>' . esc_html__( 'Custom quote', 'seo-booster-core' ) . '</strong></div>';
			echo '<p>' . esc_html__( 'This package is priced to your requirements. Tell us what you need and we will reply with a fixed price.', 'seo-booster-core' ) . '</p>';
			echo '<a class="sb-btn sb-btn--primary sb-order__submit" href="' . esc_url( SB_Packages::quote_url( $product ) ) . '">' . esc_html__( 'Get a quote', 'seo-booster-core' ) . '</a></div>';
			return (string) ob_get_clean();
		}
		echo '<strong>' . wp_kses_post( $product->get_price_html() ) . '</strong>';
		if ( $turn ) {
			echo '<span class="sb-order__turn">' . esc_html( sprintf( /* translators: %s: turnaround */ __( 'Delivery: %s', 'seo-booster-core' ), $turn ) ) . '</span>';
		}
		echo '</div>';

		echo '<ol class="sb-order__steps" aria-label="' . esc_attr__( 'Order steps', 'seo-booster-core' ) . '"><li class="is-done">' . esc_html__( 'Package', 'seo-booster-core' ) . '</li><li class="is-current" aria-current="step">' . esc_html__( 'Project details', 'seo-booster-core' ) . '</li><li>' . esc_html__( 'Checkout', 'seo-booster-core' ) . '</li><li>' . esc_html__( 'Kick-off', 'seo-booster-core' ) . '</li></ol>';

		// phpcs:disable WordPress.Security.NonceVerification.Missing -- refill after a failed validation only.
		$posted = self::posted_for( $product->get_id() ) && isset( $_POST['sb_order'] ) && is_array( $_POST['sb_order'] ) ? wp_unslash( $_POST['sb_order'] ) : array();
		// phpcs:enable
		echo '<form class="sb-order__form cart" method="post" action="' . esc_url( $product->get_permalink() ) . '#order" enctype="multipart/form-data" novalidate>';
		wp_nonce_field( self::NONCE, 'sb_order_nonce' );
		echo '<input type="hidden" name="add-to-cart" value="' . esc_attr( (string) $product->get_id() ) . '">';
		echo '<input type="hidden" name="quantity" value="1">';
		echo '<input type="hidden" name="sb_order_product" value="' . esc_attr( (string) $product->get_id() ) . '">';
		$required = array();
		$optional = array();
		foreach ( self::fields( $product ) as $key => $def ) {
			$html = SB_Brief::field_html( 'sb_order[' . $key . ']', 'sb-order-' . $key, $def, sanitize_textarea_field( (string) ( $posted[ $key ] ?? '' ) ) );
			if ( $def[2] ) {
				$required[] = $html;
			} else {
				$optional[] = $html;
			}
		}
		echo '<div class="sb-order__fields">' . implode( '', $required ) . '</div>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in field_html().
		if ( $optional ) {
			echo '<details class="sb-order__more"><summary>' . esc_html__( 'More details (optional, you can add these later)', 'seo-booster-core' ) . '</summary><div class="sb-order__fields">' . implode( '', $optional ) . '</div></details>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in field_html().
		}
		echo '<button type="submit" class="sb-btn sb-btn--primary sb-order__submit single_add_to_cart_button">' . esc_html__( 'Continue to checkout', 'seo-booster-core' ) . ' →</button>';
		echo '<ul class="sb-order__trust"><li>' . esc_html__( 'Secure checkout', 'seo-booster-core' ) . '</li><li>' . esc_html__( 'Upload brand files after payment', 'seo-booster-core' ) . '</li><li>' . esc_html__( 'Never share passwords, we use user invites', 'seo-booster-core' ) . '</li></ul>';
		echo '</form></div>';
		return (string) ob_get_clean();
	}

	/**
	 * @param bool $ok         Current validity.
	 * @param int  $product_id Product.
	 * @param int  $qty        Quantity.
	 */
	public static function validate( $ok, $product_id, $qty ) {
		if ( ! self::posted_for( (int) $product_id ) ) {
			return $ok;
		}
		if ( ! isset( $_POST['sb_order_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['sb_order_nonce'] ) ), self::NONCE ) ) {
			wc_add_notice( __( 'Your session expired. Please submit your project details again.', 'seo-booster-core' ), 'error' );
			return false;
		}
		$product = wc_get_product( $product_id );
		$input   = isset( $_POST['sb_order'] ) && is_array( $_POST['sb_order'] ) ? wp_unslash( $_POST['sb_order'] ) : array(); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput.InputNotSanitized -- sanitized per field.
		$missing = array();
		foreach ( self::fields( $product ) as $key => $def ) {
			$val = SB_Brief::sanitize( (string) ( $input[ $key ] ?? '' ), $def );
			if ( $def[2] && '' === $val ) {
				$missing[] = $def[0];
			} elseif ( '' !== trim( (string) ( $input[ $key ] ?? '' ) ) && '' === $val && in_array( $def[1], array( 'url', 'email' ), true ) ) {
				/* translators: %s: field label */
				wc_add_notice( sprintf( __( 'Please check the format of: %s', 'seo-booster-core' ), $def[0] ), 'error' );
				return false;
			}
		}
		if ( $missing ) {
			/* translators: %s: list of field labels */
			wc_add_notice( sprintf( __( 'Please complete: %s', 'seo-booster-core' ), implode( ', ', $missing ) ), 'error' );
			return false;
		}
		return $ok;
	}

	public static function cart_item_data( array $data, int $product_id ): array {
		if ( ! self::posted_for( $product_id ) ) {
			return $data;
		}
		$product = wc_get_product( $product_id );
		$input   = isset( $_POST['sb_order'] ) && is_array( $_POST['sb_order'] ) ? wp_unslash( $_POST['sb_order'] ) : array(); // phpcs:ignore WordPress.Security.NonceVerification.Missing,WordPress.Security.ValidatedSanitizedInput.InputNotSanitized -- nonce checked in validate(); sanitized per field.
		$details = array();
		foreach ( self::fields( $product ) as $key => $def ) {
			$val = SB_Brief::sanitize( (string) ( $input[ $key ] ?? '' ), $def );
			if ( '' !== $val ) {
				$details[ $key ] = $val;
			}
		}
		$data['sb_details'] = $details;
		return $data;
	}

	/** Short summary in cart and checkout (key fields only). */
	public static function item_data( array $item_data, array $cart_item ): array {
		if ( empty( $cart_item['sb_details'] ) || empty( $cart_item['data'] ) ) {
			return $item_data;
		}
		$fields = self::fields( $cart_item['data'] );
		$shown  = 0;
		foreach ( $cart_item['sb_details'] as $key => $val ) {
			if ( ! isset( $fields[ $key ] ) || ! $fields[ $key ][2] || $shown >= 3 ) {
				continue;
			}
			$item_data[] = array(
				'key'   => wp_strip_all_tags( $fields[ $key ][0] ),
				'value' => esc_html( wp_html_excerpt( str_replace( "\n", ', ', SB_Brief::display_value( $fields[ $key ], $val ) ), 60, '…' ) ),
			);
			++$shown;
		}
		$item_data[] = array(
			'key'   => __( 'Project details', 'seo-booster-core' ),
			'value' => __( 'Received ✓', 'seo-booster-core' ),
		);
		return $item_data;
	}

	public static function save_line( WC_Order_Item_Product $item, $cart_item_key, array $values ): void {
		if ( ! empty( $values['sb_details'] ) ) {
			$item->add_meta_data( '_sb_details', $values['sb_details'], true );
		}
	}

	/**
	 * Copy the project details into the order brief. Brief = complete when all required fields are answered.
	 *
	 * @param int|WC_Order $order Order or ID.
	 */
	public static function prefill_brief( $order ): void {
		$order = $order instanceof WC_Order ? $order : wc_get_order( $order );
		if ( ! $order || $order->get_meta( '_sb_brief_data' ) ) {
			return;
		}
		$lines = SB_Brief::lines( $order );
		if ( ! $lines ) {
			return;
		}
		$profiles = SB_Brief::profiles();
		$data     = array();
		$missing  = 0;
		foreach ( $lines as $item_id => $line ) {
			$item    = $order->get_item( $item_id );
			$details = $item ? (array) $item->get_meta( '_sb_details' ) : array();
			foreach ( $profiles[ $line['profile'] ] as $key => $def ) {
				$data[ $item_id ][ $key ] = (string) ( $details[ $key ] ?? '' );
				if ( $def[2] && '' === $data[ $item_id ][ $key ] ) {
					++$missing;
				}
			}
		}
		$order->update_meta_data( '_sb_brief_data', $data );
		$order->update_meta_data( '_sb_brief_status', $missing ? 'partial' : 'complete' );
		$order->update_meta_data( '_sb_brief_submitted_at', gmdate( 'c' ) );
		$order->add_order_note( $missing ? __( 'Project details captured at checkout; some brief fields still to complete.', 'seo-booster-core' ) : __( 'Project details captured at checkout; brief complete.', 'seo-booster-core' ) );
		$order->save();
	}

	public static function redirect( $url ) {
		// phpcs:ignore WordPress.Security.NonceVerification.Missing -- read-only routing.
		return isset( $_POST['sb_order_product'] ) ? wc_get_checkout_url() : $url;
	}

	public static function quiet_message( $message ) {
		// phpcs:ignore WordPress.Security.NonceVerification.Missing -- read-only.
		return isset( $_POST['sb_order_product'] ) ? '' : $message;
	}
}
