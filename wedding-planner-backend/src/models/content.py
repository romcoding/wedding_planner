from src.models import db
from datetime import datetime

class Content(db.Model):
    """Content model for managing wedding information displayed to guests"""
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)  # e.g., 'welcome_message', 'venue_info'
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(50), default='text')  # text, html, markdown
    is_public = db.Column(db.Boolean, default=True)  # Visible to guests
    order = db.Column(db.Integer, default=0)  # For ordering on public page
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert content to dictionary"""
        return {
            'id': self.id,
            'key': self.key,
            'title': self.title,
            'content': self.content,
            'content_type': self.content_type,
            'is_public': self.is_public,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

