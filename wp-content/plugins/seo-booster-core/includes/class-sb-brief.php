<?php
/**
 * Post-purchase project brief: My Account endpoint, conditional fields per package type,
 * protected uploads, admin view, reminders.
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

/**
 * Project brief attached to service orders.
 */
class SB_Brief {

	const ENDPOINT   = 'sb-brief';
	const UPLOAD_DIR = 'sb-briefs';
	const MAX_BYTES  = 20971520; // 20 MB.
	const MAX_FILES  = 10;

	/** Allowed upload extensions => MIME types. SVG deliberately excluded (script risk). */
	const MIMES = array(
		'pdf'  => 'application/pdf',
		'png'  => 'image/png',
		'jpg'  => 'image/jpeg',
		'jpeg' => 'image/jpeg',
		'webp' => 'image/webp',
		'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
		'xlsx' => 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
		'csv'  => 'text/csv',
		'txt'  => 'text/plain',
		'zip'  => 'application/zip',
	);

	/**
	 * Fields per brief profile. key => [label, type, required, help].
	 * Types: url, urls (one per line), text, textarea, email.
	 * Never add password fields: access is granted through delegated invites only.
	 */
	public static function profiles(): array {
		$common = array(
			'goals' => array( __( 'Anything else we should know?', 'seo-booster-core' ), 'textarea', false, '' ),
		);
		return array(
			'offpage' => array(
				'target_urls'   => array( __( 'Target URL(s) to build links to (one per line)', 'seo-booster-core' ), 'urls', true, __( 'Usually your homepage plus up to 3 key pages.', 'seo-booster-core' ) ),
				'keywords'      => array( __( 'Main keywords / anchor themes (one per line)', 'seo-booster-core' ), 'textarea', true, __( 'We use natural, branded and partial-match anchors. No keyword stuffing.', 'seo-booster-core' ) ),
				'business_name' => array( __( 'Business name (exactly as it should appear)', 'seo-booster-core' ), 'text', true, '' ),
				'business_addr' => array( __( 'Business address (for citations; leave blank if online-only)', 'seo-booster-core' ), 'textarea', false, '' ),
				'business_tel'  => array( __( 'Business phone (for citations)', 'seo-booster-core' ), 'text', false, '' ),
				'contact_email' => array( __( 'Email to register listings with', 'seo-booster-core' ), 'email', true, __( 'Use an address you control; listing verification emails go here.', 'seo-booster-core' ) ),
				'niche_geo'     => array( __( 'Industry and target country/city', 'seo-booster-core' ), 'text', true, '' ),
				'description'   => array( __( 'Short business description (50–150 words)', 'seo-booster-core' ), 'textarea', true, '' ),
				'avoid'         => array( __( 'Existing profiles or sites to avoid (one per line)', 'seo-booster-core' ), 'textarea', false, '' ),
			) + $common,
			'web'     => array(
				'site_url'   => array( __( 'Current website (if any)', 'seo-booster-core' ), 'url', false, '' ),
				'pages'      => array( __( 'Pages you need (one per line)', 'seo-booster-core' ), 'textarea', true, '' ),
				'features'   => array( __( 'Features (forms, booking, shop, languages…)', 'seo-booster-core' ), 'textarea', false, '' ),
				'references' => array( __( 'Websites you like (one per line)', 'seo-booster-core' ), 'urls', false, '' ),
				'content'    => array( __( 'Is your text/content ready?', 'seo-booster-core' ), 'text', true, '' ),
				'platform'   => array( __( 'Hosting / platform details', 'seo-booster-core' ), 'textarea', false, __( 'Do not send passwords. We will ask you to invite us as a user when needed.', 'seo-booster-core' ) ),
			) + $common,
			'content' => array(
				'topics'   => array( __( 'Topic(s) or working titles (one per line)', 'seo-booster-core' ), 'textarea', true, '' ),
				'audience' => array( __( 'Target audience', 'seo-booster-core' ), 'text', true, '' ),
				'keywords' => array( __( 'Target keywords (one per line)', 'seo-booster-core' ), 'textarea', false, '' ),
				'tone'     => array( __( 'Tone of voice and examples', 'seo-booster-core' ), 'textarea', false, '' ),
				'site_url' => array( __( 'Website the content is for', 'seo-booster-core' ), 'url', true, '' ),
			) + $common,
			'design'  => array(
				'formats'    => array( __( 'Formats and sizes needed', 'seo-booster-core' ), 'textarea', true, '' ),
				'copy'       => array( __( 'Text to include', 'seo-booster-core' ), 'textarea', false, '' ),
				'references' => array( __( 'Reference designs (links, one per line)', 'seo-booster-core' ), 'urls', false, '' ),
				'deadline'   => array( __( 'Any fixed deadline?', 'seo-booster-core' ), 'text', false, '' ),
			) + $common,
			'seo'     => array(
				'site_url'    => array( __( 'Website URL', 'seo-booster-core' ), 'url', true, '' ),
				'priority'    => array( __( 'Priority pages (one per line)', 'seo-booster-core' ), 'urls', false, '' ),
				'competitors' => array( __( 'Main competitors (one per line)', 'seo-booster-core' ), 'urls', false, '' ),
				'access'      => array( __( 'Search Console / Analytics access', 'seo-booster-core' ), 'text', false, __( 'Invite our team email as a user. Never send passwords.', 'seo-booster-core' ) ),
			) + $common,
			'generic' => array(
				'site_url' => array( __( 'Website URL', 'seo-booster-core' ), 'url', false, '' ),
				'details'  => array( __( 'What do you need?', 'seo-booster-core' ), 'textarea', true, '' ),
			) + $common,
		);
	}

