from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

bp_like=Blueprint("like", __name__)


@bp_like.route("/dar_like/<id>")
@login_required
def darLike(id:str):

	id_publicacion=int(id)

	con=Conexion()

	if not con.existe_id_publicacion(id_publicacion):

		con.cerrarConexion()

		return redirect("/publicaciones")

	id_usuario=con.obtenerIdUsuario(current_user.username)

	if con.like_dado(id_usuario, id_publicacion):

		con.cerrarConexion()

		return redirect("/publicaciones")

	con.darLike(id_usuario, id_publicacion)

	con.cerrarConexion()

	return redirect("/publicaciones")