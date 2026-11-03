"""
All site copy and business data lives here. Edit this file, run `python3 build.py`, deploy `public/`.

Copy marked SOURCE: WP is carried over from the live WordPress site (rankrightmedia.uk) screenshots.
Copy marked NEW is added for on-page SEO / AI-overview coverage.
"""

# --------------------------------------------------------------------------------------------
# Business facts — single source of truth (used in pages, schema, llms.txt)
# --------------------------------------------------------------------------------------------
SITE = {
    "name": "RankRight Media",
    "legal_name": "RankRight Media Ltd",
    "domain": "https://rankrightmedia.uk",
    "tagline": "UK digital marketing agency for SEO, link building, websites, content, PPC and social media.",
    "phone_display": "+44 7446 254421",       # SOURCE: WP (Premium Support card)
    "phone_e164": "+447446254421",
    "email": "support@rankrightmedia.uk",
    "address": {"street": "68 Trelawney Road", "locality": "Ilford", "postcode": "IG6 2NJ", "region": "England"},
    "company_number": "",                     # TODO: Companies House number (strong trust/E-E-A-T signal)
    "founded": "",                            # TODO: year founded
    "same_as": [],                            # TODO: Google Business Profile, LinkedIn, Facebook, Instagram, Trustpilot URLs
    "currency_code": "USD",
    "currency_symbol": "$",
    "area_served": ["United Kingdom", "Worldwide"],
    "rating_display": "",
    "founded_text": "",
}

# One consistent set of numbers (the WP site showed three conflicting sets — see AUDIT.md).
STATS = [
    {"value": 1, "suffix": "K+", "label": "Projects delivered"},
    {"value": 500, "suffix": "+", "label": "Happy clients"},
    {"value": 5, "suffix": "+", "label": "Industry awards"},
]

# Founders / team — SOURCE: WP About page (not reachable from the build environment).
# Add each person, drop their photo in src/assets/img/team/ and the section + Person schema appear automatically.
TEAM = [
    {"name": "Zain Ul Abdeen", "role": "Founder — SEO, Web & eCommerce Expert", "photo": "team/zain-ul-abdeen.webp",
     "bio": "Founder of SEO Booster UK with 10+ years of experience in SEO, website development and eCommerce strategy. Helping businesses grow online with data-driven, results-focused solutions."},
    {"name": "Wajid Maqsood", "role": "eCommerce Solutions Specialist", "photo": "team/wajid-maqsood.webp",
     "bio": "eCommerce specialist focused on store setup, product listing optimisation and conversion-focused solutions across WooCommerce, Shopify and marketplace platforms."},
    {"name": "Rizwan Hussain", "role": "Visual Marketing Specialist", "photo": "team/rizwan-hussain.webp",
     "bio": "Creative graphic designer specialising in brand identity, product visuals, social media creatives and marketing assets that make brands stand out online and in the marketplace."},
]

# --------------------------------------------------------------------------------------------
# Testimonials — SOURCE: WP (names, words and photos exactly as published)
# --------------------------------------------------------------------------------------------
TESTIMONIALS = {
    "thomas-graham": {"name": "Thomas Graham", "context": "Content Writing client", "photo": None,
        "quote": "I loved working with RankRightMedia.uk! They delivered blog content that matched our eco-friendly brand tone perfectly. It felt like they were part of our team."},
    "emma-clarke": {"name": "Emma Clarke", "context": "Content Writing client", "photo": "testimonials/emma-clarke.webp",
        "quote": "We were struggling with product descriptions. Their team rewrote everything and made it sound exciting and clear. Sales have definitely improved."},
    "sophie-bennett": {"name": "Sophie Bennett", "context": "Content Writing client", "photo": "testimonials/sophie-bennett.webp",
        "quote": "Their web content made our site look professional and trustworthy. The writing was clean, SEO-friendly, and just what we needed to connect with our customers."},
    "daniel-reid": {"name": "Daniel Reid", "context": "SEO client", "photo": "testimonials/daniel-reid.webp",
        "quote": "Thanks to RankRightMedia.uk, our website now ranks on the first page for multiple keywords. Organic traffic has doubled in just three months!"},
    "mason-blake": {"name": "Mason Blake", "context": "SEO client", "photo": "testimonials/mason-blake.webp",
        "quote": "Brilliant SEO service! They improved our site structure and backlink profile, and now we’re getting consistent inquiries through search engines."},
    "harper-lane": {"name": "Harper Lane", "context": "SEO client", "photo": "testimonials/harper-lane.webp",
        "quote": "Their SEO strategies are spot on. From keyword research to on-page optimization, everything was handled professionally. We’re seeing real results!"},
    "nathan-clarke": {"name": "Nathan Clarke", "context": "Link Building client", "photo": "testimonials/nathan-clarke.webp",
        "quote": "Professional, transparent, and results-driven. The outreach was strategic and clean. I've worked with many SEO firms, and RankRightMedia.uk stands out in link building."},
    "olivia-mason": {"name": "Olivia Mason", "context": "Link Building client", "photo": "testimonials/olivia-mason.webp",
        "quote": "I was impressed with how natural and high-quality the backlinks were. Our brand visibility has grown and our rankings are climbing. A real game changer for our SEO strategy."},
    "amelia-hart": {"name": "Amelia Hart", "context": "Link Building client", "photo": "testimonials/amelia-hart.webp",
        "quote": "The link building service from RankRightMedia.uk delivered measurable results. Our domain authority improved within weeks, and traffic has steadily increased. Highly recommended."},
}

# --------------------------------------------------------------------------------------------
# Featured projects — SOURCE: WP "What We've Done for Our Clients"
# --------------------------------------------------------------------------------------------
PROJECTS = [
    {"tag": "Digital Branding", "name": "Loka Perfume & Co", "client": "Emma Smith", "date": "Jan 2024", "location": "Manchester, UK", "budget": "£5,000", "img": None, "art": 1, "icon": "i-sparkle"},
    {"tag": "Digital Marketing", "name": "Compass Shoes", "client": "Sophie Williams", "date": "Apr 2024", "location": "Bristol, UK", "budget": "£7,000", "img": None, "art": 2, "icon": "i-trend"},
    {"tag": "Content Writing", "name": "Style & Stitch Boutique", "client": "Olivia Bennett", "date": "Apr 2024", "location": "Nottingham, UK", "budget": "£20,000", "img": None, "art": 3, "icon": "i-pen"},  # WP showed "£20,00" — confirm
    {"tag": "SEO", "name": "Fresh Bites Catering", "client": "Harry Collins", "date": "Jun 2024", "location": "Sheffield, UK", "budget": "£9,000", "img": "work/fresh-bites-catering.webp", "art": 0, "icon": ""},
    {"tag": "PPC Campaign", "name": "LuxeGlow Skincare", "client": "Amelia Roberts", "date": "Sep 2024", "location": "Liverpool, UK", "budget": "£10,000", "img": "work/luxeglow-skincare.webp", "art": 0, "icon": ""},
    {"tag": "Website Development", "name": "UrbanNest Interiors", "client": "James Walker", "date": "Jan 2025", "location": "Edinburgh, UK", "budget": "£25,000", "img": None, "art": 4, "icon": "i-monitor"},  # WP showed "£25,00" — confirm
]

# --------------------------------------------------------------------------------------------
# Services
# --------------------------------------------------------------------------------------------
SERVICES = {}

