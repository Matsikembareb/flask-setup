from app.modules.health import bp

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}, 200