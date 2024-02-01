import os
import sys
sys.path.append("..")

import pytest
from src import crear_app
from src.database.conexion import Conexion
from confmain import config

@pytest.fixture()
def app():

	configuracion=config["development"]

	app=crear_app(configuracion)

	yield app

@pytest.fixture()
def cliente(app):

	return app.test_client()

@pytest.fixture()
def conexion():

	con=Conexion()

	con.c.execute("DELETE FROM usuarios")

	con.c.execute("DELETE FROM publicaciones")

	con.confirmar()

	return con