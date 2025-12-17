# ============================================
# RoverWranglingData — Environment Setup Script
# ============================================

Write-Host "`n🚀 Starting setup for RoverWranglingData..." -ForegroundColor Cyan

# 1. Create virtual environment
Write-Host "🔧 Creating virtual environment 'env'..." -ForegroundColor Yellow
python -m venv env

# 2. Activate the environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
.\env\Scripts\Activate.ps1

# 3. Upgrade pip
Write-Host "⬆ Upgrading pip..." -ForegroundColor Yellow
pip install --upgrade pip

# 4. Install all dependencies from requirements.txt
Write-Host "📦 Installing Python dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

# 5. Register the Jupyter kernel so notebooks can select it
Write-Host "📚 Creating Jupyter kernel 'RWD'..." -ForegroundColor Yellow
python -m ipykernel install --user --name RWD --display-name "RWD Kernel"

# 6. Success message
Write-Host "`n🎉 RoverWranglingData environment successfully created!" -ForegroundColor Green
Write-Host "➡ Activate next time using:  .\env\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "➡ Launch JupyterLab with:   jupyter lab" -ForegroundColor Green

# End
