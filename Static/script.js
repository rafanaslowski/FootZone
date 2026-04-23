// mascara para nome, permitindo apenas letras e espaços e limitando a 50 caracteres
function MascaraNome (input) {
    let valor = input.value;
    valor = valor.replace(/[^a-zA-ZÀ-ÿ\s]/g, "");
    input.value = valor;

    if (valor.length > 100) {
        input.value = valor.slice(0, 100);
    }
}

// mascara para cahve de acesso, permitindo apenas números e limitando a 8 caracteres
function mascaraChavedeAcesso (input) {
   let valor = input.value;
    valor = valor.replace(/\D/g, "");
    input.value = valor;

    if (valor.length > 8) {
        input.value = valor.slice(0, 8);
    }
}
//mascara para email, permitindo carateres validos e apenas letras minusculas
function mascaraEmail (input) {
    let valor = input.value;
    valor = valor.replace(/[^a-zA-Z0-9@._-]/g, "");
    input.value = valor.toLowerCase();

    if (valor.length > 100) {
        input.value = valor.slice(0, 100);
    }
}

// mascara para cpf, permitindo apenas números e limitando a 11 caracteres
function mascaraCPF (input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    valor = valor.slice(0,11);

    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    input.value = valor;
}

// mascara para telefone permitindo apenas números e limitando a 11 caracteres e formatando
function mascaraTelefone (input) {
    let valor = input.value;    
    valor = valor.replace(/\D/g, "");
    valor = valor.slice(0,11);

    valor = valor.replace(/(\d{2})(\d)/, "($1) $2");
    valor = valor.replace(/(\d{5})(\d)/, "$1-$2"); 
    
    input.value = valor;
}

// mascara para cnpj, permitindo apenas números e limitando a 14 caracteres e formatando
function mascaraCNPJ (input) {
    let valor = input.value;  
    valor = valor.replace(/\D/g, "");
    valor = valor.slice(0,14); 
         
    valor = valor.replace(/(\d{2})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d)/, "$1/$2");
    valor = valor.replace(/(\d{4})(\d{1,2})$/, "$1-$2");

    input.value = valor;
}

// senha forte
function senhaForte (input) {
    let valor = input.value;
    let regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$/;

    if (!regex.test(valor)) {
        input.setCustomValidity("A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.");
    } else {
        input.setCustomValidity("");
    }
}

// confirmar senha
function confirmarSenha() {
    const senha = document.getElementById("senha");
    const confirmar = document.getElementById("confirmarSenha");
    const erro = document.getElementById("erro-confirmar-senha");

    erro.textContent = "";
    confirmar.style.borderColor = "";

    if (confirmar.value !== senha.value) {
        erro.textContent = "As senhas não coincidem.";
        confirmar.style.borderColor = "red";
        return false;
    }

    return true;
}

// personalização da validação dos campos
function validarCampo(campo) {
    const input = document.getElementById(campo.id);
    const erro = document.getElementById("erro-" + campo.id);

    let valor = input.value.trim();

    if (campo.tipo === 'numero') {
        valor = valor.replace(/\D/g, "");
    }

    // Limpa erros anteriores
    erro.textContent = "";
    input.style.borderColor = "";

    // Validação específica para o campo email
    if (campo.id === "email") {
        if (valor.length < campo.min || !valor.includes("@")) {
            erro.textContent = "Digite um email válido.";
            input.style.borderColor = "red";
            return false;
        }
        return true;
    }

    // Validação genérica para outros campos
    if (valor === "") {
        erro.textContent = `${campo.nome} é obrigatório.`;
        input.style.borderColor = "red";
        return false;
    }

    if (valor.length < campo.min) {
        switch (campo.id) {
            case "nome":
                erro.textContent = "O nome deve ter pelo menos 3 letras.";
                break;
            case "cpf":
                erro.textContent = "CPF deve ter 11 números.";
                break;
            case "telefone":
                erro.textContent = "Telefone inválido.";
                break;
            default:
                erro.textContent = `${campo.nome} inválido.`;
        }

        input.style.borderColor = "red";
        return false;
    }

    return true;
}

// configuração dos campos para validação
const campos = [
    { id: 'nome', nome: 'Nome', min: 3, tipo: 'texto' },
    { id: 'cpf', nome: 'CPF', min: 11, tipo: 'numero' },
    { id: 'email', nome: 'E-mail', min: 5, tipo: 'texto' },
    { id: 'telefone', nome: 'Telefone', min: 11, tipo: 'numero' },
    { id: 'senha', nome: 'Senha', min: 8, tipo: 'texto' },
    { id: 'confirmarSenha', nome: 'ConfirmarSenha', min: 8, tipo: 'texto' }
];

// validação em tempo real
campos.forEach(campo => {
    const input = document.getElementById(campo.id);

    input.addEventListener("input", () => {
        validarCampo(campo);

        if (campo.id === "senha") {
            senhaForte(input);

            const erroSenha = document.getElementById("erro-senha");

            if (!input.checkValidity()) {
                erroSenha.textContent = input.validationMessage;
                input.style.borderColor = "red";
            } else {
                erroSenha.textContent = "";
                input.style.borderColor = "";
            }

            confirmarSenha();
        }
    });
});

document.getElementById("confirmarSenha")
    .addEventListener("input", confirmarSenha);

//  validação ao enviar o formulário
document.getElementById("cadastro").addEventListener("submit", function(event) {

    let formValido = true;

    campos.forEach(campo => {
        if (!validarCampo(campo)) {
            formValido = false;
        }
    });

    // senha forte
    const senha = document.getElementById("senha");
    const erroSenha = document.getElementById("erro-senha");

    if (!senha.checkValidity()) {
        erroSenha.textContent = senha.validationMessage;
        senha.style.borderColor = "red";
        formValido = false;
    } else {
        erroSenha.textContent = "";
        senha.style.borderColor = "";
    }

    // confirmar senha
    if (!confirmarSenha()) {
        formValido = false;
    }

    if (!formValido) {
        event.preventDefault();
    }
});

// visualir senha
function toggleSenha() {
    const input = document.getElementById("senha");

    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}
// visualizar confirmar senha
function toggleConfirmarSenha() {
    const input = document.getElementById("confirmarSenha");

    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}

function toggleSenha() {
    const senhaInput = document.getElementById('senha');
    const tipo = senhaInput.getAttribute('type') === 'password' ? 'text' : 'password';
    senhaInput.setAttribute('type', tipo);
}

// Opcional: Impedir espaços no campo de senha
document.getElementById('senha').addEventListener('input', function(e) {
    this.value = this.value.replace(/\s/g, '');
});