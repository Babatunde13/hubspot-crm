from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.logger import Logger
from app.validation.validator import SearchUsersSchema
from app.services.hubspot import hubspot_service

contacts_bp = Blueprint("contacts", __name__)
logger = Logger('ContactRouter')

@contacts_bp.route("", methods=["GET"])
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

@contacts_bp.route("/pipelines", methods=["GET"])
@jwt_required()
def get_tickets():
    tickets = hubspot_service.get_pipeline_tickets()
    return jsonify({
        "message": "Pipeline tickets retrieved successfully",
        "data": tickets
    }), 200
