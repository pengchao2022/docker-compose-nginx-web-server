from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

# 这里导入routes并注册路由
# 注意：必须在app创建后导入
from .routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)