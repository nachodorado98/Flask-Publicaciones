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

def test_id_usuario_existen_existente(conexion):

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

def test_tabla_publicaciones_vacia(conexion):

	conexion.c.execute("SELECT * FROM publicaciones")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["titulo", "descripcion"],
	[
		("Titulo", "Descripcion"),
		("Me gustan los buses", "Descripcion buses"),
		("Atleti", "Simplemente ATM e basta")
	]
)
def test_insertar_publicacion(conexion, titulo, descripcion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, titulo, descripcion)

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	assert len(publicaciones)==1
	assert publicaciones[0]["id_usuario"]==id_usuario
	assert publicaciones[0]["titulo"]==titulo
	assert publicaciones[0]["descripcion"]==descripcion

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_publicaciones(conexion, numero_publicaciones):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	for _ in range(numero_publicaciones):

		conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	assert len(publicaciones)==numero_publicaciones

def test_obtener_publicaciones_no_existen(conexion):

	assert conexion.obtenerPublicaciones() is None

def test_obtener_publicaciones_existe(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][3]=="nacho98"

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_existen(conexion, numero_publicaciones):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	for _ in range(numero_publicaciones):

		conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==numero_publicaciones
	assert publicaciones[0][0]>publicaciones[-1][0]

def test_obtener_datos_perfil_no_existen(conexion):

	assert conexion.obtenerPerfil(0) is None

def test_obtener_datos_perfil_existen_no_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	assert conexion.obtenerPerfil(1) is None

def test_obtener_datos_perfil_existen_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	assert conexion.obtenerPerfil(id_usuario)==("nacho dorado", 25)

def test_numero_publicaciones_no_existe_usuario(conexion):

	assert conexion.numero_publicaciones(0)==0

