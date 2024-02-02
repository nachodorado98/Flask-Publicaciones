def test_pagina_anadir_publicacion_sin_login(cliente):

	respuesta=cliente.get("/anadir_publicacion", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_anadir_publicacion_con_login(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"})

		respuesta=cliente_abierto.get("/anadir_publicacion", follow_redirects=True)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>Nueva Publicacion</h1>" in contenido