## PDF PREVIEW APP

#### Description :
**Django-turnit :** est un tag personnalisé, permettant d’afficher un lecteur de fichier PDF à base d'images des pages.

#### Dépendances :
	pip install PyPDF2
	
#### Description du tag :
	{% lecteur_pdf idpdf='id' res='' w='' h='' %} 
		- idpdf : [*] Identifiant du pdf dans la base de données.
		- res : Résolution des images en ppp. 
		- w : Largeur du lecteur
		- h : Hauteur du lecteur
	
		* : Argument obligatoire.

#### Utilisation :

Ce projet inclut une page de test (index.html) : 

- Copier le dossier du projet pdfviewerProject dans le dossier de votre choix, exemple celui d'un virtualenv avec django préinstallé. 
- Installer les dépendances. 
- Lancer le serveur. 
- Aller la page d'index via le navigateur web.

