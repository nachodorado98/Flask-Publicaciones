import pytest

def test_pagina_like_sin_login(cliente, conexion):

	respuesta=cliente.get("/dar_like/1", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_pagina_like_con_login_no_existe(cliente, conexion, id_publicacion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/dar_like/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_like_con_login_existe_like_dado(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		conexion.c.execute("SELECT * FROM usuarios")

		usuarios=conexion.c.fetchall()

		id_usuario=usuarios[0]["id"]

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		conexion.darLike(id_usuario, id_publicacion)

		respuesta=cliente_abierto.get(f"/dar_like/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_like_con_login_existe_like_no_dado(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		conexion.c.execute("SELECT * FROM usuarios")

		usuarios=conexion.c.fetchall()

		id_usuario=usuarios[0]["id"]

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		respuesta=cliente_abierto.get(f"/dar_like/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion.c.execute("SELECT * FROM likes")

		likes=conexion.c.fetchall()

		assert len(likes)==1
		assert likes[0]["id_usuario"]==id_usuario
		assert likes[0]["id_publicacion"]==id_publicacion