<?php
defined( 'ABSPATH' ) || exit;
get_header();
?>
<section class="section nf"><div class="container narrow center"><b class="grad-text">404</b>
<h1>This page has moved or doesn’t exist</h1><p class="lead">Try one of our services, browse all packages, or head back to the homepage.</p>
<div class="btn-row"><a class="btn btn-primary" href="<?php echo esc_url( home_url( '/' ) ); ?>">Back to home</a><a class="btn btn-ghost" href="<?php echo esc_url( function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' ) ); ?>">All packages</a></div></div></section>
<?php
get_footer();
