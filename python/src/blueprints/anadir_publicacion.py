from flask import Blueprint, render_template
from flask_login import login_required, current_user


bp_anadir_publicacion=Blueprint("anadir_publicacion", __name__)


@bp_anadir_publicacion.route("/anadir_publicacion")
@login_required
def anadirPublicacion():

	return render_template("anadir.html", usuario=current_user.username)