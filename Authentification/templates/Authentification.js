//Authentification.js

import './Authentification.py';

const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    
    const username = form.username.value.trim();
    const password = form.password.value.trim();
  
    if (username === '') {
      alert('Veuillez entrer un nom d\'utilisateur.');
      return;
    }
  
    if (password === '') {
      alert('Veuillez entrer un mot de passe.');
      return;
    }
  
    fetch('/Authentification', {
      method: 'POST',
      body: new FormData(form)
    })
    .then(response => response.text())
    .then(result => alert(result))
    .catch(error => console.error(error));
});