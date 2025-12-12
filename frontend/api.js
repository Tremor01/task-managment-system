class ApiService {
    constructor() {
        this.baseURL = 'https://improved-broccoli-gg64vpp976phvxj4-8123.app.github.dev'; // Измените на адрес вашего бэкенда
    }

    // Проверить авторизацию перед запросом
    checkAuthBeforeRequest() {
        if (!utils.checkAuth()) {
            throw new Error('Not authenticated');
        }
    }

    // Обертка для запросов требующих авторизации
    async makeAuthenticatedRequest(url, options = {}) {
        this.checkAuthBeforeRequest();
        
        const headers = {
            ...utils.getAuthHeaders(),
            ...options.headers
        };

        const response = await fetch(`${this.baseURL}${url}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Токен недействителен
            throw { response: { status: 401, data: { detail: 'Session expired' } } };
        }

        if (!response.ok) {
            throw await response.json();
        }

        return response.json();
    }

    // Аутентификация (не требует авторизации)
    async login(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        formData.append('grant_type', 'password');

        try {
            const response = await fetch(`${this.baseURL}/auth/jwt/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });

            if (!response.ok) {
                throw await response.json();
            }

            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            
            // Получить данные пользователя
            const userData = await this.getCurrentUser();
            localStorage.setItem('user_data', JSON.stringify(userData));
            
            return data;
        } catch (error) {
            throw error;
        }
    }

    async register(email, password) {
        try {
            const response = await fetch(`${this.baseURL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            if (!response.ok) {
                throw await response.json();
            }

            const data = await response.json();
            return data;
        } catch (error) {
            throw error;
        }
    }

    async logout() {
        try {
            const response = await fetch(`${this.baseURL}/auth/jwt/logout`, {
                method: 'POST',
                headers: utils.getAuthHeaders()
            });

            return response.ok;
        } catch (error) {
            console.error('Logout error:', error);
            return false;
        }
    }

    async forgotPassword(email) {
        try {
            const response = await fetch(`${this.baseURL}/auth/forgot-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });

            if (!response.ok) {
                throw await response.json();
            }

            return true;
        } catch (error) {
            throw error;
        }
    }

    async verifyToken(token) {
        try {
            const response = await fetch(`${this.baseURL}/auth/verify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token })
            });

            if (!response.ok) {
                throw await response.json();
            }

            return response.json();
        } catch (error) {
            throw error;
        }
    }

    // Задачи (требуют авторизации)
    async getTasks() {
        return this.makeAuthenticatedRequest('/tasks/get', {
            method: 'GET'
        }).then(data => data.items || []);
    }

    async createTask(taskData) {
        return this.makeAuthenticatedRequest('/tasks/create', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    }

    async updateTask(taskId, taskData) {
        return this.makeAuthenticatedRequest(`/tasks/${taskId}`, {
            method: 'PATCH',
            body: JSON.stringify({ task_id: taskId, ...taskData })
        });
    }

    async deleteTask(taskId) {
        return this.makeAuthenticatedRequest(`/tasks/${taskId}`, {
            method: 'DELETE'
        });
    }

    // Метки (требуют авторизации)
    async getLabels() {
        return this.makeAuthenticatedRequest('/labels/get', {
            method: 'GET'
        }).then(data => data.items || []);
    }

    async createLabel(name) {
        return this.makeAuthenticatedRequest('/labels/create', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
    }

    async deleteLabel(labelId) {
        return this.makeAuthenticatedRequest(`/labels/${labelId}`, {
            method: 'DELETE'
        });
    }

    // Статусы (требуют авторизации)
    async getStatuses() {
        return this.makeAuthenticatedRequest('/statuses/get', {
            method: 'GET'
        }).then(data => data.items || []);
    }

    async createStatus(name) {
        return this.makeAuthenticatedRequest('/statuses/create', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
    }

    async deleteStatus(statusId) {
        return this.makeAuthenticatedRequest(`/statuses/${statusId}`, {
            method: 'DELETE'
        });
    }

    // Приоритеты (требуют авторизации)
    async getPriorities() {
        return this.makeAuthenticatedRequest('/priorities/get', {
            method: 'GET'
        }).then(data => data.items || []);
    }

    async createPriority(name) {
        return this.makeAuthenticatedRequest('/priorities/create', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
    }

    async deletePriority(priorityId) {
        return this.makeAuthenticatedRequest(`/priorities/${priorityId}`, {
            method: 'DELETE'
        });
    }

    // Пользователи (требуют авторизации)
    async getCurrentUser() {
        return this.makeAuthenticatedRequest('/users/me', {
            method: 'GET'
        });
    }

    async updateUser(userId, userData) {
        return this.makeAuthenticatedRequest(`/users/${userId}`, {
            method: 'PATCH',
            body: JSON.stringify(userData)
        });
    }
}

// Экспорт API сервиса
const api = new ApiService();