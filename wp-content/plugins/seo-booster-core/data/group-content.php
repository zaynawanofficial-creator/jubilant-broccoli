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
		'intro'        => 'Guest posts on established websites, grouped by Domain Rating (DR, an Ahrefs authority metric), plus press release writing and distribution. Higher DR tiers mean stronger, harder-to-get publishers.',
		'brief'        => 'offpage',
		'ideal_for'    => array(),
		'featured'     => array(),
		'featured_index' => array( 3 ),
		'ideal_for_index' => array( 1 => 'Testing or adding variety', 2 => 'New sites building authority', 3 => 'Most businesses — best value', 4 => 'Competitive local niches', 5 => 'Established sites', 6 => 'Competitive national niches', 7 => 'High-competition keywords', 8 => 'Launches, funding and company news' ),
		'deliverables' => "Publisher at or above the DR tier you order, relevant to your niche where available\nOriginal article written for the publisher’s audience (or your supplied article)\nContextual link to your page within the article\nSponsored/disclosure labelling where the publisher requires it\nLive URL report with the site’s DR at time of publishing\nPress release: 400–500 word release written for you and distributed to a news network",
		'exclusions'   => "Guaranteed rankings or traffic\nGuaranteed dofollow attribute (set by the publisher)\nPermanent placement guarantee (free replacement if removed within 90 days)\nPrivate blog networks (PBNs) or link farms",
		'requirements' => "Target URL and anchor/topic ideas\nYour niche and target country\nNews angle (for press releases)",
	),
	'website-packages'        => array(
		'intro'        => 'Responsive WordPress websites built on a maintainable theme, with your content entered, basic on-page SEO set up and a short handover video so you can edit pages yourself.',
		'brief'        => 'web',
		'ideal_for'    => array( 1 => 'Launching one offer or campaign', 2 => 'Simple service business', 5 => 'Small business website', 10 => 'Established business or several services' ),
		'featured'     => array( 5 ),
		'deliverables' => "Mobile-friendly WordPress pages built to your brief\nYour content and images added (you supply text and logo)\nContact form connected to your email\nBasic on-page SEO: titles, meta descriptions, headings, sitemap\nSpeed basics: image compression and caching\nHandover video showing how to edit pages",
		'exclusions'   => "Domain, hosting and premium theme/plugin licences\nCopywriting (available as a separate package)\nEcommerce/shop setup, bookings or custom features (quoted)\nOngoing maintenance after handover",
		'requirements' => "Logo and brand colours\nText for each page (or order copywriting)\nHosting access via a user invite\nExamples of websites you like",
	),
	'maintenance-plans'       => array(
		'intro'        => 'Fast fixes for WordPress problems and simple monthly care: updates, backups, uptime checks and small changes handled by a developer.',
		'brief'        => 'web',
		'ideal_for'    => array(),
		'featured'     => array(),
		'featured_index' => array( 2 ),
		'ideal_for_index' => array( 1 => 'Not sure what is wrong yet', 2 => 'One clear problem', 3 => 'Several issues at once', 4 => 'Small sites that need upkeep', 5 => 'Business sites that change often' ),
		'deliverables' => "Investigation by a WordPress developer\nBackup taken before any change\nClear written summary of what was wrong and what was changed\nCare plans: plugin/theme/core updates, weekly backups and uptime monitoring for 30 days",
		'exclusions'   => "Fixes needing a full redesign or custom development (quoted)\nMalware clean-up of heavily infected sites (assessed first)\nPremium plugin licences or hosting fees\nGuaranteed fix where the cause is the host or a third-party service",
		'requirements' => "Website URL and a description of the problem\nAdmin access via a user invite (never send passwords)\nScreenshots or steps to reproduce the issue",
	),
	'article-writing'         => array(
		'intro'        => 'Original, researched articles written for people first and structured for search: clear headings, answers to real questions and natural keyword use.',
		'brief'        => 'content',
		'ideal_for'    => array( 500 => 'News, updates and short guides', 1000 => 'Standard blog posts', 1500 => 'In-depth how-to guides', 2000 => 'Pillar pages and comparisons', 3000 => 'Ultimate guides' ),
		'featured'     => array( 1000, 1500 ),
		'deliverables' => "Original article written to your topic and audience\nKeyword-informed headings and structure\nMeta title and meta description\nPlagiarism check\nDelivered as a Google Doc or Word file",
		'exclusions'   => "Publishing to your website (available on request)\nStock image licences\nRanking or traffic guarantees\nHighly technical, medical, legal or financial expertise (quoted separately)",
		'requirements' => "Topic or working title\nTarget audience and keyword\nTone of voice and any examples",
	),
	'content-batches'         => array(
		'intro'        => 'A month or more of blog content in one order, planned as a topic cluster so the articles support each other and your main service pages.',
		'brief'        => 'content',
		'ideal_for'    => array( 5 => 'One month of weekly posts', 10 => 'Building a topic cluster fast' ),
		'featured'     => array( 10 ),
		'deliverables' => "Topic list planned around one cluster, approved before writing\n1,000-word original articles\nMeta titles and descriptions\nSuggested internal links between the articles\nPlagiarism check",
		'exclusions'   => "Publishing to your website (available on request)\nStock image licences\nRanking or traffic guarantees",
		'requirements' => "Your website and main services\nTarget audience\nAny topics to include or avoid",
	),
	'social-creatives'        => array(
		'intro'        => 'On-brand graphics for social posts and ads, sized for each platform and delivered ready to upload.',
		'brief'        => 'design',
		'ideal_for'    => array( 1 => 'A single post or ad', 3 => 'A short campaign', 5 => 'A week of posts', 10 => 'Two weeks of content' ),
		'featured'     => array( 5 ),
		'deliverables' => "Custom graphics in your brand colours and fonts\nSized for your chosen platform (Instagram, Facebook, LinkedIn, X)\nPNG/JPG files ready to post\nEditable source file on request",
		'exclusions'   => "Copywriting and captions\nPaid stock photos (free-licence images used, or you supply)\nVideo or animation\nPosting and account management",
		'requirements' => "Logo and brand colours\nText for each graphic\nPlatform and size\nReference designs you like",
	),
	'branding'                => array(
		'intro'        => 'A clear, consistent visual identity: logo, colours and typography with simple guidelines your team and suppliers can follow.',
		'brief'        => 'design',
		'ideal_for'    => array(),
		'featured'     => array(),
		'featured_index' => array( 2 ),
		'ideal_for_index' => array( 1 => 'New businesses and side projects', 2 => 'Businesses launching or rebranding', 3 => 'Brands with a dated logo' ),
		'deliverables_by_index' => array(
			1 => "2 logo concepts\nColour palette\nFont pairing\nOne-page brand guide\nVector (SVG/PDF) and PNG files",
			2 => "3 logo concepts\nLogo variations (horizontal, stacked, icon)\nColour palette and typography\nBrand guidelines PDF\nSocial profile kit\nVector (AI/SVG/PDF) and PNG files",
			3 => "Modernised version of your existing logo\nUpdated colour palette\nUpdated one-page brand guide\nVector (SVG/PDF) and PNG files",
		),
		'deliverables' => "Vector source files (AI/SVG/PDF) and PNG exports",
		'exclusions'   => "Trademark searches or registration\nPrinting\nWebsite design\nUnlimited concepts",
		'requirements' => "Business name and what you do\nAudience and competitors\nStyles you like and dislike\nExisting logo (for refresh)",
	),
	'audit-packages'          => array(
		'intro'        => 'A prioritised list of what is holding your site back in search, written in plain English with the fix for each issue.',
		'brief'        => 'seo',
		'ideal_for'    => array(),
		'featured'     => array(),
		'featured_index' => array( 2 ),
		'ideal_for_index' => array( 1 => 'Quick health check', 2 => 'Sites planning an SEO push', 3 => 'Large and ecommerce sites' ),
		'deliverables' => "Crawl of your site and review of indexing, speed, mobile and on-page basics\nPrioritised issue list (high / medium / low) with how to fix each one\nFull audit adds: content and keyword review, internal linking, backlink profile overview and competitor comparison\nPDF report",
		'exclusions'   => "Implementing the fixes (see Technical SEO packages)\nRanking guarantees\nSites over 500 pages (quoted as Enterprise)",
		'requirements' => "Website URL\nGoogle Search Console access via user invite (recommended)\nMain competitors and target market",
	),
	'technical-seo-packages'  => array(
		'intro'        => 'Hands-on fixes to the technical issues that stop search engines crawling, understanding and ranking your pages.',
		'brief'        => 'seo',
		'ideal_for'    => array(),
		'ideal_for_index' => array( 1 => 'After an audit — get the fixes done', 2 => 'Slow sites failing Core Web Vitals', 3 => 'Ongoing technical upkeep' ),
		'featured'     => array(),
		'deliverables' => "Fixes made directly on your site after a backup\nCovers indexing, redirects, broken links, canonical tags, sitemaps, schema basics and page speed\nBefore/after report of every change\nCore Web Vitals package: image, script and caching optimisation with lab measurements",
		'exclusions'   => "Redesigns or new features\nGuaranteed scores or rankings (field data depends on real users)\nHosting upgrades or premium plugin licences",
		'requirements' => "Website URL\nAdmin and Search Console access via user invites\nPlatform details (WordPress, Shopify, etc.)",
	),
	'ppc-packages'            => array( 'brief' => 'generic' ),
	'tracking-setup'          => array( 'brief' => 'seo' ),
	'email-packages'          => array( 'brief' => 'generic' ),
	'automation-packages'     => array( 'brief' => 'generic' ),
);