SERVICES["seo"] = {
    "slug": "search-engine-optimization",   # SOURCE: WP URL
    "name": "Search Engine Optimization (SEO)",
    "short_name": "SEO",
    "menu_blurb": "Rank higher on Google and win organic leads",
    "icon": "i-layers",
    "card": "We help you rank higher on Google, attract the right audience, and stay ahead of your competition.",
    "card_points": ["Keyword research & strategy", "On-page & technical SEO", "Local SEO for UK businesses"],
    "service_type": "Search engine optimisation",
    "title": "SEO Services UK | Monthly SEO Packages from $299",
    "description": "UK SEO services that turn rankings into revenue: keyword research, on-page, technical and local SEO plus link building. Monthly plans from $299.",
    "eyebrow": "Search engine optimization",
    "h1": "Boost Your Google Ranking with Proven SEO Strategies",
    "lead": "Get seen by the right people at the right time. At RankRight Media, we use smart SEO techniques to help your website climb search results and attract more traffic. From keyword research to technical fixes — we handle it all, so you stay ahead of the competition.",
    "visual": {"kind": "dash", "label": "Organic performance", "chip": "Page 1 rankings"},
    "intro": """
<h2>Search Engine Optimization (SEO) services for UK businesses</h2>
<p><strong>SEO (search engine optimisation) is the process of improving your website so it appears higher in Google for the searches your customers make</strong> — bringing you free, compounding traffic instead of paying for every click.</p>
<p>Your website deserves more than just being online — it deserves to be found by the right people at the right time. At <strong>RankRight Media</strong>, we specialise in driving <strong>organic traffic</strong> that actually converts into real business. Whether you’re a small local shop or a national brand, our expert SEO strategies help your website climb search engine rankings and stay ahead of the competition.</p>
<p>With years of experience and proven results, we’ve successfully ranked websites across many different industries. From deep keyword research to building high-authority backlinks — we handle every part of SEO for you. And we don’t just aim for traffic — we aim for <strong>revenue-generating visibility</strong>.</p>
<p>Let us help you dominate Google, attract quality visitors, and grow your brand online — step by step, strategy by strategy.</p>
<h2>What does an SEO service include?</h2>
<p>Every RankRight SEO package combines the four pillars Google rewards: <strong>technical health</strong> (speed, crawlability, indexing), <strong>relevance</strong> (keyword-mapped pages and content), <strong>authority</strong> (high-quality backlinks) and <strong>local trust</strong> (Google Business Profile and citations). You get a clear monthly report showing rankings, traffic and enquiries — not vanity metrics.</p>
""",
    "checklist": ["In-Depth Keyword Research", "Local SEO (for UK Businesses)", "On-Page Optimization", "Competitor Analysis", "Technical SEO Fixes", "Content Optimization & Blog Strategy", "High-Quality Backlink Building", "SEO Audit & Roadmap", "Monthly Progress Reports", "Conversion-Focused SEO"],
    "features": [("i-layers", "Website Audit", "#includes"), ("i-target", "On-Page SEO", "#includes"), ("i-shield", "Off-Page SEO", "#includes"), ("i-monitor", "Technical SEO", "#includes"), ("i-award", "Keyword Strategy", "#includes")],
    "facts": [("Service", "Search engine optimisation (SEO)"), ("Packages", "6 monthly plans, from $299/month"), ("Includes", "Keyword research, on-page, technical, local SEO, link building"), ("Reporting", "Monthly performance report (weekly on E-commerce SEO)"), ("Typical timeline", "First movements in 4–8 weeks; strongest gains at 3–6 months"), ("Area served", "United Kingdom")],
    "packages": {
        "heading": "Our SEO Monthly Packages", "unit": "/month",
        "note": "Prices are per month. Every plan includes a written monthly performance report.",
        "items": [
            {"id": "seo-basic", "name": "Basic SEO", "price": 299, "tagline": "For local businesses starting out", "features": ["Up to 5 keywords", "On-Page Optimization for 5 Pages", "Meta Tags & Description Optimization", "Google Analytics Setup", "Monthly Performance Report"]},
            {"id": "seo-standard", "name": "Standard SEO", "price": 499, "featured": True, "tagline": "For growing SMEs ready to compete", "features": ["Up to 20 keywords", "On-Page Optimization for 20 Pages", "Technical SEO Audit & Fixes", "Link Building (20 backlinks)", "Blog & Content Strategy"]},
            {"id": "seo-premium", "name": "Premium SEO", "price": 1099, "tagline": "For competitive and multi-location brands", "features": ["Up to 30 keywords", "On-Page Optimization for 30 Pages", "Advanced Local SEO", "SEO Audit & Optimization", "Link Building (30 backlinks)", "Content Strategy + 4 Articles"]},
            {"id": "seo-enterprise", "name": "Enterprise SEO", "price": 1499, "tagline": "For large sites and national reach", "features": ["Up to 50 keywords", "On-Page Optimization for 50 Pages", "Technical SEO & Site Speed Optimization", "Comprehensive Link Building", "Blog & Content Strategy + 8 Articles"]},
            {"id": "seo-ecommerce", "name": "E-commerce SEO", "price": 1899, "tagline": "For online stores and product catalogues", "features": ["Up to 70 keywords", "On-Page Optimization for 70+ Product Pages", "Advanced Product Description Optimization", "Link Building (100 backlinks)", "Content Strategy + 12 Articles", "Weekly Performance Report with ROI Tracking"]},
            {"id": "seo-custom", "name": "Custom SEO", "price": None, "tagline": "Tailored to complex or international goals", "features": ["Unlimited Keywords", "Full Website Audit & Custom SEO Strategy", "On-Page Optimization for Unlimited Pages", "Advanced Technical SEO", "High-Quality Link Building", "E-commerce, Local, & International SEO", "ROI & Conversion Tracking"]},
        ],
    },
    "process_heading": "Our SEO Process",
    "process": [
        ("i-globe", "Website Audit & Fixes", "We perform a full SEO audit to identify technical issues and improve your site’s performance."),
        ("i-search", "Keyword Research", "We find the most relevant and high-volume keywords using top tools like Ahrefs and Semrush."),
        ("i-file", "On-Page Optimization", "We optimise your website content, titles, and structure to match search engine best practices."),
        ("i-link", "Backlink Building", "Quality backlinks are created from trusted sources to increase your domain authority and rankings."),
    ],
    "panel": {"img": "team-at-monitors.webp", "alt": "RankRight Media SEO specialists reviewing a client website together",
        "h2": "Unlock Your Website’s Potential with Expert SEO Services",
        "body": "<p>In today’s digital world, standing out online is more important than ever. At RankRightMedia.uk, we specialise in delivering top-notch SEO services that drive real results for your business. Whether you’re looking to increase your website’s visibility on search engines, attract more qualified traffic, or convert visitors into loyal customers, we’ve got you covered.</p><p>Our team of SEO experts uses a data-driven approach, implementing strategies tailored to your specific business needs. From keyword research and on-page optimisation to link building and content creation, we ensure your website ranks higher and performs better.</p>"},
    "includes_heading": "Our SEO Services Include",
    "includes": [
        ("i-search", "Keyword Research & Strategy", "We identify high-performing keywords that your target audience is searching for. Our strategy ensures your content ranks for the right terms. This builds stronger visibility and connects you with potential customers. Data-driven insights make all the difference."),
        ("i-file", "On-Page SEO Optimization", "We optimise your website’s structure, titles, meta tags, and content for maximum visibility. On-page SEO is the foundation of a successful strategy. We ensure everything from headings to images aligns with best practices. Cleaner pages, better rankings."),
        ("i-chart", "Technical SEO", "Our technical audits fix issues that can harm your site’s performance. We improve site speed, fix crawl errors, and ensure mobile-friendliness. Search engines love a technically sound site — and so do your visitors. Better experience, higher trust."),
        ("i-link", "Link Building", "We build high-quality, relevant backlinks from trusted sources. These links improve your site’s authority and help you rank higher in search results. Our ethical strategies ensure long-term benefits. It’s all about smart, sustainable growth."),
        ("i-pin", "Local SEO", "Want to attract customers nearby? Our local SEO services optimise your Google Business Profile and local listings. You’ll rank better in map results and get found by local searchers. Perfect for service providers and physical businesses across the UK."),
        ("i-target", "Monthly SEO Reporting", "Stay in the loop with clear, data-driven monthly reports. We show your traffic growth, keyword rankings, and what’s working. Transparency is key — we want you to see real progress every month. Our results speak for themselves."),
    ],
    "includes_cta": "Get started",
    "testimonials": ["daniel-reid", "mason-blake", "harper-lane"],
    "faqs": [
        ("How much do SEO services cost in the UK?", "<p>Our monthly SEO packages start at <strong>$299 per month</strong> (Basic SEO, up to 5 keywords) and go up to <strong>$1,899 per month</strong> for E-commerce SEO covering 70+ product pages. Standard SEO at $499/month adds a technical audit, 20 backlinks and a content strategy. Larger or international projects are quoted on our Custom SEO plan.</p>"),
        ("How long does SEO take to work?", "<p>Most websites see first ranking movements within <strong>4–8 weeks</strong> of on-page and technical fixes going live. Meaningful traffic and lead growth typically builds over <strong>3–6 months</strong>, depending on your competition, your site’s history and how many keywords you target.</p>"),
        ("What is included in an SEO package?", "<p>Every plan includes keyword research, on-page optimisation of your key pages, meta title and description optimisation and a monthly performance report. Higher plans add technical SEO audits and fixes, link building, local SEO, content strategy and written articles.</p>"),
        ("Do you offer local SEO for UK businesses?", "<p>Yes. Local SEO is included from our Premium plan and available on request. We optimise your Google Business Profile, build consistent local citations and create location-relevant content so you show up in the map pack and “near me” searches.</p>"),
        ("Do you guarantee first-page rankings?", "<p>No honest agency can guarantee rankings — Google controls the algorithm. What we guarantee is the work: every deliverable in your package, done to best practice, with transparent monthly reporting so you can see exactly what was done and what moved.</p>"),
        ("Is your SEO white-hat and Google-safe?", "<p>Yes. We follow Google’s Search Essentials and spam policies: no private blog networks, no link schemes, no keyword stuffing. That protects your site from penalties and builds rankings that last.</p>"),
    ],
    "related": ["link-building", "content-writing", "website-development"],
}

