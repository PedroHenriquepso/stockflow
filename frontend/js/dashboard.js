// 1. Verifica se tem token. Se não tiver, volta para o login.
const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "/";
}

// 2. Mostra o email do usuário logado no canto superior
const email = localStorage.getItem("email") || "usuário";
document.getElementById("nome-usuario").textContent = email;

// 3. Botão "Sair": apaga o token e volta para o login
document.getElementById("botao-sair").addEventListener("click", () => {
  localStorage.removeItem("token");
  localStorage.removeItem("email");
  window.location.href = "/";
});