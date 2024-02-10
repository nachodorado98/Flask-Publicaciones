import pytest

def test_pagina_perfil_sin_login(cliente, conexion):

	respuesta=cliente.get("/me", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_perfil_con_login_sin_publicaciones(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get("/me")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>NACHO98</h1>" in contenido
		assert "<p><strong>Numero de Publicaciones:</strong> 0</p>" in contenido
		assert "No has publicado nada aun...¡Publica!" in contenido

def test_pagina_perfil_con_login_con_publicacion(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		respuesta=cliente_abierto.get("/me")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>NACHO98</h1>" in contenido
		assert "<p><strong>Numero de Publicaciones:</strong> 1</p>" in contenido
		assert "No has publicado nada aun...¡Publica!" not in contenido
		assert "<h2>Titulo</h2>" in contenido
		assert "Descripcion" in contenido

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_perfil_con_login_con_publicaciones(cliente, conexion, numero_publicaciones):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		for _ in range(numero_publicaciones):

			cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		respuesta=cliente_abierto.get("/me")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>NACHO98</h1>" in contenido
		assert f"<p><strong>Numero de Publicaciones:</strong> {numero_publicaciones}</p>" in contenido
		assert "No has publicado nada aun...¡Publica!" not in contenido
		assert "<h2>Titulo</h2>" in contenido
		assert "Descripcion" in contenido

def test_pagina_perfil_con_login_con_publicacion_sin_likes_sin_comentarios(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		respuesta=cliente_abierto.get("/me")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<p class="likes">0</p>' in contenido
		assert '<p class="comentarios">0</p>' in contenido

@pytest.mark.parametrize(["likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_perfil_con_login_con_publicacion_con_likes_sin_comentarios(cliente, conexion, likes):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		for _ in range(likes):

			conexion.darLike(id_usuario, id_publicacion)

		respuesta=cliente_abierto.get("/me")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert f'<p class="likes">{likes}</p>' in contenido
		assert '<p class="comentarios">0</p>' in contenido

@pytest.mark.parametrize(["comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_perfil_con_login_con_publicacion_sin_likes_con_comentarios(cliente, conexion, comentarios):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		for _ in range(comentarios):

			conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

		respuesta=cliente_abierto.get("/me")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<p class="likes">0</p>' in contenido
		assert f'<p class="comentarios">{comentarios}</p>' in contenido

@pytest.mark.parametrize(["likes", "comentarios"],
	[
		(2, 13),
		(22, 13),
		(5, 1),
		(13, 5),
		(25, 25)
	]
)
def test_pagina_perfil_con_login_con_publicacion_con_likes_con_comentarios(cliente, conexion, likes, comentarios):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		for _ in range(likes):

			conexion.darLike(id_usuario, id_publicacion)

		for _ in range(comentarios):

			conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

		respuesta=cliente_abierto.get("/me")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert f'<p class="likes">{likes}</p>' in contenido
		assert f'<p class="comentarios">{comentarios}</p>' in contenido