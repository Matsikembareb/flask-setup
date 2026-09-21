class TestMain:
    def test_index(self, client):
        """Root health blueprint index returns Hello, World!"""
        response = client.get('/health/')
        assert response.status_code == 200
        assert response.json == {'message': 'Hello, World!'}

    def test_health_check(self, client):
        """Health endpoint returns ok status."""
        response = client.get('/health/health')
        assert response.status_code == 200
        assert response.json == {'status': 'ok'}

    def test_cors_preflight_allows_configured_origin(self, client):
        """CORS preflight on an API route must reflect the configured origin."""
        response = client.open(
            '/health/health',
            method='OPTIONS',
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'GET',
            },
        )
        assert response.status_code in (200, 204)
        assert response.headers.get('Access-Control-Allow-Origin') == 'http://localhost:3000'

    def test_not_found_returns_json(self, client):
        """404 handler returns a JSON error body."""
        response = client.get('/this/does/not/exist')
        assert response.status_code == 404
        data = response.json
        assert data['error'] == 'Not Found'