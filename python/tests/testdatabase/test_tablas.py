import pytest

def test_tabla_usuarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["usuario", "contrasena", "nombre", "apellido", "edad"],
	[
		("nacho98", "1234", "nacho", "dorado", 25),
		("nacho948", "12vvnvvb34", "naegcho", "dordado", 215),
		("nacho", "12vvn&fvvb34", "nachitoo", "dordado", 22)
	]
)
def test_insertar_usuario(conexion, usuario, contrasena, nombre, apellido, edad):

	conexion.insertarUsuario(usuario, contrasena, nombre, apellido, edad)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1
	assert usuarios[0]["usuario"]==usuario
	assert usuarios[0]["contrasena"]==contrasena
	assert usuarios[0]["nombre"]==nombre
	assert usuarios[0]["apellido"]==apellido
	assert usuarios[0]["edad"]==edad

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_usuarios(conexion, numero_usuarios):

	for _ in range(numero_usuarios):

		conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==numero_usuarios

def test_existe_usuario_no_existen(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_existe_usuario_existen_no_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	assert not conexion.existe_usuario("nacho99")

def test_existe_usuario_existen_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	assert conexion.existe_usuario("nacho98")

def test_obtener_contrasena_usuario_no_existen(conexion):

	assert conexion.obtenerContrasenaUsuario("nacho98") is None

def test_obtener_contrasena_usuario_existen(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	assert conexion.obtenerContrasenaUsuario("nacho98")=="1234"

def test_obtener_id_usuario_no_existen(conexion):

	assert conexion.obtenerIdUsuario("nacho98") is None

def test_obtener_id_usuario_existen(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	assert conexion.obtenerIdUsuario("nacho98")==id_usuario

def test_id_usuario_no_existen(conexion):

	assert not conexion.existe_id(0)

def test_id_usuario_existen_no_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	assert not conexion.existe_id(1)

def test_usuario_existen_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	assert conexion.existe_id(id_usuario)

def test_obtener_nombre_usuario_usuario_no_existen(conexion):

	assert conexion.obtenerNombreUsuarioUsuario(0) is None

def test_obtener_nombre_usuario_usuario_existe(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	assert conexion.obtenerNombreUsuarioUsuario(id_usuario)=="nacho98"