@echo off
REM Verifie si Conda est installe
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo "Conda n'est pas detecte. Veuillez l'installer avant de continuer."
    echo "Vous pouvez le telecharger ici : https://www.anaconda.com/products/distribution"
    exit /b 1
)

echo "Creation de l'environnement Conda 'conda-env'..."
conda create --prefix ./conda-env python=3.10 -y

echo "Installation des dependances..."
conda install -c pytorch faiss-cpu
call conda run --prefix ./conda-env pip install numpy llama-cpp-python sentence-transformers Flask

echo.
echo "=== Installation terminee ==="
echo.
echo "Pour lancer l'application, executez les commandes suivantes dans votre terminal :"
echo.
echo "conda activate ./conda-env"
echo "python app.py"
echo.
