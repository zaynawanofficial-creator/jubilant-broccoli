<?php
/**
 * Default copy per package group, applied by the importer. Editable afterwards in wp-admin per product.
 * Keys are sanitize_title( group name ) from SERVICE_CATALOG.csv.
 *
 * Copy rules: no ranking, indexing, dofollow or permanence guarantees; describe what is actually delivered.
 *
 * @package SEOBoosterCore
 */

defined( 'ABSPATH' ) || exit;

return array(
	'profiles-and-citations'  => array(
		'intro'        => 'Foundational links that make your business easy to find and verify: business listings, local citations, directory submissions and brand profiles on established platforms. Ideal for new sites, local businesses and brands that need consistent name, address and phone (NAP) data across the web.',
		'brief'        => 'offpage',
		'ideal_for'    => array(
			5   => 'Trying us out or topping up a new site',
			10  => 'New websites building a base',
			15  => 'Small local businesses',
			20  => 'Local businesses in one city',
			30  => 'Businesses targeting several locations',
			50  => 'Growing brands and ecommerce stores',
			75  => 'Competitive local or national niches',
			100 => 'Agencies and multi-location brands',
		),
		'featured'     => array( 20, 50 ),
		'deliverables' => "Mix of business listings, local citations, directory submissions and profile links\nManually created — no automated submission tools\nBusiness name, address and phone kept consistent (NAP)\nRelevant categories and a written business description on each listing\nSpreadsheet report with every live URL",
		'exclusions'   => "Guaranteed rankings, indexing, or dofollow status (each platform decides)\nPaid or premium directory fees\nRemoval of existing or duplicate listings\nPhone/postcard verification that only the business owner can complete",
		'requirements' => "Website URL\nBusiness name, address and phone (or online-only)\nShort business description and category\nEmail address you control for listing verification",
	),
	'premium-links'           => array(
		'intro'        => 'Editorial placements on real, traffic-earning websites and press release distribution. Pricing depends on the publisher’s authority, traffic and niche, so every order is quoted with a list of available sites before you pay.',
		'brief'        => 'offpage',
		'ideal_for'    => array(),
		'featured'     => array(),
		'deliverables' => "Shortlist of available publishers with metrics before you commit\nOriginal article written for the publisher’s audience (or your supplied article)\nContextual link to your page within the article\nSponsored/disclosure labelling where the publisher requires it\nLive URL report on publication",
		'exclusions'   => "Guaranteed rankings or traffic\nGuaranteed dofollow attribute (set by the publisher)\nPermanent placement guarantee — replacement terms are stated per quote\nPrivate blog networks (PBNs) or link farms",
		'requirements' => "Target URL and topic\nPreferred niche and country\nBudget range per placement",
	),
	'website-packages'        => array( 'brief' => 'web' ),
	'maintenance-plans'       => array( 'brief' => 'web' ),
	'article-writing'         => array( 'brief' => 'content' ),
	'content-batches'         => array( 'brief' => 'content' ),
	'social-creatives'        => array( 'brief' => 'design' ),
	'branding'                => array( 'brief' => 'design' ),
	'audit-packages'          => array( 'brief' => 'seo' ),
	'technical-seo-packages'  => array( 'brief' => 'seo' ),
	'ppc-packages'            => array( 'brief' => 'generic' ),
	'tracking-setup'          => array( 'brief' => 'seo' ),
	'email-packages'          => array( 'brief' => 'generic' ),
	'automation-packages'     => array( 'brief' => 'generic' ),
);
