#!/usr/bin/env bash
# ForgeKit packaging script — builds one .zip per product plus a mega-bundle zip.
# Usage: ./scripts/zip-all.sh
# Output: dist/<slug>.zip for each product, dist/forgekit-mega-bundle.zip with everything.

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
echo "Building mega-bundle (all products + packaging docs)..."
MEGA_STAGE="$DIST_DIR/.mega-stage"
rm -rf "$MEGA_STAGE"
mkdir -p "$MEGA_STAGE/ForgeKit-Mega-Bundle"
cp -R "$PRODUCTS_DIR" "$MEGA_STAGE/ForgeKit-Mega-Bundle/products"
cp -R "$ROOT_DIR/packaging" "$MEGA_STAGE/ForgeKit-Mega-Bundle/packaging"
cp -R "$ROOT_DIR/brand" "$MEGA_STAGE/ForgeKit-Mega-Bundle/brand"

(cd "$MEGA_STAGE" && zip -rq "$DIST_DIR/forgekit-mega-bundle.zip" "ForgeKit-Mega-Bundle" \
  -x "*.DS_Store" -x "__pycache__/*" -x "*.pyc" -x ".venv/*")

rm -rf "$MEGA_STAGE"

echo ""
echo "Done. Files ready for Gumroad upload:"
ls -lh "$DIST_DIR"
