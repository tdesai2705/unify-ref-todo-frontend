from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import requests
import os

bp = Blueprint('main', __name__)

@bp.route('/health')
def health_check():
    """Health check endpoint for Kubernetes probes"""
    from flask import jsonify
    return jsonify({'status': 'healthy', 'service': 'todo-frontend'}), 200

def get_backend_url():
    """Get backend API URL from config"""
    return current_app.config['BACKEND_API_URL']

def check_feature_flag(flag_name, user_id=None):
    """Check if a feature flag is enabled (Cask integration placeholder)"""
    # TODO: Integrate with CloudBees Feature Management (Cask)
    # For now, return default values
    feature_flags = {
        'due-date-feature': os.getenv('FEATURE_DUE_DATE', 'false').lower() == 'true',
        'dark-mode': os.getenv('FEATURE_DARK_MODE', 'false').lower() == 'true'
    }
    return feature_flags.get(flag_name, False)

@bp.route('/')
def index():
    """Home page - redirect to todos"""
    return redirect(url_for('main.todo_list'))

@bp.route('/todos')
def todo_list():
    """Display all todos"""
    user_id = session.get('user_id', 1)  # Default user for now

    # Get filter parameters
    filter_completed = request.args.get('completed')
    filter_priority = request.args.get('priority')
    filter_category = request.args.get('category')

    # Build query parameters
    params = {'user_id': user_id}
    if filter_completed:
        params['completed'] = filter_completed
    if filter_priority:
        params['priority'] = filter_priority
    if filter_category:
        params['category'] = filter_category

    try:
        # Fetch todos from backend
        response = requests.get(f"{get_backend_url()}/todos", params=params, timeout=5)
        todos = response.json() if response.status_code == 200 else []

        # Fetch statistics
        stats_response = requests.get(f"{get_backend_url()}/todos/stats", params={'user_id': user_id}, timeout=5)
        stats = stats_response.json() if stats_response.status_code == 200 else {}

        # Check feature flags
        feature_due_date = check_feature_flag('due-date-feature', user_id)
        feature_dark_mode = check_feature_flag('dark-mode', user_id)

        return render_template('todo_list.html',
                             todos=todos,
                             stats=stats,
                             feature_due_date=feature_due_date,
                             feature_dark_mode=feature_dark_mode,
                             current_filter={
                                 'completed': filter_completed,
                                 'priority': filter_priority,
                                 'category': filter_category
                             })
    except requests.exceptions.RequestException as e:
        flash(f'Error connecting to backend: {str(e)}', 'error')
        return render_template('todo_list.html', todos=[], stats={},
                             feature_due_date=False, feature_dark_mode=False)

@bp.route('/todos/add', methods=['POST'])
def add_todo():
    """Add a new todo"""
    user_id = session.get('user_id', 1)

    todo_data = {
        'user_id': user_id,
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'priority': request.form.get('priority', 'medium'),
        'category': request.form.get('category')
    }

    # Add due_date if feature flag is enabled
    if check_feature_flag('due-date-feature', user_id) and request.form.get('due_date'):
        todo_data['due_date'] = request.form.get('due_date') + 'T00:00:00'

    try:
        response = requests.post(f"{get_backend_url()}/todos", json=todo_data, timeout=5)
        if response.status_code == 201:
            flash('Todo added successfully!', 'success')
        else:
            flash(f'Error adding todo: {response.json().get("error", "Unknown error")}', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Error connecting to backend: {str(e)}', 'error')

    return redirect(url_for('main.todo_list'))

@bp.route('/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle_todo(todo_id):
    """Toggle todo completed status"""
    try:
        # Get current todo
        response = requests.get(f"{get_backend_url()}/todos/{todo_id}", timeout=5)
        if response.status_code == 200:
            todo = response.json()
            # Toggle completed status
            update_response = requests.put(
                f"{get_backend_url()}/todos/{todo_id}",
                json={'completed': not todo['completed']},
                timeout=5
            )
            if update_response.status_code == 200:
                flash('Todo updated!', 'success')
            else:
                flash('Error updating todo', 'error')
        else:
            flash('Todo not found', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Error connecting to backend: {str(e)}', 'error')

    return redirect(url_for('main.todo_list'))

@bp.route('/todos/<int:todo_id>/delete', methods=['POST'])
def delete_todo(todo_id):
    """Delete a todo"""
    try:
        response = requests.delete(f"{get_backend_url()}/todos/{todo_id}", timeout=5)
        if response.status_code == 204:
            flash('Todo deleted!', 'success')
        else:
            flash('Error deleting todo', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Error connecting to backend: {str(e)}', 'error')

    return redirect(url_for('main.todo_list'))

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'todo-frontend'}, 200
