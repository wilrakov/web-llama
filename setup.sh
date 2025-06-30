#!/bin/bash
# Verifie si Conda est installe
if ! command -v conda &> /dev/null
then
    echo "Conda n'est pas detecte. Veuillez l'installer avant de continuer."
    echo "Vous pouvez le telecharger ici : https://www.anaconda.com/products/distribution"
    exit 1
fi

echo "Creation de l'environnement Conda 'conda-env'..."
conda create --prefix ./conda-env python=3.10 -y

echo "Installation des dependances..."
conda run -p ./conda-env pip install faiss-cpu numpy llama-cpp-python sentence-transformers Flask

echo
echo "=== Installation terminee ==="
echo
echo "Pour lancer l'application, executez les commandes suivantes dans votre terminal :"
echo
echo "conda activate ./conda-env"
echo "python app.py"
echo