SERVICES["link-building"] = {
    "slug": "link-building-services",       # SOURCE: WP URL
    "name": "Link Building",
    "short_name": "Link Building",
    "menu_blurb": "Manual outreach backlinks from real sites",
    "icon": "i-link",
    "card": "Boost your website’s authority with high-quality, niche-relevant backlinks. Our manual outreach ensures safe and effective SEO growth.",
    "card_points": ["100% manual outreach", "DA 10+ to DA 50+ sites", "Dofollow, contextual placements"],
    "service_type": "Link building",
    "title": "Link Building Services UK | Manual Outreach Backlinks from $3.49",
    "description": "White-hat link building: manual outreach, guest posts and contextual dofollow backlinks on niche-relevant DA 10–50+ sites. From $3.49 with reports.",
    "eyebrow": "Link building",
    "h1": "Build Powerful Backlinks That Boost Your Rankings",
    "lead": "Rank higher and gain authority with our proven link building strategies. We create high-quality backlinks that drive traffic and grow your business.",
    "visual": {"kind": "bars", "label": "Authority growth", "chip": "Manual outreach",
               "bars": [("Referring domains", "w-84"), ("Domain authority", "w-70"), ("Topical relevance", "w-90"), ("Organic traffic", "w-78")]},
    "intro": """
<h2>Link Building Services That Drive Real SEO Results</h2>
<p><strong>Link building is the process of earning links from other reputable websites to yours.</strong> Google treats each relevant link as a vote of confidence, so a stronger backlink profile is one of the most reliable ways to lift rankings.</p>
<p>At <strong>RankRightMedia.uk</strong>, we understand that quality backlinks are one of the most important ranking factors in SEO. Our <strong>Link Building Services</strong> are designed to help your website earn trusted, relevant, and powerful backlinks that boost your domain authority, increase search engine rankings, and drive targeted traffic.</p>
<h2>Why Link Building Matters</h2>
<p>Search engines like Google use backlinks as a vote of confidence. The more high-quality backlinks your website has, the more trustworthy and authoritative it appears. This leads to:</p>
<ul><li>Better keyword rankings</li><li>More organic traffic</li><li>Higher domain authority</li><li>Increased visibility in competitive markets</li></ul>
""",
    "checklist": ["Manual Outreach Only", "Contextual Link Placement", "High Domain Authority (DA) Sites", "Custom Strategy for Every Client", "Niche-Relevant Backlinks", "In-Depth Competitor Analysis", "High-Quality Backlink Building", "Dofollow Backlinks", "White-Hat Techniques", "Content Creation Included"],
    "features": [("i-layers", "100% Manual Link Building", "#includes"), ("i-target", "White-Hat & Google-Safe Techniques", "#why"), ("i-shield", "Niche-Relevant High-Quality Sites", "#why"), ("i-monitor", "Transparent Reporting", "#pricing"), ("i-award", "Proven Track Record of Results", "#reviews")],
    "facts": [("Service", "Manual outreach link building"), ("Packages", "6 one-off plans, from $3.49"), ("Site quality", "DA 10+ up to DA 50+, niche-relevant"), ("Link type", "Dofollow, contextual placements"), ("Delivery", "3 to 12 days depending on plan"), ("Reporting", "Placement report with live URLs")],
    "packages": {
        "heading": "Our Link Building Packages", "unit": "one-off",
        "note": "One-off packages. Each order includes a placement report listing every live URL.",
        "items": [
            {"id": "lb-basic", "name": "Basic Plan", "price": 3.49, "tagline": "Test the waters", "features": ["2 Dofollow backlinks", "DA 10+ website", "Manual Outreach", "Basic placement report", "Delivery in 3 days"]},
            {"id": "lb-starter", "name": "Starter Plan", "price": 6.49, "tagline": "Niche relevance on a budget", "features": ["6 Niche-relevant backlinks", "DA 15+ website", "Dofollow + Contextual placement", "Basic content included", "Delivery in 5–7 days"]},
            {"id": "lb-standard", "name": "Standard Boost", "price": 11.49, "featured": True, "tagline": "Guest posts plus profile links", "features": ["3 Guest Post backlinks", "5 Profile Backlinks", "DA 25+ niche site", "400-word SEO content", "Manual outreach", "Delivery in 7 days"]},
            {"id": "lb-advanced", "name": "Advanced Reach", "price": 24.49, "tagline": "Premium guest posting", "features": ["5 Premium guest posts", "DA 30+ site", "500–600 word content", "Dofollow & niche placement", "Delivery in 7–10 days"]},
            {"id": "lb-pro", "name": "Pro Authority", "price": 39.49, "tagline": "High-traffic authority links", "features": ["8 backlinks from DA 40+ sites", "700-word premium article", "High-traffic, relevant website", "Manual outreach only", "Report with metrics", "Delivery in 10 days"]},
            {"id": "lb-elite", "name": "Elite Plan", "price": 64.49, "tagline": "Editorial links from DA 50+", "features": ["10 backlinks from DA 50+ websites", "1000-word editorial content", "High-engagement niche site", "Manual & ethical outreach", "Detailed performance report", "Delivery in 10–12 days"]},
        ],
    },
    "process_heading": "Our Link Building Process",
    "process": [
        ("i-globe", "Niche Analysis", "We study your industry, competitors, and existing backlink profile to build a strategy tailored to your goals."),
        ("i-search", "Targeted Outreach", "Our outreach specialists connect with reputable websites and blogs relevant to your niche."),
        ("i-file", "Content Creation", "We craft valuable, SEO-optimised content that naturally includes your backlinks."),
        ("i-monitor", "Quality Link Placement", "Backlinks are placed contextually on authority sites with high domain ratings for maximum impact."),
    ],
    "panel": {"img": "outreach-team.webp", "alt": "RankRight Media outreach team planning backlink placements",
        "h2": "Why Choose RankRightMedia.uk for Link Building?", "anchor": "why",
        "body": "<p>At <strong>RankRightMedia.uk</strong>, we don’t just build backlinks — we build credibility, trust, and long-term SEO success. Here’s what sets us apart:</p>",
        "ticks": [
            ("Proven SEO Results", "We’ve helped businesses climb Google through high-quality link building strategies. Our data-driven approach ensures you see real improvements in visibility, traffic, and rankings."),
            ("100% White-Hat Methods", "We strictly follow Google’s guidelines. No spammy links, no shady tactics — just ethical, sustainable SEO that protects your website’s reputation."),
            ("Manual Outreach by Experts", "Every backlink is earned through genuine, one-on-one outreach. We build relationships with site owners and editors to secure placements on real, high-authority websites."),
            ("Industry-Relevant Placements", "Your links appear on websites that are highly relevant to your niche, which increases trust and drives better quality traffic."),
            ("High DA, Quality-Checked Sites", "We vet every site for strong domain authority, real traffic and a clean backlink profile. You get real value — not just a link."),
            ("Customised Strategy", "Every business is different. We build a custom link building plan around your industry, goals, and competition — no cookie-cutter plans."),
        ]},
    "includes_heading": "Our Link Building Services Include",
    "includes": [
        ("i-link", "High Authority Backlinks", "We focus on acquiring backlinks from domains with high DA (Domain Authority) to increase your website’s trust and search engine rankings."),
        ("i-layers", "Broken Link Building", "We identify broken links on niche-relevant sites and suggest your content as a valuable replacement, earning high-quality links ethically."),
        ("i-target", "Competitor Link Analysis", "Our experts analyse your competitors’ backlink profiles to uncover new link-building opportunities and outperform them in search results."),
        ("i-pen", "Guest Post Outreach", "We pitch and write genuinely useful articles for relevant blogs and publications, with a contextual link back to your site."),
        ("i-file", "Contextual Placements", "Links placed inside relevant, existing content where they add value for readers — the placements Google trusts most."),
        ("i-users", "Profile & Citation Links", "Brand profiles and business citations that build a natural, diverse link profile and support local SEO."),
    ],
    "includes_cta": "Contact us",
    "testimonials": ["nathan-clarke", "olivia-mason", "amelia-hart"],
    "faqs": [
        ("How much does link building cost?", "<p>Our link building packages start at <strong>$3.49</strong> for 2 dofollow backlinks on a DA 10+ site and go up to <strong>$64.49</strong> for 10 editorial backlinks from DA 50+ websites with 1,000-word content. Every package is a one-off price with a placement report.</p>"),
        ("Are your backlinks dofollow?", "<p>Yes. Our packages deliver dofollow backlinks placed contextually within relevant content. Profile backlinks in the Standard Boost plan diversify your link profile alongside guest posts.</p>"),
        ("Is link building safe for my website?", "<p>Yes, when it is done the way we do it: manual outreach to real, niche-relevant websites with genuine content. We never use private blog networks or automated link spam, which are what trigger Google penalties.</p>"),
        ("How long until backlinks improve my rankings?", "<p>Links are usually indexed within a few weeks of going live. Ranking improvements typically follow over <strong>4–12 weeks</strong>, depending on your competition and how relevant the linking sites are to your niche.</p>"),
        ("What is the difference between DA and DR?", "<p>Domain Authority (DA, by Moz) and Domain Rating (DR, by Ahrefs) are third-party scores from 0–100 estimating a site’s backlink strength. Google doesn’t use either directly, so we also check real traffic, relevance and link profile quality before placing your links.</p>"),
        ("Will I get a report of my links?", "<p>Yes. Every order includes a placement report with the live URL of each link; higher plans add metrics such as authority and traffic for each linking site.</p>"),
    ],
    "related": ["seo", "content-writing", "social-media-marketing"],
}

