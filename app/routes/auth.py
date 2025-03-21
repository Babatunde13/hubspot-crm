from flask import Blueprint, request, jsonify
from app.services.auth import AuthService
from app.services.user import UserService
from app.logger import Logger
from app.validation.validator import RegisterSchema, LoginSchema
from app.services.hubspot import hubspot_service

auth_bp = Blueprint("auth", __name__)
logger = Logger('AuthRouter')

@auth_bp.route("/register", methods=["POST"])
def register():
    body = request.get_json()
    errors = RegisterSchema().validate(body)
    if errors:
        logger.error("Validation error", errors)
        return jsonify(errors), 400

    data = RegisterSchema().get_user_data(body)
    password = data.pop("password")
    contact_response = hubspot_service.create_or_update_contact(data)
    if "error" in contact_response:
        logger.error(contact_response["error"], contact_response)
        return jsonify({"error": "Failed to create account" }), 500

    data["contact_id"] = contact_response["data"]
    response = AuthService.register_user(**data, password=password)
    if "error" in response:
        logger.error(response["error"], response)
        return jsonify(response), 400

    return jsonify(response), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    errors = LoginSchema().validate(data)
    if errors:
        logger.error("Validation error", errors)
        return jsonify(errors), 400
    response = AuthService.authenticate_user(data["email"], data["password"])
    if "error" in response:
        logger.error(response["error"], response)
        return jsonify(response), 401
    return jsonify(response)
