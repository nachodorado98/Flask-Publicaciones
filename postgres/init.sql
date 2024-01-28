CREATE DATABASE bbdd_usuarios;

\c bbdd_usuarios;

CREATE TABLE usuarios (id SERIAL PRIMARY KEY,
    					usuario VARCHAR(255),
						contrasena VARCHAR(255),
						nombre VARCHAR(255),
						apellido VARCHAR(255),
						edad INT);