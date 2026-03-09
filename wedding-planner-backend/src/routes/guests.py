from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Guest, User, Invitation, GuestPhoto, SeatAssignment, Message, PageView, Visit, ReminderSent
from datetime import datetime
import json
import logging
import csv
import io
import os
from src.utils.rbac import require_roles

guests_bp = Blueprint('guests', __name__)
logger = logging.getLogger(__name__)

def _safe_int(value, default, minimum=1, maximum=1000):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(min(parsed, maximum), minimum)

@guests_bp.route('/update-rsvp', methods=['PUT'])
@jwt_required()
def update_rsvp():
    """Update RSVP information (guest authenticated via token)"""
    # Enforce RSVP deadline
    if datetime.now() > datetime(2026, 4, 30, 23, 59, 59):
        return jsonify({'error': 'RSVP changes are no longer possible after 30 April 2026.'}), 403

    identity = get_jwt_identity()
    
    if not identity:
        return jsonify({'error': 'Unauthorized - No token provided'}), 403
    
    identity_str = str(identity)
    if not identity_str.startswith('guest_'):
        return jsonify({'error': 'Unauthorized - Guest token required'}), 403
    
    try:
        guest_id = int(identity_str.split('_')[1])
    except (ValueError, IndexError):
        return jsonify({'error': 'Invalid token format'}), 403
    
    guest = Guest.query.get(guest_id)
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    data = request.get_json()
    
    # Update RSVP fields
    if 'first_name' in data:
        guest.first_name = (data.get('first_name') or '').strip() or guest.first_name
    if 'last_name' in data:
        guest.last_name = (data.get('last_name') or '').strip() or guest.last_name
    if 'email' in data:
        email = (data.get('email') or '').strip()
        if email:
            existing = Guest.query.filter(
                Guest.email == email,
                Guest.id != guest.id
            ).first()
            if existing:
                return jsonify({'error': 'Email already in use by another guest'}), 400
        # Keep email optional here so guests can add it later.
        guest.email = email
    if 'rsvp_status' in data:
        guest.rsvp_status = data['rsvp_status']
    if 'overnight_stay' in data:
        guest.overnight_stay = bool(data['overnight_stay'])
    if 'number_of_guests' in data:
        guest.number_of_guests = data['number_of_guests']
    if 'attending_names' in data:
        # Accept list of names; store JSON. Also sync number_of_guests to attending count when confirmed.
        names = data.get('attending_names')
        if names is None:
            guest.attending_names = None
        elif isinstance(names, list):
            cleaned = [str(x).strip() for x in names if str(x).strip()]
            invitees = guest.get_invitee_names()
            if invitees:
                allowed = {n for n in invitees}
                cleaned = [n for n in cleaned if n in allowed]
            guest.attending_names = json.dumps(cleaned)
            if guest.rsvp_status == 'confirmed':
                guest.number_of_guests = len(cleaned)
    if 'dietary_restrictions' in data:
        guest.dietary_restrictions = data['dietary_restrictions']
    if 'allergies' in data:
        guest.allergies = data['allergies']
    if 'special_requests' in data:
        guest.special_requests = data['special_requests']
    if 'music_wish' in data:
        guest.music_wish = data['music_wish']
    if 'phone' in data:
        guest.phone = data['phone']
    if 'address' in data:
        guest.address = data['address']
    
    guest.updated_at = datetime.utcnow()
    guest.last_accessed = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'RSVP updated successfully',
        'guest': guest.to_dict(include_sensitive=False)
    }), 200

