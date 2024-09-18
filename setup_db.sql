-- Active: 1725969245203@@127.0.0.1@3306@teste
-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS alocacao_professores;
USE alocacao_professores;

-- Inserir dados dos professores
INSERT INTO Professores (nome) VALUES 
('Bruno Morgillo'),
('Carlos'),
('Luciana'),
('Luciano'),
('Danilo');

-- Inserir dados das turmas
INSERT INTO Turmas (nome) VALUES 
('Auckland'),
('Brooklyn'),
('Wyoming'),
('Senegal'),
('Connecticut');

-- Verificar os professores
SELECT * FROM Professores;

-- Verificar as turmas
SELECT * FROM Turmas;

-- Verificar as alocações (inicialmente estará vazia)
SELECT * FROM Alocacoes;