from .pages import pages_bp
from .analysis import analysis_bp


def register_blueprints(app):
    app.register_blueprint(pages_bp)
    app.register_blueprint(analysis_bp)
