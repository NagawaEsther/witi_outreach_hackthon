from flask import Blueprint, request, jsonify
from app.models.donation_record_model import DonationRecord
from app import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound, BadRequest
from datetime import datetime

# Define Blueprint for the donor controller
donation_blueprint = Blueprint('donor_record', __name__)

# POST a new donation record
@donation_blueprint.route('/donors', methods=['POST'])
def create_donor():
    try:
        data = request.get_json()  # Get JSON data from the request
        if not data:
            raise BadRequest('No input data provided')

        # Validate incoming data
        required_fields = ['donor_id', 'hospital_id', 'blood_type', 'next_eligible_donation']
        for field in required_fields:
            if field not in data:
                raise BadRequest(f'Missing required field: {field}')
        
        # Create a new donation record
        new_donor = DonationRecord(
            donor_id=data['donor_id'],
            hospital_id=data['hospital_id'],
            blood_type=data['blood_type'],
            next_eligible_donation=datetime.strptime(data['next_eligible_donation'], '%Y-%m-%dT%H:%M:%S')  # Convert to datetime
        )
        
        db.session.add(new_donor)
        db.session.commit()  # Commit the transaction
        
        return jsonify(new_donor.to_dict()), 201  # Return the new donor record as JSON
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400  # Handle bad request error
    except SQLAlchemyError:
        db.session.rollback()  # Rollback in case of DB error
        return jsonify({'error': 'Database error occurred'}), 500  # Handle DB error
