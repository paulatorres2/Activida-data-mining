import os
from flask import Flask, request, has_request_context
from routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.jinja_env.globals['enumerate'] = enumerate

    @app.context_processor
    def inject_endpoint():
        return {'current_endpoint': request.endpoint if has_request_context() else None}

    register_blueprints(app)
    return app


if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    create_app().run(debug=debug)
