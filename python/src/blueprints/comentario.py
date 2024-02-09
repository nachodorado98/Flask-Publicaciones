from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user

from src.database.conexion import Conexion

bp_comentario=Blueprint("comentario", __name__)


@bp_comentario.route("/comentar/<id>")
@login_required
def comentario(id:str):

	id_publicacion=int(id)

	con=Conexion()

	if not con.existe_id_publicacion(id_publicacion):

		con.cerrarConexion()

		return redirect("/publicaciones")

	con.cerrarConexion()

	return render_template("comentario.html", usuario=current_user.username, id_publicacion=id_publicacion)

@bp_comentario.route("/insertar_comentario/<id>", methods=["POST"])
@login_required
def insertarComentario(id:str):

	id_publicacion=int(id)

	con=Conexion()

	if not con.existe_id_publicacion(id_publicacion):

		con.cerrarConexion()

		return redirect("/publicaciones")

	comentario=request.form.get("comentario")

	if comentario is None:

		return redirect(f"/comentar/{id_publicacion}")

	id_usuario=con.obtenerIdUsuario(current_user.username)

	con.insertarComentario(id_usuario, id_publicacion, comentario)

	con.cerrarConexion()

	return redirect("/publicaciones")