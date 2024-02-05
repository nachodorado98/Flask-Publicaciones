import pytest

def test_pagina_usuario_sin_login(cliente, conexion):

	respuesta=cliente.get("/usuario/1", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["id_usuario"],
	[(2,),(1,),(5,),(13,),(0,)]
)
def test_pagina_usuario_con_login_no_existe(cliente, conexion, id_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/usuario/{id_usuario}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_usuario_con_login_perfil(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		conexion.c.execute("SELECT * FROM usuarios")

		usuarios=conexion.c.fetchall()

		id_usuario=usuarios[0]["id"]

		respuesta=cliente_abierto.get(f"/usuario/{id_usuario}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/me"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_usuario_con_login_sin_publicaciones(cliente, conexion):

	cliente.post("/singin", data={"nombre":"amanda", "apellido":"aranda", "usuario":"amanda99", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/usuario/{id_usuario}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>AMANDA99</h1>" in contenido
		assert "<p><strong>Numero de Publicaciones:</strong> 0</p>" in contenido
		assert "No hay ninguna publicacion de AMANDA99..." in contenido

def test_pagina_usuario_con_login_con_publicacion(cliente, conexion):

	with cliente as cliente_abierto:

		cliente.post("/singin", data={"nombre":"amanda", "apellido":"aranda", "usuario":"amanda99", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "amanda99", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/usuario/{id_usuario}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>AMANDA99</h1>" in contenido
		assert "<p><strong>Numero de Publicaciones:</strong> 1</p>" in contenido
		assert "No hay ninguna publicacion de AMANDA99..." not in contenido
		assert "<h2>Titulo</h2>" in contenido
		assert "Descripcion" in contenido

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_usuario_con_login_con_publicaciones(cliente, conexion, numero_publicaciones):

	with cliente as cliente_abierto:

		cliente.post("/singin", data={"nombre":"amanda", "apellido":"aranda", "usuario":"amanda99", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "amanda99", "contrasena": "NachoDorado1998&"})

		for _ in range(numero_publicaciones):

			cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/usuario/{id_usuario}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>AMANDA99</h1>" in contenido
		assert f"<p><strong>Numero de Publicaciones:</strong> {numero_publicaciones}</p>" in contenido
		assert "No hay ninguna publicacion de AMANDA99..." not in contenido
		assert "<h2>Titulo</h2>" in contenido
		assert "Descripcion" in contenido