-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS interior_design CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE interior_design;

-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 装修案例表
CREATE TABLE design_cases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    style VARCHAR(50), -- 装修风格：现代、简约、欧式等
    area DECIMAL(8,2), -- 面积
    budget DECIMAL(12,2), -- 预算
    duration INT, -- 工期（天）
    location VARCHAR(200), -- 位置
    cover_image VARCHAR(500),
    images TEXT, -- JSON格式存储多张图片
    featured BOOLEAN DEFAULT FALSE,
    status ENUM('planning', 'in_progress', 'completed') DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 设计师表
CREATE TABLE designers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    title VARCHAR(100), -- 职位/头衔
    bio TEXT, -- 简介
    experience_years INT, -- 经验年数
    specialization VARCHAR(200), -- 专长
    rating DECIMAL(3,2) DEFAULT 0,
    portfolio_images TEXT, -- JSON格式存储作品集图片
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 服务项目表
CREATE TABLE services (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price_range VARCHAR(100),
    duration VARCHAR(50),
    icon VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 预约表
CREATE TABLE appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_name VARCHAR(100) NOT NULL,
    client_phone VARCHAR(20) NOT NULL,
    client_email VARCHAR(100),
    service_type VARCHAR(100),
    project_type VARCHAR(100),
    budget_range VARCHAR(100),
    preferred_date DATE,
    preferred_time VARCHAR(50),
    message TEXT,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    assigned_to INT, -- 分配的设计师ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_to) REFERENCES designers(id) ON DELETE SET NULL
);

-- 评价表
CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    case_id INT,
    user_id INT,
    designer_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    images TEXT, -- JSON格式存储评价图片
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES design_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (designer_id) REFERENCES designers(id) ON DELETE CASCADE
);

-- 博客文章表
CREATE TABLE blog_posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    excerpt TEXT,
    content LONGTEXT,
    author_id INT,
    cover_image VARCHAR(500),
    tags VARCHAR(500),
    view_count INT DEFAULT 0,
    published BOOLEAN DEFAULT TRUE,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 插入初始数据
INSERT INTO services (name, description, price_range, duration, icon) VALUES
('室内设计咨询', '专业室内设计方案咨询，包括空间规划、风格选择等', '¥500-¥5000', '1-3天', 'design'),
('全包装修', '一站式装修服务，从设计到施工全程负责', '¥800-¥2000/平方米', '30-90天', 'construction'),
('局部改造', '厨房、卫生间等局部空间改造服务', '¥20000-¥100000', '15-45天', 'renovation'),
('软装设计', '家具、窗帘、灯具等软装搭配设计', '¥3000-¥30000', '7-14天', 'furniture'),
('智能家居集成', '智能灯光、安防、影音系统集成方案', '¥10000-¥100000', '7-30天', 'smart-home');

-- 创建默认管理员用户 (密码: Admin123!)
INSERT INTO users (username, email, password_hash, full_name, is_admin) VALUES
('admin', 'admin@interiordesign.com', '$2b$12$qwertyuiopasdfghjklzxcvbnm1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', '系统管理员', TRUE);

-- 创建示例设计师用户 (密码: Designer123!)
INSERT INTO users (username, email, password_hash, full_name, phone) VALUES
('designer_li', 'li.design@interiordesign.com', '$2b$12$qwertyuiopasdfghjklzxcvbnm1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', '李设计师', '13800138000'),
('designer_wang', 'wang.design@interiordesign.com', '$2b$12$qwertyuiopasdfghjklzxcvbnm1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', '王设计师', '13900139000');

INSERT INTO designers (user_id, title, bio, experience_years, specialization, rating) VALUES
(2, '首席设计师', '拥有10年室内设计经验，擅长现代简约风格和欧式古典风格', 10, '现代简约,欧式古典', 4.8),
(3, '高级设计师', '专注于小户型空间优化和智能家居设计', 7, '小户型设计,智能家居', 4.6);