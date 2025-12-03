class AuthHandler {
    constructor() {
        this.initAuthForms();
    }

    initAuthForms() {
        // Переключение между формами входа и регистрации
        document.querySelectorAll('.auth-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.dataset.tab;
                this.switchAuthTab(tabName);
            });
        });

        // Форма входа
        const loginForm = document.getElementById('loginFormElement');
        if (loginForm) {
            // Очистка ошибок при вводе
            loginForm.querySelectorAll('input').forEach(input => {
                input.addEventListener('input', () => {
                    utils.clearFieldError(input.id);
                });
            });

            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleLogin();
            });
        }

        // Форма регистрации
        const registerForm = document.getElementById('registerFormElement');
        if (registerForm) {
            // Очистка ошибок при вводе
            registerForm.querySelectorAll('input').forEach(input => {
                input.addEventListener('input', () => {
                    utils.clearFieldError(input.id);
                });
            });

            registerForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleRegister();
            });
        }

        // Форма восстановления пароля
        const forgotPasswordForm = document.getElementById('forgotPasswordFormElement');
        if (forgotPasswordForm) {
            // Очистка ошибок при вводе
            forgotPasswordForm.querySelectorAll('input').forEach(input => {
                input.addEventListener('input', () => {
                    utils.clearFieldError(input.id);
                });
            });

            forgotPasswordForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleForgotPassword();
            });
        }

        // Ссылка "Забыли пароль?"
        const forgotPasswordLink = document.getElementById('forgotPasswordLink');
        if (forgotPasswordLink) {
            forgotPasswordLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.showForgotPasswordForm();
            });
        }

        // Ссылка "Назад ко входу"
        const backToLogin = document.getElementById('backToLogin');
        if (backToLogin) {
            backToLogin.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchAuthTab('login');
            });
        }
    }

    switchAuthTab(tabName) {
        // Очистить все ошибки при переключении вкладок
        utils.clearFormErrors('loginFormElement');
        utils.clearFormErrors('registerFormElement');
        utils.clearFormErrors('forgotPasswordFormElement');
        
        // Обновить активные вкладки
        document.querySelectorAll('.auth-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Показать/скрыть соответствующие формы
        document.querySelectorAll('.auth-form').forEach(form => {
            form.classList.toggle('active', form.id === `${tabName}Form`);
        });
    }

    showForgotPasswordForm() {
        // Очистить ошибки
        utils.clearFormErrors('loginFormElement');
        utils.clearFormErrors('registerFormElement');
        
        // Показать форму восстановления пароля и скрыть остальные
        document.querySelectorAll('.auth-form').forEach(form => {
            form.classList.toggle('active', form.id === 'forgotPasswordForm');
        });
        
        // Скрыть вкладки
        document.querySelectorAll('.auth-tab').forEach(tab => {
            tab.classList.remove('active');
        });
    }

    async handleLogin() {
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;

        // Базовая валидация на фронте
        let hasError = false;
        
        if (!email) {
            utils.showFieldError('loginEmail', 'Email is required');
            hasError = true;
        } else if (!this.isValidEmail(email)) {
            utils.showFieldError('loginEmail', 'Please enter a valid email address');
            hasError = true;
        }
        
        if (!password) {
            utils.showFieldError('loginPassword', 'Password is required');
            hasError = true;
        }
        
        if (hasError) return;

        const loginFormElement = document.getElementById('loginFormElement');
        if (!loginFormElement) return;

        try {
            const loginButton = loginFormElement.querySelector('button[type="submit"]');
            loginButton.disabled = true;
            loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';

            await api.login(email, password);
            
            // Успешный вход
            utils.showNotification('Login successful!', 'success');
            
            // Обновить интерфейс
            utils.updateBodyClasses();
            utils.showPage('dashboardPage');
            utils.loadUserData();
            app.loadDashboardData();
            
        } catch (error) {
            // Передаем formId для привязки ошибок к полям
            utils.handleApiError(error, 'login');
        } finally {
            const loginButton = loginFormElement.querySelector('button[type="submit"]');
            if (loginButton) {
                loginButton.disabled = false;
                loginButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';
            }
        }
    }

    async handleRegister() {
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        // Базовая валидация на фронте
        let hasError = false;
        
        if (!email) {
            utils.showFieldError('registerEmail', 'Email is required');
            hasError = true;
        } else if (!this.isValidEmail(email)) {
            utils.showFieldError('registerEmail', 'Please enter a valid email address');
            hasError = true;
        }
        
        if (!password) {
            utils.showFieldError('registerPassword', 'Password is required');
            hasError = true;
        } else if (password.length < 3) {
            utils.showFieldError('registerPassword', 'Password must be at least 3 characters');
            hasError = true;
        }
        
        if (!confirmPassword) {
            utils.showFieldError('confirmPassword', 'Please confirm your password');
            hasError = true;
        } else if (password !== confirmPassword) {
            utils.showFieldError('confirmPassword', 'Passwords do not match');
            hasError = true;
        }
        
        if (hasError) return;

        const registerFormElement = document.getElementById('registerFormElement');
        if (!registerFormElement) return;

        try {
            const registerButton = registerFormElement.querySelector('button[type="submit"]');
            registerButton.disabled = true;
            registerButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registering...';

            await api.register(email, password);
            
            // Успешная регистрация
            utils.showNotification('Registration successful! Please check your email for verification.', 'success');
            
            // Переключиться на форму входа
            this.switchAuthTab('login');
            
            // Очистить форму регистрации
            registerFormElement.reset();
            
        } catch (error) {
            // Передаем formId для привязки ошибок к полям
            utils.handleApiError(error, 'register');
        } finally {
            const registerButton = registerFormElement.querySelector('button[type="submit"]');
            if (registerButton) {
                registerButton.disabled = false;
                registerButton.innerHTML = '<i class="fas fa-user-plus"></i> Register';
            }
        }
    }

    async handleForgotPassword() {
        const email = document.getElementById('resetEmail').value.trim();

        // Базовая валидация
        if (!email) {
            utils.showFieldError('resetEmail', 'Email is required');
            return;
        }
        
        if (!this.isValidEmail(email)) {
            utils.showFieldError('resetEmail', 'Please enter a valid email address');
            return;
        }

        const forgotPasswordFormElement = document.getElementById('forgotPasswordFormElement');
        if (!forgotPasswordFormElement) return;

        try {
            const resetButton = forgotPasswordFormElement.querySelector('button[type="submit"]');
            resetButton.disabled = true;
            resetButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            await api.forgotPassword(email);
            
            // Успешно отправлено
            utils.showNotification('Password reset link sent to your email!', 'success');
            
            // Вернуться к форме входа
            this.switchAuthTab('login');
            
            // Очистить форму
            forgotPasswordFormElement.reset();
            
        } catch (error) {
            utils.handleApiError(error, 'reset');
        } finally {
            const resetButton = forgotPasswordFormElement.querySelector('button[type="submit"]');
            if (resetButton) {
                resetButton.disabled = false;
                resetButton.innerHTML = '<i class="fas fa-key"></i> Send Reset Link';
            }
        }
    }

    // Проверка валидности email (базовая)
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
}

// Инициализация обработчика аутентификации
const authHandler = new AuthHandler();