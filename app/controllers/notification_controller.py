from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from app.models.notification_model import Notification
from app.models.donor_model import Donor
from app.models.blood_request_model import BloodRequest
from app.models.donor_match_model import DonorMatch
from app import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound, BadRequest

# Define the Blueprint for handling notifications
notification_blueprint = Blueprint('notification_blueprint', __name__, url_prefix='/api/v1/notifications')

# GET all notifications
@notification_blueprint.route('/', methods=['GET'])
def get_notifications():
    try:
        notifications = Notification.query.all()
        return jsonify([notification.to_dict() for notification in notifications]), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error occurred'}), 500

# GET a specific notification by ID
@notification_blueprint.route('/<int:id>', methods=['GET'])
def get_notification(id):
    try:
        notification = Notification.query.get(id)
        if not notification:
            raise NotFound('Notification not found')
        return jsonify(notification.to_dict()), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error occurred'}), 500

# POST a new notification
@notification_blueprint.route('/', methods=['POST'])
def create_notification():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest('No input data provided')
        
        required_fields = ['donor_id', 'message']
        for field in required_fields:
            if field not in data:
                raise BadRequest(f'Missing required field: {field}')
        
        donor = Donor.query.get(data['donor_id'])
        if not donor:
            raise NotFound('Donor not found')
            
        new_notification = Notification(
            donor_id=data['donor_id'],
            request_id=data.get('request_id'),
            message=data['message'],
            status='Pending'
        )
        
        # Send SMS using Africa's Talking API
        recipient = donor.phone
        response = current_app.sms.send(new_notification.message, [recipient])
        
        # Update status based on SMS response
        if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
            new_notification.status = 'Sent'
        else:
            new_notification.status = 'Failed'
            
        db.session.add(new_notification)
        db.session.commit()
            
        return jsonify(new_notification.to_dict()), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        return jsonify({'error': f'SMS sending failed: {str(e)}'}), 500

# PUT to update an existing notification
@notification_blueprint.route('/<int:id>', methods=['PUT'])
def update_notification(id):
    try:
        data = request.get_json()
        if not data:
            raise BadRequest('No input data provided')
        
        notification = Notification.query.get(id)
        if not notification:
            raise NotFound('Notification not found')
            
        if 'message' in data:
            notification.message = data['message']
        if 'status' in data:
            notification.status = data['status']
            
        db.session.commit()
        return jsonify(notification.to_dict()), 200
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

# DELETE a notification by ID
@notification_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_notification(id):
    try:
        notification = Notification.query.get(id)
        if not notification:
            raise NotFound('Notification not found')
            
        db.session.delete(notification)
        db.session.commit()
        return jsonify({'message': 'Notification deleted successfully'}), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

# Notify a donor about a match (with automatic SMS)
@notification_blueprint.route('/notify-match/<int:match_id>', methods=['POST'])
def notify_match(match_id):
    try:
        match = DonorMatch.query.get(match_id)
        if not match:
            raise NotFound('Donor match not found')
            
        donor = Donor.query.get(match.donor_id)
        blood_request = BloodRequest.query.get(match.request_id)
        
        if not donor or not blood_request:
            raise NotFound('Donor or blood request not found')
            
        # Create message
        message = f"Hello {donor.name}, you have been matched with a blood request. " \
                  f"Blood type needed: {blood_request.blood_type}, " \
                  f"Urgency: {blood_request.urgency_level}. " \
                  f"Please respond if you can donate."
        
        # Create notification record
        new_notification = Notification(
            donor_id=donor.id,
            request_id=blood_request.id,
            message=message,
            status='Pending'
        )
        
        # Send SMS using Africa's Talking API
        # recipient = donor.phone
        recipient = f'+256{donor.phone[1:]}'  # Converts '0771234567' to '+256771234567'

        response = current_app.sms.send(message, [recipient])
        
        # Update status based on response
        if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
            new_notification.status = 'Sent'
            match.status = 'Notified'
            match.notified_at = datetime.utcnow()
        else:
            new_notification.status = 'Failed'
            
        db.session.add(new_notification)
        db.session.commit()
        
        return jsonify(new_notification.to_dict()), 201
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'SMS sending failed: {str(e)}'}), 500

# Batch notify all donors for a specific blood request
@notification_blueprint.route('/batch-notify-request/<int:request_id>', methods=['POST'])
def batch_notify_request(request_id):
    try:
        blood_request = BloodRequest.query.get(request_id)
        if not blood_request:
            raise NotFound('Blood request not found')
            
        pending_matches = DonorMatch.query.filter_by(
            request_id=request_id,
            status='Pending'
        ).all()
        
        if not pending_matches:
            return jsonify({'message': 'No pending matches to notify'}), 200
            
        notifications_sent = 0
        notifications_failed = 0
        
        for match in pending_matches:
            donor = Donor.query.get(match.donor_id)
            if not donor:
                continue
                
            message = f"Hello {donor.name}, you have been matched with a blood request. " \
                      f"Blood type needed: {blood_request.blood_type}, " \
                      f"Urgency: {blood_request.urgency_level}. " \
                      f"Please respond if you can donate."
            
            new_notification = Notification(
                donor_id=donor.id,
                request_id=blood_request.id,
                message=message,
                status='Pending'
            )
            
            recipient = donor.phone
            response = current_app.sms.send(message, [recipient])
            
            if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
                new_notification.status = 'Sent'
                match.status = 'Notified'
                match.notified_at = datetime.utcnow()
                notifications_sent += 1
            else:
                new_notification.status = 'Failed'
                notifications_failed += 1
                
            db.session.add(new_notification)
            
        db.session.commit()
        
        return jsonify({
            'message': f'Sent {notifications_sent} notifications, {notifications_failed} failed',
            'request_id': request_id
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'SMS sending failed: {str(e)}'}), 500