@guests_bp.route('', methods=['POST'])
@jwt_required()
def create_guest():
    """Create a new guest (admin/planner) - generates unique token"""
    user, err = require_roles(['admin', 'planner'])
    if err:
        return err
    
    data = request.get_json()
    
    if not data or not data.get('first_name') or not data.get('last_name'):
        return jsonify({'error': 'First name and last name are required'}), 400
    
    # Generate unique token
    unique_token = Guest.generate_unique_token()
    # Ensure uniqueness
    while Guest.query.filter_by(unique_token=unique_token).first():
        unique_token = Guest.generate_unique_token()
    
    email = (data.get('email') or '').strip()
    # Email is optional at creation; generate an internal placeholder
    # so admins can add the real email later.
    if not email:
        email = f"guest-{unique_token[:16]}@placeholder.local"
    else:
        existing_guest = Guest.query.filter_by(email=email).first()
        if existing_guest:
            return jsonify({'error': 'Guest with this email already exists'}), 400

    invitee_names = data.get('invitee_names')
    invitee_json = None
    if isinstance(invitee_names, list):
        cleaned = [str(x).strip() for x in invitee_names if str(x).strip()]
        if cleaned:
            invitee_json = json.dumps(cleaned)

    # Create guest with all admin-provided info
    guest = Guest(
        email=email,
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        unique_token=unique_token,
        rsvp_status=data.get('rsvp_status', 'pending'),
        overnight_stay=data.get('overnight_stay', False),
        number_of_guests=data.get('number_of_guests', 1),
        invitee_names=invitee_json,
        dietary_restrictions=data.get('dietary_restrictions'),
        allergies=data.get('allergies'),
        special_requests=data.get('special_requests'),
        music_wish=data.get('music_wish'),
        address=data.get('address'),
        notes=data.get('notes'),
        language=data.get('language', 'en')
    )
    
    db.session.add(guest)
    db.session.commit()
    
    # Refresh to get the guest with all fields
    db.session.refresh(guest)
    
    # Get frontend URL for the unique link
    import os
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    rsvp_link = f"{frontend_url}/rsvp/{guest.unique_token}"
    
    # Build guest dict with rsvp_link included
    guest_dict = guest.to_dict(include_sensitive=True)
    guest_dict['rsvp_link'] = rsvp_link
    
    return jsonify({
        'message': 'Guest created successfully',
        'guest': guest_dict,
        'rsvp_link': rsvp_link
    }), 201

@guests_bp.route('', methods=['GET'])
@jwt_required()
def get_guests():
    """Get guests (admin/planner) with pagination to avoid oversized payloads."""
    user, err = require_roles(['admin', 'planner'])
    if err:
        return err
    
    # Filtering options
    rsvp_status = request.args.get('rsvp_status')
    overnight_stay = request.args.get('overnight_stay')
    
    query = Guest.query
    
    if rsvp_status:
        query = query.filter_by(rsvp_status=rsvp_status)
    if overnight_stay is not None:
        query = query.filter_by(overnight_stay=overnight_stay.lower() == 'true')
    
    page = _safe_int(request.args.get('page', 1), default=1, minimum=1, maximum=100000)
    per_page = _safe_int(request.args.get('per_page', 100), default=100, minimum=1, maximum=500)
    pagination = query.order_by(Guest.registered_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    guests = pagination.items
    
    # Include RSVP links for admin
    import os
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    guests_data = []
    for guest in guests:
        guest_dict = guest.to_dict(include_sensitive=True)
        # Generate token if missing (for backward compatibility)
        if not guest.unique_token:
            guest.unique_token = Guest.generate_unique_token()
            # Ensure uniqueness
            while Guest.query.filter_by(unique_token=guest.unique_token).filter(Guest.id != guest.id).first():
                guest.unique_token = Guest.generate_unique_token()
            db.session.commit()
        guest_dict['rsvp_link'] = f"{frontend_url}/rsvp/{guest.unique_token}" if guest.unique_token else None
        guests_data.append(guest_dict)
    
    response = jsonify(guests_data)
    response.headers['X-Total-Count'] = str(pagination.total)
    response.headers['X-Page'] = str(page)
    response.headers['X-Per-Page'] = str(per_page)
    response.headers['X-Has-More'] = 'true' if pagination.has_next else 'false'
    return response, 200

@guests_bp.route('/export', methods=['GET'])
@jwt_required()
def export_guests():
    """Export guests as CSV (admin/planner)."""
    user, err = require_roles(['admin', 'planner'])
    if err:
        return err

    rsvp_status = request.args.get('rsvp_status')
    overnight_stay = request.args.get('overnight_stay')

    query = Guest.query
    if rsvp_status:
        query = query.filter_by(rsvp_status=rsvp_status)
    if overnight_stay is not None:
        query = query.filter_by(overnight_stay=overnight_stay.lower() == 'true')

    guests = query.order_by(Guest.registered_at.desc()).all()

    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    tokens_generated = False

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'language',
        'rsvp_status',
        'number_of_guests',
        'overnight_stay',
        'invitee_names',
        'attending_names',
        'dietary_restrictions',
        'allergies',
        'special_requests',
        'music_wish',
        'address',
        'notes',
        'registered_at',
        'updated_at',
        'last_accessed',
        'rsvp_link',
    ])

    for guest in guests:
        if not guest.unique_token:
            guest.unique_token = Guest.generate_unique_token()
            while Guest.query.filter_by(unique_token=guest.unique_token).filter(Guest.id != guest.id).first():
                guest.unique_token = Guest.generate_unique_token()
            tokens_generated = True

        invitee_names = ', '.join(guest.get_invitee_names())
        attending_names = ', '.join(guest.get_attending_names())
        rsvp_link = f"{frontend_url}/rsvp/{guest.unique_token}" if guest.unique_token else ''

        writer.writerow([
            guest.id,
            guest.first_name or '',
            guest.last_name or '',
            guest.email or '',
            guest.phone or '',
            guest.language or '',
            guest.rsvp_status or '',
            guest.number_of_guests or '',
            'Yes' if guest.overnight_stay else 'No',
            invitee_names,
            attending_names,
            guest.dietary_restrictions or '',
            guest.allergies or '',
            guest.special_requests or '',
            guest.music_wish or '',
            guest.address or '',
            guest.notes or '',
            guest.registered_at.isoformat() if guest.registered_at else '',
            guest.updated_at.isoformat() if guest.updated_at else '',
            guest.last_accessed.isoformat() if guest.last_accessed else '',
            rsvp_link,
        ])

    if tokens_generated:
        db.session.commit()

    csv_bytes = output.getvalue().encode('utf-8-sig')
    buffer = io.BytesIO(csv_bytes)
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='text/csv; charset=utf-8',
        as_attachment=True,
        download_name='wedding_guests.csv',
    )

