from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    design_cases = db.relationship('DesignCase', backref='owner', lazy=True)
    blog_posts = db.relationship('BlogPost', backref='author', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)
    designer_profile = db.relationship('Designer', backref='user', uselist=False, lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class DesignCase(db.Model):
    __tablename__ = 'design_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    style = db.Column(db.String(50))
    area = db.Column(db.Numeric(8, 2))
    budget = db.Column(db.Numeric(12, 2))
    duration = db.Column(db.Integer)
    location = db.Column(db.String(200))
    cover_image = db.Column(db.String(500))
    _images = db.Column('images', db.Text)
    featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('planning', 'in_progress', 'completed'), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # 关系
    reviews = db.relationship('Review', backref='case', lazy=True)
    
    @property
    def images(self):
        if self._images:
            return json.loads(self._images)
        return []
    
    @images.setter
    def images(self, value):
        self._images = json.dumps(value) if value else '[]'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'style': self.style,
            'area': float(self.area) if self.area else None,
            'budget': float(self.budget) if self.budget else None,
            'duration': self.duration,
            'location': self.location,
            'cover_image': self.cover_image,
            'images': self.images,
            'featured': self.featured,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
        }

class Designer(db.Model):
    __tablename__ = 'designers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    title = db.Column(db.String(100))
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    specialization = db.Column(db.String(200))
    rating = db.Column(db.Numeric(3, 2), default=0)
    _portfolio_images = db.Column('portfolio_images', db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    appointments = db.relationship('Appointment', backref='designer', lazy=True)
    reviews = db.relationship('Review', backref='designer', lazy=True)
    
    @property
    def portfolio_images(self):
        if self._portfolio_images:
            return json.loads(self._portfolio_images)
        return []
    
    @portfolio_images.setter
    def portfolio_images(self, value):
        self._portfolio_images = json.dumps(value) if value else '[]'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'bio': self.bio,
            'experience_years': self.experience_years,
            'specialization': self.specialization.split(',') if self.specialization else [],
            'rating': float(self.rating) if self.rating else 0,
            'portfolio_images': self.portfolio_images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user': self.user.to_dict() if self.user else None,
        }

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price_range = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    icon = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price_range': self.price_range,
            'duration': self.duration,
            'icon': self.icon,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    client_email = db.Column(db.String(100))
    service_type = db.Column(db.String(100))
    project_type = db.Column(db.String(100))
    budget_range = db.Column(db.String(100))
    preferred_date = db.Column(db.Date)
    preferred_time = db.Column(db.String(50))
    message = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'confirmed', 'completed', 'cancelled'), default='pending')
    assigned_to = db.Column(db.Integer, db.ForeignKey('designers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_phone': self.client_phone,
            'client_email': self.client_email,
            'service_type': self.service_type,
            'project_type': self.project_type,
            'budget_range': self.budget_range,
            'preferred_date': self.preferred_date.isoformat() if self.preferred_date else None,
            'preferred_time': self.preferred_time,
            'message': self.message,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('design_cases.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    designer_id = db.Column(db.Integer, db.ForeignKey('designers.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    _images = db.Column('images', db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def images(self):
        if self._images:
            return json.loads(self._images)
        return []
    
    @images.setter
    def images(self, value):
        self._images = json.dumps(value) if value else '[]'
    
    def to_dict(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'user_id': self.user_id,
            'designer_id': self.designer_id,
            'rating': self.rating,
            'comment': self.comment,
            'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user': self.reviewer.to_dict() if self.reviewer else None,
        }

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cover_image = db.Column(db.String(500))
    tags = db.Column(db.String(500))
    view_count = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=True)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'content': self.content,
            'author_id': self.author_id,
            'cover_image': self.cover_image,
            'tags': self.tags.split(',') if self.tags else [],
            'view_count': self.view_count,
            'published': self.published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'author': self.author.to_dict() if self.author else None,
        }