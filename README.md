
[![Licencia](https://img.shields.io/badge/Licencia-MIT-blue.svg)](LICENSE)

# Publicaciones App

Bienvenido a mi aplicación de publicaciones, una plataforma interactiva diseñada para ayudarte a registrarte y compartir tus publicaciones con el resto de usuarios.

## Tabla de Contenidos
- [Funcionalidades Principales](#funcionalidades-principales)
- [Instrucciones de Uso](#instrucciones-de-uso)
  - [Prerequisitos](#prerequisitos)
  - [Instalación](#instalación)
  - [Tests](#tests)
- [Tecnologías Utilizadas](#tecnologias-utilizadas)
- [Licencia](#licencia)
- [Contacto](#contacto)
## Funcionalidades Principales

- **Registro de Usuario:** Registrate en la aplicacion de manera rápida y sencilla.

- **Login:** Accede a tu sesion con el usuario creado para ti.

- **Registro de Publicaciones:** Registra las publicaciones creadas por ti y los demas usuarios las podran visualizar.

- **Like y Comentarios:** Podras dar like a las publicaciones que mas te han gustado y comentar en ellas.

- **Perfil:** Podras acceder a tu perfil para ver tus datos y publicaciones creadas.

## Instrucciones de Uso

### Prerequisitos

Antes de comenzar, asegúrate de tener instalado Docker en tu máquina. Puedes descargarlo [aquí](https://www.docker.com/get-started).

### Instalación

Para ejecutar la aplicación con Docker:

1. Clona este repositorio con el siguiente comando:

    ```bash
    git clone https://github.com/nachodorado98/Flask-Publicaciones.git
    ```

2. Navega al directorio del proyecto.

3. Ejecuta el siguiente comando para construir y levantar los contenedores:

    ```bash
    docker-compose up
    ```

4. Accede a la aplicación desde tu navegador web: `http://localhost:5000`.

### Tests

Para ejecutar los tests de la aplicación:

1. Asegúrate de que los contenedores estén en funcionamiento. Si aún no has iniciado los contenedores, utiliza el siguiente comando:

    ```bash
    docker-compose up
    ```

2. Dentro del contenedor de la aplicaicon, cambia al directorio de los tests:

    ```bash
    cd tests
    ```

3. Ejecuta el siguiente comando para ejecutar los tests utilizando pytest:

    ```bash
    pytest
    ```

Este comando ejecutará todas las pruebas en el directorio `tests` y mostrará los resultados en la consola.


## Tecnologías Utilizadas

- [![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
- [![flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
- [![postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
- [![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [![css](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [![docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
## Licencia

Este proyecto está bajo la licencia MIT. Para mas informacion ver `LICENSE.txt`.
## 🔗 Contacto
[![portfolio](https://img.shields.io/badge/proyecto-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/nachodorado98/Flask-Publicaciones)

[![email](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:natxo98@gmail.com)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nacho-dorado-ruiz-339209237/)
