Creation projet Demo docker, python, flask : 

last update : 08 fev 2023
vscode version : 1.74.3 (top menu > help > about) 
Tutoriel video : https://www.youtube.com/watch?v=ZZ7BpJYN-DM

# 1. Creer le projet
 - Lancer vscode a partir d'un repertoire vide
 - Creer un fichier app/app.py avec le code quickstart du site officiel de flask : https://flask.palletsprojects.com/en/2.2.x/quickstart/

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

# 2.Creer un Dockerfile
- Tapez ctrl+alt+p, pour faire apparaitre des options de commande vscode.
- Tapez "Docker: add dockerfile to workspace"
 - Choisir : python flask > app.py > 5002 > yes 
- Dans le Dockerfile changer : 
  - COPY ./app /app (ligne 17)
	-> "./app" est le dossier source de l'application. "/app" est le dossier sur la machine virtuel docker.
  - CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"] (ligne 25)
	-> Supprimer un "app.". Sur l'image docker les service web sont lancer a l'interieur du path "/app" (mentionner a la ligne 17)
	   L'argument "app:app" signifie que le fichier d'entree de l'application (la ou est initialiser flask) est nomme app et que le nom de la variable flask est nomme "app" (__app__ = Flask(__name\__)).


- Quelques commandes utile de docker : 
 ``` docker-compose build  ```
  ```docker-compose up  ``` ouvre les services web
  ```docker images  ``` liste toute les images et leur status
  ```docker run <nomImage> ``` fait la meme chose que docker-compose up pour une image.


- Maintenant, on a une application flask qui s'execute a partir d'un serveur. 
  Pour partie l'application il faut lancer : 
  ``` $ docker-compose build  ``` pour "pousser" le code dans l'image
   ```$ docker-compose up  ``` pour debuter un serveur a partir du docker


> **_NOTE:_**  (Docker hot reload). Le probleme avec l'utilisation de docker c'est qu'il n'y a pas de methode prefabriquer fait pour hot relaod et debugger une application python/flask.
La methode suivante va permettre de developper le front end python/flask la recharche de code automatique. En plus, on va pouvoir debugger le code backend python a l'aide de l'interface vscode.

# 3. Partir l'application a partir du docker.
Pour avoir le "hot reload", une facon possible est d'editer les fichiers directement a l'interieur du docker.
Vscode offre une extension qui aide a faire cela.

- Telecharger l'extension "Dev containers" fait par microsoft
- Clicker sur le bouton "><" vert en bas a gauche sur vscode. ctrl+shift+p fonctionne aussi
- Choisir l'option "(re)open folder in container" > from Dockfile
 -> vsCode va creer un dossier .devcontainer avec des configs. 

 
  [*] Les fichiers qui appraissent ici sont les fichier a l'interieur du docker. 
    Lors qu'on modifie un fichier avec devcontainer, ca modifie les fichier aussi 
    a l'interieur du docker. Plus besoin de lancer docker-compose build a chaque fois.
  
  [*] En ouvrant un terminal : Menu en haut vscode > terminal > new Terminal. On voit qu'on se 
    trouve dans le docker dans le workspace.   
  
  [*] Cmds utiles : 
  ``` $ which python; ```  donne le path repertoir ou est installer python 
``` $ python -v```  
  
  [*] Pour quitter ce mode et revenir aux fichiers locaux. Recliquer sur les signes "><".


## 3.1 Lancer python/flask avec reload

Avant de lancer la commande suivante, assurez-vous d'avoir flask version 2.2.0 ou plus. 
Pour ce faire : ```  $flask --version``` . Ouvrir requirements.txt, mettre "flask==2.2.0" et lancer :
``` $ pip install -r requirements; pip freeze > requirements.txt``` 

> **_NOTE:_** Pour ajouter d'autre librairie python, soit l'ajouter dans le fichier requirements.txt ou on peut l'installer normalement avec
```$ pip install python```

Ensuite, on demarre l'application : 
``` $ flask --app app/app --debug run``` 

On peu modifier les fichier front-end, puis f5 la page web pour actualiser 

# 4. Debugger l'application Python flask 

Pour debbuger le back-end, il va falloir ajouter une configuration pour que vsCode soit en mesure
d'executer ligne par ligne.

## 4.1 Installer l'extension python par microsoft dans le docker. 
- Faire une recherche parmis les extensions pour "python" et reinstaller dans l'image du docker.
- Il est possible que vsCode ne charge pas l'interpreteur automatiquement. Il faut : 
 -> ctrl+shift+p > Python: select interpreter

## 4.2 Partir le debbuger
Pour partir le debugger de VsCode il faut ajouter une config le fichier lauch.json
- Clicker sur Le bouton a gauche "Run and debug" (ctrl+shift+d)
- Normalement, il y a un fichier .vscode/lauch.json deja creer. Pour ajouter une config il faut : 
  -> ctrl+shift+p > debug config
- Choisir python > flask > app/app.py
  -> il faut ajouter "app/", car le point d'entre de flask est dans le repertoire app/ 
- Clicker sur le bouton vert run and debug.
> **_NOTE:_** La barre bleu tout en bas devient orange pour indiquer le mode debuging.
- Mettre un breakPoint a la ligne "def hello_world():" (6) en cliquant dans la marge gauche 
  du code (un point rouge devrait apparaitre). S'il n'est pas present, cela veux dire que 
  l'interpreteur python n'est pas choisie (Voir 4.1).
  
- Aller dans un furteur et lancer une requete sur la route "/". 
  VsCode arrete l'execution du code et affiche les variables locals actives. 

#### Trucs utiles pour debugger:  
 - f10 skiper ligne
 - f11 entrer dans une fonction 
 - f5 resumer 
 - f12 voir la definition d'une fonction 
 - Surligner une expression > clique gauche > evaluate in debbug console : 
 -> affiche le resultat. Il est possible de modifier le code en arret et voir le resultat des modification avant que le code soit execute
 - hover over variable -> voir le contenu de l'objet/variable. 

## 4.3 Hot realod ET Debug
Pour faire le hot reload ET le debbug en meme temps il faut modifier la config lauch.json

- supprimer la ligne 19 "--no-reload" (pas oublier la virgule a la fin de la ligne precedente)
- Modifier la ligne 22 (maintenant rendu 21) "justMyCode": false".

Le fichier lauch.json ressemble a ca : 

```
{
    "version": "0.1.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app/app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger"
            ],
            "jinja": true,
            "justMyCode": false
        }
    ]
}
```

> **_NOTE:_**  Remarque: Il n'est pas necessaire d'avoir un environment python sur une machine local.


### Ressources utiles : 

__Youtube :__ 
Container, Python tuto :
https://www.youtube.com/watch?v=cJbvcH0JNGA&t=1s
Django tutoriel, mais claire et pertinant
https://www.youtube.com/watch?v=x7lZAmMVo2M

__vsCode :__  
Flask Tutorial in Visual Studio Code : 
https://code.visualstudio.com/docs/python/tutorial-flask
Python in a container : 
https://code.visualstudio.com/docs/containers/quickstart-python

__vsCode bug report version 1.75 :__
https://github.com/microsoft/vscode/issues/173319














 
