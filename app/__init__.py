from flask import Flask


def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.modules.health import bp as health_bp
    app.register_blueprint(health_bp)


    #initialize_swagger(app)

    return app
    """if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5000, app)"""