from flask import Flask
import os

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['BACKEND_API_URL'] = os.getenv('BACKEND_API_URL', 'http://localhost:5000/api')
    app.config['CASK_API_KEY'] = os.getenv('CASK_API_KEY', '')

    # Register blueprints
    from app.views import bp
    app.register_blueprint(bp)

    # Initialize CloudBees Feature Management (Cask) SDK
    from app.feature_flags import setup as setup_flags
    setup_flags(app.config['CASK_API_KEY'])

    return app
