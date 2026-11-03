<?php
defined( 'ABSPATH' ) || exit;
$s       = rrm_data( 'settings' );
$current = trailingslashit( strtok( isset( $_SERVER['REQUEST_URI'] ) ? esc_url_raw( wp_unslash( $_SERVER['REQUEST_URI'] ) ) : '/', '?' ) );
$is      = function ( $path ) use ( $current ) {
	return $current === $path ? ' aria-current="page"' : '';
};
$svc_active = false;
foreach ( (array) rrm_data( 'service_order' ) as $k ) {
	$sv = rrm_service( $k );
	if ( 0 === strpos( $current, '/' . $sv['slug'] . '/' ) ) {
		$svc_active = true;
	}
}
if ( function_exists( 'is_shop' ) && ( is_singular( 'product' ) || is_shop() || is_product_category() ) ) {
	$svc_active = true;
}
?><!doctype html>
<html <?php language_attributes(); ?> class="no-js">
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip" href="#main"><?php esc_html_e( 'Skip to content', 'rankright' ); ?></a>
<header class="site-header">
	<div class="container nav">
		<a class="brand" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="<?php echo esc_attr( $s['name'] ); ?> home"><img src="<?php echo esc_url( rrm_assets_url( 'img/logo-rankright-media.webp' ) ); ?>" alt="<?php echo esc_attr( $s['name'] ); ?>" width="232" height="73"></a>
		<nav aria-label="Main">
			<ul class="nav-links" id="nav-links">
				<li><a href="<?php echo esc_url( home_url( '/' ) ); ?>"<?php echo $is( '/' ); // phpcs:ignore ?>>Home</a></li>
				<li class="has-menu"><button type="button" aria-expanded="false" aria-controls="svc-menu"<?php echo $svc_active ? ' aria-current="true"' : ''; ?>>Services <?php echo rrm_icon( 'i-chevron' ); // phpcs:ignore ?></button>
					<ul class="menu" id="svc-menu">
						<?php foreach ( (array) rrm_data( 'service_order' ) as $k ) : $sv = rrm_service( $k ); ?>
							<li><a href="<?php echo esc_url( home_url( '/' . $sv['slug'] . '/' ) ); ?>"><span class="mi"><?php echo rrm_icon( $sv['icon'] ); // phpcs:ignore ?></span><span><strong><?php echo esc_html( $sv['menu_name'] ); ?></strong><small><?php echo esc_html( $sv['menu_blurb'] ); ?></small></span></a></li>
						<?php endforeach; ?>
						<li class="menu-all"><a href="<?php echo esc_url( function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/shop/' ) ); ?>"><span class="mi"><?php echo rrm_icon( 'i-card' ); // phpcs:ignore ?></span><span><strong>Compare all packages</strong><small>Every plan and price in one place</small></span></a></li>
					</ul></li>
				<li><a href="<?php echo esc_url( home_url( '/about-us/' ) ); ?>"<?php echo $is( '/about-us/' ); // phpcs:ignore ?>>About Us</a></li>
				<li><a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>"<?php echo ( is_home() || is_singular( 'post' ) || is_category() ) ? ' aria-current="page"' : ''; ?>>Blog</a></li>
				<li><a href="<?php echo esc_url( home_url( '/contact-us/' ) ); ?>"<?php echo $is( '/contact-us/' ); // phpcs:ignore ?>>Contact Us</a></li>
			</ul>
		</nav>
		<div class="nav-cta">
			<a class="nav-phone" href="tel:<?php echo esc_attr( $s['phone_e164'] ); ?>"><?php echo rrm_icon( 'i-phone' ); // phpcs:ignore ?><?php echo esc_html( $s['phone_display'] ); ?></a>
			<a class="btn btn-primary btn-sm" href="<?php echo esc_url( home_url( '/contact-us/' ) ); ?>">Get started <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a>
			<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu"><?php echo rrm_icon( 'i-menu', 'i-open' ) . rrm_icon( 'i-close', 'i-close' ); // phpcs:ignore ?></button>
		</div>
	</div>
</header>
<main id="main">
