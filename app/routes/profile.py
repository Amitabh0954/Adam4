from flask import Blueprint, request, jsonify
from app.services.profile_service import ProfileService

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
profile_service = ProfileService()


@profile_bp.route('/update', methods=['POST'])
def update_profile():
    """Endpoint for updating user profile."""
    data = request.json
    response = profile_service.update_profile(data)
    return jsonify(response)
