// --- MÁSCARAS DE ENTRADA ---
function MascaraNome(input) {
    input.value = input.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, "").slice(0, 100);
}

function mascaraChavedeAcesso(input) {
    input.value = input.value.replace(/\D/g, "").slice(0, 8);
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

// --- VALIDAÇÃO DE SENHA ---
function senhaForte(input) {
    let regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$/;
    if (!regex.test(input.value)) {
        input.setCustomValidity("A senha deve ter 8+ caracteres, maiúsculas, minúsculas, números e símbolos.");
    } else {
        input.setCustomValidity("");
    }
}

function confirmarSenha() {
    const senha = document.getElementById("senha");
    const confirmar = document.getElementById("confirmarSenha");
    if (confirmar.value !== senha.value) {
        confirmar.setCustomValidity("As senhas não coincidem.");
    } else {
        confirmar.setCustomValidity("");
    }
}

// --- CONTROLE DE ENVIO ---
document.addEventListener('DOMContentLoaded', function() {
    // Escuta qualquer formulário de cadastro ou login
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                alert("Verifique os campos! Algumas informações não cumprem os requisitos de segurança.");
                event.preventDefault(); // Trava o envio para o Python se houver erro
            }
        });
    });
});