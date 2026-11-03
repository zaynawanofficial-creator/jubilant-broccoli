<?php
/* Blog index and archives. */
defined( 'ABSPATH' ) || exit;
get_header();
if ( is_home() ) {
	rrm_page_hero( 'The RankRight Blog', 'Practical guides on SEO, link building, websites, content, PPC and social media — written by people who do the work every day.', 'Insights', array( array( 'Home', home_url( '/' ) ), array( 'Blog', home_url( '/blog/' ) ) ) );
} else {
	rrm_page_hero( wp_strip_all_tags( get_the_archive_title() ), wp_strip_all_tags( get_the_archive_description() ), 'Blog', array( array( 'Home', home_url( '/' ) ), array( 'Blog', home_url( '/blog/' ) ), array( wp_strip_all_tags( single_term_title( '', false ) ), '' ) ) );
}
$cats = get_categories( array( 'hide_empty' => true ) );
?>
<section class="section"><div class="container">
	<?php if ( $cats ) : ?>
		<nav class="chip-row" aria-label="Blog categories"><a class="chip<?php echo is_home() ? ' on' : ''; ?>" href="<?php echo esc_url( home_url( '/blog/' ) ); ?>">All</a>
		<?php foreach ( $cats as $c ) : ?><a class="chip<?php echo is_category( $c->term_id ) ? ' on' : ''; ?>" href="<?php echo esc_url( get_category_link( $c ) ); ?>"><?php echo esc_html( $c->name ); ?></a><?php endforeach; ?></nav>
	<?php endif; ?>
	<?php if ( have_posts() ) : $i = 0; ?>
		<div class="grid-3 post-grid-list">
		<?php while ( have_posts() ) : the_post(); rrm_post_card( get_the_ID(), $i++ ); endwhile; ?>
		</div>
		<div class="pager"><?php the_posts_pagination( array( 'mid_size' => 1 ) ); ?></div>
	<?php else : ?>
		<p class="lead center">No posts yet — check back soon.</p>
	<?php endif; ?>
</div></section>
<?php
rrm_partial( 'cta' );
get_footer();
