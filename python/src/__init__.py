from flask import Flask

from .blueprints.inicio import bp_inicio
from .blueprints.registro import bp_registro
from .blueprints.login import bp_login
from .blueprints.anadir_publicacion import bp_anadir_publicacion
from .blueprints.perfil import bp_perfil
from .blueprints.usuario import bp_usuario
from .blueprints.like import bp_like
from .blueprints.comentario import bp_comentario
from .blueprints.detalle import bp_detalle

from .extensiones.manager import login_manager

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	login_manager.init_app(app)
	login_manager.login_view="login.login"

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_registro)
	app.register_blueprint(bp_login)
	app.register_blueprint(bp_anadir_publicacion)
	app.register_blueprint(bp_perfil)
	app.register_blueprint(bp_usuario)
	app.register_blueprint(bp_like)
	app.register_blueprint(bp_comentario)
	app.register_blueprint(bp_detalle)

	return app