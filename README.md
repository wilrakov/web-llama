# ConsuLex AI

## Objectif
L'objectif est de fournir une IA afin d'aider les membres de ConsuLex.
## Site web du projet
https://chatlibre.vercel.app
## Facilité d'utilisation
ConsuLex AI est construit pour être simple à utiliser. Vous pouvez ajouter vos fichiers simplement à partir de l'interface graphique, mais aussi directement dans le dossier `files`.
Les formats de fichers qui sont supportées sont le **Markdown** ainsi que le **texte brute**. Il est fortement conseillé d'utiliser la première option. Vous pouvez tout à fait **exporter vos docx et autres en Markdown** directement depuis votre éditeur de texte favoris. Et pour les plus courageux, vous avez la possibilité d'écrire directement vos fichers avec l'extension `.md`. Mais ça requiert d'apprendre une nouvelle façon de structurer des documents. Tous le texte que vous lisez actuellement est écrit directement en **Markdown**.
## Installation
Tout d'abord, installer python en vous rendant sur https://python.org.

Pour une utilisation continue, je recommande de payer un vps disposant d'une puissance minimum. Ainsi, l'utilisation d'au moins une carte graphique est obligatoire pour obtenir de bonnes performances. Mais si les performances ce n'est pas ce qui vous intéresse, alors vous pouvez tout à fait lancer le chatbot directement sur votre ordinateur personnel.

L'installation se fait en seulement 4 étapes dans le **terminal**.
### Etape 1
En premier lieu, il faut télécharger le projet. Vous pouvez le faire directement depuis Github en cliquant sur `Code` puis `Download zip`. Mais vous pouvez aussi le faire dans le terminal.
```bash
git clone https://github.com/wilrakov/website-llama.git 
```
### Etape 2
L'étape 2 consiste à installer les différentes dépendances de ce projet. Pour ce faire, il faut se rendre dans le dossier contenant le code dans le terminal.
#### Si vous avez utiliser le terminal à l'étape 1, copier ce code et coller le dans le terminal
```bash
cd website-llama
```
#### Sinon, aller dans le dossier que vous avez télécharger via l'explorateur de fichier puis **clic droit -> ouvrir dans le terminal** ou **clic droit -> ouvrir avec powershell/cmd**
Ensuite, il vous suffit de copier le code suivant puis le coller dans le terminal.
- Linux/MacOS
```bash
bash setup.sh
```
- Windows
```bash
setup.bat
```
### Etape 3
Lancer l'environnement virtuel.
```bash
conda activate ./conda-env
```
### Etape 4
Lancer l'application
```bash
python app.py
```
## Accéder à l'application
Bon si vous installez ce code sur votre ordinateur personnel, c'est plutôt simple. Une fois le serveur web lancé, accéder simplement à http://localhost:5001 dans votre navigateur internet

Par contre, dans le cas où ce n'est pas pour une utilisation personnelle mais pour une utilisation en continue avec plusieurs connexions et un besoin de meilleures performances, ça se complique un peu.
Il vous faudra mettre en place un serveur disponible sur internet. Pour cela, d'abord, procurez-vous un vps ou un serveur avec une puissance minimale. Ensuite, installez Caddy et suivez les instructions afin de le configurer. Je vous conseille aussi de demander à quelqu'un qui s'y connait en informatique si vous n'êtes pas encore à l'aise avec le terminal et toutes ces choses là.

Lien vers la documentation de Caddy : https://caddyserver.com/docs/

## Valeur ajoutée à ConsuLex
Je pense qu'une IA personnalisé qui ne partagerait pas ses données avec des tiers, ça peut vraiment être utile. Il faut vivre avec son temps et nous sommes dans une aire où les technologies évoluent très rapidement. Il y a peine 3 ans, nous n'entendions même pas parler d'intelligence artificielle. C'est pour ça que je suis pour la démocratisation de l'IA au plus grand nombre et notamment chez `ConsuLex`. J'espère que ce code sera utilisé par cette ASBL un jour. N'oubliez jamais que le fond est plus important que la forme.
