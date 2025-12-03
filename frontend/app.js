class TaskManagerApp {
    constructor() {
        this.currentTaskId = null;
        this.currentItemType = null;
        this.initApp();
    }

    initApp() {
        // Инициализация утилит
        utils.init();

        // Защитить все защищенные страницы
        this.protectPages();

        // Инициализация модальных окон
        this.initModals();

        // Инициализация кнопок
        this.initButtons();

        // Инициализация фильтров
        this.initFilters();

        // Обработка изменения страниц
        this.initPageChangeListeners();

        // Периодическая проверка аутентификации
        this.startAuthCheck();
    }

    // Защита страниц
    protectPages() {
        const currentPage = utils.getCurrentPage();
        if (utils.isProtectedPage(currentPage) && !utils.checkAuth()) {
            utils.showPage('authPage');
        }
    }

    // Запустить периодическую проверку аутентификации
    startAuthCheck() {
        setInterval(() => {
            if (utils.isProtectedPage(utils.getCurrentPage()) && !utils.checkAuth()) {
                utils.showNotification('Session expired. Please login again.', 'error');
                utils.logout();
            }
        }, 60000);
    }

    // Инициализация модальных окон с проверкой авторизации
    initModals() {
        // Модальное окно задачи
        const closeTaskModal = document.getElementById('closeTaskModal');
        const cancelTask = document.getElementById('cancelTask');

        if (closeTaskModal) {
            closeTaskModal.addEventListener('click', () => {
                this.closeTaskModal();
            });
        }

        if (cancelTask) {
            cancelTask.addEventListener('click', () => {
                this.closeTaskModal();
            });
        }

        // Модальное окно элемента
        const closeItemModal = document.getElementById('closeItemModal');
        const cancelItem = document.getElementById('cancelItem');

        if (closeItemModal) {
            closeItemModal.addEventListener('click', () => {
                this.closeItemModal();
            });
        }

        if (cancelItem) {
            cancelItem.addEventListener('click', () => {
                this.closeItemModal();
            });
        }

        // Закрытие модальных окон по клику на overlay
        const overlay = document.getElementById('modalOverlay');
        if (overlay) {
            overlay.addEventListener('click', () => {
                this.closeTaskModal();
                this.closeItemModal();
            });
        }

        // Форма задачи
        const taskForm = document.getElementById('taskForm');
        if (taskForm) {
            // Очистка ошибок при вводе
            taskForm.querySelectorAll('input, textarea, select').forEach(field => {
                field.addEventListener('input', () => {
                    utils.clearFieldError(field.id);
                });
                field.addEventListener('change', () => {
                    utils.clearFieldError(field.id);
                });
            });

            taskForm.addEventListener('submit', (e) => {
                if (!utils.checkAuth()) {
                    e.preventDefault();
                    utils.showNotification('Please login to create tasks', 'error');
                    return;
                }
                this.handleTaskSubmit(e);
            });
        }

        // Форма элемента
        const itemForm = document.getElementById('itemForm');
        if (itemForm) {
            // Очистка ошибок при вводе
            itemForm.querySelectorAll('input').forEach(field => {
                field.addEventListener('input', () => {
                    utils.clearFieldError(field.id);
                });
            });

            itemForm.addEventListener('submit', (e) => {
                if (!utils.checkAuth()) {
                    e.preventDefault();
                    utils.showNotification('Please login to add items', 'error');
                    return;
                }
                this.handleItemSubmit(e);
            });
        }
    }

    // Закрыть модальное окно задачи
    closeTaskModal() {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login first', 'error');
            return;
        }
        utils.hideModal('taskModal');
        utils.clearFormErrors('taskForm');
    }

    // Закрыть модальное окно элемента
    closeItemModal() {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login first', 'error');
            return;
        }
        utils.hideModal('itemModal');
        utils.clearFormErrors('itemForm');
    }

    initButtons() {
        // Кнопка добавления задачи
        const addTaskBtn = document.getElementById('addTaskBtn');
        if (addTaskBtn) {
            addTaskBtn.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to add tasks', 'error');
                    return;
                }
                this.openTaskModal();
            });
        }

        // Кнопки добавления элементов
        const addLabelBtn = document.getElementById('addLabelBtn');
        if (addLabelBtn) {
            addLabelBtn.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to add labels', 'error');
                    return;
                }
                this.openItemModal('label');
            });
        }

        const addStatusBtn = document.getElementById('addStatusBtn');
        if (addStatusBtn) {
            addStatusBtn.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to add statuses', 'error');
                    return;
                }
                this.openItemModal('status');
            });
        }

        const addPriorityBtn = document.getElementById('addPriorityBtn');
        if (addPriorityBtn) {
            addPriorityBtn.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to add priorities', 'error');
                    return;
                }
                this.openItemModal('priority');
            });
        }

        // Кнопки профиля
        const editProfileBtn = document.getElementById('editProfileBtn');
        if (editProfileBtn) {
            editProfileBtn.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to edit profile', 'error');
                    return;
                }
                this.editProfile();
            });
        }

        const changePasswordBtn = document.getElementById('changePasswordBtn');
        if (changePasswordBtn) {
            changePasswordBtn.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to change password', 'error');
                    return;
                }
                this.changePassword();
            });
        }
    }

    initFilters() {
        const applyFilters = document.getElementById('applyFilters');
        const clearFilters = document.getElementById('clearFilters');

        if (applyFilters) {
            applyFilters.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to apply filters', 'error');
                    return;
                }
                this.applyTaskFilters();
            });
        }

        if (clearFilters) {
            clearFilters.addEventListener('click', () => {
                if (!utils.checkAuth()) {
                    utils.showNotification('Please login to clear filters', 'error');
                    return;
                }
                this.clearTaskFilters();
            });
        }
    }

    initPageChangeListeners() {
        // Загрузка данных при смене страницы
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const page = mutation.target;
                    if (page.classList.contains('active')) {
                        this.handlePageChange(page.id);
                    }
                }
            });
        });

        // Наблюдать за всеми страницами
        document.querySelectorAll('.page').forEach(page => {
            observer.observe(page, { attributes: true });
        });
    }

    handlePageChange(pageId) {
        // Проверить авторизацию для защищенных страниц
        if (utils.isProtectedPage(pageId) && !utils.checkAuth()) {
            utils.showNotification('Please login to access this page', 'error');
            utils.showPage('authPage');
            return;
        }

        switch (pageId) {
            case 'tasksPage':
                this.loadTasks();
                this.loadFiltersData();
                break;
            case 'labelsPage':
                this.loadLabels();
                break;
            case 'statusesPage':
                this.loadStatuses();
                break;
            case 'prioritiesPage':
                this.loadPriorities();
                break;
            case 'dashboardPage':
                this.loadDashboardData();
                break;
            case 'profilePage':
                utils.loadUserData();
                break;
        }
    }

    // Загрузка данных для dashboard
    async loadDashboardData() {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to view dashboard', 'error');
            return;
        }

        try {
            const [tasks, labels, statuses, priorities] = await Promise.all([
                api.getTasks(),
                api.getLabels(),
                api.getStatuses(),
                api.getPriorities()
            ]);

            document.getElementById('totalTasks').textContent = tasks.length;
            document.getElementById('totalLabels').textContent = labels.length;
            document.getElementById('totalStatuses').textContent = statuses.length;
            document.getElementById('totalPriorities').textContent = priorities.length;
            
            this.displayRecentTasks(tasks.slice(0, 5));
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            utils.handleApiError(error);
        }
    }

    // Отображение последних задач
    displayRecentTasks(tasks) {
        const tableBody = document.querySelector('#recentTasksTable tbody');
        if (!tableBody) return;

        tableBody.innerHTML = '';

        if (!tasks || tasks.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="loading">
                        <i class="fas fa-inbox"></i>
                        <p>No tasks found</p>
                    </td>
                </tr>
            `;
            return;
        }

        tasks.forEach(task => {
            const row = document.createElement('tr');
            
            const shortDescription = task.description.length > 50 
                ? task.description.substring(0, 50) + '...' 
                : task.description;
            
            row.innerHTML = `
                <td>${shortDescription}</td>
                <td>
                    <span class="badge">${task.status}</span>
                </td>
                <td>
                    <span class="badge">${task.priority}</span>
                </td>
                <td>${utils.formatDate(task.deadline)}</td>
                <td class="auth-only">
                    <div class="action-buttons">
                        <button class="action-btn edit-btn" onclick="app.editTask('${task.task_id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete-btn" onclick="app.deleteTask('${task.task_id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    // Загрузка задач
    async loadTasks() {
        if (!utils.checkAuth()) {
            return;
        }

        try {
            const tasks = await api.getTasks();
            this.displayTasks(tasks);
        } catch (error) {
            console.error('Error loading tasks:', error);
            utils.handleApiError(error);
        }
    }

    // Отображение задач
    displayTasks(tasks) {
        const tableBody = document.querySelector('#tasksTable tbody');
        if (!tableBody) return;

        tableBody.innerHTML = '';

        if (!tasks || tasks.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="loading">
                        <i class="fas fa-inbox"></i>
                        <p>No tasks found</p>
                    </td>
                </tr>
            `;
            return;
        }

        tasks.forEach(task => {
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${task.description}</td>
                <td>
                    <span class="badge">${task.status}</span>
                </td>
                <td>
                    <span class="badge">${task.priority}</span>
                </td>
                <td>
                    <span class="badge">${task.label}</span>
                </td>
                <td>${utils.formatDate(task.created_at)}</td>
                <td>${utils.formatDate(task.deadline)}</td>
                <td class="auth-only">
                    <div class="action-buttons">
                        <button class="action-btn edit-btn" onclick="app.editTask('${task.task_id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete-btn" onclick="app.deleteTask('${task.task_id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    // Загрузка меток
    async loadLabels() {
        if (!utils.checkAuth()) {
            return;
        }

        try {
            const labels = await api.getLabels();
            this.displayItems('labelsTable', labels, 'label');
        } catch (error) {
            console.error('Error loading labels:', error);
            utils.handleApiError(error);
        }
    }

    // Загрузка статусов
    async loadStatuses() {
        if (!utils.checkAuth()) {
            return;
        }

        try {
            const statuses = await api.getStatuses();
            this.displayItems('statusesTable', statuses, 'status');
        } catch (error) {
            console.error('Error loading statuses:', error);
            utils.handleApiError(error);
        }
    }

    // Загрузка приоритетов
    async loadPriorities() {
        if (!utils.checkAuth()) {
            return;
        }

        try {
            const priorities = await api.getPriorities();
            this.displayItems('prioritiesTable', priorities, 'priority');
        } catch (error) {
            console.error('Error loading priorities:', error);
            utils.handleApiError(error);
        }
    }

    // Отображение элементов (метки, статусы, приоритеты)
    displayItems(tableId, items, type) {
        const tableBody = document.querySelector(`#${tableId} tbody`);
        if (!tableBody) return;

        tableBody.innerHTML = '';

        if (!items || items.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="2" class="loading">
                        <i class="fas fa-inbox"></i>
                        <p>No ${type}s found</p>
                    </td>
                </tr>
            `;
            return;
        }

        items.forEach(item => {
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${item.name}</td>
                <td class="auth-only">
                    <div class="action-buttons">
                        <button class="action-btn delete-btn" onclick="app.deleteItem('${type}', ${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    // Загрузка данных для фильтров
    async loadFiltersData() {
        if (!utils.checkAuth()) {
            return;
        }

        try {
            const [labels, statuses, priorities] = await Promise.all([
                api.getLabels(),
                api.getStatuses(),
                api.getPriorities()
            ]);

            utils.populateSelect('filterLabel', labels, 'id', 'name', true);
            utils.populateSelect('filterStatus', statuses, 'id', 'name', true);
            utils.populateSelect('filterPriority', priorities, 'id', 'name', true);

            utils.populateSelect('taskLabel', labels, 'id', 'name', true);
            utils.populateSelect('taskStatus', statuses, 'id', 'name', false);
            utils.populateSelect('taskPriority', priorities, 'id', 'name', false);

        } catch (error) {
            console.error('Error loading filters data:', error);
            utils.handleApiError(error);
        }
    }

    // Открытие модального окна задачи
    async openTaskModal(taskId = null) {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to edit tasks', 'error');
            return;
        }

        this.currentTaskId = taskId;
        
        const modalTitle = document.getElementById('taskModalTitle');
        modalTitle.textContent = taskId ? 'Edit Task' : 'Add New Task';
        
        const form = document.getElementById('taskForm');
        form.reset();
        utils.clearFormErrors('taskForm');
        
        try {
            await this.loadFiltersData();
            
            if (taskId) {
                await this.loadTaskData(taskId);
            }
            
            utils.showModal('taskModal');
        } catch (error) {
            console.error('Error opening task modal:', error);
            utils.handleApiError(error);
        }
    }

    // Загрузка данных задачи для редактирования
    async loadTaskData(taskId) {
        try {
            const tasks = await api.getTasks();
            const task = tasks.find(t => t.task_id == taskId);
            
            if (task) {
                document.getElementById('taskId').value = task.task_id;
                document.getElementById('taskDescription').value = task.description;
                
                if (task.deadline) {
                    const deadlineDate = new Date(task.deadline);
                    document.getElementById('taskDeadline').value = deadlineDate.toISOString().slice(0, 16);
                }
            }
        } catch (error) {
            console.error('Error loading task data:', error);
            utils.handleApiError(error);
        }
    }

    // Обработка отправки формы задачи
    async handleTaskSubmit(e) {
        console.log("SAVE TASK")
        e.preventDefault();
        
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to save tasks', 'error');
            return;
        }
        
        // Очистить предыдущие ошибки
        utils.clearFormErrors('taskForm');
        
        // Базовая валидация на фронте
        const description = document.getElementById('taskDescription').value.trim();
        if (!description) {
            utils.showFieldError('taskDescription', 'Description is required');
            return;
        }
        
        const taskData = {
            description: description,
            label_id: document.getElementById('taskLabel').value || null,
            status_id: document.getElementById('taskStatus').value || null,
            priority_id: document.getElementById('taskPriority').value || null,
            deadline: document.getElementById('taskDeadline').value || null,
        };
        
        try {
            if (this.currentTaskId) {
                await api.updateTask(this.currentTaskId, taskData);
            } else {
                await api.createTask(taskData);
            }
            
            this.closeTaskModal();
            await this.loadTasks();
            await this.loadDashboardData();
            
        } catch (error) {
            console.error('Error saving task:', error);
            utils.handleApiError(error, 'task');
        }
    }

    // Редактирование задачи
    editTask(taskId) {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to edit tasks', 'error');
            return;
        }
        this.openTaskModal(taskId);
    }

    // Удаление задачи
    async deleteTask(taskId) {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to delete tasks', 'error');
            return;
        }

        if (confirm('Are you sure you want to delete this task?')) {
            try {
                await api.deleteTask(taskId);
                await this.loadTasks();
                await this.loadDashboardData();
            } catch (error) {
                console.error('Error deleting task:', error);
                utils.handleApiError(error);
            }
        }
    }

    // Открытие модального окна элемента
    openItemModal(type) {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to add items', 'error');
            return;
        }

        this.currentItemType = type;
        
        const modalTitle = document.getElementById('itemModalTitle');
        modalTitle.textContent = `Add New ${type.charAt(0).toUpperCase() + type.slice(1)}`;
        
        const form = document.getElementById('itemForm');
        form.reset();
        utils.clearFormErrors('itemForm');
        document.getElementById('itemId').value = '';
        
        utils.showModal('itemModal');
    }

    // Обработка отправки формы элемента
    async handleItemSubmit(e) {
        e.preventDefault();
        
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to save items', 'error');
            return;
        }
        
        // Очистить предыдущие ошибки
        utils.clearFormErrors('itemForm');
        
        const name = document.getElementById('itemName').value.trim();
        
        if (!name) {
            utils.showFieldError('itemName', 'Name is required');
            return;
        }
        
        try {
            switch (this.currentItemType) {
                case 'label':
                    await api.createLabel(name);
                    await this.loadLabels();
                    break;
                case 'status':
                    await api.createStatus(name);
                    await this.loadStatuses();
                    break;
                case 'priority':
                    await api.createPriority(name);
                    await this.loadPriorities();
                    break;
            }
            
            this.closeItemModal();
            await this.loadFiltersData();
            await this.loadDashboardData();
            
        } catch (error) {
            console.error('Error saving item:', error);
            utils.handleApiError(error, 'item');
        }
    }

    // Удаление элемента
    async deleteItem(type, id) {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to delete items', 'error');
            return;
        }

        if (confirm(`Are you sure you want to delete this ${type}?`)) {
            try {
                switch (type) {
                    case 'label':
                        await api.deleteLabel(id);
                        await this.loadLabels();
                        break;
                    case 'status':
                        await api.deleteStatus(id);
                        await this.loadStatuses();
                        break;
                    case 'priority':
                        await api.deletePriority(id);
                        await this.loadPriorities();
                        break;
                }
                
                await this.loadFiltersData();
                await this.loadDashboardData();
                
            } catch (error) {
                console.error('Error deleting item:', error);
                utils.handleApiError(error);
            }
        }
    }

    // Применение фильтров задач
    async applyTaskFilters() {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to apply filters', 'error');
            return;
        }

        utils.showNotification('Filters applied', 'success');
    }

    // Очистка фильтров
    clearTaskFilters() {
        if (!utils.checkAuth()) {
            utils.showNotification('Please login to clear filters', 'error');
            return;
        }

        document.getElementById('filterStatus').value = '';
        document.getElementById('filterPriority').value = '';
        document.getElementById('filterLabel').value = '';
        utils.showNotification('Filters cleared', 'success');
    }

    // Редактирование профиля
    editProfile() {
        utils.showNotification('Edit profile feature coming soon!', 'info');
    }

    // Смена пароля
    changePassword() {
        utils.showNotification('Change password feature coming soon!', 'info');
    }
}

// Инициализация приложения при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TaskManagerApp();
});