<?php
defined( 'ABSPATH' ) || exit;
get_header();
while ( have_posts() ) :
	the_post();
	$id      = get_the_ID();
	$cat     = get_the_category();
	$content = apply_filters( 'the_content', get_the_content() );
	$toc     = rrm_toc( $content );
	$take    = json_decode( (string) get_post_meta( $id, '_rrm_takeaways', true ), true );
	$faqs    = json_decode( (string) get_post_meta( $id, '_rrm_faqs', true ), true );
	$svc     = rrm_service( (string) get_post_meta( $id, '_rrm_service', true ) );
	$author  = get_the_author_meta( 'ID' );
	?>
	<article class="post">
		<header class="post-hero"><div class="aurora"></div>
			<div class="container rel narrow-wide">
				<nav aria-label="Breadcrumb"><ol class="crumbs"><li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a></li><li><a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>">Blog</a></li><?php if ( $cat ) : ?><li><a href="<?php echo esc_url( get_category_link( $cat[0] ) ); ?>"><?php echo esc_html( $cat[0]->name ); ?></a></li><?php endif; ?></ol></nav>
				<?php if ( $cat ) : ?><span class="eyebrow"><?php echo esc_html( $cat[0]->name ); ?></span><?php endif; ?>
				<h1><?php the_title(); ?></h1>
				<p class="lead"><?php echo esc_html( wp_strip_all_tags( get_the_excerpt() ) ); ?></p>
				<div class="byline">
					<img src="<?php echo esc_url( rrm_assets_url( 'img/team/zain-ul-abdeen.webp' ) ); ?>" alt="<?php echo esc_attr( get_the_author() ); ?>" width="48" height="48">
					<span><b><?php the_author(); ?></b><span>Founder, RankRight Media · <time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date() ); ?></time> · Updated <time datetime="<?php echo esc_attr( get_the_modified_date( 'c' ) ); ?>"><?php echo esc_html( get_the_modified_date() ); ?></time> · <?php echo (int) rrm_reading_time( $id ); ?> min read</span></span>
				</div>
			</div>
		</header>
		<div class="container narrow-wide">
			<figure class="post-feature"><?php the_post_thumbnail( 'rrm-wide', array( 'loading' => 'eager', 'fetchpriority' => 'high' ) ); ?></figure>
		</div>
		<div class="container post-grid">
			<aside class="post-aside" aria-label="On this page">
				<?php if ( $toc ) : ?>
					<nav class="toc"><h2>On this page</h2><ol><?php foreach ( $toc as $t ) : ?><li><a href="#<?php echo esc_attr( $t[0] ); ?>"><?php echo esc_html( $t[1] ); ?></a></li><?php endforeach; ?></ol></nav>
				<?php endif; ?>
				<?php if ( $svc ) : ?>
					<div class="side-card side-cta"><h2><?php echo esc_html( $svc['short_name'] ); ?> packages</h2><p><?php echo esc_html( $svc['card'] ); ?></p><a class="btn btn-dark btn-block" href="<?php echo esc_url( home_url( '/' . $svc['slug'] . '/#pricing' ) ); ?>">See packages <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a></div>
				<?php endif; ?>
			</aside>
			<div class="post-body">
				<?php if ( $take ) : ?>
					<aside class="facts takeaways" aria-labelledby="kt"><h2 id="kt"><?php echo rrm_icon( 'i-sparkle' ); // phpcs:ignore ?>Key takeaways</h2><ul><?php foreach ( $take as $t ) : ?><li><?php echo esc_html( $t ); ?></li><?php endforeach; ?></ul></aside>
				<?php endif; ?>
				<div class="prose entry"><?php echo $content; // phpcs:ignore ?></div>
				<?php if ( $faqs ) : ?>
					<section class="post-faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2><div class="faq">
					<?php foreach ( $faqs as $f ) : ?>
						<details><summary><?php echo esc_html( $f[0] ); ?><span class="pm"><?php echo rrm_icon( 'i-chevron' ); // phpcs:ignore ?></span></summary><div class="a"><?php echo wp_kses_post( $f[1] ); ?></div></details>
					<?php endforeach; ?></div></section>
				<?php endif; ?>
				<section class="author-box" aria-label="About the author">
					<img src="<?php echo esc_url( rrm_assets_url( 'img/team/zain-ul-abdeen.webp' ) ); ?>" alt="<?php echo esc_attr( get_the_author() ); ?>" width="96" height="96" loading="lazy">
					<div><span class="eyebrow">Written by</span><h2><?php the_author(); ?></h2><p><?php echo esc_html( get_the_author_meta( 'description' ) ); ?></p><a class="text-link" href="<?php echo esc_url( home_url( '/about-us/' ) ); ?>">Meet the team <?php echo rrm_icon( 'i-arrow' ); // phpcs:ignore ?></a></div>
				</section>
			</div>
		</div>
	</article>
	<?php
	$related = get_posts( array( 'numberposts' => 3, 'post__not_in' => array( $id ), 'category__in' => $cat ? array( $cat[0]->term_id ) : array() ) );
	if ( count( $related ) < 3 ) {
		$related = get_posts( array( 'numberposts' => 3, 'post__not_in' => array( $id ) ) );
	}
	if ( $related ) :
		?>
		<section class="section"><div class="container"><div class="section-head"><span class="eyebrow">Keep reading</span><h2>Related guides</h2></div>
		<div class="grid-3"><?php foreach ( $related as $i => $r ) { rrm_post_card( $r->ID, $i ); } ?></div></div></section>
		<?php
	endif;
	rrm_partial( 'cta' );
endwhile;
get_footer();
