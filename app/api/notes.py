from flask import Flask, jsonify, Blueprint, request
from app.services.notes import create_service, get_service, update_service, delete_service
from app.utils.token_auth import token_required

notes_bp = Blueprint("notes_bp", __name__)

@notes_bp.route("/", methods=["POST"])
@token_required
def create_note(user_id):
    data = request.get_json()
    notes = create_service(user_id, data)

    if "error" in notes:
        return jsonify(notes), 404
    return jsonify({"message":"Note Created!", "notes_id":notes["notes_id"]}), 201

@notes_bp.route("/", methods=["GET"])
@token_required
def get_note(user_id):
    notes = get_service(user_id)

    if "error" in notes:
        return jsonify(notes), 404
    return jsonify(notes), 200

@notes_bp.route("/<int:notes_id>", methods=["PUT"])
@token_required
def update_note(user_id, notes_id):
    data = request.get_json()
    notes = update_service(user_id, notes_id, data)

    if "error" in notes:
        return jsonify(notes), 404
    return jsonify({"message":"Note Updated!"}), 201

@notes_bp.route("/<int:notes_id>", methods=["DELETE"])
@token_required
def delete_note(user_id, notes_id):
    notes = delete_service(user_id, notes_id)

    if "error" in notes:
        return jsonify(notes), 404
    return jsonify({"message":"Note Deleted!"}), 201