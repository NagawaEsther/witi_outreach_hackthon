from datetime import datetime
from app.extensions import db

class DonationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    donated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensures donors don’t donate too frequently (e.g., every 8 weeks)
    next_eligible_donation = db.Column(db.DateTime, nullable=False)
    
    # Method to return a dictionary representation of the object
    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'hospital_id': self.hospital_id,
            'blood_type': self.blood_type,
            'donated_at': self.donated_at.isoformat() if self.donated_at else None,
            'next_eligible_donation': self.next_eligible_donation.isoformat() if self.next_eligible_donation else None,
        }
