#!/bin/sh
# Wraps the artifact-form index.html into a complete HTML document for static hosting.
cd "$(dirname "$0")" && mkdir -p dist dist/assets && cp styles.css site.js dist/ && cp assets/*.svg dist/assets/ 2>/dev/null
{
  printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<link rel="icon" href="assets/horus-mark-small-gold.svg" type="image/svg+xml">\n'
  # title, description and font links from the source head
  grep -E '^<(title|meta name="description"|link rel="(preconnect|stylesheet)")' index.html
  printf '</head>\n<body style="margin:0">\n'
  grep -vE '^<(title|meta name=|link rel=)' index.html
  printf '</body>\n</html>\n'
} > dist/index.html
echo "built dist/index.html ($(wc -c < dist/index.html) bytes)"
