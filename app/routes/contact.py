from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.logger import Logger
from app.validation.validator import SearchUsersSchema, DealSchema, TicketSchema
from app.services.hubspot import hubspot_service
from app.services.user import UserService

contacts_bp = Blueprint("contacts", __name__)
logger = Logger('ContactRouter')

# use jwt_required_int() decorator, create a decorator that gets the id from get_jwt_identity() and convert it to an integer
# if the conversion fails, return a 401 response with a message "Invalid token"
# if the user id is valid, call the function and return the response
def jwt_required_int():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user_id = int(get_jwt_identity())
            except ValueError:
                return jsonify({"error": "Invalid token"}), 401
            return f(user_id, *args, **kwargs)
        return wrapper
    return decorator

@contacts_bp.route("/new-crm-objects", methods=["GET"])
@jwt_required()
def search():
    schema = SearchUsersSchema()
    errors = schema.validate(request.args)
    if errors:
        return jsonify(errors), 400

    data = schema.load(request.args)
    cursor = data.get("cursor")
    limit = data.get("limit")
    contacts = hubspot_service.get_contacts(limit, cursor)

    return jsonify({
        "message": "Contacts retrieved successfully",
        "data": contacts
    }), 200

@contacts_bp.route("/deals", methods=["POST"])
@jwt_required()
@jwt_required_int()
def create_deal(user_id: int):
    body = request.get_json()
    errors = DealSchema().validate(body)
    if errors:
        logger.error("Validation error", errors)
        return jsonify(errors), 400

    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    contact_id = user.contact_id
    data = DealSchema().load(body)
    data["dealstage"] = data["dealstage"].value
    response = hubspot_service.create_or_update_deal(contact_id, data["dealname"], data)
    if "error" in response:
        logger.error(response["error"], response)
        return jsonify(response), 400

    return jsonify(response), 201

@contacts_bp.route("/tickets/<deal_id>", methods=["POST"])
@jwt_required()
@jwt_required_int()
def create_ticket(user_id: int, deal_id: int):
    body = request.get_json()
    errors = TicketSchema().validate(body)
    if errors:
        logger.error("Validation error", errors)
        return jsonify(errors), 400

    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    contact_id = user.contact_id
    data = TicketSchema().load(body)
    data["category"] = data["category"].value
    response = hubspot_service.create_ticket(contact_id, deal_id, data)
    if "error" in response:
        logger.error(response["error"], response)
        return jsonify(response), 400

    return jsonify(response), 201
