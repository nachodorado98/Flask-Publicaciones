from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.database.conexion import Conexion

bp_perfil=Blueprint("perfil", __name__)


@bp_perfil.route("/me")
@login_required
def perfil():

	con=Conexion()

	id_usuario=con.obtenerIdUsuario(current_user.username)

	nombre_apellido, edad=con.obtenerPerfil(id_usuario)

	numero_publicaciones=con.numero_publicaciones(id_usuario)

	publicaciones_usuario=con.publicaciones_usuario(id_usuario)

	con.cerrarConexion()

	return render_template("perfil.html",
							usuario=current_user.username,
							nombre_apellido=nombre_apellido,
							edad=edad,
							numero_publicaciones=numero_publicaciones,
							publicaciones_usuario=publicaciones_usuario)