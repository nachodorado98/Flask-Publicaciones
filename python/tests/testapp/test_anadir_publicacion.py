import pytest

def test_pagina_anadir_publicacion_sin_login(cliente, conexion):

	respuesta=cliente.get("/anadir_publicacion", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_anadir_publicacion_con_login(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get("/anadir_publicacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>Nueva Publicacion</h1>" in contenido

def test_pagina_insertar_publicacion_sin_login(cliente, conexion):

	data={"titulo":"Titulo", "descripcion":"Descripcion"}

	respuesta=cliente.post("/insertar_publicacion", data=data, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["data"],
	[
		({"titulo":"Titulo"},),
		({"descripcion":"Descripcion"},),
		({},)
	]
)
def test_pagina_insertar_publicacion_con_login_datos_error(cliente, conexion, data):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.post("/insertar_publicacion", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_publicacion"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_insertar_publicacion_con_login(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		data={"titulo":"Titulo", "descripcion":"Descripcion"}

		respuesta=cliente_abierto.post("/insertar_publicacion", data=data, follow_redirects=True)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>Publicaciones</h1>" in contenido
		assert "Nadie ha publicado aun...¡Se el primero en publicar!" not in contenido
		assert "<h2>Titulo</h2>" in contenido
		assert "Descripcion" in contenido

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	assert len(publicaciones)==1
	assert publicaciones[0]["titulo"]=="Titulo"
	assert publicaciones[0]["descripcion"]=="Descripcion"

def test_pagina_insertar_publicaciones_con_login(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		data={"titulo":"Titulo", "descripcion":"Descripcion"}

		cliente_abierto.post("/insertar_publicacion", data=data)
		cliente_abierto.post("/insertar_publicacion", data=data, follow_redirects=True)
		cliente_abierto.post("/insertar_publicacion", data=data, follow_redirects=True)
		cliente_abierto.post("/insertar_publicacion", data=data, follow_redirects=True)
		cliente_abierto.post("/insertar_publicacion", data=data, follow_redirects=True)

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	assert len(publicaciones)==5