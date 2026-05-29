// Frontend JavaScript for Todo App

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.transition = 'opacity 0.5s';
            flash.style.opacity = '0';
            setTimeout(function() {
                flash.remove();
            }, 500);
        }, 5000);
    });
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const addTodoForm = document.querySelector('.add-todo-form form');
    if (addTodoForm) {
        addTodoForm.addEventListener('submit', function(e) {
            const titleInput = this.querySelector('input[name="title"]');
            if (!titleInput.value.trim()) {
                e.preventDefault();
                alert('Please enter a todo title');
                titleInput.focus();
            }
        });
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Focus on title input when pressing 'N' (new todo)
    if (e.key === 'n' && !e.ctrlKey && !e.metaKey && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        const titleInput = document.querySelector('input[name="title"]');
        if (titleInput) {
            titleInput.focus();
        }
    }
});

console.log('CloudBees Unify Reference - Todo App Frontend Loaded');