SERVICES["website-development"] = {
    "slug": "website-development",          # TODO: confirm WP URL slug
    "name": "Website Development",
    "short_name": "Website Development",
    "menu_blurb": "Fast, mobile-first sites that convert",
    "icon": "i-globe",
    "card": "Beautiful, fast, and mobile-friendly websites built to impress and convert visitors into customers.",
    "card_points": ["Custom, mobile-first design", "SEO-ready from day one", "WordPress, Shopify & custom code"],
    "service_type": "Website design and development",
    "title": "Website Development Services UK | Fast, SEO-Ready Sites",
    "description": "Website design and development for UK businesses: fast, mobile-first, SEO-ready sites on WordPress, Shopify or custom code, built to convert.",
    "eyebrow": "Website development",
    "h1": "We Don’t Just Build Sites — We Build Your Online Identity",
    "lead": "Your website is more than just pages — it’s the face of your business. We create custom websites that reflect your brand, connect with your audience, and drive real results. Whether you’re starting fresh or need a revamp, we’re here to build a site that truly represents you.",
    "visual": {"kind": "bars", "label": "Site quality checks", "chip": "Core Web Vitals",
               "bars": [("Performance", "w-95"), ("Accessibility", "w-90"), ("Best practices", "w-95"), ("SEO", "w-95")]},
    "intro": """
<h2>Website development services built for growth</h2>
<p><strong>Website development is the design, build and launch of a website that is fast, secure, easy to manage and built to convert visitors into enquiries or sales.</strong> At RankRight Media, every site we build is mobile-first, accessible and optimised for search from the very first line of code.</p>
<p>Your website is often the first impression a customer has of your business. We combine clean design with conversion-focused page structure — clear calls to action, trust signals and fast load times — so your site works as hard as you do.</p>
<h2>What kind of websites do you build?</h2>
<p>We build business websites, landing pages, e-commerce stores and redesigns on <strong>WordPress</strong>, <strong>Shopify</strong> or <strong>lightweight custom code</strong>, depending on what suits your goals, budget and team. Every build includes on-page SEO foundations, analytics setup and a handover so you can update content yourself.</p>
""",
    "checklist": ["Custom, Mobile-First Design", "SEO-Ready Page Structure", "Fast Load Times & Core Web Vitals", "Conversion-Focused Layouts", "WordPress & Shopify Builds", "E-commerce Stores", "Secure Hosting Setup & SSL", "Google Analytics & Search Console", "Accessibility Best Practice", "Training & Handover"],
    "features": [("i-monitor", "Custom Web Design", "#includes"), ("i-cart", "E-commerce Websites", "#includes"), ("i-zap", "Speed & Core Web Vitals", "#includes"), ("i-search", "SEO-Ready Builds", "#includes"), ("i-wrench", "Maintenance & Support", "#includes")],
    "facts": [("Service", "Website design & development"), ("Platforms", "WordPress, Shopify, custom HTML/CSS/JS"), ("Included", "Mobile-first design, on-page SEO, analytics setup"), ("Pricing", "Fixed quote after a free discovery call"), ("Area served", "United Kingdom")],
    "packages": {
        "heading": "Our Website Development Packages", "unit": "one-off",
        "note": "One-off project prices. Hosting and domain are not included unless stated.",
        "items": [
            {"id": "web-starter", "name": "Starter Site", "price": 199, "tagline": "A professional presence, fast", "features": ["Up to 3 pages", "Mobile responsive design", "WordPress CMS setup", "Basic contact form", "Delivery: 3–5 working days", "7-day post-launch support"]},
            {"id": "web-business", "name": "Business Site", "price": 399, "featured": True, "tagline": "For growing service businesses", "features": ["5–7 pages", "Custom design layout", "Mobile + tablet responsive", "WordPress CMS", "SEO-ready structure", "2 revisions", "14-day post-launch support"]},
            {"id": "web-pro", "name": "Pro Site", "price": 699, "tagline": "Fully custom, built to rank", "features": ["Up to 10 pages", "Fully custom design", "Advanced contact forms", "Blog integration", "On-page SEO setup", "3 design revisions", "Delivery: 7–10 working days", "30-day post-launch support"]},
            {"id": "web-ecom-basic", "name": "E-Commerce Basic", "price": 799, "tagline": "Start selling online", "features": ["Up to 8 product pages", "Shopify or WooCommerce setup", "Cart + Checkout system", "Payment gateway integration", "Responsive design", "30-day support"]},
            {"id": "web-ecom-pro", "name": "E-Commerce Pro", "price": 1199, "tagline": "A fully custom online store", "features": ["Up to 20 product pages", "Fully custom store", "Product filters, categories", "Secure payments setup", "SEO-friendly product pages", "Delivery: 10–14 working days"]},
            {"id": "web-custom", "name": "Custom Plan", "price": None, "tagline": "Complex builds and integrations", "features": ["Unlimited pages", "Any platform (WordPress, Shopify, custom)", "Advanced features & integrations", "Priority support", "Custom design + backend functionality"]},
        ],
    },
    "process_heading": "Our Website Development Process",
    "process": [
        ("i-message", "Discovery", "We learn about your business, customers and goals, then agree a sitemap, features and a fixed quote."),
        ("i-pen", "Design", "We design key pages for desktop and mobile with your branding, and refine them with your feedback."),
        ("i-monitor", "Build", "We develop a fast, secure, SEO-ready site and load your content, images and tracking."),
        ("i-rocket", "Launch & Support", "We test across devices, go live, submit to Google and support you after launch."),
    ],
    "panel": {"img": "team-at-monitors.webp", "alt": "RankRight Media web developers reviewing a website build",
        "h2": "Designed to Grow With You",
        "body": "<p>Whether you’re just starting or scaling fast, our web solutions are responsive, flexible, and future-ready. We build on platforms you can manage yourself, keep the code lean so pages load quickly, and set up the analytics you need to see what’s working.</p><p>Because SEO is built in from the start — clean headings, structured data, fast pages and a logical site structure — your new website is ready to rank, not just ready to launch.</p>"},
    "includes_heading": "Our Website Services Include",
    "includes": [
        ("i-monitor", "Business Websites", "Professional multi-page websites that explain what you do, build trust and make it easy for visitors to get in touch."),
        ("i-cart", "E-commerce Stores", "Online shops on Shopify or WooCommerce with product pages, secure checkout and the structure to rank in Google Shopping and search."),
        ("i-target", "Landing Pages", "High-converting landing pages for campaigns and ads, built around one goal and tested for speed and clarity."),
        ("i-zap", "Speed Optimisation", "We improve Core Web Vitals — loading, interactivity and visual stability — for a better experience and stronger rankings."),
        ("i-search", "SEO-Ready Structure", "Logical page hierarchy, clean URLs, meta tags, schema markup and internal links set up properly from day one."),
        ("i-wrench", "Maintenance & Updates", "Ongoing updates, backups, security monitoring and small changes so your website stays fast, safe and current."),
    ],
    "includes_cta": "Get a quote",
    "testimonials": ["sophie-bennett", "mason-blake", "amelia-hart"],
    "faqs": [
        ("How much does a website cost in the UK?", "<p>It depends on the number of pages, features and whether you need e-commerce. We give you a <strong>fixed, itemised quote</strong> after a free discovery call, so there are no surprises. Tell us what you need via our contact form and we’ll come back with a price.</p>"),
        ("How long does it take to build a website?", "<p>A typical business website takes <strong>2–6 weeks</strong> from discovery to launch. Larger e-commerce sites with many products or custom features can take longer; we agree a timeline before work starts.</p>"),
        ("Will my website be mobile-friendly and SEO-ready?", "<p>Yes. Every site we build is designed mobile-first and includes on-page SEO foundations: optimised titles and descriptions, heading structure, fast loading, image optimisation, schema markup and Google Search Console setup.</p>"),
        ("Can I update the website myself?", "<p>Yes. We build on easy-to-manage platforms such as WordPress and Shopify and show you how to edit pages, add blog posts and update products.</p>"),
        ("Do you redesign existing websites?", "<p>Yes. We can redesign your current site and migrate content carefully, keeping your URLs or setting up redirects so you don’t lose the rankings you already have.</p>"),
    ],
    "related": ["seo", "content-writing", "ppc"],
}

