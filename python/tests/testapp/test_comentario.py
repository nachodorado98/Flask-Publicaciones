import pytest

def test_pagina_comentar_sin_login(cliente, conexion):

	respuesta=cliente.get("/comentar/1", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_pagina_comentar_con_login_no_existe(cliente, conexion, id_publicacion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get(f"/comentar/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_comentar_con_login_existe(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		respuesta=cliente_abierto.get(f"/comentar/{id_publicacion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>Nuevo Comentario</h1>" in contenido

def test_pagina_insertar_comentario_sin_login(cliente, conexion):

	data={"comentario":"Comentario"}

	respuesta=cliente.post("/insertar_comentario/0", data=data, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_pagina_insertar_comentario_con_login_no_existe(cliente, conexion, id_publicacion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		data={"comentario":"Comentario"}

		respuesta=cliente_abierto.post(f"/insertar_comentario/{id_publicacion}", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_insertar_comentario_con_login_existe_dato_error(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		cliente_abierto.post("/insertar_publicacion", data={"titulo":"Titulo", "descripcion":"Descripcion"})

		conexion.c.execute("SELECT * FROM publicaciones")

		publicaciones=conexion.c.fetchall()

		id_publicacion=publicaciones[0]["id"]

		respuesta=cliente_abierto.post(f"/insertar_comentario/{id_publicacion}", data={})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location==f"/comentar/{id_publicacion}"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_insertar_comentario_con_login_comentario(cliente, conexion):

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

		data={"comentario":"Comentario"}

		respuesta=cliente_abierto.post(f"/insertar_comentario/{id_publicacion}", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/publicaciones"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion.c.execute("SELECT * FROM comentarios")

		comentarios=conexion.c.fetchall()

		assert len(comentarios)==1
		assert comentarios[0]["id_usuario"]==id_usuario
		assert comentarios[0]["id_publicacion"]==id_publicacion

@pytest.mark.parametrize(["numero_comentarios"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_pagina_insertar_comentario_con_login_comentarios(cliente, conexion, numero_comentarios):

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

		data={"comentario":"Comentario"}

		for _ in range(numero_comentarios):

			cliente_abierto.post(f"/insertar_comentario/{id_publicacion}", data=data)

		conexion.c.execute("SELECT * FROM comentarios")
		
		comentarios=conexion.c.fetchall()

		assert len(comentarios)==numero_comentarios