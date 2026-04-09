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

