<?php
/**
 * Article helpers for single posts: "On this page" contents, heading anchors, related posts, reading progress.
 *
 * @package SEOBoosterTheme
 */

defined( 'ABSPATH' ) || exit;

/**
 * H2 headings of the current post, in order, with unique anchor ids.
 *
 * @return array<int, array{text:string, id:string}>
 */
function sbt_post_headings(): array {
	static $cache = array();
	$post_id = get_the_ID();
	if ( ! $post_id ) {
		return array();
	}
	if ( isset( $cache[ $post_id ] ) ) {
		return $cache[ $post_id ];
	}
	$out  = array();
	$seen = array();
	$walk = static function ( array $blocks ) use ( &$walk, &$out, &$seen ): void {
		foreach ( $blocks as $b ) {
			if ( 'core/heading' === $b['blockName'] && 2 === (int) ( $b['attrs']['level'] ?? 2 ) ) {
				$text = trim( wp_strip_all_tags( (string) $b['innerHTML'] ) );
				if ( '' !== $text ) {
					$id = sanitize_title( $text );
					$id = '' === $id ? 'section' : $id;
					$n  = 2;
					$base = $id;
					while ( isset( $seen[ $id ] ) ) {
						$id = $base . '-' . $n++;
					}
					$seen[ $id ] = true;
					$out[]       = array(
						'text' => html_entity_decode( $text, ENT_QUOTES, 'UTF-8' ),
						'id'   => ! empty( $b['attrs']['anchor'] ) ? (string) $b['attrs']['anchor'] : $id,
					);
				}
			}
			if ( ! empty( $b['innerBlocks'] ) ) {
				$walk( $b['innerBlocks'] );
			}
		}
	};
	$walk( parse_blocks( (string) get_post_field( 'post_content', $post_id ) ) );
	$cache[ $post_id ] = $out;
	return $out;
}

/* Give each article H2 its anchor (front end only; saved content is untouched). */
add_filter(
	'render_block_core/heading',
	static function ( string $html, array $block ): string {
		static $used = array();
		if ( ! is_singular( 'post' ) || is_admin() || 2 !== (int) ( $block['attrs']['level'] ?? 2 ) || ! class_exists( 'WP_HTML_Tag_Processor' ) ) {
			return $html;
		}
		$text = html_entity_decode( trim( wp_strip_all_tags( $html ) ), ENT_QUOTES, 'UTF-8' );
		foreach ( sbt_post_headings() as $h ) {
			if ( $h['text'] === $text && empty( $used[ $h['id'] ] ) ) {
				$used[ $h['id'] ] = true;
				$p                = new WP_HTML_Tag_Processor( $html );
				if ( $p->next_tag( 'h2' ) && null === $p->get_attribute( 'id' ) ) {
					$p->set_attribute( 'id', $h['id'] );
					return $p->get_updated_html();
				}
				return $html;
			}
		}
		return $html;
	},
	10,
	2
);

/** [sb_toc] "On this page" list for the current post (needs 3+ sections). */
function sbt_toc_shortcode(): string {
	$heads = sbt_post_headings();
	if ( count( $heads ) < 3 ) {
		return '';
	}
	$out = '<nav class="sb-otp" aria-label="' . esc_attr__( 'On this page', 'seo-booster' ) . '"><p class="sb-otp__h">' . esc_html__( 'On this page', 'seo-booster' ) . '</p><ol>';
	foreach ( $heads as $h ) {
		$out .= '<li><a href="#' . esc_attr( $h['id'] ) . '">' . esc_html( $h['text'] ) . '</a></li>';
	}
	return sbt_raw( $out . '</ol></nav>' );
}

/** [sb_related] three more articles, same category first. */
function sbt_related_shortcode(): string {
	$id   = get_the_ID();
	$cats = wp_get_post_categories( $id );
	$args = array(
		'post_type'           => 'post',
		'posts_per_page'      => 3,
		'post__not_in'        => array( $id ),
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	);
	$posts = $cats ? get_posts( $args + array( 'category__in' => $cats ) ) : array();
	if ( count( $posts ) < 3 ) {
		$more  = get_posts( array_merge( $args, array( 'post__not_in' => array_merge( array( $id ), wp_list_pluck( $posts, 'ID' ) ), 'posts_per_page' => 3 - count( $posts ) ) ) );
		$posts = array_merge( $posts, $more );
	}
	if ( ! $posts ) {
		return '';
	}
	$out = '<div class="sb-related__grid">';
	foreach ( $posts as $p ) {
		$cat  = get_the_category( $p->ID );
		$link = get_permalink( $p );
		$out .= '<article class="sb-related__card">';
		if ( has_post_thumbnail( $p ) ) {
			$out .= '<a class="sb-related__img" href="' . esc_url( $link ) . '" tabindex="-1" aria-hidden="true">' . get_the_post_thumbnail( $p, 'medium_large', array( 'loading' => 'lazy', 'alt' => '' ) ) . '</a>';
		}
		$out .= '<div class="sb-related__body">';
		if ( $cat ) {
			$out .= '<p class="sb-related__cat">' . esc_html( $cat[0]->name ) . '</p>';
		}
		$out .= '<h3 class="sb-related__title"><a href="' . esc_url( $link ) . '">' . esc_html( get_the_title( $p ) ) . '</a></h3>';
		$out .= '<p class="sb-related__ex">' . esc_html( wp_trim_words( get_the_excerpt( $p ), 18 ) ) . '</p>';
		$out .= '</div></article>';
	}
	return sbt_raw( $out . '</div>' );
}

/** [sb_post_dek] the excerpt as a standfirst under the title. */
function sbt_dek_shortcode(): string {
	$ex = has_excerpt() ? get_the_excerpt() : '';
	return '' === $ex ? '' : sbt_raw( '<p class="sb-post-dek">' . esc_html( $ex ) . '</p>' );
}

add_action(
	'init',
	static function () {
		add_shortcode( 'sb_toc', 'sbt_toc_shortcode' );
		add_shortcode( 'sb_related', 'sbt_related_shortcode' );
		add_shortcode( 'sb_post_dek', 'sbt_dek_shortcode' );
	}
);

/* Thin reading-progress bar on articles. */
add_action(
	'wp_footer',
	static function () {
		if ( ! is_singular( 'post' ) ) {
			return;
		}
		echo '<div class="sb-progress" aria-hidden="true"><span></span></div>';
		echo "<script>(function(){var b=document.querySelector('.sb-progress span'),a=document.querySelector('.sb-prose');if(!b||!a)return;var t=0;function u(){t=0;var r=a.getBoundingClientRect(),h=r.height-innerHeight*.6,p=h>0?Math.min(1,Math.max(0,-r.top/h)):1;b.style.transform='scaleX('+p+')';}addEventListener('scroll',function(){if(!t){t=requestAnimationFrame(u);}},{passive:true});u();})();</script>\n";
	},
	20
);
