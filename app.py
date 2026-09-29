# app.py
"""
Fabs Data Warehouse — all-in-one platform orchestration layer.
"""
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from config import config_map
from extensions import db, migrate, login_manager, csrf, limiter


def create_app(config_name: str | None = None) -> Flask:
    config_name = config_name or os.getenv("FLASK_ENV", "default")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_map.get(config_name, config_map["default"]))

    _init_extensions(app)
    _register_blueprints(app)
    _register_context(app)
    _register_health_routes(app)
    _register_error_handlers(app)
    _register_security_headers(app)
    _register_cli(app)

    app.logger.info("Fabs Data Warehouse initialised — env=%s", config_name)
    return app


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.path.startswith("/api/"):
            return jsonify({"error": "authentication_required"}), 401
        from flask import redirect, url_for, flash
        flash("Please sign in to continue.", "warning")
        return redirect(url_for("auth.login", next=request.path))


def _register_blueprints(app: Flask) -> None:
    from blueprints.main       import main_bp
    from blueprints.auth       import auth_bp
    from blueprints.dashboard  import dashboard_bp
    from blueprints.admin      import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,      url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp,     url_prefix="/admin")

    if app.config["ENABLE_PAYMENTS"]:
        from blueprints.payments import payments_bp
        app.register_blueprint(payments_bp, url_prefix="/payments")

    if app.config["ENABLE_BIOMETRICS"]:
        from blueprints.biometrics import biometrics_bp
        app.register_blueprint(biometrics_bp, url_prefix="/biometrics")

    if app.config["ENABLE_LOGISTICS"]:
        from blueprints.logistics import logistics_bp
        app.register_blueprint(logistics_bp, url_prefix="/logistics")

    if app.config["ENABLE_COUNTY"]:
        from blueprints.county import county_bp
        app.register_blueprint(county_bp, url_prefix="/county")

    if app.config["ENABLE_TENDERS"]:
        from blueprints.tenders import tenders_bp
        app.register_blueprint(tenders_bp, url_prefix="/tenders")

    from blueprints.companies import companies_bp
    from blueprints.merchants import merchants_bp
    app.register_blueprint(companies_bp, url_prefix="/companies")
    app.register_blueprint(merchants_bp, url_prefix="/merchants")


def _register_context(app: Flask) -> None:
    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.utcnow().year,
            "app_name": "Fabs Data Warehouse",
            "app_short": "FABS DATA",
            "partner": app.config["OFFICIAL_LOGISTICS_PARTNER"],
            "modules": {
                "payments":    app.config["ENABLE_PAYMENTS"],
                "biometrics":  app.config["ENABLE_BIOMETRICS"],
                "logistics":   app.config["ENABLE_LOGISTICS"],
                "county":      app.config["ENABLE_COUNTY"],
                "tenders":     app.config["ENABLE_TENDERS"],
                "petroleum":   app.config["ENABLE_PETROLEUM"],
            },
        }

    @app.template_filter("money")
    def money_filter(value, currency="KES"):
        try:
            return f"{currency} {float(value):,.2f}"
        except (TypeError, ValueError):
            return f"{currency} 0.00"

    @app.template_filter("shortdate")
    def shortdate_filter(value):
        if not value:
            return "—"
        return value.strftime("%d %b %Y, %H:%M")


def _register_health_routes(app: Flask) -> None:
    @app.get("/api/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            db_ok = True
        except Exception:
            db_ok = False
        return jsonify({
            "status": "ok" if db_ok else "degraded",
            "app": "Fabs Data Warehouse",
            "version": "0.1.0",
            "partner": app.config["OFFICIAL_LOGISTICS_PARTNER"],
            "modules": {
                "payments":   app.config["ENABLE_PAYMENTS"],
                "biometrics": app.config["ENABLE_BIOMETRICS"],
                "logistics":  app.config["ENABLE_LOGISTICS"],
                "county":     app.config["ENABLE_COUNTY"],
                "tenders":    app.config["ENABLE_TENDERS"],
                "petroleum":  app.config["ENABLE_PETROLEUM"],
            },
            "database": "up" if db_ok else "down",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        })


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(400)
    def bad_request(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "bad_request", "detail": str(e)}), 400
        return render_template("errors/400.html"), 400

    @app.errorhandler(401)
    def unauthorized(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "unauthorized"}), 401
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "forbidden"}), 403
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "not_found", "path": request.path}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(429)
    def rate_limited(e):
        return jsonify({"error": "rate_limited", "detail": str(e)}), 429

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        app.logger.exception("Unhandled server error: %s", e)
        if request.path.startswith("/api/"):
            return jsonify({"error": "internal_server_error"}), 500
        return render_template("errors/500.html"), 500


def _register_security_headers(app: Flask) -> None:
    @app.after_request
    def set_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Permissions-Policy", "geolocation=(self), microphone=(), camera=(self)"
        )
        return response


def _register_cli(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db():
        """Create all database tables."""
        db.create_all()
        print("Database tables created.")

    @app.cli.command("seed-db")
    def seed_db():
        """Seed demo admin + sample records."""
        from models import User, Company

        if User.query.filter_by(email="admin@fabsdata.io").first():
            print("Already seeded.")
            return

        company = Company(name="Fabs Data Warehouse", slug="fabs-data", industry="Fintech")
        db.session.add(company)
        db.session.flush()

        admin = User(
            email="admin@fabsdata.io",
            full_name="Fabs Administrator",
            company_name="Fabs Data Warehouse",
            role="admin",
            is_admin=True,
            company_id=company.id,
        )
        admin.set_password("ChangeMe123!")

        demo = User(
            email="demo@fabsdata.io",
            full_name="Demo Merchant",
            phone="712345678",
            country_code="+254",
            role="merchant",
            company_id=company.id,
        )
        demo.set_password("Demo12345!")

        db.session.add_all([admin, demo])
        db.session.commit()
        print("Seeded admin@fabsdata.io / ChangeMe123!")
        print("Seeded demo@fabsdata.io / Demo12345!")

    @app.cli.command("routes")
    def list_routes():
        """List every registered route."""
        for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
            methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
            print(f"{rule.endpoint:38s} {methods:18s} {rule}")


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])