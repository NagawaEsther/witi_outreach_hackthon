from datetime import datetime
from app.extensions import db
class DonorMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('blood_request.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    status = db.Column(db.Enum('Notified', 'Accepted', 'Rejected', 'Completed', name='match_status'), default='Notified')
    notified_at = db.Column(db.DateTime, default=datetime.utcnow)

    donor = db.relationship('Donor', backref='matches')
    request = db.relationship('BloodRequest', backref='matches')    
    
    def to_dict(self):
        return {
            'id': self.id,
            'request_id': self.request_id,
            'donor_id': self.donor_id,
            'status': self.status,
            'notified_at': self.notified_at.isoformat() if self.notified_at else None,
            'donor': self.donor.to_dict() if self.donor else None,  # assuming the Donor model also has a to_dict method
            'request': self.request.to_dict() if self.request else None  # assuming the BloodRequest model also has a to_dict method
        }