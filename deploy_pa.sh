#!/bin/bash

# TeleNote Deployment Script for PythonAnywhere
# Usage: source deploy_pa.sh

# Configuration
REPO_URL="https://github.com/zoidberg-xgd/TeleNote.git"
PROJECT_DIR="$HOME/tapnote"
VENV_NAME="tapnote-venv"
PYTHON_VERSION="python3.10"

echo "🚀 Starting TeleNote Deployment on PythonAnywhere..."

# 1. Clone or Pull Repository
if [ -d "$PROJECT_DIR" ]; then
    echo "📂 Directory $PROJECT_DIR exists. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull
else
    echo "📂 Cloning repository..."
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# 2. Setup Virtual Environment
echo "🐍 Setting up Virtual Environment..."
if ! workon $VENV_NAME 2>/dev/null; then
    echo "   Creating new virtualenv: $VENV_NAME"
    mkvirtualenv --python=/usr/bin/$PYTHON_VERSION $VENV_NAME
else
    echo "   Activating existing virtualenv: $VENV_NAME"
    workon $VENV_NAME
fi

# 3. Install Dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 4. Configure .env file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    # Generate a random secret key
    SECRET=$(openssl rand -base64 32)
    
    cat > .env <<EOL
DEBUG=False
SECRET_KEY=$SECRET
ALLOWED_HOSTS=.pythonanywhere.com
DATABASE_URL=sqlite:///$PROJECT_DIR/db.sqlite3
EOL
    echo "✅ .env file created with secure defaults."
else
    echo "ℹ️  .env file already exists. Skipping creation."
fi

# 5. Django Setup
echo "🗄️  Migrating database..."
python manage.py migrate

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "----------------------------------------------------------------"
echo "✅ Deployment script completed successfully!"
echo "----------------------------------------------------------------"
echo "⚠️  MANUAL STEPS REQUIRED IN WEB TAB:"
echo ""
echo "1. Go to the 'Web' tab."
echo "2. Set 'Virtualenv' path to:"
echo "   $WORKON_HOME/$VENV_NAME"
echo ""
echo "3. Add 'Static files':"
echo "   URL:  /static/"
echo "   Path: $PROJECT_DIR/staticfiles"
echo ""
echo "4. Edit 'WSGI configuration file' and paste the configuration from DEPLOY_PYTHONANYWHERE.md"
echo ""
echo "5. Click the green 'Reload' button."
echo "----------------------------------------------------------------"
