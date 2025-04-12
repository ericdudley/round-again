#!/bin/bash

echo "Setting up Tailwind CSS for Round Again..."

# Install Node.js dependencies
if [ ! -d "node_modules" ]; then
  echo "Installing Node.js dependencies..."
  npm install
else
  echo "Node.js dependencies already installed."
fi

# Build Tailwind CSS
echo "Building Tailwind CSS..."
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/styles.css --minify

echo "Tailwind CSS setup complete!"
echo "To watch for CSS changes during development, run: npm run watch"
echo "Or to use the dev server with Tailwind CSS watch, run: make dev"