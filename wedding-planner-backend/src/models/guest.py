from src.models import db
from datetime import datetime

class Guest(db.Model):
    """Guest model for wedding registration"""
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    # Primary guest information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20))
    
    # RSVP information
    rsvp_status = db.Column(db.String(20), default='pending')  # pending, confirmed, declined
    attendance_type = db.Column(db.String(20))  # ceremony, reception, both
    number_of_guests = db.Column(db.Integer, default=1)  # Including plus-ones
    
    # Dietary and special requirements
    dietary_restrictions = db.Column(db.Text)  # JSON string or comma-separated
    allergies = db.Column(db.Text)
    special_requests = db.Column(db.Text)
    
    # Additional information
    address = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Metadata
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_accessed = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert guest to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'rsvp_status': self.rsvp_status,
            'attendance_type': self.attendance_type,
            'number_of_guests': self.number_of_guests,
            'dietary_restrictions': self.dietary_restrictions,
            'allergies': self.allergies,
            'special_requests': self.special_requests,
            'address': self.address,
            'notes': self.notes,
            'registered_at': self.registered_at.isoformat() if self.registered_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }

