# Fabs Data Warehouse

All-in-one platform for payments, biometrics, bulk payouts, county revenue collection,
tender tracking, petroleum transportation, company management, merchant onboarding
and DHL-partnered logistics tracking.

## Stack
- **Backend:** Flask 3 · SQLAlchemy 2 · Flask-Login · Flask-WTF · Flask-Limiter
- **Frontend:** Tailwind CSS (CDN) · inline CSS/JS · glassmorphic dark UI
- **Payments:** M-Pesa · DPO · Pesapal · Finserve
- **Logistics:** DHL (official partner) · Fleetbase
- **Biometrics:** Pay-off API
- **Core banking:** Mifos / Fineract · TransFi
- **county payments. Elgeyo Marakwet intergration for payments.**
## Quick start

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then edit SECRET_KEY and integration keys

flask --app app init-db           # create tables
flask --app app seed-db           # seed admin@fabsdata.io / ChangeMe123!

python app.py                     # http://localhost:5000
# FABS Data Warehouse — FABS Trading brand update

This patch updates the supplied homepage, base template and shared CSS to the white-and-red FABS Trading identity. Data Warehouse remains the product name; FABS Trading Global E-Commerce is the company brand.

## Install

1. Back up your current `templates/base.html`, `templates/index.html` and `static/css/style.css`.
2. Copy this package's `templates` and `static` folders into your existing Flask project, merging the directories and replacing those three files.
3. Include the entire supplied `static/images` folder. It contains the existing company logo, the homepage's original photographs, original provider artwork and a fallback illustration.
4. Keep your existing `app.py`, models, routes, credentials and `static/js/main.js`. This is a frontend patch, not a standalone Flask application.
5. Restart your application and refresh the browser with Ctrl+F5. The stylesheet link also includes a new version query to refresh cached CSS.

## What changed

- White navigation, page sections, cards and form fields; charcoal typography and red actions.
- FABS Trading's existing logo is used in the header and footer, with Data Warehouse shown as the product label.
- The corporate website is linked from the footer; the page metadata also identifies FABS Trading.
- Exact website accent: `#ED3138`. Accessible small text and primary buttons: `#C9252D`. Hover: `#AC1B23`.
- Brand colours are centralized under `:root` in `static/css/style.css`. The homepage reads these shared tokens. The Tailwind brand configuration in `base.html` uses the same values.
- Existing Tailwind names such as `brand-green`, and legacy CSS tokens such as `--fabs-cyan`, remain aliases to the red palette for compatibility with other templates. Provider colours and success/warning states keep their own meanings.
- Original photos and provider logos were extracted from the supplied embedded images into reusable static assets. Off-screen images now load lazily.
- Fixed malformed Markdown-wrapped asset URLs from the supplied base template.
- Shared image fallbacks, keyboard-accessible mobile navigation and clearly labelled flash messages are included in `base.html`.
- Existing endpoint names, contact fields and CSRF handling are preserved. Homepage carousel, payout sample and fingerprint/iris sample interactions remain in `index.html`.

## Scope

Only the supplied frontend files were available. Validate the patch in your complete Flask app before deploying, especially any page-specific styles or behaviours in your existing `main.js`. Other templates may still contain their own hard-coded dark backgrounds or white text and can be updated in a later pass.

The biometric and payout panels are demonstrations already present in the supplied homepage. They do not collect biometric data or send payments. Provider integration and account activation remain server-side.

The separate HTML preview is a portable visual preview. Navigation to other application routes and enquiry submission are disabled in that preview; the actual Flask templates retain their normal links and form submission.

## Asset sources

- FABS company identity and unchanged logo: https://www.fabstrading.com/ and https://www.fabstrading.com/static/images/fabs-brand-v2.png
- Original Pexels photo links and provider artwork sources remain documented at the end of `templates/index.html`.
- No new photos or replacement company logos were generated.

## Checks completed

The supplied templates rendered with strict Jinja validation for anonymous, member and administrator contexts, including flash messages. Shared and inline CSS parsed successfully.

A headless Chromium check found no horizontal overflow at 320, 390, 768, 1024, 1280 and 1440 pixels, no broken local images, and no JavaScript exceptions. Carousel navigation, payout and iris demos, mobile navigation, Escape, flash dismissal and the logo fallback were exercised. Contact field constraints, POST target and CSRF field were retained.

The homepage and shared shell were also checked with external CDN requests unavailable. This does not test the real application backend, provider services or your existing main.js.
