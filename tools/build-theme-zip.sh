#!/usr/bin/env bash
# Builds dist/seo-booster-theme.zip (Appearance → Themes → Add New → Upload Theme).
# Regenerates art + page patterns first so the zip always matches tools/*.py.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build_art.py >/dev/null
(cd tools && python3 build_patterns.py >/dev/null)
for f in $(find wp-content/themes/seo-booster -name '*.php'); do php -l "$f" >/dev/null; done
python3 -c "import json;json.load(open('wp-content/themes/seo-booster/theme.json'))"
mkdir -p dist && rm -f dist/seo-booster-theme.zip
(cd wp-content/themes && zip -qr ../../dist/seo-booster-theme.zip seo-booster -x '*.DS_Store')
echo "Built dist/seo-booster-theme.zip"
