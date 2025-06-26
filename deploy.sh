#!/bin/bash

echo "🚀 BioLab Associates - Easy Deployment Script"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - BioLab Associates deployment"
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed."
    echo "📥 Please install it first:"
    echo "   Mac: brew install heroku/brew/heroku"
    echo "   Windows: Download from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "🔐 Logging into Heroku..."
heroku login

echo "🏗️  Creating Heroku app..."
heroku create biolabassociates

echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy BioLab Associates with domain setup"
git push heroku main

echo "⚙️  Setting production configuration..."
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(openssl rand -base64 32)

echo "🌐 Adding custom domain..."
heroku domains:add biolabass.com
heroku domains:add www.biolabass.com

echo "📋 Getting domain configuration..."
heroku domains

echo ""
echo "✅ Deployment Complete!"
echo "========================"
echo "🌐 Your app is live at: https://biolabassociates.herokuapp.com"
echo "🔗 Custom domain: https://biolabass.com (after DNS setup)"
echo ""
echo "📝 Next Steps:"
echo "1. Update your DNS settings:"
echo "   - CNAME: www → biolabassociates.herokuapp.com"
echo "   - A: @ → (IP shown above)"
echo "2. Domain propagation takes 24-48 hours"
echo "3. Test your site: https://biolabass.com/login"
echo ""
echo "👤 Test accounts:"
echo "   - admin / biolab123"
echo "   - researcher / research456"
echo "   - student / student789" 