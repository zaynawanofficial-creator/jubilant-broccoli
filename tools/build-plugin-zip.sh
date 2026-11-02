#!/usr/bin/env bash
# Builds dist/seo-booster-core.zip for upload via wp-admin → Plugins → Add New → Upload.
set -euo pipefail
cd "$(dirname "$0")/.."
cp SERVICE_CATALOG.csv wp-content/plugins/seo-booster-core/data/SERVICE_CATALOG.csv
for f in $(find wp-content/plugins/seo-booster-core -name '*.php'); do php -l "$f" >/dev/null; done
mkdir -p dist && rm -f dist/seo-booster-core.zip
(cd wp-content/plugins && zip -qr ../../dist/seo-booster-core.zip seo-booster-core -x '*.DS_Store')
echo "Built dist/seo-booster-core.zip"
