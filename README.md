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

## Quick start

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then edit SECRET_KEY and integration keys

flask --app app init-db           # create tables
flask --app app seed-db           # seed admin@fabsdata.io / ChangeMe123!

python app.py                     # http://localhost:5000