<?php
/**
 * SEO helpers that complement Rank Math (which handles titles, meta, Organization, WebPage,
 * Article and Product schema and the XML sitemaps). We add only what Rank Math doesn't:
 * Service + OfferCatalog on service pages, FAQPage, team Person nodes, redirects and llms.txt.
 */
defined( 'ABSPATH' ) || exit;

/** Page-level JSON-LD stored at import time (with {{HOME}} placeholders). */
add_action(
	'wp_head',
	function () {
		$nodes = array();
		if ( is_singular( 'page' ) ) {
			$raw = get_post_meta( get_queried_object_id(), '_rrm_schema', true );
			$n   = $raw ? json_decode( rrm_placeholders( $raw ), true ) : null;
			if ( is_array( $n ) ) {
				$nodes = array_merge( $nodes, $n );
			}
		}
		if ( is_singular( 'post' ) ) {
			$faqs = json_decode( (string) get_post_meta( get_queried_object_id(), '_rrm_faqs', true ), true );
			if ( $faqs ) {
				$nodes[] = rrm_faq_node( $faqs, get_permalink() );
			}
		}
		if ( is_singular( 'product' ) ) {
			$product = wc_get_product( get_queried_object_id() );
			$svc     = $product ? rrm_service( rrm_pkg_meta( $product, 'service' ) ) : null;
			if ( $svc && ! empty( $svc['faqs'] ) ) {
				$nodes[] = rrm_faq_node( $svc['faqs'], get_permalink() );
			}
		}
		if ( ! $nodes ) {
			return;
		}
		$json = wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $nodes ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		echo '<script type="application/ld+json">' . str_replace( '</', '<\/', $json ) . "</script>\n"; // phpcs:ignore
	},
	30
);

function rrm_faq_node( $faqs, $url ) {
	$q = array();
	foreach ( $faqs as $f ) {
		$q[] = array(
			'@type'          => 'Question',
			'name'           => $f[0],
			'acceptedAnswer' => array( '@type' => 'Answer', 'text' => trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( $f[1] ) ) ) ),
		);
	}
	return array( '@type' => 'FAQPage', '@id' => $url . '#faq', 'mainEntity' => $q );
}

/** Use Rank Math's Organization @id so our Service nodes connect to its graph. */
add_filter(
	'rank_math/json_ld',
	function ( $data ) {
		if ( isset( $data['publisher'] ) ) {
			$data['publisher']['@id'] = home_url( '/#organization' );
		}
		return $data;
	},
	99
);

/** 301 redirects from old WordPress URLs on rankrightmedia.uk. */
add_action(
	'template_redirect',
	function () {
		if ( ! is_404() ) {
			return;
		}
		$path = trim( (string) wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? esc_url_raw( wp_unslash( $_SERVER['REQUEST_URI'] ) ) : '', PHP_URL_PATH ), '/' );
		$map  = (array) rrm_data( 'redirects' );
		if ( isset( $map[ $path ] ) ) {
			wp_safe_redirect( home_url( $map[ $path ] ), 301 );
			exit;
		}
	},
	1
);

/** /llms.txt: concise, factual brief for AI assistants (generated live from packages). */
add_action(
	'init',
	function () {
		add_rewrite_rule( '^llms\.txt$', 'index.php?rrm_llms=1', 'top' );
	}
);
add_filter(
	'query_vars',
	function ( $v ) {
		$v[] = 'rrm_llms';
		return $v;
	}
);
add_action(
	'template_redirect',
	function () {
		if ( ! get_query_var( 'rrm_llms' ) ) {
			return;
		}
		$s   = rrm_data( 'settings' );
		$out = "# {$s['name']}\n\n> {$s['llms_summary']}\n\n";
		$out .= '- Website: ' . home_url( '/' ) . "\n- Phone: {$s['phone_display']}\n- Email: {$s['email']}\n- Address: {$s['address']['street']}, {$s['address']['locality']} {$s['address']['postcode']}, United Kingdom\n- Serves: UK and international clients\n- Currency: USD\n\n## Services\n\n";
		foreach ( (array) rrm_data( 'service_order' ) as $key ) {
			$svc  = rrm_service( $key );
			$out .= "- [{$svc['name']}](" . home_url( '/' . $svc['slug'] . '/' ) . "): {$svc['description']}\n";
		}
		foreach ( (array) rrm_data( 'service_order' ) as $key ) {
			$svc  = rrm_service( $key );
			$out .= "\n## {$svc['heading']}\n\n";
			foreach ( rrm_packages( $key ) as $p ) {
				$out .= '- [' . rrm_pkg_meta( $p, 'short', $p->get_name() ) . '](' . get_permalink( $p->get_id() ) . ') — ' . rrm_money( $p->get_regular_price() ) . ( '' === $p->get_regular_price() ? '' : ' ' . rrm_pkg_meta( $p, 'unit' ) ) . ': ' . implode( '; ', rrm_pkg_features( $p ) ) . "\n";
			}
		}
		$out .= "\n## Guides\n\n";
		foreach ( get_posts( array( 'numberposts' => 20 ) ) as $post ) {
			$out .= '- [' . get_the_title( $post ) . '](' . get_permalink( $post ) . '): ' . wp_strip_all_tags( get_the_excerpt( $post ) ) . "\n";
		}
		header( 'Content-Type: text/plain; charset=utf-8' );
		header( 'X-Robots-Tag: noindex' );
		echo $out; // phpcs:ignore
		exit;
	}
);

/** robots.txt: welcome search engines and AI answer engines; point to Rank Math sitemap. */
add_filter(
	'robots_txt',
	function ( $output, $public ) {
		if ( ! $public ) {
			return $output;
		}
		$bots = array( 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'PerplexityBot', 'Google-Extended', 'Applebot-Extended', 'Bingbot' );
		$add  = "\n# AI assistants are welcome to read and cite this site\n";
		foreach ( $bots as $b ) {
			$add .= "User-agent: {$b}\nAllow: /\nDisallow: /wp-admin/\nDisallow: /cart/\nDisallow: /checkout/\nDisallow: /my-account/\n\n";
		}
		return $output . $add . 'Sitemap: ' . home_url( '/sitemap_index.xml' ) . "\n";
	},
	99,
	2
);
