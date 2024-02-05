from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

bp_usuario=Blueprint("usuario", __name__)


@bp_usuario.route("/usuario/<id>")
@login_required
def usuario(id:str):

	id_buscado=int(id)

	con=Conexion()

	if not con.existe_id(id_buscado):

		con.cerrarConexion()

		return redirect("/publicaciones")

	id_usuario=con.obtenerIdUsuario(current_user.username)

	if id_usuario==id_buscado:

		con.cerrarConexion()

		return redirect("/me")

	usuario_perfil=con.obtenerNombreUsuarioUsuario(id_buscado)

	nombre_apellido, edad=con.obtenerPerfil(id_buscado)

	numero_publicaciones=con.numero_publicaciones(id_buscado)

	publicaciones_usuario=con.publicaciones_usuario(id_buscado)

	con.cerrarConexion()

	return render_template("usuario.html",
							usuario=current_user.username,
							nombre_apellido=nombre_apellido,
							edad=edad,
							numero_publicaciones=numero_publicaciones,
							publicaciones_usuario=publicaciones_usuario,
							usuario_perfil=usuario_perfil)