const token = localStorage.getItem("token");
if (!token) window.location.href = "/";
document.getElementById("nome-usuario").textContent = localStorage.getItem("nome_usuario") || "Vendedor";

document.getElementById("botao-sair").addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "/";
});

// Força letras maiúsculas
document.querySelectorAll('input[type="text"]').forEach(input => {
  input.addEventListener('input', function() { this.value = this.value.toUpperCase(); });
});

// Variáveis globais
let itens = [];
let produtos = [];

async function carregarProdutos() {
  const res = await fetch("/produtos/", { headers: { "Authorization": `Bearer ${token}` } });
  produtos = await res.json();
}

// ================= BUSCA DE CLIENTE =================
const inputCliente = document.getElementById("busca-cliente");
const divSugestoesCliente = document.createElement("div");
divSugestoesCliente.style.cssText = "background: white; border: 1px solid #ccc; position: absolute; z-index: 10; width: 100%; display: none;";
inputCliente.parentElement.appendChild(divSugestoesCliente);

inputCliente.addEventListener("input", async function() {
  const termo = this.value.trim();
  if (termo.length < 1) { divSugestoesCliente.style.display = "none"; return; }

  const res = await fetch(`/clientes/buscar/${termo}`, { headers: { "Authorization": `Bearer ${token}` } });
  const clientes = await res.json();
  
  if (clientes.length === 0) { divSugestoesCliente.style.display = "none"; return; }

  divSugestoesCliente.innerHTML = "";
  divSugestoesCliente.style.display = "block";

  clientes.forEach(c => {
    const div = document.createElement("div");
    div.style.padding = "10px";
    div.style.cursor = "pointer";
    div.style.borderBottom = "1px solid #eee";
    div.innerHTML = `<strong>CÓD: ${c.id}</strong> - ${c.nome}`;
    div.addEventListener("click", () => {
      inputCliente.value = c.nome;
      document.getElementById("cliente-id").value = c.id;
      document.getElementById("cliente-nome").textContent = c.nome;
      divSugestoesCliente.style.display = "none";
    });
    divSugestoesCliente.appendChild(div);
  });
});

// ================= BUSCA DE VEÍCULO =================
const inputVeiculo = document.getElementById("busca-veiculo");
const divSugestoesVeiculo = document.createElement("div");
divSugestoesVeiculo.style.cssText = "background: white; border: 1px solid #ccc; position: absolute; z-index: 10; width: 100%; display: none;";
inputVeiculo.parentElement.appendChild(divSugestoesVeiculo);

inputVeiculo.addEventListener("input", async function() {
  const termo = this.value.trim();
  if (termo.length < 3) { divSugestoesVeiculo.style.display = "none"; return; }

  const res = await fetch(`/veiculos/buscar/${termo}`, { headers: { "Authorization": `Bearer ${token}` } });
  const veiculos = await res.json();
  
  if (veiculos.length === 0) { divSugestoesVeiculo.style.display = "none"; return; }

  divSugestoesVeiculo.innerHTML = "";
  divSugestoesVeiculo.style.display = "block";

  veiculos.forEach(v => {
    const div = document.createElement("div");
    div.style.padding = "10px";
    div.style.cursor = "pointer";
    div.style.borderBottom = "1px solid #eee";
    div.innerHTML = `<strong>${v.placa}</strong> - ${v.marca} ${v.modelo}`;
    div.addEventListener("click", () => {
      inputVeiculo.value = `${v.placa} - ${v.modelo}`;
      document.getElementById("veiculo-id").value = v.id;
      divSugestoesVeiculo.style.display = "none";
    });
    divSugestoesVeiculo.appendChild(div);
  });
});

// ================= BUSCA DE PRODUTO =================
document.getElementById("busca-produto").addEventListener("input", function() {
  const termo = this.value.toUpperCase();
  const divSugestoes = document.getElementById("sugestoes-produto");
  
  if (termo.length < 1) { divSugestoes.style.display = "none"; return; }

  const filtrados = produtos.filter(p => 
    (p.codigo_interno && p.codigo_interno.toUpperCase().includes(termo)) || 
    p.nome.toUpperCase().includes(termo)
  ).slice(0, 5);

  if (filtrados.length === 0) { divSugestoes.style.display = "none"; return; }

  divSugestoes.innerHTML = "";
  divSugestoes.style.display = "block";

  filtrados.forEach(p => {
    const item = document.createElement("div");
    item.style.padding = "10px";
    item.style.cursor = "pointer";
    item.style.borderBottom = "1px solid #eee";
    item.innerHTML = `<strong>${p.codigo_interno || ''}</strong> - ${p.nome} (Estoque: ${p.estoque_atual})`;
    
    item.addEventListener("click", () => {
      document.getElementById("busca-produto").value = p.nome;
      document.getElementById("busca-produto").dataset.id = p.id;
      document.getElementById("busca-produto").dataset.preco = p.preco_venda;
      divSugestoes.style.display = "none";
    });
    
    divSugestoes.appendChild(item);
  });
});

