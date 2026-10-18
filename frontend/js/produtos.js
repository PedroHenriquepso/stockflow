// 1. Verifica login e pega o token
const token = localStorage.getItem("token");
if (!token) window.location.href = "/";

document.getElementById("nome-usuario").textContent = localStorage.getItem("nome_usuario") || "Vendedor";

// 2. Função para sair
document.getElementById("botao-sair").addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "/";
});

// 3. Função para buscar produtos do backend
async function carregarProdutos() {
  const resposta = await fetch("/produtos/", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  
  if (resposta.status === 401) {
    localStorage.clear();
    window.location.href = "/";
    return;
  }

  const produtos = await resposta.json();
  const tabela = document.getElementById("tabela-produtos");
  tabela.innerHTML = ""; // limpa a tabela

  produtos.forEach(produto => {
    const tr = document.createElement("tr");
    tr.style.borderBottom = "1px solid #e2e8f0";
    tr.innerHTML = `
      <td style="padding: 12px 8px;">${produto.id}</td>
      <td style="padding: 12px 8px;"><strong>${produto.nome}</strong></td>
      <td style="padding: 12px 8px;">R$ ${produto.preco_custo.toFixed(2)}</td>
      <td style="padding: 12px 8px;">R$ ${produto.preco_venda.toFixed(2)}</td>
      <td style="padding: 12px 8px;">${produto.estoque_atual} un</td>
      <td style="padding: 12px 8px;">
        <button onclick="deletarProduto(${produto.id})" style="color: #dc2626; background: none; border: none; cursor: pointer; font-weight: 600;">Excluir</button>
      </td>
    `;
    tabela.appendChild(tr);
  });
}

// 4. Cadastrar novo produto
document.getElementById("form-produto").addEventListener("submit", async (e) => {
  e.preventDefault();

  const botao = document.getElementById("botao-cadastrar");
  const msg = document.getElementById("mensagem-feedback");
  
  botao.disabled = true;
  botao.textContent = "Salvando...";
  msg.classList.remove("visivel");

  const novoProduto = {
    nome: document.getElementById("nome").value,
    codigo_barras: document.getElementById("codigo_barras").value || null,
    preco_custo: parseFloat(document.getElementById("preco_custo").value),
    preco_venda: parseFloat(document.getElementById("preco_venda").value),
    estoque_atual: parseInt(document.getElementById("estoque_atual").value),
    estoque_minimo: 0
  };

  try {
    const resposta = await fetch("/produtos/", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}` 
      },
      body: JSON.stringify(novoProduto)
    });

    if (!resposta.ok) throw new Error("Erro ao cadastrar produto");

    // Se deu certo:
    document.getElementById("form-produto").reset();
    msg.textContent = "Produto cadastrado com sucesso!";
    msg.style.background = "#f0fdf4";
    msg.style.color = "#16a34a";
    msg.style.borderColor = "#bbf7d0";
    msg.classList.add("visivel");
    
    carregarProdutos(); // recarrega a tabela
  } catch (erro) {
    msg.textContent = erro.message;
    msg.style.background = "#fef2f2";
    msg.style.color = "#dc2626";
    msg.style.borderColor = "#fecaca";
    msg.classList.add("visivel");
  } finally {
    botao.disabled = false;
    botao.textContent = "Cadastrar Produto";
  }
});

// 5. Excluir produto
async function deletarProduto(id) {
  if (!confirm("Tem certeza que deseja excluir este produto?")) return;

  const resposta = await fetch(`/produtos/${id}`, {
    method: "DELETE",
    headers: { "Authorization": `Bearer ${token}` }
  });

  if (resposta.ok) {
    carregarProdutos(); // recarrega a tabela
  } else {
    alert("Erro ao excluir o produto.");
  }
}

// 6. Carrega a tabela quando a página abre
carregarProdutos();