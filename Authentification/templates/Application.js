window.onload = function() {
    // Fonction pour mettre à jour les informations sur les fichiers
    function updateFiles() {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          document.getElementById("file-count").innerHTML = response.files.length;
        }
      };
      xhr.open("GET", "http://127.0.0.1:9090/files", true); // le nom de la route Flask est inclus dans l'URL
      xhr.send();
    }
    
    // Fonction pour mettre à jour les informations sur les répertoires
    function updateDirs() {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          document.getElementById("dir-count").innerHTML = response.dirs.length;
        }
      };
      xhr.open("GET", "http://127.0.0.1:9090/dirs", true); // le nom de la route Flask est inclus dans l'URL
      xhr.send();
    }
    
    // Fonction pour mettre à jour les informations sur l'espace utilisé
    function updateSpace() {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          document.getElementById("space-used").innerHTML = response.total_size;
        }
      };
      xhr.open("GET", "http://127.0.0.1:9090/space", true); // le nom de la route Flask est inclus dans l'URL
      xhr.send();
    }
    
    // Mettre à jour les informations sur les fichiers lorsqu'on clique sur le bouton "Files"
    document.getElementById("files-button").addEventListener("click", function() {
      updateFiles();
    });
    
    // Mettre à jour les informations sur les répertoires lorsqu'on clique sur le bouton "Dirs"
    document.getElementById("dirs-button").addEventListener("click", function() {
      updateDirs();
    });
    
    // Mettre à jour les informations sur l'espace utilisé lorsqu'on clique sur le bouton "Space"
    document.getElementById("space-button").addEventListener("click", function() {
      updateSpace();
    });
  };
  