def test_numero_publicaciones_existe_usuario_sin_publicaciones(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	assert conexion.numero_publicaciones(id_usuario)==0

def test_numero_publicaciones_existe_usuario_con_publicacion(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	assert conexion.numero_publicaciones(id_usuario)==1

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_numero_publicaciones_existe_usuario_con_publicaciones(conexion, numero_publicaciones):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	for _ in range(numero_publicaciones):

		conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	assert conexion.numero_publicaciones(id_usuario)==numero_publicaciones

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_numero_publicaciones_existe_usuario_con_publicaciones_varios_usuarios(conexion, numero_publicaciones):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios where usuario='nacho98'")

	usuarios_nacho=conexion.c.fetchall()

	id_usuario_nacho=usuarios_nacho[0]["id"]

	for _ in range(numero_publicaciones):

		conexion.insertarPublicacion(id_usuario_nacho, "Titulo", "Descripcion")

	conexion.insertarUsuario("amanda99", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios where usuario='amanda99'")

	usuarios_amanda=conexion.c.fetchall()

	id_usuario_amanda=usuarios_amanda[0]["id"]

	conexion.insertarPublicacion(id_usuario_amanda, "Titulo", "Descripcion")
	conexion.insertarPublicacion(id_usuario_amanda, "Titulo", "Descripcion")
	conexion.insertarPublicacion(id_usuario_amanda, "Titulo", "Descripcion")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==numero_publicaciones+3
	assert conexion.numero_publicaciones(id_usuario_nacho)==numero_publicaciones

def test_publicaciones_usuario_no_existe_usuario(conexion):

	assert conexion.publicaciones_usuario(0) is None

def test_publicaciones_usuario_existe_usuario_sin_publicaciones(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	assert conexion.publicaciones_usuario(id_usuario) is None

def test_publicaciones_usuario_existe_usuario_con_publicacion(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][3]=="nacho98"

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_publicaciones_usuario_existe_usuario_con_publicaciones(conexion, numero_publicaciones):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	for _ in range(numero_publicaciones):

		conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==numero_publicaciones

@pytest.mark.parametrize(["numero_publicaciones"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_publicaciones_usuario_existe_usuario_con_publicaciones_varios_usuarios(conexion, numero_publicaciones):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios where usuario='nacho98'")

	usuarios_nacho=conexion.c.fetchall()

	id_usuario_nacho=usuarios_nacho[0]["id"]

	for _ in range(numero_publicaciones):

		conexion.insertarPublicacion(id_usuario_nacho, "Titulo", "Descripcion")

	conexion.insertarUsuario("amanda99", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios where usuario='amanda99'")

	usuarios_amanda=conexion.c.fetchall()

	id_usuario_amanda=usuarios_amanda[0]["id"]

	conexion.insertarPublicacion(id_usuario_amanda, "Titulo", "Descripcion")
	conexion.insertarPublicacion(id_usuario_amanda, "Titulo", "Descripcion")
	conexion.insertarPublicacion(id_usuario_amanda, "Titulo", "Descripcion")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==numero_publicaciones+3

	publicaciones_nacho=conexion.publicaciones_usuario(id_usuario_nacho)

	assert len(publicaciones_nacho)==numero_publicaciones

def test_tabla_likes_vacia(conexion):

	conexion.c.execute("SELECT * FROM likes")

	assert not conexion.c.fetchall()

def test_id_publicacion_no_existen(conexion):

	assert not conexion.existe_id_publicacion(0)

def test_id_publicacion_existen_no_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	assert not conexion.existe_id_publicacion(1)

def test_id_publicacion_existen_existente(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	assert conexion.existe_id_publicacion(id_publicacion)

def test_insertar_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.darLike(id_usuario, id_publicacion)

	conexion.c.execute("SELECT * FROM likes")

	likes=conexion.c.fetchall()

	assert len(likes)==1
	assert likes[0]["id_usuario"]==id_usuario
	assert likes[0]["id_publicacion"]==id_publicacion

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_likes(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	conexion.c.execute("SELECT * FROM likes")

	likes=conexion.c.fetchall()

	assert len(likes)==numero_likes

def test_like_dado_no_existen(conexion):

	assert not conexion.like_dado(1, 1)

def test_like_dado_existen_no_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	assert not conexion.like_dado(id_usuario, id_publicacion)

def test_like_dado_existen_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.darLike(id_usuario, id_publicacion)

	assert conexion.like_dado(id_usuario, id_publicacion)

def test_like_dado_existen_likes(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(5):

		conexion.darLike(id_usuario, id_publicacion)

	assert conexion.like_dado(id_usuario, id_publicacion)

def test_obtener_publicaciones_existe_sin_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==0

def test_obtener_publicaciones_existe_con_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.darLike(id_usuario, id_publicacion)

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==1

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_existe_con_likes(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==numero_likes

def test_obtener_publicaciones_usuario_existe_sin_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==0

def test_obtener_publicaciones_usuario_existe_con_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.darLike(id_usuario, id_publicacion)

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==1

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_usuario_existe_con_likes(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==numero_likes

def test_tabla_comentarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM comentarios")

	assert not conexion.c.fetchall()

def test_insertar_comentario(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	conexion.c.execute("SELECT * FROM comentarios")

	comentarios=conexion.c.fetchall()

	assert len(comentarios)==1
	assert comentarios[0]["id_usuario"]==id_usuario
	assert comentarios[0]["id_publicacion"]==id_publicacion

@pytest.mark.parametrize(["numero_comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_comentarios(conexion, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	conexion.c.execute("SELECT * FROM comentarios")

	comentarios=conexion.c.fetchall()

	assert len(comentarios)==numero_comentarios

def test_obtener_publicaciones_existe_sin_comentario(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-1]==0

def test_obtener_publicaciones_existe_con_comentario(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-1]==1

@pytest.mark.parametrize(["numero_comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_existe_con_comentarios(conexion, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-1]==numero_comentarios

def test_obtener_publicaciones_usuario_existe_sin_comentario(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-1]==0

def test_obtener_publicaciones_usuario_existe_con_comentario(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-1]==1

@pytest.mark.parametrize(["numero_comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_usuario_existe_con_comentarios(conexion, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-1]==numero_comentarios

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_existe_con_likes_sin_comentarios(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==numero_likes
	assert publicaciones[0][-1]==0

@pytest.mark.parametrize(["numero_comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_existe_sin_likes_con_comentarios(conexion, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==0
	assert publicaciones[0][-1]==numero_comentarios

@pytest.mark.parametrize(["numero_likes", "numero_comentarios"],
	[
		(2, 5),
		(22, 10),
		(5, 1),
		(13, 22),
		(25, 25)
	]
)
def test_obtener_publicaciones_existe_con_likes_con_comentarios(conexion, numero_likes, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.obtenerPublicaciones()

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==numero_likes
	assert publicaciones[0][-1]==numero_comentarios

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_usuario_existe_con_likes_sin_comentarios(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==numero_likes
	assert publicaciones[0][-1]==0

@pytest.mark.parametrize(["numero_comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_obtener_publicaciones_usuario_existe_sin_likes_con_comentarios(conexion, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==0
	assert publicaciones[0][-1]==numero_comentarios

@pytest.mark.parametrize(["numero_likes", "numero_comentarios"],
	[
		(2, 5),
		(22, 10),
		(5, 1),
		(13, 22),
		(25, 25)
	]
)
def test_obtener_publicaciones_usuario_existe_con_likes_con_comentarios(conexion, numero_likes, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	publicaciones=conexion.publicaciones_usuario(id_usuario)

	assert len(publicaciones)==1
	assert publicaciones[0][-2]==numero_likes
	assert publicaciones[0][-1]==numero_comentarios

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_detalle_publicacion_no_existe(conexion, id_publicacion):

	assert conexion.detalle_publicacion(id_publicacion) is None

def test_detalle_publicacion_existe_sin_likes_sin_comentarios(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	datos=conexion.detalle_publicacion(id_publicacion)

	assert datos[-2]==0
	assert datos[-1]==0

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_detalle_publicacion_existe_con_likes_sin_comentarios(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	datos=conexion.detalle_publicacion(id_publicacion)

	assert datos[-2]==numero_likes
	assert datos[-1]==0

@pytest.mark.parametrize(["numero_comentarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_detalle_publicacion_existe_sin_likes_con_comentarios(conexion, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	datos=conexion.detalle_publicacion(id_publicacion)

	assert datos[-2]==0
	assert datos[-1]==numero_comentarios

@pytest.mark.parametrize(["numero_likes", "numero_comentarios"],
	[
		(2, 5),
		(22, 10),
		(5, 1),
		(13, 22),
		(25, 25)
	]
)
def test_detalle_publicacion_existe_con_likes_con_comentarios(conexion, numero_likes, numero_comentarios):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	for _ in range(numero_comentarios):

		conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	datos=conexion.detalle_publicacion(id_publicacion)

	assert datos[-2]==numero_likes
	assert datos[-1]==numero_comentarios

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_obtener_comentarios_no_existen(conexion, id_publicacion):

	assert conexion.obtenerComentariosPublicacion(id_publicacion) is None

def test_obtener_comentarios_existe(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.insertarComentario(id_usuario, id_publicacion, "Comentario")

	comentarios=conexion.obtenerComentariosPublicacion(id_publicacion)

	assert len(comentarios)==1

def test_numero_likes_no_existe_publicacion(conexion):

	assert conexion.numero_likes(0)==0

def test_numero_likes_existe_publicacion_sin_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	assert conexion.numero_likes(id_publicacion)==0

def test_numero_likes_existe_publicacion_con_like(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.darLike(id_usuario, id_publicacion)

	assert conexion.numero_likes(id_publicacion)==1

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_numero_likes_existe_publicacion_con_likes(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion)

	assert conexion.numero_likes(id_publicacion)==numero_likes

@pytest.mark.parametrize(["numero_likes"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_numero_likes_existe_publicacion_con_likes_varias_publicaciones(conexion, numero_likes):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")
	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion_1=publicaciones[0]["id"]
	id_publicacion_2=publicaciones[1]["id"]

	for _ in range(numero_likes):

		conexion.darLike(id_usuario, id_publicacion_1)

	conexion.darLike(id_usuario, id_publicacion_2)
	conexion.darLike(id_usuario, id_publicacion_2)
	conexion.darLike(id_usuario, id_publicacion_2)

	assert conexion.numero_likes(id_publicacion_1)==numero_likes

@pytest.mark.parametrize(["id_publicacion"],
	[(2,),(1,),(5,),(10,),(0,)]
)
def test_obtener_likes_no_existen(conexion, id_publicacion):

	assert conexion.obtenerLikesPublicacion(id_publicacion) is None

def test_obtener_likes_existe(conexion):

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", 25)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	id_usuario=usuarios[0]["id"]

	conexion.insertarPublicacion(id_usuario, "Titulo", "Descripcion")

	conexion.c.execute("SELECT * FROM publicaciones")

	publicaciones=conexion.c.fetchall()

	id_publicacion=publicaciones[0]["id"]

	conexion.darLike(id_usuario, id_publicacion)

	likes=conexion.obtenerLikesPublicacion(id_publicacion)

	assert len(likes)==1