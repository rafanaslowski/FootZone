-- 1. Cria e usa o banco de dados
CREATE DATABASE IF NOT EXISTS db_footzone;
USE db_footzone;

-- 2. Tabela de Usuários (Ajustada com CPF e Unique)
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE, -- Não deixa repetir email
    cpf VARCHAR(14) NOT NULL UNIQUE,    -- Não deixa repetir CPF
    telefone VARCHAR(20),
    senha_hash VARCHAR(255) NOT NULL    -- Nomeado como senha_hash para segurança
);

-- 3. Tabela de Empresas (Para a sua aba "Empresa")
CREATE TABLE IF NOT EXISTS empresa (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    nome_fantasia VARCHAR(100) NOT NULL,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL
);

-- 4. Tabela de Admins (Para a sua aba "Admin")
CREATE TABLE IF NOT EXISTS administrador (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    chave_acesso VARCHAR(50) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL
);