# Horus website

Static site built on the brand. `index.html` is written in the Claude artifact form (no document skeleton); `build-standalone.sh` wraps it into `dist/index.html` for hosting on any static host (Netlify, Vercel, GitHub Pages, S3).

Positioning (27 October 2026, from the founder's review): Horus is a technology company whose AI runs policy engagements for governments end to end. The site never calls the company "Horus Advisory" or "Policy Advisory", never mentions human supervision, approvals or AI disclosure, names no third-party frameworks, and shows Horus deciding with its decision record. Engagements start from a scope-of-work document, not a question; both forms accept a scope document.

Before hosting:

1. In `site.js`, set `FORM_ENDPOINT` to a form service URL that accepts multipart posts with a file (the forms send the text fields plus `scope_file`), and `CONTACT` to the company's address for the copy-and-send fallback. In the artifact preview the forms store requests in the page's private database instead: a scope file up to 160 KB is stored inline, a larger one is recorded by name and size.
2. Replace the illustrative engagement codes, names and figures in `site.js` and `index.html` if you prefer other examples.
3. Run `sh build-standalone.sh` and upload `dist/`.

No tracking, no cookies, no third-party scripts; fonts come from Google Fonts.
