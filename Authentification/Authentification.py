import spwd
import bcrypt
from flask import Flask, session,send_file,request,redirect, render_template,jsonify
import os
import logging
import secrets
import zipfile


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

home_directory = os.path.expanduser("~")
def verify_Authentification(username, password):
    try:
        user_info = spwd.getspnam(username)
        #user_password=str(user_info.sp_pwdp)
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
        
        if username==user_info.sp_namp:
            return True
            
        else:
            return False
    except KeyError:
        return False


@app.route('/')
def index():
    return render_template('Authentification.html')

@app.route('/Authentification', methods=['POST'])
def Authentification():
    username = request.form['username']
    #password = request.form['password']
    password = "$y$j9T$F0xjXi6Yjw4wDgGPAAaTP1$xiwyiTXQqrNhWuHQE3eVcgAe.g8SZwhEtPbD5FYQ/Q3"

    if verify_Authentification(username, password):
        session['username'] = username
        app.logger.info(f'User {username} logged in')
        return render_template('Application.html')
    else:
        app.logger.info(f'User {username} failed logging in')
        return 'Nom d\'utilisateur ou mot de passe incorrect.', 401

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
    path = request.args.get("path", home_directory )
    if not os.path.exists(path):
        return f"Le chemin {path} n'existe pas.", 404

    if os.path.isfile(path):
        
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
    path = request.args.get('path', home_directory )
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
    return f"Le nombre des files utilisé par le répertoire {home_directory} est de {num_files} ."
@app.route('/dirs')
def dirs():
    path = request.args.get('path', home_directory )
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
    return f"Le nombre des directories utilisé par le répertoire {home_directory} est de {num_dirs} ."

import shutil

def get_space_used():
    total, used, free = shutil.disk_usage(home_directory )
    space_used = used / (2**30) 
    return space_used
@app.route('/space')
def space():
    space_used = get_space_used()
    return f"L'espace utilisé par le répertoire {home_directory } est de {space_used:.2f} Go."

@app.route('/search')
def search():
    query = request.args.get('search')
    path = home_directory 
    files_and_dirs = []

    for filename in os.listdir(path):
        if query in filename:
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                files_and_dirs.append({
                    'name': f'<a href="/file?path={file_path}">{filename}</a>',
                    'type': 'file',
                    'size': os.path.getsize(file_path)
                })
            elif os.path.isdir(file_path):
                files_and_dirs.append({
                    'name': f'<a href="/home?path={file_path}">{filename}</a>',
                    'type': 'directory',
                    'size': 0
                })
    return render_template('Search.html', query=query, files_and_dirs=files_and_dirs)


@app.route("/download")
def download():
    path = home_directory 
    if not os.path.exists(path):
        return f"Le chemin {path} n'existe pas.", 404
    
    zip_file_path = "/tmp/home.zip"
    with zipfile.ZipFile(zip_file_path, "w") as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path)
        
        username = session['username']
        app.logger.info(f'User {username} downloaded {home_directory}')


    return send_file(zip_file_path, as_attachment=True)
    

@app.route('/logout')
def logout():
    username = session['username']
    app.logger.info(f'User {username} logged out')
    session.pop('username', None)
    return redirect('/')



if __name__ == '__main__':
    app.run()
