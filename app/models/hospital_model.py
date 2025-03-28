from datetime import datetime
from app.extensions import db

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))  # Optional GPS coordinates
    contact_number = db.Column(db.String(20), nullable=False)

    blood_requests = db.relationship('BloodRequest', backref='hospital', lazy=True)
    def __repr__(self):
        return f"Hospital('{self.name}', '{self.city}', '{self.location}', '{self.contact_number}')"
    
    # Method to convert the object to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'location': self.location,
            'contact_number': self.contact_number
        }