// MÁSCARAS
function MascaraNome(input) {
    input.value = input.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, "").slice(0, 100);
}
function mascaraEmail(input) {
    input.value = input.value.replace(/[^a-zA-Z0-9@._-]/g, "").toLowerCase().slice(0, 100);
}
function mascaraCPF(input) {
    let v = input.value.replace(/\D/g, "").slice(0, 11);
    v = v.replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    input.value = v;
}
function mascaraTelefone(input) {
    let v = input.value.replace(/\D/g, "").slice(0, 11);
    v = v.replace(/(\d{2})(\d)/, "($1) $2").replace(/(\d{5})(\d)/, "$1-$2");
    input.value = v;
}

// INTEGRAÇÃO (INSERT E REDIRECIONAMENTO PARA O SELECT)
document.getElementById('btnCadastrar').addEventListener('click', function() {
    const dados = {
        nome: document.getElementById('nome').value,
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value
    };

    if (!dados.nome || !dados.email || !dados.senha) {
        alert("Preencha os campos obrigatórios!");
        return;
    }

    fetch('http://127.0.0.1:5000/usuarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(res => res.json())
    .then(data => {
        if (data.mensagem) {
            alert("Sucesso! " + data.mensagem);
            // PROVA DO SELECT: Redireciona para ver o dado no banco
            window.location.href = "http://127.0.0.1:5000/usuarios";
        } else {
            alert("Erro: " + data.erro);
        }
    })
    .catch(err => alert("Erro de conexão! Verifique o terminal do Python."));
});