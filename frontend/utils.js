class Utils {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.protectedPages = ['dashboardPage', 'tasksPage', 'labelsPage', 'statusesPage', 'prioritiesPage', 'profilePage'];
    }

    // Показать уведомление
    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type} show`;
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000); // Увеличил время для лучшего чтения ошибок
    }

    // Показать ошибки валидации под полями
    showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        if (!field) return;
        
        // Удалить старую ошибку
        const oldError = field.parentNode.querySelector('.field-error');
        if (oldError) {
            oldError.remove();
        }
        
        // Добавить новую ошибку
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        errorDiv.style.color = 'var(--danger-color)';
        errorDiv.style.fontSize = '0.85rem';
        errorDiv.style.marginTop = '0.25rem';
        
        field.parentNode.appendChild(errorDiv);
        
        // Подсветить поле
        field.style.borderColor = 'var(--danger-color)';
    }

    // Очистить ошибки поля
    clearFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return;
        
        // Удалить сообщение об ошибке
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
        
        // Сбросить стиль поля
        field.style.borderColor = '';
    }

    // Очистить все ошибки в форме
    clearFormErrors(formId) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        form.querySelectorAll('.field-error').forEach(error => error.remove());
        form.querySelectorAll('input, select, textarea').forEach(field => {
            field.style.borderColor = '';
        });
    }

    // Обработка ошибок API с валидацией
    handleApiError(error, formId = null) {
        console.error('API Error:', error.response);

        if (formId == 'login') {
            this.showNotification('User does not exsist', 'error');
            return;
        }

        if (error.response) {
            // Ошибка 401 - неавторизован
            if (error.response.status === 401) {
                this.showNotification('Session expired. Please login again.', 'error');
                this.logout();
                return;
            }
            
            const errorData = error.response.data;
            
            // Обработка ошибок валидации (422)
            if (error.response.status === 422 && errorData.detail && Array.isArray(errorData.detail)) {
                this.handleValidationErrors(errorData.detail, formId);
                return;
            }
            
            // Обработка пользовательских ошибок
            if (errorData.detail) {
                this.handleErrorDetail(errorData.detail, formId);
                return;
            }
            
            // Общая ошибка
            this.showNotification(`Error ${error.response.status}: ${error.response.statusText}`, 'error');
            
        } else if (error.message === 'Not authenticated') {
            this.showNotification('Please login to perform this action', 'error');
            this.logout();
        } else {
            this.showNotification('Network error. Please check your connection.', 'error');
        }
    }

    // Обработка ошибок валидации
    handleValidationErrors(errors, formId = null) {
        errors.forEach(error => {
            const fieldName = error.loc[error.loc.length - 1];
            const fieldId = this.getFieldIdFromName(fieldName, formId);
            
            if (fieldId) {
                this.showFieldError(fieldId, error.msg);
            } else {
                // Если не нашли конкретное поле, показываем общее уведомление
                this.showNotification(error.msg, 'error');
            }
        });
    }

    // Обработка детализированных ошибок
    handleErrorDetail(detail, formId = null) {
        if (typeof detail === 'string') {
            this.showNotification(detail, 'error');
        } else if (detail.code) {
            // Обработка структурированных ошибок
            switch (detail.code) {
                case 'REGISTER_INVALID_PASSWORD':
                case 'RESET_PASSWORD_INVALID_PASSWORD':
                case 'UPDATE_USER_INVALID_PASSWORD':
                    const passwordField = formId ? `${formId}Password` : 'registerPassword';
                    this.showFieldError(passwordField, detail.reason || 'Invalid password');
                    break;
                    
                case 'REGISTER_USER_ALREADY_EXISTS':
                case 'UPDATE_USER_EMAIL_ALREADY_EXISTS':
                    const emailField = formId ? `${formId}Email` : 'registerEmail';
                    this.showFieldError(emailField, 'A user with this email already exists');
                    break;
                    
                case 'LOGIN_BAD_CREDENTIALS':
                    this.showNotification('Invalid email or password', 'error');
                    break;
                    
                case 'LOGIN_USER_NOT_VERIFIED':
                    this.showNotification('Please verify your email before logging in', 'error');
                    break;
                    
                case 'VERIFY_USER_BAD_TOKEN':
                    this.showNotification('Invalid verification token', 'error');
                    break;
                    
                case 'VERIFY_USER_ALREADY_VERIFIED':
                    this.showNotification('User is already verified', 'error');
                    break;
                    
                case 'RESET_PASSWORD_BAD_TOKEN':
                    this.showNotification('Invalid or expired reset token', 'error');
                    break;
                    
                default:
                    this.showNotification(detail.reason || detail.code, 'error');
            }
        } else if (typeof detail === 'object') {
            // Обработка вложенных ошибок
            Object.entries(detail).forEach(([key, value]) => {
                const fieldId = this.getFieldIdFromName(key, formId);
                if (fieldId) {
                    this.showFieldError(fieldId, value);
                }
            });
        }
    }

    // Получить ID поля по имени из API
    getFieldIdFromName(fieldName, formId = null) {
        const fieldMap = {
            'email': formId ? `${formId}Email` : 'email',
            'password': formId ? `${formId}Password` : 'password',
            'username': 'loginEmail',
            'grant_type': 'loginGrantType',
            'scope': 'loginScope',
            'client_id': 'loginClientId',
            'client_secret': 'loginClientSecret',
            'token': 'resetToken',
            'is_active': 'isActive',
            'is_superuser': 'isSuperuser',
            'is_verified': 'isVerified',
            'description': 'taskDescription',
            'label_id': 'taskLabel',
            'status_id': 'taskStatus',
            'priority_id': 'taskPriority',
            'deadline': 'taskDeadline',
            'executors': 'taskExecutors',
            'name': 'itemName',
            'task_id': 'taskId'
        };
        
        return fieldMap[fieldName] || fieldName;
    }

    // Форматирование даты
    formatDate(dateString) {
        if (!dateString) return 'N/A';
        
        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) return 'N/A';
            
            return date.toLocaleDateString('ru-RU', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (e) {
            return 'N/A';
        }
    }

    // Показать/скрыть модальное окно
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        const overlay = document.getElementById('modalOverlay');
        
        modal.classList.add('active');
        overlay.style.display = 'block';
        
        setTimeout(() => {
            overlay.style.opacity = '1';
        }, 10);
    }

    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        const overlay = document.getElementById('modalOverlay');
        
        modal.classList.remove('active');
        overlay.style.opacity = '0';
        
        setTimeout(() => {
            overlay.style.display = 'none';
        }, 300);
    }

    // Проверка аутентификации
    checkAuth() {
        const token = localStorage.getItem('access_token');
        return !!token;
    }

    // Проверка защищенной страницы
    isProtectedPage(pageId) {
        return this.protectedPages.includes(pageId);
    }

    // Получить текущую страницу
    getCurrentPage() {
        const activePage = document.querySelector('.page.active');
        return activePage ? activePage.id : 'authPage';
    }

    // Переключение страниц с проверкой авторизации
    showPage(pageId) {
        // Проверить доступ к странице
        if (this.isProtectedPage(pageId) && !this.checkAuth()) {
            this.showNotification('Please login to access this page', 'error');
            this.showPage('authPage');
            return;
        }

        // Скрыть все страницы
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Показать выбранную страницу
        const page = document.getElementById(pageId);
        if (page) {
            page.classList.add('active');
        }
        
        // Обновить активную ссылку в навигации
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.dataset.page === pageId.replace('Page', '')) {
                link.classList.add('active');
            }
        });

        // Обновить классы body
        this.updateBodyClasses();
    }

    // Обновить классы body в зависимости от авторизации
    updateBodyClasses() {
        const body = document.body;
        const nav = document.querySelector('.navbar');
        
        if (this.checkAuth()) {
            body.classList.add('authenticated');
            body.classList.remove('guest-only');
            if (nav) nav.classList.remove('hidden');
        } else {
            body.classList.add('guest-only');
            body.classList.remove('authenticated');
            if (nav) nav.classList.add('hidden');
        }
    }

    // Заполнить select опциями
    populateSelect(selectId, items, valueKey = 'id', textKey = 'name', emptyOption = true) {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        select.innerHTML = '';
        
        if (emptyOption) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Select...';
            select.appendChild(option);
        }
        
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valueKey];
            option.textContent = item[textKey];
            select.appendChild(option);
        });
    }

    // Получить заголовки с токеном
    getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }

    // Выход из системы
    logout() {
        api.logout().then(() => {
            this.clearAuthData();
        }).catch(() => {
            this.clearAuthData();
        });
    }

    // Очистить данные аутентификации
    clearAuthData() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
        this.showPage('authPage');
        this.showNotification('Logged out successfully', 'success');
        this.updateBodyClasses();
    }

    // Загрузка данных пользователя
    loadUserData() {
        const userData = localStorage.getItem('user_data');
        if (userData) {
            try {
                const user = JSON.parse(userData);
                document.getElementById('userEmail').textContent = user.email;
                document.getElementById('userId').textContent = `ID: ${user.id}`;
                document.getElementById('emailVerified').textContent = user.is_verified ? 'Yes' : 'No';
                document.getElementById('accountActive').textContent = user.is_active ? 'Yes' : 'No';
                document.getElementById('isSuperuser').textContent = user.is_superuser ? 'Yes' : 'No';
            } catch (e) {
                console.error('Error parsing user data:', e);
            }
        }
    }

    // Инициализация
    init() {
        // Проверить аутентификацию
        if (this.checkAuth()) {
            this.showPage('dashboardPage');
            this.loadUserData();
        } else {
            this.showPage('authPage');
        }

        // Обновить классы body
        this.updateBodyClasses();

        // Инициализация навигационного меню
        this.initNavigation();
    }

    // Инициализация навигации
    initNavigation() {
        // Навигационные ссылки
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                if (!this.checkAuth()) {
                    this.showNotification('Please login to access this page', 'error');
                    return;
                }
                const pageId = `${link.dataset.page}Page`;
                this.showPage(pageId);
                
                // Закрыть мобильное меню если открыто
                const navMenu = document.getElementById('navMenu');
                if (navMenu) {
                    navMenu.classList.remove('active');
                }
            });
        });

        // Кнопка выхода
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                this.logout();
            });
        }

        // Мобильное меню
        const navToggle = document.getElementById('navToggle');
        if (navToggle) {
            navToggle.addEventListener('click', () => {
                const navMenu = document.getElementById('navMenu');
                if (navMenu) {
                    navMenu.classList.toggle('active');
                }
            });
        }
    }
}

// Экспорт утилит
const utils = new Utils();