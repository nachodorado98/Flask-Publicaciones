import pytest

def test_pagina_detalle_sin_login(cliente, conexion):

	respuesta=cliente.get("/detalle_publicacion/1", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_pagina_detalle_con_login_no_existe(cliente, conexion, id_publicacion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_detalle_con_login_existe(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h2>Titulo</h2>" in contenido
		assert "Descripcion" in contenido

def test_pagina_detalle_con_login_existe_sin_likes_sin_comentarios(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<p class="likes">0</p>' in contenido
		assert '<p class="comentarios">0</p>' in contenido

@pytest.mark.parametrize(["likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_detalle_con_login_existe_con_likes_sin_comentarios(cliente, conexion, likes):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		conexion.c.execute("SELECT * FROM usuarios")

		usuarios=conexion.c.fetchall()

		id_usuario=usuarios[0]["id"]

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		for _ in range(likes):

			conexion.darLike(id_usuario, id_publicacion)

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert f'<p class="likes">{likes}</p>' in contenido
		assert '<p class="comentarios">0</p>' in contenido

@pytest.mark.parametrize(["comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_detalle_con_login_existe_sin_likes_con_comentarios(cliente, conexion, comentarios):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		conexion.c.execute("SELECT * FROM usuarios")

		usuarios=conexion.c.fetchall()

		id_usuario=usuarios[0]["id"]

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		for _ in range(comentarios):

			conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<p class="likes">0</p>' in contenido
		assert f'<p class="comentarios">{comentarios}</p>' in contenido
		assert "Comentario" in contenido

@pytest.mark.parametrize(["likes", "comentarios"],
	[
		(2, 13),
		(22, 13),
		(5, 1),
		(13, 5),
		(25, 25)
	]
)
def test_pagina_detalle_con_login_existe_con_likes_con_comentarios(cliente, conexion, likes, comentarios):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		conexion.c.execute("SELECT * FROM usuarios")

		usuarios=conexion.c.fetchall()

		id_usuario=usuarios[0]["id"]

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		for _ in range(likes):

			conexion.darLike(id_usuario, id_publicacion)

		for _ in range(comentarios):

			conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert f'<p class="likes">{likes}</p>' in contenido
		assert f'<p class="comentarios">{comentarios}</p>' in contenido
		assert "Comentario" in contenido

def test_pagina_detalle_likes_sin_login(cliente, conexion):

	respuesta=cliente.get("/detalle_publicacion/1/likes", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_pagina_detalle_likes_con_login_no_existe(cliente, conexion, id_publicacion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}/likes")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_detalle_likes_con_login_existe_sin_like(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}/likes")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location==f"/detalle_publicacion/{id_publicacion}"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_detalle_likes_con_login_existe_con_like(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		conexion.c.execute("SELECT * FROM usuarios")

		usuarios=conexion.c.fetchall()

		id_usuario=usuarios[0]["id"]

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		conexion.darLike(id_usuario, id_publicacion)

		respuesta=cliente_abierto.get(f"/detalle_publicacion/{id_publicacion}/likes")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Le gustó a:" in contenido
		assert "class='usuario'>nacho98</a>"