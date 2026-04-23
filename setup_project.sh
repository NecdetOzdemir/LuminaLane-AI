#!/bin/bash

echo "🚀 LuminaLane AI - Project Setup Started..."

# 1. Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists."
fi

# 2. Install Dependencies
echo "📥 Installing dependencies from requirements.txt..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Check for Model Weights
if [ ! -f "weights/tusimple_18.pth" ]; then
    echo "⚠️ Warning: Model weights not found. Ensure you have Git LFS installed or download weights manually."
else
    echo "✅ Model weights detected."
fi

echo "✨ Setup Complete! You can now run the app using ./launch_app.sh"
