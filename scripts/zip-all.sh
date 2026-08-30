#!/usr/bin/env bash
# ForgeKit packaging script — builds one .zip per product plus forgekit-complete.zip.
# Usage: ./scripts/zip-all.sh
# Output: dist/<slug>.zip for each product, dist/forgekit-complete.zip with everything.
# Excludes .venv/ and __pycache__/ (and other build junk) from every zip.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PRODUCTS_DIR="$ROOT_DIR/products"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

echo "ForgeKit packaging — building product zips into $DIST_DIR"
echo ""

for product_path in "$PRODUCTS_DIR"/*/; do
  product_name="$(basename "$product_path")"
  # Strip the leading "NN-" ordering prefix for the zip filename, e.g. 01-forge-notes -> forge-notes.zip
  slug="${product_name#*-}"
  zip_path="$DIST_DIR/${slug}.zip"

  echo "  -> ${product_name}  =>  dist/${slug}.zip"
  (cd "$product_path" && zip -rq "$zip_path" . -x "*.DS_Store" -x "__pycache__/*" -x "*.pyc" -x ".venv/*")
done

echo ""
echo "Building forgekit-complete.zip (all products + packaging docs)..."
COMPLETE_STAGE="$DIST_DIR/.complete-stage"
rm -rf "$COMPLETE_STAGE"
mkdir -p "$COMPLETE_STAGE/ForgeKit-Complete"
cp -R "$PRODUCTS_DIR" "$COMPLETE_STAGE/ForgeKit-Complete/products"
cp -R "$ROOT_DIR/packaging" "$COMPLETE_STAGE/ForgeKit-Complete/packaging"
cp -R "$ROOT_DIR/brand" "$COMPLETE_STAGE/ForgeKit-Complete/brand"

# Drop any venvs/pycache that snuck into a product folder before zipping.
find "$COMPLETE_STAGE/ForgeKit-Complete" -type d \( -name "__pycache__" -o -name ".venv" \) -exec rm -rf {} + 2>/dev/null || true

(cd "$COMPLETE_STAGE" && zip -rq "$DIST_DIR/forgekit-complete.zip" "ForgeKit-Complete" \
  -x "*.DS_Store" -x "__pycache__/*" -x "*.pyc" -x ".venv/*")

rm -rf "$COMPLETE_STAGE"

echo ""
echo "Done. Files ready for Gumroad upload:"
ls -lh "$DIST_DIR"
