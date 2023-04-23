import spwd
import bcrypt
from flask import Flask, send_file,request,redirect, render_template,jsonify
import os
app = Flask(__name__)

def verify_Authentification(username, password):
    try:
        # Récupérer l'entrée utilisateur dans le fichier /etc/shadow
        user_info = spwd.getspnam(username)
        user_password=str(user_info.sp_pwdp)

        '''# Extraire le hash du mot de passe stocké
        hashed_password = user_info.sp_pwdp.encode('utf-8')

        # Vérifier si le hash correspond à bcrypt
        if hashed_password.startswith(b'$2b$'):
            # Vérifier si le mot de passe fourni correspond au hash stocké
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return True
                
        else:
            # Le hash n'est pas reconnu
            return False'''
        
        if password==user_password:
            return True
        else:
            return False
    except KeyError:
        # L'utilisateur n'existe pas
        return False

@app.route('/')
def index():
    return render_template('Authentification.html')

@app.route('/Authentification', methods=['POST'])
def Authentification():
    username = request.form['username']
    #password = request.form['password']
    password = "$y$j9T$F0xjXi6Yjw4wDgGPAAaTP1$xiwyiTXQqrNhWuHQE3eVcgAe.g8SZwhEtPbD5FYQ/Q3"

    #s=str(spwd.getspnam(username))
    # Vérifier si le mot de passe fourni correspond au hash stocké dans /etc/shadow
    if verify_Authentification(username, password):
        return render_template('Application.html')
    else:
        return 'Nom d\'utilisateur ou mot de passe incorrect.', 401


import os


def get_files_and_directories(path):
    files_and_dirs = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            files_and_dirs.append({
                'name': filename,
                'type': 'file',
                'size': os.path.getsize(file_path)
            })
        elif os.path.isdir(file_path):
            files_and_dirs.append({
                'name': filename,
                'type': 'directory',
                'size': 0
            })
    return files_and_dirs


@app.route("/home")
def home():
    path = request.args.get("path", "/home/ihssane")
    if not os.path.exists(path):
        return f"Le chemin {path} n'existe pas.", 404

    if os.path.isfile(path):
        # Rediriger vers la page du fichier
        return redirect(f"/file?path={path}")

    files_and_dirs = get_files_and_directories(path)
    return render_template("Home.html", path=path, files_and_dirs=files_and_dirs, os=os)


@app.route("/file")
def get_file():
    path = request.args.get("path")
    if not os.path.exists(path):
        return f"Le chemin {path} n'existe pas.", 404
    return send_file(path)

@app.route('/files')
def files():
    path = request.args.get('path', '/home/ihssane')
    files = []
    total_size = 0
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            files.append({
                'name': filename,
                'type': 'file',
                'size': os.path.getsize(file_path)
            })
            total_size += os.path.getsize(file_path)
    num_files=len(files)
    response = {
        'files': files,
        'total_size': total_size
    }
    return f"Le nombre des files utilisé par le répertoire /home/ihssane est de {num_files} ."
@app.route('/dirs')
def dirs():
    path = request.args.get('path', '/home/ihssane')
    dirs = []
    total_size = 0
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):
            dirs.append({
                'name': filename,
                'type': 'directory',
                'size': 0
            })
    num_dirs = len(dirs)
    return f"Le nombre des directories utilisé par le répertoire /home/ihssane est de {num_dirs} ."

import shutil

def get_space_used():
    total, used, free = shutil.disk_usage("/home/ihssane")
    space_used = used / (2**30)  # Convertir en gigaoctets
    return space_used
@app.route('/space')
def space():
    space_used = get_space_used()
    return f"L'espace utilisé par le répertoire /home/ihssane est de {space_used:.2f} Go."

if __name__ == '__main__':
    app.run()