	public static function init(): void {
		add_action( 'init', array( __CLASS__, 'add_endpoint' ) );
		add_filter( 'woocommerce_get_query_vars', array( __CLASS__, 'query_vars' ) );
		add_action( 'woocommerce_account_' . self::ENDPOINT . '_endpoint', array( __CLASS__, 'render_endpoint' ) );
		add_action( 'template_redirect', array( __CLASS__, 'handle_post' ) );
		add_action( 'template_redirect', array( __CLASS__, 'maybe_serve_file' ) );
		add_action( 'woocommerce_order_details_before_order_table', array( __CLASS__, 'order_banner' ) );
		add_action( 'woocommerce_thankyou', array( __CLASS__, 'thankyou_banner' ), 5 );
		add_action( 'add_meta_boxes', array( __CLASS__, 'admin_meta_box' ) );
		add_action( 'woocommerce_order_status_sb-awaiting-brief', array( __CLASS__, 'schedule_reminders' ) );
		add_action( 'sb_brief_reminder', array( __CLASS__, 'send_reminder' ) );
		add_filter( 'manage_woocommerce_page_wc-orders_columns', array( __CLASS__, 'admin_column' ) );
		add_action( 'manage_woocommerce_page_wc-orders_custom_column', array( __CLASS__, 'admin_column_value' ), 10, 2 );
	}

	public static function add_endpoint(): void {
		add_rewrite_endpoint( self::ENDPOINT, EP_ROOT | EP_PAGES );
	}

	public static function query_vars( array $vars ): array {
		$vars[ self::ENDPOINT ] = self::ENDPOINT;
		return $vars;
	}

	/** Profiles required by an order (one form section per package line). */
	public static function lines( WC_Order $order ): array {
		$out = array();
		foreach ( $order->get_items() as $item_id => $item ) {
			if ( ! $item instanceof WC_Order_Item_Product ) {
				continue;
			}
			$profile = $item->get_meta( 'sb_brief_profile' );
			if ( ! $profile && SB_Packages::is_package( $item->get_product_id() ) ) {
				$profile = get_post_meta( $item->get_product_id(), '_sb_brief_profile', true );
			}
			if ( $profile ) {
				$out[ $item_id ] = array(
					'name'    => $item->get_name(),
					'profile' => isset( self::profiles()[ $profile ] ) ? $profile : 'generic',
				);
			}
		}
		return $out;
	}

