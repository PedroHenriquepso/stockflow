document.addEventListener("keydown", (e) => {
  // Se estiver digitando em um input, não ativa os atalhos globais
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;

  if (e.key === "Escape") {
    if (window.location.pathname !== "/dashboard") window.location.href = "/dashboard";
  }

  if (e.key === "F3") {
    e.preventDefault();
    // Se estiver na tela de orçamentos, foca a busca
    if (window.location.pathname === "/orcamentos") {
      const btnF3 = document.getElementById("btn-f3");
      if (btnF3) btnF3.click();
    }
  }

  if (e.key === "F9") {
    e.preventDefault();
    // Se estiver na tela de orçamentos, cria um novo
    if (window.location.pathname === "/orcamentos") {
      window.location.href = "/orcamentos/novo";
    }
  }
});