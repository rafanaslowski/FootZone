// mascara para nome, permitindo apenas letras e espaços e limitando a 50 caracteres
function MascaraNome (input) {
    let valor = input.value;

    valor = valor.replace(/[^a-zA-ZÀ-ÿ\s]/g, "");
    input.value = valor;

    if (valor.length > 50) {
        input.value = valor.slice(0, 50);
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
    }