	public static function url( WC_Order $order ): string {
		return wc_get_endpoint_url( self::ENDPOINT, (string) $order->get_id(), wc_get_page_permalink( 'myaccount' ) );
	}

	/** Current user may view/edit the brief of this order. */
	private static function can_access( WC_Order $order ): bool {
		$uid = get_current_user_id();
		return ( $uid && (int) $order->get_customer_id() === $uid ) || current_user_can( 'edit_shop_orders' );
	}

	public static function status( WC_Order $order ): string {
		return $order->get_meta( '_sb_brief_status' ) ? $order->get_meta( '_sb_brief_status' ) : 'pending';
	}

	public static function render_endpoint( $order_id ): void {
		$order = wc_get_order( absint( $order_id ) );
		if ( ! $order || ! self::can_access( $order ) || ! self::lines( $order ) ) {
			wc_print_notice( __( 'Order not found.', 'seo-booster-core' ), 'error' );
			return;
		}
		$data  = (array) $order->get_meta( '_sb_brief_data' );
		$files = (array) $order->get_meta( '_sb_brief_files' );
		/* translators: %s: order number */
		echo '<h2>' . esc_html( sprintf( __( 'Project brief for order #%s', 'seo-booster-core' ), $order->get_order_number() ) ) . '</h2>';
		echo '<p>' . esc_html__( 'This tells our team exactly what to deliver. Please never include passwords — we will ask you to invite us as a user if access is needed.', 'seo-booster-core' ) . '</p>';
		echo '<form method="post" enctype="multipart/form-data" class="sb-brief-form woocommerce-EditAccountForm">';
		wp_nonce_field( 'sb_brief_' . $order->get_id(), 'sb_brief_nonce' );
		echo '<input type="hidden" name="sb_brief_order" value="' . esc_attr( (string) $order->get_id() ) . '">';
		foreach ( self::lines( $order ) as $item_id => $line ) {
			echo '<fieldset class="sb-brief-line"><legend>' . esc_html( $line['name'] ) . '</legend>';
			foreach ( self::profiles()[ $line['profile'] ] as $key => $def ) {
				$name  = 'sb_brief[' . (int) $item_id . '][' . $key . ']';
				$id    = 'sb-brief-' . (int) $item_id . '-' . $key;
				$value = $data[ $item_id ][ $key ] ?? '';
				$req   = $def[2] ? ' required aria-required="true"' : '';
				echo '<p class="form-row form-row-wide"><label for="' . esc_attr( $id ) . '">' . esc_html( $def[0] ) . ( $def[2] ? ' <abbr class="required" title="required">*</abbr>' : '' ) . '</label>';
				if ( in_array( $def[1], array( 'textarea', 'urls' ), true ) ) {
					echo '<textarea class="input-text" rows="4" id="' . esc_attr( $id ) . '" name="' . esc_attr( $name ) . '"' . $req . '>' . esc_textarea( $value ) . '</textarea>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static attribute string.
				} else {
					$type = in_array( $def[1], array( 'url', 'email' ), true ) ? $def[1] : 'text';
					echo '<input class="input-text" type="' . esc_attr( $type ) . '" id="' . esc_attr( $id ) . '" name="' . esc_attr( $name ) . '" value="' . esc_attr( $value ) . '"' . $req . '>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static attribute string.
				}
				if ( $def[3] ) {
					echo '<span class="description">' . esc_html( $def[3] ) . '</span>';
				}
				echo '</p>';
			}
			echo '</fieldset>';
		}
		echo '<fieldset><legend>' . esc_html__( 'Files (logos, brand guides, briefs)', 'seo-booster-core' ) . '</legend>';
		if ( $files ) {
			echo '<ul>';
			foreach ( $files as $f ) {
				echo '<li><a href="' . esc_url( self::file_url( $order, $f['name'] ) ) . '">' . esc_html( $f['original'] ) . '</a></li>';
			}
			echo '</ul>';
		}
		/* translators: 1: max files, 2: max MB, 3: extensions */
		echo '<p><label for="sb-brief-files">' . esc_html( sprintf( __( 'Add files (up to %1$d files, %2$d MB each: %3$s)', 'seo-booster-core' ), self::MAX_FILES, self::MAX_BYTES / 1048576, implode( ', ', array_keys( self::MIMES ) ) ) ) . '</label> <input type="file" id="sb-brief-files" name="sb_brief_files[]" multiple accept=".' . esc_attr( implode( ',.', array_keys( self::MIMES ) ) ) . '"></p></fieldset>';
		echo '<p><button type="submit" class="button sb-btn sb-btn--primary">' . esc_html__( 'Save brief', 'seo-booster-core' ) . '</button></p></form>';
	}

