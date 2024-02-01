from flask import Blueprint, request, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from typing import Optional

from src.extensiones.manager import login_manager

from src.modelos.usuario import Usuario

from src.database.conexion import Conexion

from src.utilidades.utils import comprobarHash


bp_login=Blueprint("login", __name__)


# Funcion para comprobar y cargar  el usuario 
@login_manager.user_loader
def cargarUsuario(id:str)->Optional[Usuario]:

	id_usuario=int(id)

	con=Conexion()

	if con.existe_id(id_usuario):

		usuario=con.obtenerNombreUsuarioUsuario(id_usuario)

		con.cerrarConexion()

		return Usuario(id_usuario, usuario)

	con.cerrarConexion()

	return None
	

@bp_login.route("/login", methods=["GET", "POST"])
def login():

	usuario=request.form.get("usuario")
	contrasena=request.form.get("contrasena")

	con=Conexion()

	if not con.existe_usuario(usuario):

		con.cerrarConexion()

		return redirect("/")

	contrasena_hash_usuario=con.obtenerContrasenaUsuario(usuario)

	if not comprobarHash(contrasena, contrasena_hash_usuario):

		con.cerrarConexion()

		return redirect("/")

	id_usuario=con.obtenerIdUsuario(usuario)

	con.cerrarConexion()

	usuario=Usuario(id=id_usuario, username=usuario)

	login_user(usuario)

	siguiente=request.args.get("next")

	return redirect(siguiente or "/publicaciones")


@bp_login.route("/publicaciones")
@login_required
def pagina_publicaciones():

	con=Conexion()

	publicaciones=con.obtenerPublicaciones()

	con.cerrarConexion()

	return render_template("publicaciones.html", usuario=current_user.username, publicaciones=publicaciones)


@bp_login.route("/logout")
@login_required
def logout():

	logout_user()

	return redirect("/")