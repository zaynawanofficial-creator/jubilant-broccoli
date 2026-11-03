<?php
defined( 'ABSPATH' ) || exit;
get_header();
rrm_page_hero( sprintf( 'Search results for “%s”', get_search_query() ), '', 'Search' );
?>
<section class="section"><div class="container">
<?php if ( have_posts() ) : $i = 0; ?><div class="grid-3"><?php while ( have_posts() ) : the_post(); rrm_post_card( get_the_ID(), $i++ ); endwhile; ?></div>
<?php else : ?><p class="lead center">Nothing found. Try another search or <a href="<?php echo esc_url( home_url( '/contact-us/' ) ); ?>">ask us directly</a>.</p><?php endif; ?>
</div></section>
<?php
get_footer();
