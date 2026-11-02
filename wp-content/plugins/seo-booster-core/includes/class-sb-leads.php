<?php
/**
 * Contact and quote forms: [sb_lead_form type="contact|quote"].
 * Leads are stored privately (wp-admin → Leads) and emailed to the site admin.
 * Spam protection: nonce, honeypot, minimum fill time, per-IP rate limit. No third-party services.
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

/**
 * Lead capture.
 */
class SB_Leads {

	const CPT       = 'sb_lead';
	const MIN_SECS  = 3;
	const RATE_MAX  = 5;

	public static function services(): array {
		return array(
			'off-page-seo'        => __( 'Off-Page SEO & Link Building', 'seo-booster-core' ),
			'seo-audit'           => __( 'SEO Audit', 'seo-booster-core' ),
			'technical-seo'       => __( 'Technical SEO', 'seo-booster-core' ),
			'website-development' => __( 'Website Development', 'seo-booster-core' ),
			'website-maintenance' => __( 'Website Maintenance & Fixes', 'seo-booster-core' ),
			'content-writing'     => __( 'Content Writing', 'seo-booster-core' ),
			'graphic-design'      => __( 'Graphic Design & Branding', 'seo-booster-core' ),
			'ppc'                 => __( 'PPC / Paid Ads', 'seo-booster-core' ),
			'analytics'           => __( 'Analytics & Tracking', 'seo-booster-core' ),
			'email'               => __( 'Email Marketing', 'seo-booster-core' ),
			'automation'          => __( 'Marketing Automation', 'seo-booster-core' ),
			'other'               => __( 'Something else / not sure', 'seo-booster-core' ),
		);
	}

	public static function budgets(): array {
		return array(
			''          => __( 'Select a range (optional)', 'seo-booster-core' ),
			'under-100' => __( 'Under $100', 'seo-booster-core' ),
			'100-500'   => '$100 – $500',
			'500-1500'  => '$500 – $1,500',
			'1500-plus' => __( '$1,500+', 'seo-booster-core' ),
		);
	}

	public static function init(): void {
		add_action( 'init', array( __CLASS__, 'register' ) );
		add_shortcode( 'sb_lead_form', array( __CLASS__, 'render' ) );
		add_action( 'template_redirect', array( __CLASS__, 'handle' ) );
		add_filter( 'manage_' . self::CPT . '_posts_columns', array( __CLASS__, 'columns' ) );
		add_action( 'manage_' . self::CPT . '_posts_custom_column', array( __CLASS__, 'column' ), 10, 2 );
		add_action( 'add_meta_boxes_' . self::CPT, array( __CLASS__, 'meta_box' ) );
	}

	public static function register(): void {
		register_post_type(
			self::CPT,
			array(
				'labels'          => array(
					'name'          => __( 'Leads', 'seo-booster-core' ),
					'singular_name' => __( 'Lead', 'seo-booster-core' ),
					'edit_item'     => __( 'Lead', 'seo-booster-core' ),
				),
				'public'          => false,
				'show_ui'         => true,
				'show_in_menu'    => true,
				'menu_icon'       => 'dashicons-email-alt',
				'menu_position'   => 56,
				'supports'        => array( 'title' ),
				'capability_type' => 'page',
				'map_meta_cap'    => true,
				'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
				'show_in_rest'    => false,
			)
		);
	}

	private static function ip_hash(): string {
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
		return substr( hash_hmac( 'sha256', $ip, wp_salt( 'nonce' ) ), 0, 20 );
	}

	public static function render( $atts ): string {
		$atts = shortcode_atts( array( 'type' => 'contact' ), $atts, 'sb_lead_form' );
		$type = 'quote' === $atts['type'] ? 'quote' : 'contact';
		// Never serve a cached copy of a page with a form (stale nonces).
		if ( ! defined( 'DONOTCACHEPAGE' ) ) {
			define( 'DONOTCACHEPAGE', true );
		}
		do_action( 'litespeed_control_set_nocache', 'sb lead form' );
		if ( ! headers_sent() ) {
			nocache_headers();
		}

		// phpcs:disable WordPress.Security.NonceVerification.Recommended -- display only.
		$state  = isset( $_GET['sb_lead'] ) ? sanitize_key( wp_unslash( $_GET['sb_lead'] ) ) : '';
		$token  = isset( $_GET['sb_t'] ) ? sanitize_key( wp_unslash( $_GET['sb_t'] ) ) : '';
		$pre    = array(
			'service' => isset( $_GET['service'] ) ? sanitize_key( wp_unslash( $_GET['service'] ) ) : '',
			'package' => isset( $_GET['package'] ) ? sanitize_text_field( wp_unslash( $_GET['package'] ) ) : '',
		);
		// phpcs:enable
		$errors = array();
		$values = array();
		if ( 'error' === $state && $token ) {
			$saved  = get_transient( 'sb_lead_err_' . $token );
			$errors = $saved['errors'] ?? array();
			$values = $saved['values'] ?? array();
		}
		$v = static fn( $k ) => esc_attr( $values[ $k ] ?? '' );

		ob_start();
		echo '<div id="sb-form" class="sb-form-wrap">';
		if ( 'sent' === $state ) {
			echo '<div class="sb-form__msg sb-form__msg--ok" role="status">' . esc_html( 'quote' === $type ? __( 'Thank you. Your request has been received and we will reply by email with a scope and price.', 'seo-booster-core' ) : __( 'Thank you. Your message has been sent and we will reply by email.', 'seo-booster-core' ) ) . '</div>';
		}
		if ( $errors ) {
			echo '<div class="sb-form__msg sb-form__msg--err" role="alert"><ul>';
			foreach ( $errors as $e ) {
				echo '<li>' . esc_html( $e ) . '</li>';
			}
			echo '</ul></div>';
		}
		$req = ' <span class="sb-form__req" aria-hidden="true">*</span>';
		echo '<form class="sb-form" method="post" action="' . esc_url( get_permalink() ) . '#sb-form" novalidate>';
		wp_nonce_field( 'sb_lead_' . $type, 'sb_lead_nonce' );
		echo '<input type="hidden" name="sb_lead_type" value="' . esc_attr( $type ) . '">';
		echo '<input type="hidden" name="sb_lead_ts" value="' . esc_attr( (string) time() ) . '">';
		echo '<input type="hidden" name="sb_lead_page" value="' . esc_attr( (string) get_the_ID() ) . '">';
		echo '<div class="sb-form__hp" aria-hidden="true"><label for="sb-hp-' . esc_attr( $type ) . '">Leave empty</label><input type="text" id="sb-hp-' . esc_attr( $type ) . '" name="sb_hp" tabindex="-1" autocomplete="off"></div>';
		echo '<div class="sb-form__row">';
		echo '<p><label for="sb-name">' . esc_html__( 'Your name', 'seo-booster-core' ) . $req . '</label><input type="text" id="sb-name" name="sb_name" required autocomplete="name" value="' . $v( 'name' ) . '"></p>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup.
		echo '<p><label for="sb-email">' . esc_html__( 'Email', 'seo-booster-core' ) . $req . '</label><input type="email" id="sb-email" name="sb_email" required autocomplete="email" value="' . $v( 'email' ) . '"></p>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup.
		echo '</div><div class="sb-form__row">';
		echo '<p><label for="sb-website">' . esc_html__( 'Website (optional)', 'seo-booster-core' ) . '</label><input type="url" id="sb-website" name="sb_website" placeholder="https://" autocomplete="url" value="' . $v( 'website' ) . '"></p>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in $v.
		$sel = $values['service'] ?? $pre['service'];
		echo '<p><label for="sb-service">' . esc_html__( 'Service', 'seo-booster-core' ) . ( 'quote' === $type ? $req : '' ) . '</label><select id="sb-service" name="sb_service"' . ( 'quote' === $type ? ' required' : '' ) . '><option value="">' . esc_html__( 'Choose a service', 'seo-booster-core' ) . '</option>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup.
		foreach ( self::services() as $k => $label ) {
			echo '<option value="' . esc_attr( $k ) . '"' . selected( $sel, $k, false ) . '>' . esc_html( $label ) . '</option>';
		}
		echo '</select></p></div>';
		if ( 'quote' === $type ) {
			$pkg = $values['package'] ?? $pre['package'];
			echo '<div class="sb-form__row">';
			echo '<p><label for="sb-budget">' . esc_html__( 'Budget', 'seo-booster-core' ) . '</label><select id="sb-budget" name="sb_budget">';
			foreach ( self::budgets() as $k => $label ) {
				echo '<option value="' . esc_attr( $k ) . '"' . selected( $values['budget'] ?? '', $k, false ) . '>' . esc_html( $label ) . '</option>';
			}
			echo '</select></p>';
			echo '<p><label for="sb-package">' . esc_html__( 'Package of interest (optional)', 'seo-booster-core' ) . '</label><input type="text" id="sb-package" name="sb_package" value="' . esc_attr( $pkg ) . '"></p></div>';
		}
		echo '<p><label for="sb-message">' . esc_html( 'quote' === $type ? __( 'What do you need?', 'seo-booster-core' ) : __( 'Message', 'seo-booster-core' ) ) . $req . '</label><textarea id="sb-message" name="sb_message" required rows="6" placeholder="' . esc_attr( 'quote' === $type ? __( 'Goals, pages, quantities, deadlines. Please do not include passwords.', 'seo-booster-core' ) : __( 'How can we help? Please do not include passwords.', 'seo-booster-core' ) ) . '">' . esc_textarea( $values['message'] ?? '' ) . '</textarea></p>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup.
		$privacy = get_privacy_policy_url();
		echo '<p><label class="sb-form__consent"><input type="checkbox" name="sb_consent" value="1" required> <span>' . wp_kses_post( sprintf( /* translators: %s: privacy policy link */ __( 'I agree that SEO Booster may store this information to reply to my request, as described in the %s.', 'seo-booster-core' ), $privacy ? '<a href="' . esc_url( $privacy ) . '">' . esc_html__( 'privacy policy', 'seo-booster-core' ) . '</a>' : esc_html__( 'privacy policy', 'seo-booster-core' ) ) ) . '</span></label></p>';
		echo '<button type="submit" name="sb_lead_submit" value="1">' . esc_html( 'quote' === $type ? __( 'Request my quote', 'seo-booster-core' ) : __( 'Send message', 'seo-booster-core' ) ) . '</button>';
		echo '</form></div>';
		return (string) ob_get_clean();
	}