SERVICES["content-writing"] = {
    "slug": "content-writing",              # TODO: confirm WP URL slug
    "name": "Content Writing",
    "short_name": "Content Writing",
    "menu_blurb": "SEO blogs, web copy and product descriptions",
    "icon": "i-file",
    "card": "High-quality blog posts, website content, and social media captions that tell your story and build trust.",
    "card_points": ["SEO blog posts & guides", "Website & landing page copy", "Product descriptions"],
    "service_type": "SEO content writing",
    "title": "SEO Content Writing Services UK | Blogs & Web Copy",
    "description": "SEO content writing services from UK writers: blog posts, website copy, product descriptions and social captions that rank in Google and turn readers into customers.",
    "eyebrow": "Content writing",
    "h1": "SEO Content Writing That Ranks and Sells",
    "lead": "High-quality blog posts, website content, and social media captions that tell your story and build trust — written by people, optimised for search and shaped around what your customers actually ask.",
    "visual": {"kind": "bars", "label": "Content quality score", "chip": "Search intent matched",
               "bars": [("Search intent match", "w-95"), ("Readability", "w-90"), ("Topical coverage", "w-84"), ("Brand voice", "w-95")]},
    "intro": """
<h2>SEO content writing services for UK brands</h2>
<p><strong>SEO content writing is creating web pages, blog posts and product copy that answer what people search for, in a way Google can understand and customers want to read.</strong> Good SEO content earns rankings, builds trust and moves readers to act.</p>
<p>At RankRight Media, our writers research the keywords and questions behind every brief, study what already ranks, and then write something clearer, more useful and more on-brand. Every piece is edited, checked for originality and formatted with the headings, internal links and meta data it needs to perform.</p>
<h2>What content can you write?</h2>
<p>Blog posts and long-form guides, service and landing page copy, product and category descriptions, email newsletters and social media captions — in your brand’s tone of voice, from a friendly local café to a technical B2B supplier.</p>
""",
    "checklist": ["Keyword & Topic Research", "SEO Blog Posts & Guides", "Website & Landing Page Copy", "Product & Category Descriptions", "Brand Tone of Voice Matching", "Meta Titles & Descriptions", "Internal Linking Suggestions", "Plagiarism-Checked Originals", "Social Media Captions", "Proofread & Publish-Ready"],
    "features": [("i-pen", "Blog Posts & Articles", "#includes"), ("i-monitor", "Website Copy", "#includes"), ("i-cart", "Product Descriptions", "#includes"), ("i-search", "Keyword-Led Briefs", "#includes"), ("i-message", "Social Captions", "#includes")],
    "facts": [("Service", "SEO content writing"), ("Formats", "Blogs, web pages, product descriptions, social captions"), ("Included", "Keyword research, meta data, internal link suggestions"), ("Quality", "Human-written, edited and plagiarism-checked"), ("Pricing", "Per piece or monthly content plans — quoted on request")],
    "packages": {
        "heading": "Our Content Writing Packages", "unit": "one-off",
        "note": "One-off prices per order. Need content every month? Ask about the Custom Plan.",
        "items": [
            {"id": "cw-starter", "name": "Starter Pack", "price": 49, "tagline": "One page, done properly", "features": ["Up to 500 words", "1 Page (Website, Blog, or Product)", "SEO Optimization", "1 Revision", "Delivery in 3 Days"]},
            {"id": "cw-basic", "name": "Basic Boost", "price": 89, "tagline": "Two pages with keyword targeting", "features": ["Up to 1,000 words", "2 Pages", "Keyword Integration", "Meta Titles & Descriptions", "2 Revisions", "Delivery in 3–4 Days"]},
            {"id": "cw-standard", "name": "Standard Plan", "price": 149, "featured": True, "tagline": "Core website pages rewritten", "features": ["Up to 2,000 words", "3–4 Pages (Home, About, Services, etc.)", "SEO Optimization + Internal Linking", "Meta Tags & CTA Included", "3 Revisions", "Delivery in 5 Days"]},
            {"id": "cw-business", "name": "Business Pro", "price": 229, "tagline": "A full site of persuasive copy", "features": ["Up to 3,500 words", "5–7 Pages", "Advanced SEO + Competitor Research", "Content Strategy Advice", "Unlimited Revisions", "Delivery in 7 Days"]},
            {"id": "cw-ecommerce", "name": "Ecommerce Pack", "price": 399, "tagline": "Product copy that converts", "features": ["10 Product Descriptions", "Homepage + Category Page", "SEO-Friendly Copywriting", "Bullet Point Features", "Brand-Tone Matching", "Delivery in 7 Days"]},
            {"id": "cw-custom", "name": "Custom Plan", "price": 649, "tagline": "Ongoing content marketing", "features": ["Content strategy consultation", "Unlimited pages or blog posts", "Full content marketing plan", "Flexible word count & delivery time", "Ideal for long-term or ongoing work"]},
        ],
    },
    "process_heading": "Our Content Writing Process",
    "process": [
        ("i-search", "Research", "We research your keywords, audience questions and the pages already ranking for them."),
        ("i-clipboard", "Brief & Outline", "We agree a brief and outline so the structure and angle are right before writing starts."),
        ("i-pen", "Write & Edit", "Our writers produce original, on-brand copy that’s edited for clarity, accuracy and SEO."),
        ("i-rocket", "Optimise & Deliver", "You receive publish-ready content with meta data and internal link suggestions."),
    ],
    "panel": {"img": "strategy-session.webp", "alt": "RankRight Media content writers planning an article",
        "h2": "Content That Sounds Like You — and Ranks Like a Pro",
        "body": "<p>Generic content doesn’t rank and doesn’t convert. We learn your products, customers and tone so every piece reads like it came from inside your business, while quietly doing the SEO work: answering search intent, covering the topic fully and linking to the pages that matter.</p><p>The result is content your customers trust and Google wants to show — including in AI-generated answers, which favour clear, well-structured, expert content.</p>"},
    "includes_heading": "Our Content Writing Services Include",
    "includes": [
        ("i-pen", "SEO Blog Posts", "Researched articles and guides that target real search questions and build topical authority over time."),
        ("i-monitor", "Website Copy", "Clear, persuasive home, about and service pages that explain your value and guide visitors to get in touch."),
        ("i-cart", "Product Descriptions", "Benefit-led product and category copy that answers buyer questions and helps your store rank."),
        ("i-target", "Landing Page Copy", "Focused copy for ads and campaigns, written around a single offer and a single call to action."),
        ("i-message", "Social Media Captions", "Scroll-stopping captions that match your brand voice and keep your channels consistent."),
        ("i-search", "Content Audits & Refreshes", "We update underperforming pages with better structure, fresher information and stronger keyword targeting."),
    ],
    "includes_cta": "Get a quote",
    "testimonials": ["thomas-graham", "emma-clarke", "sophie-bennett"],
    "faqs": [
        ("What is SEO content writing?", "<p>SEO content writing is writing web pages, articles and product copy that answer what people search for and are structured so search engines can understand and rank them — while still being genuinely useful and persuasive for readers.</p>"),
        ("Do you use AI to write content?", "<p>Our content is written and edited by people. We may use tools for research and checks, but every piece is human-written, fact-checked, plagiarism-checked and edited to match your brand voice.</p>"),
        ("How much does SEO content writing cost?", "<p>We price per piece based on length and research depth, or as a monthly content plan. Content is also included in our SEO packages — for example, Premium SEO includes 4 articles a month. Contact us for a quote for your project.</p>"),
        ("Can you match my brand’s tone of voice?", "<p>Yes. We start from your existing content, brand guidelines and customer language, and refine the tone with your feedback on the first pieces.</p>"),
        ("Will you upload the content to my website?", "<p>We can. Content is delivered publish-ready with headings, meta titles, meta descriptions and internal link suggestions, and we can upload it to WordPress or Shopify for you on request.</p>"),
    ],
    "related": ["seo", "link-building", "social-media-marketing"],
}

