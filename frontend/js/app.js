// API基础URL
const API_BASE_URL = 'http://localhost:5000/api';

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    // 加载服务项目
    loadServices();
    
    // 加载设计案例
    loadCases();
    
    // 加载设计师
    loadDesigners();
    
    // 设置筛选按钮事件
    setupFilterButtons();
    
    // 设置移动菜单
    setupMobileMenu();
    
    // 设置表单提交
    setupAppointmentForm();
});

// 加载服务项目
async function loadServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/services`);
        const services = await response.json();
        
        const container = document.getElementById('services-container');
        container.innerHTML = services.map(service => `
            <div class="service-card">
                <div class="service-icon">
                    <i class="fas fa-${service.icon || 'paint-roller'}"></i>
                </div>
                <h3>${service.name}</h3>
                <p>${service.description}</p>
                <p><strong>价格区间:</strong> ${service.price_range}</p>
                <p><strong>工期:</strong> ${service.duration}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('加载服务失败:', error);
        document.getElementById('services-container').innerHTML = 
            '<p class="error">加载服务失败，请稍后重试</p>';
    }
}

// 加载设计案例
let currentPage = 1;
let currentStyle = 'all';

async function loadCases(page = 1, style = 'all') {
    try {
        let url = `${API_BASE_URL}/cases?page=${page}&per_page=6`;
        if (style !== 'all') {
            url += `&style=${style}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        const container = document.getElementById('cases-container');
        
        if (page === 1) {
            container.innerHTML = '';
        }
        
        if (data.cases && data.cases.length > 0) {
            container.innerHTML += data.cases.map(designCase => `
                <div class="case-card">
                    <img src="${designCase.cover_image || 'images/default-case.jpg'}" 
                         alt="${designCase.title}" 
                         class="case-image">
                    <div class="case-content">
                        <h3>${designCase.title}</h3>
                        <p>${designCase.description?.substring(0, 100) || ''}...</p>
                        <div class="case-tags">
                            <span class="case-tag">${designCase.style || '现代'}</span>
                            <span class="case-tag">${designCase.area || '0'}㎡</span>
                            <span class="case-tag">${designCase.budget ? '¥' + designCase.budget : '面议'}</span>
                        </div>
                        <button class="btn-secondary" onclick="viewCaseDetail(${designCase.id})">
                            查看详情
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="no-results">暂无案例</p>';
        }
    } catch (error) {
        console.error('加载案例失败:', error);
        document.getElementById('cases-container').innerHTML = 
            '<p class="error">加载案例失败，请稍后重试</p>';
    }
}

// 加载更多案例
function loadMoreCases() {
    currentPage++;
    loadCases(currentPage, currentStyle);
}

// 设置案例筛选
function setupFilterButtons() {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // 更新活跃按钮
            buttons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // 加载对应风格的案例
            currentStyle = this.dataset.style;
            currentPage = 1;
            loadCases(1, currentStyle);
        });
    });
}

// 加载设计师
async function loadDesigners() {
    try {
        const response = await fetch(`${API_BASE_URL}/designers`);
        const designers = await response.json();
        
        const container = document.getElementById('designers-container');
        container.innerHTML = designers.map(designer => `
            <div class="designer-card">
                <img src="${designer.portfolio_images?.[0] || 'images/default-designer.jpg'}" 
                     alt="${designer.user?.full_name || '设计师'}" 
                     class="designer-image">
                <div class="designer-content">
                    <h3>${designer.user?.full_name || '设计师'}</h3>
                    <p class="designer-title">${designer.title || '设计师'}</p>
                    <div class="designer-rating">
                        ${getStarRating(designer.rating || 0)}
                    </div>
                    <p><strong>经验:</strong> ${designer.experience_years || 0}年</p>
                    <p><strong>专长:</strong> ${designer.specialization?.join(', ') || '室内设计'}</p>
                    <p>${designer.bio?.substring(0, 100) || ''}...</p>
                    <button class="btn-secondary" onclick="viewDesignerDetail(${designer.id})">
                        查看作品集
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('加载设计师失败:', error);
        document.getElementById('designers-container').innerHTML = 
            '<p class="error">加载设计师失败，请稍后重试</p>';
    }
}

// 生成星级评分
function getStarRating(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
    
    let stars = '';
    for (let i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }
    if (halfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }
    for (let i = 0; i < emptyStars; i++) {
        stars += '<i class="far fa-star"></i>';
    }
    return stars;
}

// 查看案例详情
function viewCaseDetail(caseId) {
    // 这里可以实现打开案例详情模态框或跳转到详情页
    alert(`查看案例 ${caseId} 的详细信息`);
    // 在实际应用中，可以打开模态框或跳转到详情页
    // window.location.href = `/case-detail.html?id=${caseId}`;
}

// 查看设计师详情
function viewDesignerDetail(designerId) {
    alert(`查看设计师 ${designerId} 的作品集`);
    // 在实际应用中，可以打开模态框或跳转到详情页
    // window.location.href = `/designer-detail.html?id=${designerId}`;
}

// 设置移动菜单
function setupMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', function() {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '100%';
            navLinks.style.left = '0';
            navLinks.style.right = '0';
            navLinks.style.backgroundColor = 'white';
            navLinks.style.padding = '20px';
            navLinks.style.boxShadow = '0 5px 10px rgba(0,0,0,0.1)';
        });
    }
}

// 显示预约弹窗
function showAppointmentModal() {
    document.getElementById('appointmentModal').style.display = 'flex';
}

// 关闭预约弹窗
function closeAppointmentModal() {
    document.getElementById('appointmentModal').style.display = 'none';
}

// 设置预约表单提交
function setupAppointmentForm() {
    const form = document.getElementById('appointmentForm');
    if (!form) return;
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            client_name: document.getElementById('clientName').value,
            client_phone: document.getElementById('clientPhone').value,
            client_email: document.getElementById('clientEmail').value,
            service_type: document.getElementById('serviceType').value,
            project_type: document.getElementById('projectType').value,
            message: document.getElementById('message').value
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/appointments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                alert('预约提交成功！我们的客服将在24小时内联系您。');
                form.reset();
                closeAppointmentModal();
            } else {
                const error = await response.json();
                alert(`提交失败: ${error.error || '请稍后重试'}`);
            }
        } catch (error) {
            console.error('提交预约失败:', error);
            alert('提交失败，请检查网络连接后重试');
        }
    });
}

// 滚动到指定区块
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const navHeight = document.querySelector('.navbar').offsetHeight;
        const sectionPosition = section.offsetTop - navHeight;
        window.scrollTo({
            top: sectionPosition,
            behavior: 'smooth'
        });
    }
}

// 关闭弹窗（点击背景）
window.onclick = function(event) {
    const modal = document.getElementById('appointmentModal');
    if (event.target === modal) {
        closeAppointmentModal();
    }
}

// 错误处理
window.onerror = function(message, source, lineno, colno, error) {
    console.error('JavaScript错误:', { message, source, lineno, colno, error });
    return true;
};