from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import db, User, DesignCase, Designer, Service, Appointment, Review, BlogPost

# 从app模块导入app实例
from .app import app

# 辅助函数
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 认证路由
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['username', 'email', 'password', 'full_name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        full_name=data['full_name'],
        phone=data.get('phone')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # 创建访问令牌
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 验证必填字段
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # 创建访问令牌
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200

# 设计案例路由
@app.route('/api/cases', methods=['GET'])
def get_cases():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    style = request.args.get('style')
    featured = request.args.get('featured', type=bool)
    
    query = DesignCase.query
    
    if style:
        query = query.filter_by(style=style)
    if featured is not None:
        query = query.filter_by(featured=featured)
    
    try:
        pagination = query.order_by(DesignCase.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        cases = [case.to_dict() for case in pagination.items]
        
        return jsonify({
            'cases': cases,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    case = DesignCase.query.get(case_id)
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    return jsonify(case.to_dict()), 200

@app.route('/api/cases', methods=['POST'])
@jwt_required()
def create_case():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # 验证必填字段
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    # 创建案例
    case = DesignCase(
        title=data['title'],
        description=data.get('description'),
        style=data.get('style'),
        area=data.get('area'),
        budget=data.get('budget'),
        duration=data.get('duration'),
        location=data.get('location'),
        cover_image=data.get('cover_image'),
        images=data.get('images', []),
        featured=data.get('featured', False),
        status=data.get('status', 'completed'),
        user_id=current_user_id
    )
    
    try:
        db.session.add(case)
        db.session.commit()
        
        return jsonify({
            'message': 'Case created successfully',
            'case': case.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 设计师路由
@app.route('/api/designers', methods=['GET'])
def get_designers():
    try:
        designers = Designer.query.all()
        return jsonify([designer.to_dict() for designer in designers]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/designers/<int:designer_id>', methods=['GET'])
def get_designer(designer_id):
    designer = Designer.query.get(designer_id)
    if not designer:
        return jsonify({'error': 'Designer not found'}), 404
    return jsonify(designer.to_dict()), 200

# 服务路由
@app.route('/api/services', methods=['GET'])
def get_services():
    try:
        services = Service.query.all()
        return jsonify([service.to_dict() for service in services]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 预约路由
@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['client_name', 'client_phone']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # 解析日期
    preferred_date = None
    if data.get('preferred_date'):
        try:
            preferred_date = datetime.strptime(data['preferred_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # 创建预约
    appointment = Appointment(
        client_name=data['client_name'],
        client_phone=data['client_phone'],
        client_email=data.get('client_email'),
        service_type=data.get('service_type'),
        project_type=data.get('project_type'),
        budget_range=data.get('budget_range'),
        preferred_date=preferred_date,
        preferred_time=data.get('preferred_time'),
        message=data.get('message'),
        assigned_to=data.get('assigned_to')
    )
    
    try:
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment': appointment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 评价路由
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    case_id = request.args.get('case_id', type=int)
    designer_id = request.args.get('designer_id', type=int)
    
    query = Review.query
    
    if case_id:
        query = query.filter_by(case_id=case_id)
    if designer_id:
        query = query.filter_by(designer_id=designer_id)
    
    try:
        reviews = query.order_by(Review.created_at.desc()).limit(20).all()
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reviews', methods=['POST'])
@jwt_required()
def create_review():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # 验证必填字段
    if not data.get('rating') or not data.get('comment'):
        return jsonify({'error': 'Rating and comment are required'}), 400
    
    # 验证评分范围
    rating = data['rating']
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
    
    # 创建评价
    review = Review(
        case_id=data.get('case_id'),
        user_id=current_user_id,
        designer_id=data.get('designer_id'),
        rating=rating,
        comment=data['comment'],
        images=data.get('images', [])
    )
    
    try:
        db.session.add(review)
        
        # 更新设计师评分
        if data.get('designer_id'):
            designer = Designer.query.get(data['designer_id'])
            if designer:
                # 重新计算平均评分
                reviews = Review.query.filter_by(designer_id=designer.id).all()
                total_rating = sum(r.rating for r in reviews)
                avg_rating = total_rating / len(reviews) if reviews else 0
                designer.rating = round(avg_rating, 2)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 博客路由
@app.route('/api/blog/posts', methods=['GET'])
def get_blog_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tag = request.args.get('tag')
    
    query = BlogPost.query.filter_by(published=True)
    
    if tag:
        query = query.filter(BlogPost.tags.like(f'%{tag}%'))
    
    try:
        pagination = query.order_by(BlogPost.published_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        posts = [post.to_dict() for post in pagination.items]
        
        return jsonify({
            'posts': posts,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blog/posts/<slug>', methods=['GET'])
def get_blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    try:
        # 增加浏览次数
        post.view_count += 1
        db.session.commit()
        
        return jsonify(post.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 统计数据路由
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        total_cases = DesignCase.query.count()
        total_designers = Designer.query.count()
        completed_cases = DesignCase.query.filter_by(status='completed').count()
        total_appointments = Appointment.query.count()
        
        return jsonify({
            'total_cases': total_cases,
            'total_designers': total_designers,
            'completed_cases': completed_cases,
            'total_appointments': total_appointments
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # 测试数据库连接
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# 根路由测试
@app.route('/api', methods=['GET'])
def api_index():
    return jsonify({
        'message': 'Interior Design API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'cases': '/api/cases',
            'designers': '/api/designers',
            'services': '/api/services',
            'appointments': '/api/appointments',
            'reviews': '/api/reviews',
            'blog': '/api/blog',
            'stats': '/api/stats',
            'health': '/api/health'
        }
    }), 200