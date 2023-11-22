-- init.sql
CREATE DATABASE IF NOT EXISTS helados_db;
USE helados_db;

CREATE TABLE IF NOT EXISTS helados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sabor VARCHAR(255) NOT NULL,
    precio FLOAT NOT NULL
);

