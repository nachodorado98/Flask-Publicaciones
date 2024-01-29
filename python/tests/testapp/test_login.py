import pytest

def test_pagina_inicio_sin_login(cliente):

	respuesta=cliente.get("/inicio", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho",),("nacho98",),("usuario_correcto",), ("amanda",)]
)
def test_pagina_inicio_con_login_usuario_no_existe(cliente, conexion, usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho", "contrasena": "213214hhj&&ff"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["contrasena"],
	[("213214hhj&&ff",),("354354vff",),("2223321",), ("fdfgh&&55fjfkAfh",)]
)
def test_pagina_inicio_con_login_usuario_existe_contrasena_error(cliente, conexion, contrasena):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": contrasena})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_inicio_con_login(cliente, conexion):

	cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":"nacho98", "contrasena":"NachoDorado1998&", "edad":25})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "NachoDorado1998&"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Bienvenido de nuevo: nacho98" in contenido