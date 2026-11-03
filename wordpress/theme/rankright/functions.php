<?php
defined( 'ABSPATH' ) || exit;

add_action(
	'after_setup_theme',
	function () {
		add_theme_support( 'title-tag' );
		add_theme_support( 'post-thumbnails' );
		add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script', 'navigation-widgets' ) );
		add_theme_support( 'responsive-embeds' );
		add_theme_support( 'align-wide' );
		add_theme_support( 'woocommerce', array( 'single_image_width' => 900, 'thumbnail_image_width' => 720 ) );
		add_image_size( 'rrm-card', 720, 540, true );
		add_image_size( 'rrm-wide', 1200, 675, true );
		register_nav_menus( array( 'primary' => 'Primary (optional override)' ) );
	}
);

add_action(
	'wp_enqueue_scripts',
	function () {
		$dir = get_template_directory();
		$uri = get_template_directory_uri();
		wp_enqueue_style( 'rrm-main', $uri . '/assets/css/main.css', array(), filemtime( $dir . '/assets/css/main.css' ) );
		wp_enqueue_style( 'rrm-wp', $uri . '/assets/css/wp.css', array( 'rrm-main' ), filemtime( $dir . '/assets/css/wp.css' ) );
		wp_enqueue_script( 'rrm-main', $uri . '/assets/js/main.js', array(), filemtime( $dir . '/assets/js/main.js' ), array( 'strategy' => 'defer', 'in_footer' => false ) );
		if ( ! is_singular( 'post' ) ) {
			wp_dequeue_style( 'wp-block-library-theme' );
		}
	},
	20
);

/* Preload the two variable fonts used above the fold. */
add_action(
	'wp_head',
	function () {
		$uri = get_template_directory_uri() . '/assets/fonts/';
		echo '<link rel="preload" href="' . esc_url( $uri . 'outfit-var.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
		echo '<link rel="preload" href="' . esc_url( $uri . 'inter-var.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
		echo '<meta name="theme-color" content="#07010f">' . "\n";
	},
	1
);

add_filter(
	'get_site_icon_url',
	function ( $url ) {
		return $url ? $url : get_template_directory_uri() . '/assets/img/icon-192.png';
	}
);

/* WooCommerce: we render our own product/shop templates; keep Woo CSS only where its UI is used. */
add_filter(
	'woocommerce_enqueue_styles',
	function ( $styles ) {
		if ( function_exists( 'is_cart' ) && ( is_cart() || is_checkout() || is_account_page() ) ) {
			return $styles;
		}
		return array();
	}
);
add_filter( 'woocommerce_add_to_cart_redirect', function () { return wc_get_checkout_url(); } );
add_filter( 'wc_add_to_cart_message_html', '__return_empty_string' );
add_filter( 'woocommerce_product_single_add_to_cart_text', function () { return __( 'Buy now — secure checkout', 'rankright' ); } );
add_filter( 'woocommerce_get_price_suffix', function ( $suffix, $product ) {
	$unit = $product->get_meta( '_rrm_unit', true );
	return ( '/month' === $unit ) ? ' <small class="per">/month</small>' : $suffix;
}, 10, 2 );
remove_action( 'woocommerce_before_main_content', 'woocommerce_breadcrumb', 20 );

/* Excerpts */
add_filter( 'excerpt_length', function () { return 26; } );
add_filter( 'excerpt_more', function () { return '…'; } );

/* Add ids to H2s in posts for the table of contents. */
function rrm_toc( &$content ) {
	$toc     = array();
	$content = preg_replace_callback(
		'/<h2([^>]*)>(.*?)<\/h2>/is',
		function ( $m ) use ( &$toc ) {
			$text = wp_strip_all_tags( $m[2] );
			if ( preg_match( '/id="([^"]+)"/', $m[1], $idm ) ) {
				$id = $idm[1];
				$attrs = $m[1];
			} else {
				$id    = sanitize_title( $text );
				$attrs = $m[1] . ' id="' . esc_attr( $id ) . '"';
			}
			$toc[] = array( $id, $text );
			return '<h2' . $attrs . '>' . $m[2] . '</h2>';
		},
		$content
	);
	return $toc;
}

function rrm_page_hero( $title, $sub = '', $eyebrow = '', $crumbs = array() ) {
	?>
	<section class="page-hero"><div class="aurora"></div><div class="gridlines"></div>
		<div class="container rel narrow center">
			<?php if ( $crumbs ) : ?>
				<nav aria-label="Breadcrumb"><ol class="crumbs crumbs-center">
				<?php foreach ( $crumbs as $i => $c ) : ?>
					<?php if ( $i < count( $crumbs ) - 1 ) : ?><li><a href="<?php echo esc_url( $c[1] ); ?>"><?php echo esc_html( $c[0] ); ?></a></li>
					<?php else : ?><li aria-current="page"><?php echo esc_html( $c[0] ); ?></li><?php endif; ?>
				<?php endforeach; ?>
				</ol></nav>
			<?php endif; ?>
			<?php if ( $eyebrow ) : ?><span class="eyebrow"><?php echo esc_html( $eyebrow ); ?></span><?php endif; ?>
			<h1><?php echo esc_html( $title ); ?></h1>
			<?php if ( $sub ) : ?><p class="lead"><?php echo esc_html( $sub ); ?></p><?php endif; ?>
		</div>
	</section>
	<?php
}

function rrm_post_card( $post_id, $i = 0 ) {
	$cat = get_the_category( $post_id );
	?>
	<article class="post-card reveal d<?php echo (int) ( $i % 3 ); ?>">
		<a class="post-card-media" href="<?php echo esc_url( get_permalink( $post_id ) ); ?>" tabindex="-1" aria-hidden="true"><?php echo get_the_post_thumbnail( $post_id, 'rrm-wide', array( 'loading' => 'lazy' ) ); ?></a>
		<div class="post-card-body">
			<?php if ( $cat ) : ?><a class="tag" href="<?php echo esc_url( get_category_link( $cat[0] ) ); ?>"><?php echo esc_html( $cat[0]->name ); ?></a><?php endif; ?>
			<h3><a href="<?php echo esc_url( get_permalink( $post_id ) ); ?>"><?php echo esc_html( get_the_title( $post_id ) ); ?></a></h3>
			<p><?php echo esc_html( wp_strip_all_tags( get_the_excerpt( $post_id ) ) ); ?></p>
			<p class="post-meta"><?php echo esc_html( get_the_date( '', $post_id ) ); ?> · <?php echo (int) rrm_reading_time( $post_id ); ?> min read</p>
		</div>
	</article>
	<?php
}

/** Stats band, testimonials and CTA reused by theme templates (content comes from site.json). */
function rrm_partial( $name ) {
	$html = rrm_data( 'partials' );
	echo isset( $html[ $name ] ) ? rrm_placeholders( $html[ $name ] ) : ''; // phpcs:ignore -- trusted bundled markup
}