	public static function handle_post(): void {
		if ( empty( $_POST['sb_brief_order'] ) || empty( $_POST['sb_brief_nonce'] ) ) {
			return;
		}
		$order = wc_get_order( absint( $_POST['sb_brief_order'] ) );
		if ( ! $order || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['sb_brief_nonce'] ) ), 'sb_brief_' . $order->get_id() ) || ! self::can_access( $order ) ) {
			wc_add_notice( __( 'Sorry, that brief could not be saved. Please reload and try again.', 'seo-booster-core' ), 'error' );
			return;
		}
		$lines    = self::lines( $order );
		$profiles = self::profiles();
		$input    = isset( $_POST['sb_brief'] ) && is_array( $_POST['sb_brief'] ) ? wp_unslash( $_POST['sb_brief'] ) : array(); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput.InputNotSanitized -- sanitized per field below.
		$data     = array();
		$missing  = 0;
		foreach ( $lines as $item_id => $line ) {
			foreach ( $profiles[ $line['profile'] ] as $key => $def ) {
				$raw = isset( $input[ $item_id ][ $key ] ) ? (string) $input[ $item_id ][ $key ] : '';
				$val = self::sanitize( $raw, $def[1] );
				if ( $def[2] && '' === $val ) {
					++$missing;
				}
				$data[ $item_id ][ $key ] = $val;
			}
		}
		$order->update_meta_data( '_sb_brief_data', $data );
		self::handle_uploads( $order );
		$status = $missing ? 'partial' : 'complete';
		$order->update_meta_data( '_sb_brief_status', $status );
		$order->update_meta_data( '_sb_brief_submitted_at', gmdate( 'c' ) );
		$order->save();

		if ( 'complete' === $status && $order->has_status( 'sb-awaiting-brief' ) ) {
			$order->update_status( 'sb-brief-received', __( 'Customer completed the project brief.', 'seo-booster-core' ) );
			self::notify_admin( $order );
		}
		wc_add_notice(
			$missing
				/* translators: %d: number of missing required fields */
				? sprintf( _n( 'Brief saved. %d required field is still empty.', 'Brief saved. %d required fields are still empty.', $missing, 'seo-booster-core' ), $missing )
				: __( 'Thank you — your brief is complete and our team has been notified.', 'seo-booster-core' ),
			$missing ? 'notice' : 'success'
		);
		wp_safe_redirect( self::url( $order ) );
		exit;
	}

	private static function sanitize( string $raw, string $type ): string {
		switch ( $type ) {
			case 'url':
				return esc_url_raw( trim( $raw ), array( 'http', 'https' ) );
			case 'urls':
				$urls = array_filter( array_map( static fn( $u ) => esc_url_raw( trim( $u ), array( 'http', 'https' ) ), preg_split( '/\r\n|\r|\n/', $raw ) ) );
				return implode( "\n", array_slice( $urls, 0, 50 ) );
			case 'email':
				return sanitize_email( $raw );
			case 'textarea':
				return mb_substr( sanitize_textarea_field( $raw ), 0, 5000 );
			default:
				return mb_substr( sanitize_text_field( $raw ), 0, 500 );
		}
	}

	/** Absolute path of the protected upload folder. */
	public static function base_dir(): string {
		$up = wp_upload_dir( null, false );
		return trailingslashit( $up['basedir'] ) . self::UPLOAD_DIR;
	}

	public static function protect_upload_dir(): void {
		$dir = self::base_dir();
		wp_mkdir_p( $dir );
		if ( ! file_exists( $dir . '/.htaccess' ) ) {
			file_put_contents( $dir . '/.htaccess', "Require all denied\nDeny from all\n" ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_file_put_contents
		}
		if ( ! file_exists( $dir . '/index.php' ) ) {
			file_put_contents( $dir . '/index.php', "<?php\n// Silence.\n" ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_file_put_contents
		}
	}

	private static function handle_uploads( WC_Order $order ): void {
		// phpcs:disable WordPress.Security.NonceVerification.Missing,WordPress.Security.ValidatedSanitizedInput -- nonce verified in handle_post(); file fields validated below.
		if ( empty( $_FILES['sb_brief_files']['name'][0] ) ) {
			return;
		}
		self::protect_upload_dir();
		$existing = (array) $order->get_meta( '_sb_brief_files' );
		$dir      = self::base_dir() . '/' . $order->get_id();
		wp_mkdir_p( $dir );
		$f     = $_FILES['sb_brief_files'];
		$count = count( (array) $f['name'] );
		for ( $i = 0; $i < $count; $i++ ) {
			if ( count( $existing ) >= self::MAX_FILES ) {
				wc_add_notice( __( 'File limit reached for this order.', 'seo-booster-core' ), 'notice' );
				break;
			}
			if ( UPLOAD_ERR_OK !== (int) $f['error'][ $i ] || ! is_uploaded_file( $f['tmp_name'][ $i ] ) ) {
				continue;
			}
			$original = sanitize_file_name( $f['name'][ $i ] );
			if ( (int) $f['size'][ $i ] > self::MAX_BYTES ) {
				/* translators: %s: file name */
				wc_add_notice( sprintf( __( '%s is larger than 20 MB and was skipped.', 'seo-booster-core' ), $original ), 'error' );
				continue;
			}
			$check = wp_check_filetype_and_ext( $f['tmp_name'][ $i ], $original, self::MIMES );
			if ( empty( $check['ext'] ) || empty( $check['type'] ) ) {
				/* translators: %s: file name */
				wc_add_notice( sprintf( __( '%s is not an allowed file type and was skipped.', 'seo-booster-core' ), $original ), 'error' );
				continue;
			}
			$stored = wp_generate_password( 20, false ) . '.' . $check['ext'];
			if ( move_uploaded_file( $f['tmp_name'][ $i ], $dir . '/' . $stored ) ) {
				$existing[] = array(
					'name'     => $stored,
					'original' => $original,
					'type'     => $check['type'],
					'at'       => gmdate( 'c' ),
				);
			}
		}
		// phpcs:enable
		$order->update_meta_data( '_sb_brief_files', $existing );
	}

	public static function file_url( WC_Order $order, string $stored ): string {
		return add_query_arg(
			array(
				'sb_file'  => rawurlencode( $stored ),
				'order'    => $order->get_id(),
				'_wpnonce' => wp_create_nonce( 'sb_file_' . $order->get_id() ),
			),
			home_url( '/' )
		);
	}

	/** Capability-checked download of a brief file. */
	public static function maybe_serve_file(): void {
		if ( empty( $_GET['sb_file'] ) || empty( $_GET['order'] ) ) {
			return;
		}
		$order = wc_get_order( absint( $_GET['order'] ) );
		$nonce = isset( $_GET['_wpnonce'] ) ? sanitize_text_field( wp_unslash( $_GET['_wpnonce'] ) ) : '';
		if ( ! $order || ! wp_verify_nonce( $nonce, 'sb_file_' . $order->get_id() ) || ! self::can_access( $order ) ) {
			wp_die( esc_html__( 'You do not have access to this file.', 'seo-booster-core' ), '', array( 'response' => 403 ) );
		}
		$stored = sanitize_file_name( wp_unslash( $_GET['sb_file'] ) );
		foreach ( (array) $order->get_meta( '_sb_brief_files' ) as $f ) {
			if ( $f['name'] === $stored ) {
				$path = self::base_dir() . '/' . $order->get_id() . '/' . $stored;
				if ( is_readable( $path ) ) {
					nocache_headers();
					header( 'Content-Type: ' . $f['type'] );
					header( 'Content-Disposition: attachment; filename="' . rawurlencode( $f['original'] ) . '"' );
					header( 'X-Content-Type-Options: nosniff' );
					header( 'Content-Length: ' . filesize( $path ) );
					readfile( $path ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_readfile
					exit;
				}
			}
		}
		wp_die( esc_html__( 'File not found.', 'seo-booster-core' ), '', array( 'response' => 404 ) );
	}

	/** Banner on the customer's order view. */
	public static function order_banner( WC_Order $order ): void {
		if ( ! self::lines( $order ) || ! $order->is_paid() ) {
			return;
		}
		$status = self::status( $order );
		$label  = 'complete' === $status ? __( 'Brief complete', 'seo-booster-core' ) : __( 'Brief needed', 'seo-booster-core' );
		$text   = 'complete' === $status ? __( 'Edit brief', 'seo-booster-core' ) : __( 'Complete your brief', 'seo-booster-core' );
		echo '<div class="woocommerce-info sb-brief-banner"><strong>' . esc_html( $label ) . '.</strong> ';
		if ( 'complete' !== $status ) {
			echo esc_html__( 'Work starts as soon as we have your project details.', 'seo-booster-core' ) . ' ';
		}
		echo '<a class="button" href="' . esc_url( self::url( $order ) ) . '">' . esc_html( $text ) . '</a></div>';
	}

	public static function thankyou_banner( $order_id ): void {
		$order = wc_get_order( $order_id );
		if ( ! $order || ! self::lines( $order ) ) {
			return;
		}
		if ( ! $order->get_customer_id() ) {
			echo '<div class="woocommerce-info">' . esc_html__( 'Next step: we will email you a link to share your project details. To submit them online, create an account with the same email address.', 'seo-booster-core' ) . '</div>';
			return;
		}
		self::order_banner( $order );
	}

	public static function admin_meta_box(): void {
		$screen = function_exists( 'wc_get_page_screen_id' ) ? wc_get_page_screen_id( 'shop-order' ) : 'shop_order';
		add_meta_box( 'sb_brief', __( 'Project brief', 'seo-booster-core' ), array( __CLASS__, 'render_admin_box' ), $screen, 'normal', 'high' );
	}

	public static function render_admin_box( $post_or_order ): void {
		$order = $post_or_order instanceof WC_Order ? $post_or_order : wc_get_order( $post_or_order->ID );
		if ( ! $order ) {
			return;
		}
		$lines = self::lines( $order );
		if ( ! $lines ) {
			echo '<p>' . esc_html__( 'No service packages on this order.', 'seo-booster-core' ) . '</p>';
			return;
		}
		$data = (array) $order->get_meta( '_sb_brief_data' );
		/* translators: %s: brief status */
		echo '<p><strong>' . esc_html( sprintf( __( 'Status: %s', 'seo-booster-core' ), self::status( $order ) ) ) . '</strong>';
		if ( $order->get_meta( '_sb_brief_submitted_at' ) ) {
			echo ' · ' . esc_html( $order->get_meta( '_sb_brief_submitted_at' ) );
		}
		echo '</p>';
		foreach ( $lines as $item_id => $line ) {
			echo '<h4>' . esc_html( $line['name'] ) . '</h4><table class="widefat striped"><tbody>';
			foreach ( self::profiles()[ $line['profile'] ] as $key => $def ) {
				$val = $data[ $item_id ][ $key ] ?? '';
				echo '<tr><th style="width:30%">' . esc_html( $def[0] ) . '</th><td>' . ( '' === $val ? '<em>—</em>' : nl2br( esc_html( $val ) ) ) . '</td></tr>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped inline.
			}
			echo '</tbody></table>';
		}
		$files = (array) $order->get_meta( '_sb_brief_files' );
		if ( $files ) {
			echo '<h4>' . esc_html__( 'Files', 'seo-booster-core' ) . '</h4><ul>';
			foreach ( $files as $f ) {
				echo '<li><a href="' . esc_url( self::file_url( $order, $f['name'] ) ) . '">' . esc_html( $f['original'] ) . '</a></li>';
			}
			echo '</ul>';
		}
	}

	public static function admin_column( array $cols ): array {
		$cols['sb_brief'] = __( 'Brief', 'seo-booster-core' );
		return $cols;
	}

	public static function admin_column_value( string $col, $order ): void {
		if ( 'sb_brief' !== $col || ! $order instanceof WC_Order || ! self::lines( $order ) ) {
			return;
		}
		$s = self::status( $order );
		echo '<mark class="order-status ' . ( 'complete' === $s ? 'status-completed' : 'status-on-hold' ) . '"><span>' . esc_html( ucfirst( $s ) ) . '</span></mark>';
	}

	public static function schedule_reminders( int $order_id ): void {
		if ( ! function_exists( 'as_schedule_single_action' ) ) {
			return;
		}
		foreach ( array( DAY_IN_SECONDS, 3 * DAY_IN_SECONDS ) as $delay ) {
			as_schedule_single_action( time() + $delay, 'sb_brief_reminder', array( 'order_id' => $order_id ), 'seo-booster' );
		}
	}

	public static function send_reminder( int $order_id ): void {
		$order = wc_get_order( $order_id );
		if ( ! $order || 'complete' === self::status( $order ) || ! $order->has_status( 'sb-awaiting-brief' ) ) {
			return;
		}
		$link   = $order->get_customer_id() ? self::url( $order ) : wc_get_page_permalink( 'myaccount' );
		$mailer = WC()->mailer();
		$head   = __( 'We need your project details', 'seo-booster-core' );
		$body   = '<p>' . esc_html__( 'Thanks for your order. We are ready to start as soon as you share your project brief.', 'seo-booster-core' ) . '</p><p><a href="' . esc_url( $link ) . '">' . esc_html__( 'Complete your brief', 'seo-booster-core' ) . '</a></p>';
		/* translators: %s: order number */
		$mailer->send( $order->get_billing_email(), sprintf( __( 'Order #%s: please complete your brief', 'seo-booster-core' ), $order->get_order_number() ), $mailer->wrap_message( $head, $body ) );
		$order->add_order_note( __( 'Brief reminder sent.', 'seo-booster-core' ) );
	}

	private static function notify_admin( WC_Order $order ): void {
		$mailer = WC()->mailer();
		/* translators: %s: order number */
		$subject = sprintf( __( 'Brief received for order #%s', 'seo-booster-core' ), $order->get_order_number() );
		$body    = '<p><a href="' . esc_url( $order->get_edit_order_url() ) . '">' . esc_html__( 'Open the order', 'seo-booster-core' ) . '</a></p>';
		$mailer->send( get_option( 'admin_email' ), $subject, $mailer->wrap_message( $subject, $body ) );
	}
}
