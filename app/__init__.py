import africastalking
from flask import  Flask, jsonify, request
from config import Config
from app.extensions import db, migrate, bcrypt, jwt, scheduler, mail, cors

#Import Models
from app.models.hospital_model import Hospital
from app.models.donor_model import Donor
from app.models.blood_request_model import BloodRequest
from app.models.donation_record_model import DonationRecord
from app.models.donor_match_model import DonorMatch
from app.models.notification_model import Notification

# Import controllers (blueprints) for each module
from app.controllers.hospital_controller import hospital_bp
from app.controllers.donor_controller import donor_bp
from app.controllers.blood_request_controller import blood_request_bp
from app.controllers.donation_records_controller import donation_blueprint
from app.controllers.donor_match_controller import donor_match_bp
from app.controllers.notification_controller import notification_blueprint


def create_app():
    """Flask application factory"""
    app = Flask(__name__)

# Load the configuration
    app.config.from_object(Config)  # Th
    

    db.init_app(app) 
    migrate.init_app(app, db)  
    cors.init_app(app)
    
    # Register Blueprints with appropriate URL prefixes
    app.register_blueprint(donor_bp, url_prefix='/api/v1/donors')
    app.register_blueprint(hospital_bp, url_prefix='/api/v1/hospitals')
    app.register_blueprint(blood_request_bp, url_prefix='/api/v1/bloodrequests')
    app.register_blueprint(donor_match_bp, url_prefix='/api/v1/donormatches')
    app.register_blueprint(notification_blueprint, url_prefix='/api/v1/notifications')
    app.register_blueprint(donation_blueprint ,url_prefix='/api/v1/donation')
   
    
    # Initialize Africa's Talking SDK
    africastalking.initialize(username='livewell_medical_app', api_key='atsk_c6f2d52c6f637e9ff0183d8d802dc7b9771902b4009ed1dfdba398c1b4370c6e8565eece')
    sms = africastalking.SMS

    # Function to send SMS
    def send_sms(phone_number, message):
        try:
            response = sms.send(message, [phone_number])
            return response
        except Exception as e:
            return {'error': str(e)}


    #Route to send SMS
    @app.route('/send-sms', methods=['POST'])
    def send_sms_route():
        data = request.get_json()
        phone_number = data.get('phone_numbers')
        message = data.get('message')
        
        if not phone_number or not message:
            return jsonify({'error': 'Phone numbers and messages are required'}), 400

        responses = []
        for number in phone_number:
            response = send_sms(number, message)
            responses.append({'number': number, 'response': response})

        return jsonify({'status': 'SMS sent', 'details': responses}), 200

    

    # Define the home route
    @app.route('/')
    def home():
        return "Hello, World!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
