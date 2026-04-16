-- =====================
-- CRIAR BANCO
-- =====================
CREATE DATABASE marketplace_tenis;
USE marketplace_tenis;

-- =====================
-- TABELAS
-- =====================

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cliente (
    id_usuario INT PRIMARY KEY,
    cpf CHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    endereco VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE admin (
    id_usuario INT PRIMARY KEY,
    nivel_acesso INT NOT NULL,
    departamento VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE empresa (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    nome_empresa VARCHAR(150) NOT NULL,
    cnpj CHAR(14) NOT NULL UNIQUE,
    endereco VARCHAR(255),
    telefone VARCHAR(20),
    id_admin INT,
    FOREIGN KEY (id_admin) REFERENCES admin(id_usuario)
        ON DELETE SET NULL
);

CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255)
);

CREATE TABLE produto (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT DEFAULT 0,
    tamanho VARCHAR(10),
    marca VARCHAR(100),
    id_categoria INT NOT NULL,
    id_empresa INT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
        ON DELETE RESTRICT,
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa)
        ON DELETE CASCADE
);

CREATE TABLE produto_imagem (
    id_imagem INT AUTO_INCREMENT PRIMARY KEY,
    id_produto INT NOT NULL,
    url VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
        ON DELETE CASCADE
);

CREATE TABLE favorito (
    id_favorito INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    data_adicionado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario)
        ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
        ON DELETE CASCADE,
    UNIQUE (id_cliente, id_produto)
);

CREATE TABLE carrinho (
    id_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL UNIQUE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE item_carrinho (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_carrinho INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (id_carrinho) REFERENCES carrinho(id_carrinho)
        ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
        ON DELETE CASCADE
);

CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_pagamento DATETIME NULL,
    status ENUM('pendente','pago','cancelado') DEFAULT 'pendente',
    forma_pagamento ENUM('boleto','cartao','pix','transferencia') DEFAULT 'pix',
    total DECIMAL(10,2) NOT NULL,
    id_cliente INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE item_pedido (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
        ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
        ON DELETE CASCADE
);

CREATE TABLE avaliacao (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    nota INT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario)
        ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
        ON DELETE CASCADE
);

-- =====================
-- INSERTS
-- =====================

-- Usuario (cliente)
INSERT INTO usuario (nome, email, senha_hash)
VALUES ('João Silva', 'joao@email.com', 'hash123');

-- Cliente
INSERT INTO cliente (id_usuario, cpf, telefone, endereco)
VALUES (1, '12345678901', '11999999999', 'Rua A, 123');

-- Usuario (admin)
INSERT INTO usuario (nome, email, senha_hash)
VALUES ('Admin Master', 'admin@email.com', 'hashadmin');

-- Admin
INSERT INTO admin (id_usuario, nivel_acesso, departamento)
VALUES (2, 1, 'TI');

-- Empresa
INSERT INTO empresa (nome_empresa, cnpj, endereco, telefone, id_admin)
VALUES ('Nike Store', '12345678000199', 'Av Central, 500', '1133334444', 2);

-- Categoria
INSERT INTO categoria (nome, descricao)
VALUES ('Corrida', 'Tênis para corrida e treino'),
       ('Casual', 'Tênis para uso diário'),
       ('Basquete', 'Tênis esportivos de quadra');

-- Produto
INSERT INTO produto (nome, descricao, preco, estoque, tamanho, marca, id_categoria, id_empresa)
VALUES ('Tênis Air Max', 'Tênis confortável para corrida', 599.90, 10, '42', 'Nike', 1, 1);

-- Produto Imagem
INSERT INTO produto_imagem (id_produto, url)
VALUES (1, 'https://imagem.com/tenis1.jpg');

-- Favorito
INSERT INTO favorito (id_cliente, id_produto)
VALUES (1, 1);

-- Carrinho
INSERT INTO carrinho (id_cliente)
VALUES (1);

INSERT INTO item_carrinho (id_carrinho, id_produto, quantidade)
VALUES (1, 1, 1);

-- Pedido
INSERT INTO pedido (id_cliente, status, forma_pagamento, total)
VALUES (1, 'pendente', 'pix', 1199.80);

-- Item Pedido
INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario)
VALUES (1, 1, 2, 599.90);

-- Avaliação
INSERT INTO avaliacao (id_cliente, id_produto, nota, comentario)
VALUES (1, 1, 5, 'Excelente produto!');

-- =====================
-- MOSTRAR TABELAS
-- =====================

SHOW TABLES;

-- =====================
-- MOSTRAR DADOS
-- =====================

SELECT * FROM usuario;
SELECT * FROM cliente;
SELECT * FROM admin;
SELECT * FROM empresa;
SELECT * FROM produto;
SELECT * FROM produto_imagem;
SELECT * FROM categoria;
SELECT * FROM favorito;
SELECT * FROM carrinho;
SELECT * FROM item_carrinho;
SELECT * FROM pedido;
SELECT * FROM item_pedido;
SELECT * FROM avaliacao;