SERVICES["ppc"] = {
    "slug": "ppc-pay-per-click",            # TODO: confirm WP URL slug
    "name": "PPC (Pay-Per-Click)",
    "short_name": "PPC",
    "menu_blurb": "Google Ads and paid social that pay back",
    "icon": "i-chart",
    "card": "Smart ad campaigns that bring instant traffic to your website through Google Ads and other platforms.",
    "card_points": ["Google Ads management", "Meta & TikTok ads", "Conversion tracking setup"],
    "service_type": "Pay-per-click advertising management",
    "title": "PPC Management Services UK | Google Ads & Paid Social",
    "description": "PPC management services for UK businesses: Google Ads, Meta and TikTok campaigns with proper conversion tracking, tight budgets and clear reporting on cost per lead.",
    "eyebrow": "PPC (pay-per-click)",
    "h1": "PPC Campaigns That Bring Instant, Profitable Traffic",
    "lead": "Smart ad campaigns that put you in front of ready-to-buy customers today — through Google Ads, Meta, TikTok and other platforms — with every pound tracked to a lead or a sale.",
    "visual": {"kind": "kpis", "label": "Campaign dashboard", "chip": "Tracked to revenue",
               "kpis": [("Clicks", "Up"), ("Cost / lead", "Down"), ("Conversions", "Up")]},
    "intro": """
<h2>PPC management services that focus on return, not clicks</h2>
<p><strong>PPC (pay-per-click) advertising means paying to appear at the top of Google, social feeds and other platforms, and only paying when someone clicks.</strong> Done well, it’s the fastest way to generate leads and sales; done badly, it burns budget.</p>
<p>At RankRight Media, we set up conversion tracking first, then build tightly themed campaigns around high-intent keywords and audiences. We write the ads, build or improve the landing pages and manage bids and budgets every week — so you can see exactly what each pound returns.</p>
<h2>Which ad platforms do you manage?</h2>
<p>We manage <strong>Google Ads</strong> (Search, Performance Max, Shopping and YouTube), <strong>Meta Ads</strong> (Facebook and Instagram), <strong>TikTok Ads</strong> and <strong>Microsoft Ads</strong>, choosing the mix that matches where your customers are and how they buy.</p>
""",
    "checklist": ["Google Ads Search & Shopping", "Performance Max Campaigns", "Facebook & Instagram Ads", "TikTok Ads", "Keyword & Audience Research", "Ad Copy & Creative Testing", "Conversion Tracking (GA4 & Pixels)", "Landing Page Optimisation", "Negative Keywords & Waste Control", "Clear Monthly Reporting"],
    "features": [("i-search", "Google Ads", "#includes"), ("i-users", "Meta & TikTok Ads", "#includes"), ("i-target", "Conversion Tracking", "#includes"), ("i-trend", "Bid & Budget Management", "#includes"), ("i-clipboard", "PPC Audits", "#includes")],
    "facts": [("Service", "PPC / paid ads management"), ("Platforms", "Google Ads, Meta, TikTok, Microsoft Ads"), ("Included", "Setup, tracking, ad copy, bid & budget management, reporting"), ("Ad spend", "Paid directly to the platform — you keep account ownership"), ("Pricing", "Monthly management fee — quoted on request")],
    "packages": {
        "heading": "Our PPC Management Packages", "unit": "/month",
        "note": "Management fees per month. Ad spend is paid directly to Google, Meta or TikTok and is not included. The PPC Audit is a one-off fee.",
        "items": [
            {"id": "ppc-audit", "name": "PPC Audit", "price": 99, "unit": "one-off", "tagline": "Find wasted spend in your account", "features": ["Full Google or Meta Ads account audit", "Wasted spend & search term review", "Conversion tracking check", "Prioritised action plan", "30-minute walkthrough call", "Delivery in 3–5 days"]},
            {"id": "ppc-starter", "name": "Starter PPC", "price": 249, "tagline": "Launch your first profitable campaign", "features": ["1 platform (Google Ads)", "Ad spend up to $2,000/month", "Up to 2 campaigns", "Keyword research & ad copy", "Conversion tracking setup", "Monthly performance report"]},
            {"id": "ppc-growth", "name": "Growth PPC", "price": 449, "featured": True, "tagline": "Search + social working together", "features": ["2 platforms (Google + Meta)", "Ad spend up to $5,000/month", "Up to 4 campaigns", "A/B ad copy & creative testing", "Landing page recommendations", "Bi-weekly optimisation", "Monthly performance report"]},
            {"id": "ppc-advanced", "name": "Advanced PPC", "price": 799, "tagline": "Multi-channel with retargeting", "features": ["3 platforms (Google, Meta, TikTok or Microsoft)", "Ad spend up to $10,000/month", "Up to 8 campaigns", "Remarketing & audience building", "Performance Max campaigns", "Weekly optimisation", "GA4 + pixel conversion tracking"]},
            {"id": "ppc-ecommerce", "name": "E-commerce PPC", "price": 1199, "tagline": "Shopping and ROAS-focused growth", "features": ["Google Shopping & Performance Max", "Product feed optimisation", "Dynamic remarketing", "Ad spend up to $20,000/month", "ROAS & revenue tracking", "Weekly performance report"]},
            {"id": "ppc-custom", "name": "Custom PPC", "price": None, "tagline": "High spend, multiple markets", "features": ["Unlimited ad spend & campaigns", "Multi-market & multi-language", "Dedicated PPC strategist", "Custom reporting dashboard", "Creative production support"]},
        ],
    },
    "process_heading": "Our PPC Process",
    "process": [
        ("i-clipboard", "Audit & Tracking", "We audit any existing accounts and set up accurate conversion tracking before spending a penny."),
        ("i-search", "Research & Build", "We research keywords, audiences and competitors and build focused campaigns and ads."),
        ("i-rocket", "Launch & Test", "We launch with controlled budgets and test ad copy, creatives and landing pages."),
        ("i-trend", "Optimise & Scale", "We cut waste weekly and scale what converts, reporting on cost per lead and return."),
    ],
    "panel": {"img": "strategy-session.webp", "alt": "RankRight Media PPC specialists analysing campaign results",
        "h2": "Every Pound Tracked, Every Click Accountable",
        "body": "<p>Most wasted ad spend comes from three things: broken tracking, broad targeting and slow, unfocused landing pages. We fix all three before we scale. You’ll always know your cost per lead, your conversion rate and what we’re changing next.</p><p>You keep ownership of your ad accounts and data. Ad spend goes directly to Google or Meta — our fee covers the expertise and the work.</p>"},
    "includes_heading": "Our PPC Services Include",
    "includes": [
        ("i-search", "Google Search Ads", "Text ads on high-intent searches, structured into tight ad groups with strong negative keyword lists."),
        ("i-cart", "Shopping & Performance Max", "Product feeds and Performance Max campaigns for e-commerce, optimised for return on ad spend."),
        ("i-users", "Facebook & Instagram Ads", "Audience-led campaigns with scroll-stopping creative for awareness, leads and sales."),
        ("i-zap", "TikTok Ads", "Native-feeling short-form video campaigns to reach new audiences fast."),
        ("i-clipboard", "PPC Audits", "A detailed review of your existing accounts to find wasted spend and quick wins."),
        ("i-target", "Landing Page Optimisation", "Faster, clearer landing pages matched to each ad so more clicks become customers."),
    ],
    "includes_cta": "Get a quote",
    "testimonials": ["mason-blake", "daniel-reid", "olivia-mason"],
    "faqs": [
        ("What is PPC management?", "<p>PPC management is the ongoing setup, monitoring and optimisation of pay-per-click ad campaigns — keyword and audience targeting, ad copy, bids, budgets, tracking and landing pages — to get the most leads or sales for your ad spend.</p>"),
        ("How much should I spend on Google Ads?", "<p>It depends on your industry’s cost per click and how many leads you need. We’ll estimate a realistic starting budget from keyword data during your free consultation, start controlled, and scale once campaigns are profitable.</p>"),
        ("Is the management fee separate from ad spend?", "<p>Yes. Ad spend is paid directly to the ad platform from your own account. Our monthly management fee covers strategy, setup, optimisation and reporting.</p>"),
        ("How quickly will I see results from PPC?", "<p>Ads can start generating clicks and enquiries within days of launch. Campaigns usually become significantly more efficient over the first <strong>4–8 weeks</strong> as we gather data and optimise.</p>"),
        ("Should I do PPC or SEO?", "<p>PPC brings immediate traffic while you pay for it; SEO builds traffic that compounds over time. Many clients run both: PPC for instant leads and keyword data, SEO to lower long-term acquisition costs.</p>"),
    ],
    "related": ["seo", "social-media-marketing", "website-development"],
}

