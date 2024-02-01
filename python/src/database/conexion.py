import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List

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

		self.c.execute("""SELECT p.id, p.titulo, p.descripcion, u.usuario, TO_CHAR(p.fecha_publicacion, 'HH24:MI DD-MM-YYYY') as fecha
						FROM usuarios u
						JOIN publicaciones p
						ON u.id=p.id_usuario
						ORDER BY p.fecha_publicacion DESC""")

		publicaciones=self.c.fetchall()

		return list(map(lambda publicacion: (publicacion["id"], publicacion["titulo"], publicacion["descripcion"], publicacion["usuario"], publicacion["fecha"]), publicaciones)) if publicaciones else None