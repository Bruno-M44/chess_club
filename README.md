## Extraire les livrables du github sur votre poste de travail :
	`git clone https://github.com/Bruno-M44/chess_club.git`

## Se positionner dans le répertoire
	` cd chess_club/` 

## Créer l'environnement virtuel :
	`virtualenv -p python3 env`

## Activer l'environnement virtuel :
	`source env/bin/activate` (sous Windows : `C:\\{venv}\\Scripts\\activate.bat`)

## Installer les dépendances :	
	`pip install -r requirements.txt`

## Lancer le programme : 
	`python main.py`

Un menu apparaît où vous pouvez naviguer pour consulter et gérer les tournois d'échecs que vous souhaitez.

## Lancer flake8 afin de vérifier que le code respecte les normes PEP8 : 
	`flake8 'chess_club' > flake8.html`