from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

bp_detalle=Blueprint("detalle", __name__)


@bp_detalle.route("/detalle_publicacion/<id>")
@login_required
def detalle_publicacion(id:str):

	id_publicacion=int(id)

	con=Conexion()

	if not con.existe_id_publicacion(id_publicacion):

		con.cerrarConexion()

		return redirect("/publicaciones")

	datos_publicacion=con.detalle_publicacion(id_publicacion)

	comentarios=con.obtenerComentariosPublicacion(id_publicacion)

	con.cerrarConexion()

	return render_template("detalle.html",
							usuario=current_user.username,
							datos_publicacion=datos_publicacion,
							comentarios=comentarios)