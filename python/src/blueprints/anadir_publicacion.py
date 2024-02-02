from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

bp_anadir_publicacion=Blueprint("anadir_publicacion", __name__)


@bp_anadir_publicacion.route("/anadir_publicacion")
@login_required
def anadirPublicacion():

	return render_template("anadir.html", usuario=current_user.username)

@bp_anadir_publicacion.route("/insertar_publicacion", methods=["POST"])
@login_required
def insertarPublicacion():

	titulo=request.form.get("titulo")
	descripcion=request.form.get("descripcion")

	if titulo is None or descripcion is None:

		return redirect("/anadir_publicacion")

	con=Conexion()

	id_usuario=con.obtenerIdUsuario(current_user.username)

	con.insertarPublicacion(id_usuario, titulo, descripcion)

	con.cerrarConexion()

	return redirect("/publicaciones")