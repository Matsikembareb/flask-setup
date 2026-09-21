from app import create_app

# Module-level app used by gunicorn and `flask run` — reads APP_ENV.
# sys.argv is NOT read here so gunicorn's own arguments can't interfere.
app = create_app()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run the Flask development server.')
    parser.add_argument(
        'env',
        nargs='?',                                          # optional positional arg
        default=None,
        choices=['development', 'production', 'testing'],
        help='Environment to run in. Overrides APP_ENV when provided.',
    )
    args = parser.parse_args()

    # Rebuild the app with the requested environment if one was passed
    if args.env:
        app = create_app(args.env)

    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5000,
    )
