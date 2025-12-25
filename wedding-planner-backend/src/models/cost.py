from src.models import db
from datetime import datetime

class Cost(db.Model):
    """Cost model for wedding budget tracking"""
    __tablename__ = 'costs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # venue, catering, decoration, etc.
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='planned')  # planned, paid, pending
    payment_date = db.Column(db.Date)
    vendor = db.Column(db.String(200))
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('costs', lazy=True))
    
    def to_dict(self):
        """Convert cost to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'amount': float(self.amount),
            'status': self.status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'vendor': self.vendor,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

