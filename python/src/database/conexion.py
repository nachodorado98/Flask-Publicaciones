import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:

			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, contrasena:str, nombre:str, apellido:str, edad:int)->None:

		self.c.execute("""INSERT INTO usuarios (usuario, contrasena, nombre, apellido, edad)
						VALUES (%s, %s, %s, %s, %s);""",
						(usuario, contrasena, nombre, apellido, edad))

		self.confirmar()

	# Metodo para comprobar si ya existe un usuario
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		usuario=self.c.fetchone()

		return False if usuario is None else True

	# Metodo para obtener la contrasena de un usuario
	def obtenerContrasenaUsuario(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT contrasena
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		contrasena=self.c.fetchone()

		return None if contrasena is None else contrasena["contrasena"]

	# Metodo para obtener el id de un usuario
	def obtenerIdUsuario(self, usuario:str)->Optional[int]:

		self.c.execute("""SELECT id
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		id_usuario=self.c.fetchone()

		return None if id_usuario is None else id_usuario["id"]

	# Metodo para comprobar si existe el id
	def existe_id(self, id_usuario:int)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE id=%s""",
						(id_usuario,))

		id_usuario_obtenido=self.c.fetchone()

		return False if id_usuario_obtenido is None else True

	# Metodo para obtener el nombre de usuario de un usuario
	def obtenerNombreUsuarioUsuario(self, id_usuario:int)->Optional[str]:

		self.c.execute("""SELECT usuario
						FROM usuarios
						WHERE id=%s""",
						(id_usuario,))

		usuario=self.c.fetchone()

		return None if usuario is None else usuario["usuario"]

	# Metodo para insertar una publicacion
	def insertarPublicacion(self, id_usuario:int, titulo:str, descripcion:str)->None:

		self.c.execute("""INSERT INTO publicaciones (id_usuario, titulo, descripcion)
						VALUES (%s, %s, %s);""",
						(id_usuario, titulo, descripcion))

		self.confirmar()

	# Metodo para obtener las publicaciones
	def obtenerPublicaciones(self)->Optional[List[tuple]]:

		self.c.execute("""SELECT pub.*, COUNT(DISTINCT l.id) AS likes, COUNT(DISTINCT c.id) AS comentarios
							FROM (SELECT p.id, p.titulo, p.descripcion, u.usuario, TO_CHAR(p.fecha_publicacion, 'HH24:MI DD-MM-YYYY') as fecha, p.fecha_publicacion, u.id as id_usuario
							    	FROM usuarios u
							    	JOIN publicaciones p
							    	ON u.id=p.id_usuario) pub
							LEFT JOIN likes l
							ON pub.id=l.id_publicacion
							LEFT JOIN comentarios c
							ON pub.id=c.id_publicacion
							GROUP BY pub.id, pub.titulo, pub.descripcion, pub.usuario, pub.fecha, pub.fecha_publicacion, pub.id_usuario
							ORDER BY pub.fecha_publicacion DESC""")

		publicaciones=self.c.fetchall()

		return list(map(lambda publicacion: (publicacion["id"],
											publicacion["titulo"],
											publicacion["descripcion"],
											publicacion["usuario"],
											publicacion["fecha"],
											publicacion["id_usuario"],
											publicacion["likes"],
											publicacion["comentarios"]), publicaciones)) if publicaciones else None

	# Metodo para obtener datos del perfil del usuario
	def obtenerPerfil(self, id_usuario:int)->Optional[tuple]:

		self.c.execute("""SELECT nombre, apellido, edad
						FROM usuarios
						WHERE id=%s""",
						(id_usuario,))

		perfil=self.c.fetchone()

		# Funcion para limpiar los datos del perfil
		def limpiarDatos(datos:Dict)->tuple:

			nombre=datos["nombre"]

			apellido=datos["apellido"]

			return (nombre+" "+apellido, datos["edad"])

		return None if perfil is None else limpiarDatos(perfil)

	# Metodo para obtener el numero de publicaciones de un usuario
	def numero_publicaciones(self, id_usuario:int)->int:

		self.c.execute("""SELECT count(1) as numero_publicaciones
						FROM publicaciones
						WHERE id_usuario=%s""",
						(id_usuario,))

		return self.c.fetchone()["numero_publicaciones"]

	# Metodo para obtener las publicaciones de un usuario
	def publicaciones_usuario(self, id_usuario:int)->Optional[List[tuple]]:

		self.c.execute("""SELECT pub.*, COUNT(DISTINCT l.id) AS likes, COUNT(DISTINCT c.id) AS comentarios
							FROM (SELECT p.id, p.titulo, p.descripcion, u.usuario, TO_CHAR(p.fecha_publicacion, 'HH24:MI DD-MM-YYYY') as fecha, p.fecha_publicacion, u.id as id_usuario
							    	FROM usuarios u
							    	JOIN publicaciones p
							    	ON u.id=p.id_usuario
							    	WHERE p.id_usuario=%s) pub
							LEFT JOIN likes l
							ON pub.id=l.id_publicacion
							LEFT JOIN comentarios c
							ON pub.id=c.id_publicacion
							GROUP BY pub.id, pub.titulo, pub.descripcion, pub.usuario, pub.fecha, pub.fecha_publicacion, pub.id_usuario
							ORDER BY pub.fecha_publicacion DESC""",
						(id_usuario,))

		publicaciones=self.c.fetchall()

		return list(map(lambda publicacion: (publicacion["id"],
											publicacion["titulo"],
											publicacion["descripcion"],
											publicacion["usuario"],
											publicacion["fecha"],
											publicacion["id_usuario"],
											publicacion["likes"],
											publicacion["comentarios"]), publicaciones)) if publicaciones else None

	# Metodo para comprobar si existe el id de la publicacion
	def existe_id_publicacion(self, id_publicacion:int)->bool:

		self.c.execute("""SELECT *
						FROM publicaciones
						WHERE id=%s""",
						(id_publicacion,))

		id_publicacion_obtenido=self.c.fetchone()

		return False if id_publicacion_obtenido is None else True

	# Metodo para dar like a una publicacion
	def darLike(self, id_usuario:int, id_publicacion:int)->None:

		self.c.execute("""INSERT INTO likes (id_usuario, id_publicacion)
						VALUES (%s, %s);""",
						(id_usuario, id_publicacion))

		self.confirmar()

	# Metodo para saber si se ha dado like a una publicacion por parte de un usuario
	def like_dado(self, id_usuario:int, id_publicacion:int)->bool:

		self.c.execute("""SELECT *
						FROM likes
						WHERE id_usuario=%s
						AND id_publicacion=%s""",
						(id_usuario, id_publicacion))

		like=self.c.fetchone()

		return False if like is None else True

	# Metodo para insertar un comentario de una publicacion
	def insertarComentario(self, id_usuario:int, id_publicacion:int, comentario:str)->None:

		self.c.execute("""INSERT INTO comentarios (id_usuario, id_publicacion, comentario)
						VALUES (%s, %s, %s);""",
						(id_usuario, id_publicacion, comentario))

		self.confirmar()