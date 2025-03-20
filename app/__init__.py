from flask import Flask
from app.extensions import db, jwt, migrate
from app.routes.auth import auth_bp
from app.logger import Logger
from app.routes.contact import contacts_bp
from app.config import config

def create_app():
    logger = Logger("App")
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(contacts_bp, url_prefix="/contacts")

    @app.errorhandler(404)
    def not_found(error):
        logger.error("Resource not found", error)
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error("Internal server error", error)
        return {"error": "Internal server error"}, 500
    
    @app.errorhandler(405)
    def bad_request(error):
        logger.error("Method not allowed", error)
        return {"error": "Method not allowed"}, 405
    
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return {"error": "Missing or invalid JWT"}, 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        return {"error": "Invalid token"}, 401

    return app
