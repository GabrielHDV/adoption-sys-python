// menu.js
document.addEventListener('DOMContentLoaded', () => {
  fetch('/menu')
    .then(res => res.text())
    .then(html => {
      document.getElementById('menu-container').innerHTML = html;

      // Redirecionamento dos botões com data-link
      document.querySelectorAll('.menu button[data-link]').forEach(btn => {
        btn.addEventListener('click', () => {
          const destino = btn.getAttribute('data-link');
          window.location.href = destino;
        });
      });

      // Logout (pode ser ajustado com base na sua lógica de sessão)
      const logoutBtn = document.getElementById('logout-btn');
      if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
          alert('Você saiu do sistema!');
          window.location.href = 'login.html'; // ou a página de login
        });
      }
    });
});
