CREATE DATABASE api_users;
\c api_users;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    cedula_identidad VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    primer_apellido VARCHAR(100) NOT NULL,
    segundo_apellido VARCHAR(100),
    fecha_nacimiento DATE NOT NULL
);