@guests_bp.route('/token/<token>', methods=['GET'])
def get_guest_by_token(token):
    """Get guest by unique token (public endpoint for RSVP link)"""
    guest = Guest.query.filter_by(unique_token=token).first()
    
    if not guest:
        return jsonify({'error': 'Invalid RSVP link'}), 404
    
    # Update last accessed
    guest.last_accessed = datetime.utcnow()
    db.session.commit()
    
    return jsonify(guest.to_dict(include_sensitive=False)), 200

@guests_bp.route('/token/<token>/auth', methods=['POST'])
def authenticate_with_token(token):
    """Authenticate guest using unique token and return JWT (public endpoint)"""
    guest = Guest.query.filter_by(unique_token=token).first()
    
    if not guest:
        return jsonify({'error': 'Invalid RSVP link'}), 404
    
    # Update last accessed
    guest.last_accessed = datetime.utcnow()
    db.session.commit()
    
    # Generate JWT token
    from flask_jwt_extended import create_access_token
    access_token = create_access_token(identity=f"guest_{guest.id}")
    
    return jsonify({
        'access_token': access_token,
        'guest': guest.to_dict(include_sensitive=False)
    }), 200

@guests_bp.route('/<int:guest_id>', methods=['GET'])
@jwt_required()
def get_guest(guest_id):
    """Get specific guest details (admin/planner)"""
    user, err = require_roles(['admin', 'planner'])
    if err:
        return err
    
    guest = Guest.query.get(guest_id)
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    # Include RSVP link
    import os
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    guest_dict = guest.to_dict(include_sensitive=True)
    # Generate token if missing
    if not guest.unique_token:
        guest.unique_token = Guest.generate_unique_token()
        # Ensure uniqueness
        while Guest.query.filter_by(unique_token=guest.unique_token).filter(Guest.id != guest.id).first():
            guest.unique_token = Guest.generate_unique_token()
        db.session.commit()
    guest_dict['rsvp_link'] = f"{frontend_url}/rsvp/{guest.unique_token}" if guest.unique_token else None
    
    return jsonify(guest_dict), 200

@guests_bp.route('/<int:guest_id>', methods=['PUT'])
@jwt_required()
def update_guest(guest_id):
    """Update guest information (admin/planner)"""
    user, err = require_roles(['admin', 'planner'])
    if err:
        return err
    
    guest = Guest.query.get(guest_id)
    
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'first_name' in data:
        guest.first_name = data['first_name']
    if 'last_name' in data:
        guest.last_name = data['last_name']
    if 'email' in data:
        email = (data.get('email') or '').strip()
        if email:
            existing_guest = Guest.query.filter(
                Guest.email == email,
                Guest.id != guest.id
            ).first()
            if existing_guest:
                return jsonify({'error': 'Guest with this email already exists'}), 400
            guest.email = email
    if 'phone' in data:
        guest.phone = data['phone']
    if 'rsvp_status' in data:
        guest.rsvp_status = data['rsvp_status']
    if 'overnight_stay' in data:
        guest.overnight_stay = bool(data['overnight_stay'])
    if 'number_of_guests' in data:
        guest.number_of_guests = data['number_of_guests']
    if 'dietary_restrictions' in data:
        guest.dietary_restrictions = data['dietary_restrictions']
    if 'allergies' in data:
        guest.allergies = data['allergies']
    if 'special_requests' in data:
        guest.special_requests = data['special_requests']
    if 'music_wish' in data:
        guest.music_wish = data['music_wish']
    if 'address' in data:
        guest.address = data['address']
    if 'notes' in data:
        guest.notes = data['notes']
    if 'language' in data:
        guest.language = data['language']
    if 'invitee_names' in data:
        names = data.get('invitee_names')
        if names is None:
            guest.invitee_names = None
        elif isinstance(names, list):
            cleaned = [str(x).strip() for x in names if str(x).strip()]
            guest.invitee_names = json.dumps(cleaned) if cleaned else None
            # If attending_names exists, ensure it's still a subset of invitees
            attending = guest.get_attending_names()
            if attending:
                allowed = set(cleaned)
                attending = [n for n in attending if n in allowed]
                guest.attending_names = json.dumps(attending)
                if guest.rsvp_status == 'confirmed':
                    guest.number_of_guests = len(attending)
    
    guest.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(guest.to_dict()), 200

@guests_bp.route('/<int:guest_id>', methods=['DELETE'])
@jwt_required()
def delete_guest(guest_id):
    """Delete guest (admin/planner)"""
    user, err = require_roles(['admin', 'planner'])
    if err:
        return err
    
    guest = Guest.query.get(guest_id)
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404

    # IMPORTANT:
    # Production can be behind migrations (e.g., invitations missing scheduled_at).
    # Avoid ORM access to models that may not match DB columns by using raw SQL here.
    try:
        from sqlalchemy import text

        db.session.execute(text("UPDATE invitations SET guest_id = NULL WHERE guest_id = :gid"), {"gid": guest_id})
        db.session.execute(text("UPDATE seat_assignments SET guest_id = NULL WHERE guest_id = :gid"), {"gid": guest_id})
        db.session.execute(text("DELETE FROM guest_photos WHERE guest_id = :gid"), {"gid": guest_id})
        db.session.execute(text("DELETE FROM reminder_sent WHERE guest_id = :gid"), {"gid": guest_id})
        db.session.execute(text("UPDATE messages SET guest_id = NULL WHERE guest_id = :gid"), {"gid": guest_id})
        db.session.execute(text("UPDATE page_views SET guest_id = NULL WHERE guest_id = :gid"), {"gid": guest_id})
        db.session.execute(text("UPDATE visits SET guest_id = NULL WHERE guest_id = :gid"), {"gid": guest_id})

        # Finally delete the guest row itself (raw delete avoids ORM lazy-loads)
        db.session.execute(text("DELETE FROM guests WHERE id = :gid"), {"gid": guest_id})
        db.session.commit()
        return jsonify({'message': 'Guest deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.exception("Failed to delete guest %s", guest_id)
        return jsonify({'error': f'Failed to delete guest: {str(e)}'}), 500

