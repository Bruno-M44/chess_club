## Extraire les livrables du github sur votre poste de travail :
	`git clone https://github.com/Bruno-M44/chess_club.git`

## Se positionner dans le répertoire
	`cd chess_club/` 

## Créer l'environnement virtuel :
	`py -3 -m venv venv`

## Activer l'environnement virtuel :
	`source env/bin/activate` (sous Windows : `C:\\{venv}\\Scripts\\activate.bat`)

## Installer les dépendances :	
	`pip install -r requirements.txt`

## Lancer le programme : 
	`python main.py`

Un menu apparaît où vous pouvez naviguer pour consulter et gérer les tournois d'échecs que vous souhaitez.

## Lancer flake8 afin de vérifier que le code respecte les normes PEP8 : 
	`flake8 controller main.py models view > flake8.html`

Un fichier flake8.html est apparu à la racine du répertoire qui doit être vide prouvant qu'il n'y a pas d'erreur.