SERVICES["social-media-marketing"] = {
    "slug": "social-media-marketing",       # TODO: confirm WP URL slug
    "name": "Social Media Marketing",
    "short_name": "Social Media",
    "menu_blurb": "Content and campaigns people engage with",
    "icon": "i-target",
    "card": "Build your presence on platforms like Facebook, Instagram, and LinkedIn with engaging posts and promotions.",
    "card_points": ["Content calendars & posting", "Community management", "Paid social campaigns"],
    "service_type": "Social media marketing",
    "title": "Social Media Marketing Services UK | RankRight Media",
    "description": "Social media marketing services for UK businesses: content creation, posting, community management and paid campaigns on Instagram, Facebook, LinkedIn and TikTok.",
    "eyebrow": "Social media marketing",
    "h1": "Social Media Marketing That Builds a Loyal Audience",
    "lead": "Build your presence on platforms like Facebook, Instagram, LinkedIn and TikTok with engaging posts and promotions — planned, created and managed for you.",
    "visual": {"kind": "bars", "label": "Social growth", "chip": "Organic + paid",
               "bars": [("Reach", "w-84"), ("Engagement", "w-78"), ("Followers", "w-70"), ("Website clicks", "w-62")]},
    "intro": """
<h2>Social media marketing services for growing brands</h2>
<p><strong>Social media marketing is using platforms such as Instagram, Facebook, LinkedIn and TikTok to build brand awareness, engage your audience and drive traffic, leads and sales.</strong> It combines consistent organic content with targeted paid promotion.</p>
<p>At RankRight Media, we plan a content calendar around your goals, create on-brand graphics, short videos and captions, publish consistently and engage with your community. When you’re ready to accelerate, we add paid social campaigns that reach the right people.</p>
<h2>Which platforms should my business be on?</h2>
<p>The ones your customers actually use. B2B brands usually see the best return on <strong>LinkedIn</strong>; consumer brands on <strong>Instagram</strong>, <strong>TikTok</strong> and <strong>Facebook</strong>. We’ll recommend a focused mix rather than spreading you thinly across everything.</p>
""",
    "checklist": ["Social Media Strategy", "Content Calendars", "Graphics & Short-Form Video", "Captions & Hashtag Research", "Scheduling & Posting", "Community Management", "Facebook & Instagram Ads", "LinkedIn for B2B", "TikTok Content", "Monthly Analytics Reports"],
    "features": [("i-clipboard", "Strategy & Calendars", "#includes"), ("i-pen", "Content Creation", "#includes"), ("i-message", "Community Management", "#includes"), ("i-mega", "Paid Social Ads", "#includes"), ("i-chart", "Analytics & Reporting", "#includes")],
    "facts": [("Service", "Social media marketing & management"), ("Platforms", "Instagram, Facebook, LinkedIn, TikTok"), ("Included", "Strategy, content creation, posting, community management"), ("Add-on", "Paid social campaigns"), ("Pricing", "Monthly plans — quoted on request")],
    "packages": {
        "heading": "Our Social Media Monthly Packages", "unit": "/month",
        "note": "Prices are per month. Ad spend for paid campaigns is paid directly to the platform.",
        "items": [
            {"id": "smm-basic", "name": "Basic", "price": 199, "tagline": "One platform, consistently", "features": ["1 Platform (e.g., Facebook or Instagram)", "8 Posts/Month", "1 Campaign/Month", "Basic targeting", "Basic community management", "Monthly Overview", "Email Support"]},
            {"id": "smm-standard", "name": "Standard", "price": 399, "featured": True, "tagline": "Two platforms working together", "features": ["2 Platforms (e.g., Facebook and Instagram)", "16 Posts/Month", "2 Campaigns/Month", "Advanced targeting", "Intermediate community management", "Email & Chat Support"]},
            {"id": "smm-advanced", "name": "Advanced", "price": 599, "tagline": "Add LinkedIn and retargeting", "features": ["3 Platforms (e.g., Facebook, Instagram, LinkedIn)", "24 Posts/Month", "3 Campaigns/Month", "Advanced + Retargeting", "Advanced community management", "Email, Chat & Phone Support"]},
            {"id": "smm-pro", "name": "Pro", "price": 799, "tagline": "Four platforms, proactive growth", "features": ["4 Platforms (e.g., Facebook, Instagram, LinkedIn, X)", "30 Posts/Month", "5 Campaigns/Month", "Premium + Retargeting", "Advanced + Proactive Community Management", "Dedicated Account Rep"]},
            {"id": "smm-premium", "name": "Premium", "price": 1199, "tagline": "Five platforms incl. TikTok", "features": ["5 Platforms (e.g., Facebook, Instagram, LinkedIn, X, TikTok)", "40 Posts/Month", "7 Campaigns/Month", "Full Targeting Options", "Full Community Management", "Dedicated Account Rep"]},
            {"id": "smm-enterprise", "name": "Enterprise", "price": 1699, "tagline": "Every major platform, always on", "features": ["6+ Platforms (all major incl. YouTube and Pinterest)", "60+ Posts/Month", "10+ Campaigns/Month", "Full Targeting + AI", "Full 24/7 Engagement Management", "Daily + Custom Reports", "24/7 Dedicated Support"]},
        ],
    },
    "process_heading": "Our Social Media Process",
    "process": [
        ("i-search", "Audit & Strategy", "We review your channels and competitors and set goals, platforms and content pillars."),
        ("i-clipboard", "Plan", "We build a monthly content calendar for your approval before anything goes live."),
        ("i-pen", "Create & Publish", "We design posts, write captions and publish on schedule across your platforms."),
        ("i-chart", "Engage & Report", "We manage comments and messages and report on growth, engagement and clicks."),
    ],
    "panel": {"img": "team-collaboration.webp", "alt": "RankRight Media social media team reviewing content on a tablet",
        "h2": "Consistent, On-Brand and Built to Convert",
        "body": "<p>Posting randomly doesn’t grow a brand. We build a plan around content pillars your audience cares about, keep your look and voice consistent, and connect your social activity to your website so followers become customers.</p><p>Every month you’ll see what performed, what we learned and what we’re doing next.</p>"},
    "includes_heading": "Our Social Media Services Include",
    "includes": [
        ("i-clipboard", "Social Media Strategy", "Clear goals, target audiences, platform choices and content pillars to guide everything we post."),
        ("i-pen", "Content Creation", "On-brand graphics, carousels, short videos and captions designed to stop the scroll."),
        ("i-clock", "Scheduling & Posting", "Consistent publishing at the times your audience is most active."),
        ("i-message", "Community Management", "Timely replies to comments and messages to build relationships and protect your reputation."),
        ("i-mega", "Paid Social Campaigns", "Targeted Facebook, Instagram, LinkedIn and TikTok ads to grow reach, leads and sales."),
        ("i-chart", "Analytics & Reporting", "Monthly reports on reach, engagement, follower growth and website traffic from social."),
    ],
    "includes_cta": "Get a quote",
    "testimonials": ["thomas-graham", "olivia-mason", "harper-lane"],
    "faqs": [
        ("What do social media marketing services include?", "<p>Typically strategy, content planning, graphic and video creation, captions, scheduling, community management and monthly reporting, with optional paid social advertising to accelerate growth.</p>"),
        ("How often should my business post on social media?", "<p>Consistency matters more than volume. For most small businesses, <strong>3–5 quality posts a week</strong> on one or two core platforms outperforms daily low-effort posting everywhere.</p>"),
        ("Do you buy followers or use bots?", "<p>No. We grow audiences with real content and targeted advertising only. Bought followers damage engagement rates and can get accounts restricted.</p>"),
        ("How long before social media marketing shows results?", "<p>Engagement often improves within the first month of consistent posting. Sustainable follower growth and traffic usually builds over <strong>3–6 months</strong>; paid campaigns can speed this up.</p>"),
        ("Can you run ads on Facebook and Instagram for us?", "<p>Yes. We plan, create and manage Facebook and Instagram ad campaigns, set up the Meta Pixel and conversion tracking, and report on cost per result.</p>"),
    ],
    "related": ["content-writing", "ppc", "seo"],
}