	public static function handle(): void {
		if ( empty( $_POST['sb_lead_submit'] ) || empty( $_POST['sb_lead_type'] ) ) {
			return;
		}
		$type = 'quote' === sanitize_key( wp_unslash( $_POST['sb_lead_type'] ) ) ? 'quote' : 'contact';
		$page = isset( $_POST['sb_lead_page'] ) ? absint( $_POST['sb_lead_page'] ) : 0;
		$back = $page ? get_permalink( $page ) : home_url( '/' );
		if ( ! isset( $_POST['sb_lead_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['sb_lead_nonce'] ) ), 'sb_lead_' . $type ) ) {
			self::fail( $back, array( __( 'Your session expired. Please submit the form again.', 'seo-booster-core' ) ), array() );
		}
		$values = array(
			'name'    => sanitize_text_field( wp_unslash( $_POST['sb_name'] ?? '' ) ),
			'email'   => sanitize_email( wp_unslash( $_POST['sb_email'] ?? '' ) ),
			'website' => esc_url_raw( wp_unslash( $_POST['sb_website'] ?? '' ), array( 'http', 'https' ) ),
			'service' => sanitize_key( wp_unslash( $_POST['sb_service'] ?? '' ) ),
			'budget'  => sanitize_key( wp_unslash( $_POST['sb_budget'] ?? '' ) ),
			'package' => sanitize_text_field( wp_unslash( $_POST['sb_package'] ?? '' ) ),
			'message' => mb_substr( sanitize_textarea_field( wp_unslash( $_POST['sb_message'] ?? '' ) ), 0, 5000 ),
		);
		// Silent drop for bots: honeypot filled or form submitted too fast.
		$ts = isset( $_POST['sb_lead_ts'] ) ? absint( $_POST['sb_lead_ts'] ) : 0;
		if ( ! empty( $_POST['sb_hp'] ) || ( time() - $ts ) < self::MIN_SECS ) {
			wp_safe_redirect( add_query_arg( 'sb_lead', 'sent', $back ) . '#sb-form' );
			exit;
		}
		$errors = array();
		if ( '' === $values['name'] ) {
			$errors[] = __( 'Please enter your name.', 'seo-booster-core' );
		}
		if ( ! is_email( $values['email'] ) ) {
			$errors[] = __( 'Please enter a valid email address.', 'seo-booster-core' );
		}
		if ( 'quote' === $type && ! array_key_exists( $values['service'], self::services() ) ) {
			$errors[] = __( 'Please choose a service.', 'seo-booster-core' );
		}
		if ( mb_strlen( $values['message'] ) < 10 ) {
			$errors[] = __( 'Please add a few words about what you need.', 'seo-booster-core' );
		}
		if ( empty( $_POST['sb_consent'] ) ) {
			$errors[] = __( 'Please tick the consent box so we can reply.', 'seo-booster-core' );
		}
		$rate_key = 'sb_lead_rate_' . self::ip_hash();
		$count    = (int) get_transient( $rate_key );
		if ( $count >= self::RATE_MAX ) {
			$errors[] = __( 'Too many messages from your connection. Please email us instead.', 'seo-booster-core' );
		}
		if ( $errors ) {
			self::fail( $back, $errors, $values );
		}
		set_transient( $rate_key, $count + 1, HOUR_IN_SECONDS );

		$services = self::services();
		$label    = $services[ $values['service'] ] ?? '';
		$id       = wp_insert_post(
			array(
				'post_type'   => self::CPT,
				'post_status' => 'private',
				'post_title'  => sprintf( '%s – %s%s', 'quote' === $type ? 'Quote' : 'Contact', $values['name'], $label ? ' – ' . $label : '' ),
			)
		);
		if ( $id && ! is_wp_error( $id ) ) {
			foreach ( $values as $k => $val ) {
				update_post_meta( $id, '_sb_' . $k, $val );
			}
			update_post_meta( $id, '_sb_type', $type );
			update_post_meta( $id, '_sb_consent_at', gmdate( 'c' ) );
			update_post_meta( $id, '_sb_source', $back );
		}

		$to      = apply_filters( 'sb_lead_email', get_option( 'admin_email' ) );
		$subject = sprintf( '[%s] %s: %s', get_bloginfo( 'name' ), 'quote' === $type ? 'New quote request' : 'New message', $values['name'] );
		$body    = '';
		foreach ( array( 'name', 'email', 'website', 'service', 'budget', 'package', 'message' ) as $k ) {
			if ( '' !== $values[ $k ] ) {
				$body .= ucfirst( $k ) . ': ' . ( 'service' === $k ? $label : $values[ $k ] ) . "\n";
			}
		}
		$body .= "\nLead in wp-admin: " . admin_url( 'post.php?post=' . (int) $id . '&action=edit' ) . "\n";
		wp_mail( $to, $subject, $body, array( 'Reply-To: ' . $values['name'] . ' <' . $values['email'] . '>' ) );

		wp_safe_redirect( add_query_arg( 'sb_lead', 'sent', $back ) . '#sb-form' );
		exit;
	}

	private static function fail( string $back, array $errors, array $values ): void {
		$token = strtolower( wp_generate_password( 12, false ) );
		set_transient( 'sb_lead_err_' . $token, array( 'errors' => $errors, 'values' => $values ), 10 * MINUTE_IN_SECONDS );
		wp_safe_redirect( add_query_arg( array( 'sb_lead' => 'error', 'sb_t' => $token ), $back ) . '#sb-form' );
		exit;
	}

	public static function columns( array $cols ): array {
		return array(
			'cb'         => $cols['cb'] ?? '',
			'title'      => __( 'Lead', 'seo-booster-core' ),
			'sb_email'   => __( 'Email', 'seo-booster-core' ),
			'sb_type'    => __( 'Type', 'seo-booster-core' ),
			'sb_service' => __( 'Service', 'seo-booster-core' ),
			'date'       => __( 'Received', 'seo-booster-core' ),
		);
	}

	public static function column( string $col, int $id ): void {
		$val = get_post_meta( $id, '_' . $col, true );
		if ( 'sb_email' === $col ) {
			echo '<a href="mailto:' . esc_attr( $val ) . '">' . esc_html( $val ) . '</a>';
		} elseif ( 'sb_service' === $col ) {
			echo esc_html( self::services()[ $val ] ?? $val );
		} else {
			echo esc_html( (string) $val );
		}
	}

	public static function meta_box(): void {
		add_meta_box(
			'sb_lead_details',
			__( 'Lead details', 'seo-booster-core' ),
			static function ( WP_Post $post ) {
				echo '<table class="widefat striped"><tbody>';
				foreach ( array( 'type', 'name', 'email', 'website', 'service', 'budget', 'package', 'message', 'consent_at', 'source' ) as $k ) {
					$val = (string) get_post_meta( $post->ID, '_sb_' . $k, true );
					if ( 'service' === $k ) {
						$val = self::services()[ $val ] ?? $val;
					}
					echo '<tr><th style="width:160px">' . esc_html( ucfirst( str_replace( '_', ' ', $k ) ) ) . '</th><td>' . nl2br( esc_html( $val ) ) . '</td></tr>';
				}
				echo '</tbody></table>';
				$email = (string) get_post_meta( $post->ID, '_sb_email', true );
				if ( $email ) {
					echo '<p><a class="button button-primary" href="mailto:' . esc_attr( $email ) . '">' . esc_html__( 'Reply by email', 'seo-booster-core' ) . '</a></p>';
				}
			},
			self::CPT,
			'normal',
			'high'
		);
	}
}
