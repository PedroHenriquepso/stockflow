const token = localStorage.getItem("token");
if (!token) window.location.href = "/";
document.getElementById("nome-usuario").textContent = localStorage.getItem("nome_usuario") || "Vendedor";

document.getElementById("botao-sair").addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "/";
});

let statusAtual = "aberto";

// Carrega os orçamentos do backend
async function carregarOrcamentos() {
  const res = await fetch(`/orcamentos/?status=${statusAtual}`, {
    headers: { "Authorization": `Bearer ${token}` }
  });
  const orcamentos = await res.json();
  
  const tbody = document.getElementById("tabela-orcamentos");
  tbody.innerHTML = "";

  if (orcamentos.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="padding: 20px; text-align: center; color: #64748b;">Nenhum orçamento encontrado.</td></tr>`;
    return;
  }

  orcamentos.forEach(orc => {
    const data = new Date(orc.criado_em).toLocaleDateString('pt-BR');
    const tr = document.createElement("tr");
    tr.style.borderBottom = "1px solid #e2e8f0";
    
    // Define a cor do status
    let corStatus = orc.status === "aberto" ? "#2563eb" : (orc.status === "concluido" ? "#16a34a" : "#dc2626");

    tr.innerHTML = `
      <td style="padding: 12px;"><strong>#${orc.id}</strong></td>
      <td style="padding: 12px;">${data}</td>
      <td style="padding: 12px;">${orc.cliente_id === 1 ? "CONSUMIDOR PADRÃO" : "Cliente " + orc.cliente_id}</td>
      <td style="padding: 12px;">${orc.veiculo_id ? "Veículo " + orc.veiculo_id : "—"}</td>
      <td style="padding: 12px; font-weight: bold;">R$ ${orc.total.toFixed(2)}</td>
      <td style="padding: 12px; color: ${corStatus}; font-weight: bold; text-transform: uppercase;">${orc.status}</td>
      <td style="padding: 12px;">
        <button onclick="abrirOrcamento(${orc.id})" style="color: #2563eb; background: none; border: none; cursor: pointer; font-weight: bold;">Visualizar / Editar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// Troca de status (Em Aberto, Concluídos, Cancelados)
document.querySelectorAll(".btn-status").forEach(btn => {
  btn.addEventListener("click", (e) => {
    // Muda a cor de todos para cinza
    document.querySelectorAll(".btn-status").forEach(b => b.style.background = "#94a3b8");
    // Pinta o clicado de azul
    e.target.style.background = "#2563eb";
    
    statusAtual = e.target.dataset.status;
    carregarOrcamentos();
  });
});

// Mostrar/Esconder campo de busca (F3)
document.getElementById("btn-f3").addEventListener("click", () => {
  const area = document.getElementById("area-busca");
  area.style.display = area.style.display === "none" ? "block" : "none";
  if (area.style.display === "block") document.getElementById("campo-busca").focus();
});

// Novo Orçamento (F9)
document.getElementById("btn-f9").addEventListener("click", () => {
  window.location.href = "/orcamentos/novo"; // Redireciona para a tela de criação
});

// Função para abrir um orçamento (por enquanto vamos só avisar)
window.abrirOrcamento = function(id) {
  alert("Abrindo orçamento #" + id + " (Em breve tela de edição)");
};

// Inicializa
carregarOrcamentos();