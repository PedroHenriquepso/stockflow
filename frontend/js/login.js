document.getElementById("form-login").addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;
  const botao = document.getElementById("botao-entrar");
  const erro = document.getElementById("mensagem-erro");

  erro.classList.remove("visivel");
  botao.disabled = true;
  botao.textContent = "Entrando...";

  try {
    // O FastAPI espera os dados como formulário (form-urlencoded), não JSON
    const corpo = new URLSearchParams();
    corpo.append("username", email);
    corpo.append("password", senha);

    const resposta = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: corpo,
    });

    if (!resposta.ok) {
      if (resposta.status === 401) {
        throw new Error("Email ou senha incorretos");
      }
      throw new Error("Erro ao fazer login. Tente novamente.");
    }

    const dados = await resposta.json();
    localStorage.setItem("token", dados.access_token);
    localStorage.setItem("email", email);

    window.location.href = "/dashboard";
  } catch (e) {
    erro.textContent = e.message;
    erro.classList.add("visivel");
    botao.disabled = false;
    botao.textContent = "Entrar";
  }
});