CREATE DATABASE bbdd_usuarios;

\c bbdd_usuarios;

CREATE TABLE usuarios (id SERIAL PRIMARY KEY,
    					usuario VARCHAR(255),
						contrasena VARCHAR(255),
						nombre VARCHAR(255),
						apellido VARCHAR(255),
						edad INT);

CREATE TABLE publicaciones (id SERIAL PRIMARY KEY,
						    id_usuario INTEGER NOT NULL,
						    titulo VARCHAR(255) NOT NULL,
						    descripcion TEXT,
						    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
						    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE);