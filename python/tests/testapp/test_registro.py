import pytest

def test_pagina_registro(cliente):

	respuesta=cliente.get("/registro")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Crear Una Cuenta</h1>" in contenido

@pytest.mark.parametrize(["nombre", "apellido", "usuario", "contrasena", "edad"],
	[
		(None, "dorado", "golden98", "contrasena100", "18"),
		("Nacho", None, "golden98", "contrasena100", "18"),
		("nacho", "dorado", None, "djkggjk&/()?", "25"),
		("nacho", "dorado", "golden98", None, "22"),
		("nachodoorado", "dorado", "golden98", "mypassword", None),
		("nach0", "dorado", "nacho98", "nacho98%&/", "19"),
		("nacho", "dor4do", "nacho98", "nacho98%&/", "19"),
		("nacho", "dorado", "nacho_98", "nacho98%hhj", "26"),
		("nacho", "dorado", "nacho98", "nac98%", "99"),
		("nacho", "dorado", "nacho98", "nacho98hhjh$", "17"),
	]
)
def test_pagina_singin_datos_incorrectos(cliente, nombre, apellido, usuario, contrasena, edad):

	respuesta=cliente.post("/singin", data={"nombre":nombre, "apellido":apellido, "usuario":usuario, "contrasena":contrasena, "edad":edad})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("naCho98",),("nacho",),("amanditaa",),("amanda99",)]
)
def test_pagina_singin_usuario_existente(cliente, conexion, usuario):

	conexion.insertarUsuario(usuario, "1234", "nacho", "dorado", 25)

	respuesta=cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":usuario, "contrasena":"12345678aA&", "edad":25})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario", "contrasena"],
	[
		("nacho98", "12345678aA&"),
		("naCho98","NachoDorado1998&"),
		("nacho","contrasena%6T"),
		("amanditaa","Amanda&aranda99"),
		("amanda99","jdfGGjkjkdjkd&&76")
	]
)
def test_pagina_singin_correcto(cliente, conexion, usuario, contrasena):

	respuesta=cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":usuario, "contrasena":contrasena, "edad":25})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert "<p>Gracias por registrarte en nuestra plataforma, Nacho.</p>" in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia!</p>" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["usuarios_agregar"],
	[
		(["nacho98", "naCho98", "nacho", "amanditaa","amanda99"],),
		(["nacho98", "nacho", "amanditaa","amanda99"],),
		(["nacho98", "amanditaa","amanda99"],),
		(["nacho98", "naCho98", "nacho", "amanda99"],),
		(["nacho98", "amanda99"],)
	]
)
def test_pagina_singin_correctos(cliente, conexion, usuarios_agregar):

	for usuario in usuarios_agregar:

		cliente.post("/singin", data={"nombre":"nacho", "apellido":"dorado", "usuario":usuario, "contrasena":"NachoDorado1998&", "edad":25})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==len(usuarios_agregar)