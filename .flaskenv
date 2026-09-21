FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1

# Security
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-key-change-in-production

# Database
DATABASE_URL=sqlite:///development.db

# CORS — comma-separated list of allowed origins
CORS_ORIGINS=http://localhost:3000

# Email Error Logging (optional — remove comments to enable)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
# MAIL_FROM=noreply@yourapp.com
# ADMINS=admin@example.com