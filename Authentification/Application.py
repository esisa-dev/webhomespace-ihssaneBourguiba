import os
import pwd
'''

#home_dir = os.path.expanduser("~")
#print(home_dir)

def lister_sous_repertoires_fichiers():
    # Obtenir le chemin absolu du home directory
    username = "ihssane"
    user_info = pwd.getpwnam(username)
    home_dir  = user_info.pw_dir
    # Initialiser une liste vide pour stocker les sous-répertoires et fichiers
    sous_repertoires_fichiers = []

    # Parcourir tous les fichiers et répertoires dans le home directory
    for root, dirs, files in os.walk(home_dir):
        for name in files:
            # Ajouter le chemin absolu du fichier à la liste
            sous_repertoires_fichiers.append(os.path.join(root, name))
        for name in dirs:
            # Ajouter le chemin absolu du répertoire à la liste
            sous_repertoires_fichiers.append(os.path.join(root, name))

    # Retourner la liste des sous-répertoires et fichiers
    return sous_repertoires_fichiers

sr=[]
sr=lister_sous_repertoires_fichiers()

print(sr)'''

from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    file_count, dir_count, space_used = count_files_and_dirs("/home/ihssane")
    return render_template("Application.html", file_count=file_count, dir_count=dir_count, space_used=space_used)

def count_files_and_dirs(path):
    file_count = 0
    dir_count = 0
    space_used = 0
    for root, dirs, files in os.walk(path):
        for file in fileAuths:
            file_count += 1
            space_used += os.path.getsize(os.path.join(root, file))
        for dir in dirs:
            dir_count += 1
    return file_count, dir_count, space_used

if __name__ == "__main__":
    app.run(debug=True,port=9090)
