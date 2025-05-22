BEGIN;

CREATE TABLE Cliente(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE Prestador(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE Solicitacao(
    id SERIAL PRIMARY KEY,
    id_cliente INT  REFERENCES Cliente(id),
    id_prestador INT NOT NULL REFERENCES Prestador(id),
    descricao TEXT,
    valor DECIMAL  NOT NULL,
    data_criacao DATE,
    status VARCHAR(30)  NOT NULL
);

CREATE TABLE Reclamacao(
    id SERIAL PRIMARY KEY,
    id_solicitacao INT NOT NULL REFERENCES Solicitacao(id),
    descricao TEXT NOT NULL,
    status VARCHAR(30) NOT NULL
);

CREATE TABLE evidencia(
    id SERIAL PRIMARY KEY,
    id_reclamacao INT NOT NULL REFERENCES Reclamacao(id),
    descricao TEXT NOT NULL,
    data_envio DATE,
    foto VARCHAR(20)
);

CREATE TABLE pagamento(
    id SERIAL PRIMARY KEY,
    id_solicitacao INT NOT NULL REFERENCES Solicitacao(id),
    valor DECIMAL NOT NULL,
    status VARCHAR(30) NOT NULL,
    data_pagamento DATE
);

CREATE TABLE Avalicao(
    id SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL REFERENCES Cliente(id),
    id_prestador INT NOT NULL REFERENCES Prestador(id),
    qtd_estrelas VARCHAR(10) NOT NULL,
    comentario TEXT,
    data_avaliacao DATE
);

CREATE TABLE Especialidade(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL
);

CREATE TABLE Prestador_especialidade(
    id_prestador INT NOT NULL REFERENCES Prestador(id) ON DELETE CASCADE,
    id_especialidade INT  NOT NULL REFERENCES Especialidade(id) ON DELETE CASCADE,
    PRIMARY KEY(id_prestador, id_especialidade)
);

COMMIT;