SERVICE_ORDER = ["website-development", "content-writing", "ppc", "link-building", "seo", "social-media-marketing"]  # SOURCE: WP menu/footer order

# --------------------------------------------------------------------------------------------
# Home page FAQ — NEW (answer-first, written for AI overviews and featured snippets)
# --------------------------------------------------------------------------------------------
HOME_FAQS = [
    ("What does RankRight Media do?", "<p>RankRight Media is a UK-based digital marketing agency offering <a href=\"/search-engine-optimization/\">SEO</a>, <a href=\"/link-building-services/\">link building</a>, <a href=\"/website-development/\">website development</a>, <a href=\"/content-writing/\">content writing</a>, <a href=\"/ppc-pay-per-click/\">PPC advertising</a> and <a href=\"/social-media-marketing/\">social media marketing</a> — all under one roof, with clear packages and monthly reporting.</p>"),
    ("How much does SEO cost with RankRight Media?", "<p>Monthly SEO packages start at <strong>$299/month</strong> (Basic SEO) and run to <strong>$1,899/month</strong> (E-commerce SEO), with a Custom SEO plan for larger projects. Link building packages start from <strong>$3.49</strong>.</p>"),
    ("How do I get started?", "<p>Choose a package, check out securely, then complete a short form about your business, goals and preferences. Our team starts work straight away and keeps you updated at every step. Prefer to talk first? Call <a href=\"tel:+447446254421\">+44 7446 254421</a>.</p>"),
    ("Do you work with small businesses?", "<p>Yes. We work with everyone from local shops and start-ups to national brands. Our packages are designed so small businesses can start affordably and scale up as results come in.</p>"),
    ("Are your SEO and link building methods safe?", "<p>Yes. We use white-hat methods that follow Google’s guidelines: manual outreach, real niche-relevant websites and genuinely useful content. No link farms, no automated spam.</p>"),
    ("Will I get reports on progress?", "<p>Yes. Every SEO client receives a clear monthly report on rankings, traffic and what we did; E-commerce SEO clients get weekly reports with ROI tracking. Link building orders include a placement report with live URLs.</p>"),
]


# General FAQs — SOURCE: WP /faq/ page (questions verbatim; answers expanded)
GENERAL_FAQS = [
    ("What digital marketing services do you offer?", "<p>We offer a full range of services including SEO, PPC (pay-per-click), social media marketing, link building, website development and content writing — all customised to suit your business goals, in the UK and internationally.</p>"),
    ("Are your services suitable for small businesses in the UK?", "<p>Yes. Our packages start small — content from $49, link building from $3.49 and SEO from $299/month — so start-ups and local businesses can begin affordably and scale as results come in.</p>"),
    ("How long does it take to see SEO results?", "<p>Most websites see first ranking movements within 4–8 weeks of on-page and technical fixes. Meaningful traffic and lead growth usually builds over 3–6 months, depending on competition and how many keywords you target.</p>"),
    ("What makes your PPC services different?", "<p>We set up accurate conversion tracking before spending a penny, build tightly themed campaigns around high-intent keywords and audiences, and report on cost per lead and return — not just clicks. You keep ownership of your ad accounts.</p>"),
    ("Can I choose only one service, like Social Media Marketing?", "<p>Absolutely. Every service has its own packages, so you can buy just social media marketing, just SEO or just content. Many clients start with one service and add others later.</p>"),
    ("Do you work with clients outside the UK?", "<p>Yes. We’re based in Ilford, England and work with businesses worldwide. Prices are shown in US dollars and all communication and reporting happens online.</p>"),
]
