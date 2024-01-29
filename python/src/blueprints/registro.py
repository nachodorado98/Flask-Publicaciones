from flask import Blueprint, render_template, request, redirect

from src.utilidades.utils import datos_regitros_correctos, generarHash

from src.database.conexion import Conexion

bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	return render_template("registro.html")

@bp_registro.route("/singin", methods=["POST"])
def singin():

	usuario=request.form.get("usuario")
	contrasena=request.form.get("contrasena")
	nombre=request.form.get("nombre")
	apellido=request.form.get("apellido")
	edad=request.form.get("edad")

	if not datos_regitros_correctos(nombre, apellido, usuario, contrasena, edad):

		return redirect("/registro")

	con=Conexion()

	if con.existe_usuario(usuario):

		con.cerrarConexion()

		return redirect("/registro")

	con.insertarUsuario(usuario, generarHash(contrasena), nombre, apellido, edad)

	con.cerrarConexion()

	return render_template("singin.html", nombre=nombre)