// ================= ADICIONAR ITEM =================
document.getElementById("botao-adicionar").addEventListener("click", () => {
  const inputBusca = document.getElementById("busca-produto");
  const produtoId = inputBusca.dataset.id;
  const preco = parseFloat(inputBusca.dataset.preco);
  const qtd = parseInt(document.getElementById("qtd-produto").value);
  const nome = inputBusca.value;

  if (!produtoId || !preco) { alert("Selecione um produto válido na lista."); return; }
  if (qtd < 1) { alert("Quantidade inválida."); return; }

  itens.push({ produto_id: parseInt(produtoId), nome: nome, quantidade: qtd, preco_unitario: preco });
  inputBusca.value = "";
  inputBusca.dataset.id = "";
  document.getElementById("qtd-produto").value = 1;
  atualizarTabela();
});

// ================= ATUALIZAR TABELA =================
function atualizarTabela() {
  const tbody = document.getElementById("tabela-itens");
  tbody.innerHTML = "";
  let bruto = 0;

  itens.forEach((item, index) => {
    const totalItem = item.quantidade * item.preco_unitario;
    bruto += totalItem;
    const tr = document.createElement("tr");
    tr.style.borderBottom = "1px solid #e2e8f0";
    tr.innerHTML = `
      <td style="padding: 10px;">${index + 1}</td>
      <td style="padding: 10px;">${item.nome}</td>
      <td style="padding: 10px;">${item.quantidade}</td>
      <td style="padding: 10px;">R$ ${item.preco_unitario.toFixed(2)}</td>
      <td style="padding: 10px;">R$ ${totalItem.toFixed(2)}</td>
      <td style="padding: 10px;"><button onclick="removerItem(${index})" style="color:red; border:none; background:none; cursor:pointer;">X</button></td>
    `;
    tbody.appendChild(tr);
  });
  document.getElementById("total-bruto").textContent = `R$ ${bruto.toFixed(2)}`;
  calcularTotal(bruto);
}

window.removerItem = function(index) {
  itens.splice(index, 1);
  atualizarTabela();
};

function calcularTotal(bruto) {
  const descPct = parseFloat(document.getElementById("desconto-porcentagem").value) || 0;
  const descVal = parseFloat(document.getElementById("desconto-valor").value) || 0;
  let desconto = descPct > 0 ? bruto * (descPct / 100) : (descVal > 0 ? descVal : 0);
  document.getElementById("total-final").textContent = `R$ ${(bruto - desconto).toFixed(2)}`;
}

document.getElementById("desconto-porcentagem").addEventListener("input", () => {
  const bruto = itens.reduce((acc, i) => acc + (i.quantidade * i.preco_unitario), 0);
  calcularTotal(bruto);
});
document.getElementById("desconto-valor").addEventListener("input", () => {
  const bruto = itens.reduce((acc, i) => acc + (i.quantidade * i.preco_unitario), 0);
  calcularTotal(bruto);
});

// ================= SALVAR =================
document.getElementById("botao-salvar").addEventListener("click", async () => {
  if (itens.length === 0) { alert("Adicione itens ao orçamento."); return; }

  const clienteId = parseInt(document.getElementById("cliente-id").value);
  const veiculoId = document.getElementById("veiculo-id").value ? parseInt(document.getElementById("veiculo-id").value) : null;
  const descPct = parseFloat(document.getElementById("desconto-porcentagem").value) || 0;
  const descVal = parseFloat(document.getElementById("desconto-valor").value) || 0;

  const payloadItens = itens.map(i => ({ produto_id: i.produto_id, quantidade: i.quantidade, desconto_item: 0 }));

  const payload = {
    cliente_id: clienteId,
    veiculo_id: veiculoId,
    desconto_porcentagem: descPct,
    desconto_valor: descVal,
    itens: payloadItens
  };

  const res = await fetch("/orcamentos/", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    alert("Orçamento salvo com sucesso!");
    window.location.href = "/orcamentos"; // Volta para a lista
  } else {
    const erro = await res.json();
    alert("Erro ao salvar: " + (erro.detail || "Erro desconhecido"));
  }
});

carregarProdutos();