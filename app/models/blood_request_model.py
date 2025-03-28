# from datetime import datetime
# from app.extensions import db

# class BloodRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     city = db.Column(db.String(50), nullable=False)
#     location = db.Column(db.String(100))  
#     contact_number = db.Column(db.String(20), nullable=False)
#     blood_type =db.Column(db.String(10) ,nullable=False)
#     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)


#     def __repr__(self):
#         return f'<BloodRequest {self.name}>'


from datetime import datetime
from app.extensions import db

class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))  # Optional GPS coordinates
    contact_number = db.Column(db.String(20), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)  # Blood type field
    urgency_level = db.Column(db.String(50), nullable=False)  # Urgency level (High/Medium/Low)
    status = db.Column(db.String(50), default='Open')  # Default status
    units_needed = db.Column(db.Integer, default=1)  # Default 1 unit of blood
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for request creation

    # Relationship to Hospital model
    # hospital = db.relationship('Hospital', backref=db.backref('blood_requests', lazy=True))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __repr__(self):
        return f"BloodRequest('{self.name}', '{self.city}', '{self.blood_type}', '{self.urgency_level}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'location': self.location,
            'contact_number': self.contact_number,
            'blood_type': self.blood_type,
            'urgency_level': self.urgency_level,
            'status': self.status,
            'units_needed': self.units_needed,
            'hospital_id': self.hospital_id,
            'created_at': self.created_at.isoformat(),  # ISO format for datetime
            'hospital_name': self.hospital.name  # Include hospital name from the relationship
        }
