import pytest
from flask_login import current_user

def test_pagina_publicaciones_sin_login(cliente):

	respuesta=cliente.get("/publicaciones", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho",),("nacho98",),("usuario_correcto",), ("amanda",)]
)
def test_pagina_publicaciones_con_login_usuario_no_existe(cliente, conexion, usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho", "contrasena": "213214hhj&&ff"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["contrasena"],
	[("213214hhj&&ff",),("354354vff",),("2223321",), ("fdfgh&&55fjfkAfh",)]
)
def test_pagina_publicaciones_con_login_usuario_existe_contrasena_error(cliente, conexion, contrasena):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": contrasena})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_publicaciones_con_login_sin_publicaciones(cliente, conexion):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Publicaciones</h1>" in contenido
	assert "Nadie ha publicado aun...¡Se el primero en publicar!" in contenido

def test_pagina_publicaciones_con_login_con_publicaciones(cliente, conexion):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Publicaciones</h1>" in contenido
	assert "Nadie ha publicado aun...¡Se el primero en publicar!" not in contenido
	assert "<h2>Titulo</h2>" in contenido
	assert "Descripcion" in contenido

def test_pagina_publicaciones_con_login_con_publicacion_sin_likes_sin_comentarios(cliente, conexion):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<p class="likes">0</p>' in contenido
	assert '<p class="comentarios">0</p>' in contenido

@pytest.mark.parametrize(["likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_publicaciones_con_login_con_publicacion_con_likes_sin_comentarios(cliente, conexion, likes):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(likes):

		conexion.darLike(id_usuario, id_publicacion)

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f'<p class="likes">{likes}</p>' in contenido
	assert '<p class="comentarios">0</p>' in contenido

@pytest.mark.parametrize(["comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_pagina_publicaciones_con_login_con_publicacion_sin_likes_con_comentarios(cliente, conexion, comentarios):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Contenido")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"}, follow_redirects=True)

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
def test_pagina_publicaciones_con_login_con_publicacion_con_likes_con_comentarios(cliente, conexion, likes, comentarios):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(likes):

		conexion.darLike(id_usuario, id_publicacion)

	for _ in range(comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Contenido")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f'<p class="likes">{likes}</p>' in contenido
	assert f'<p class="comentarios">{comentarios}</p>' in contenido

def test_pagina_logout(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		assert current_user.is_authenticated

		respuesta=cliente_abierto.get('/logout', follow_redirects=True)

		contenido=respuesta.data.decode()

		assert not current_user.is_authenticated

		assert respuesta.status_code==200
		assert "<h1>Iniciar Sesión</h1>" in contenido