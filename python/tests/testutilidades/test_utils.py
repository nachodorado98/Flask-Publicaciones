import pytest

from src.utilidades.utils import nombre_apellido_correcto, usuario_correcto, edad_correcta, contrasena_correcta
from src.utilidades.utils import datos_regitros_correctos, generarHash, comprobarHash

@pytest.mark.parametrize(["nombre", "apellido", "resultado"],
	[
	    ("Juan", "Pérez", True),
	    ("Ana María", "López", False),
	    ("Carlos", "123", False),
	    (None, "González", False),
	    ("Laura", None, False),
	    (None, None, False)
	]
)
def test_nombre_apellido_correcto(nombre, apellido, resultado):

    assert nombre_apellido_correcto(nombre, apellido)==resultado

@pytest.mark.parametrize(["usuario", "resultado"],
	[("juan123", True),("ana_maria", False),("carlos_456", False),("", False),("usuario1", True),("12345", True),(None, False)]
)
def test_usuario_correcto(usuario, resultado):

    assert usuario_correcto(usuario)==resultado

@pytest.mark.parametrize(["edad", "resultado"],
	[("25", True),("abc", False),("150", False),("-5", False),("17", False),("18", True),(99, True),("100", False),("", False),(22, True)]
)
def test_edad_correcta(edad, resultado):

    assert edad_correcta(edad)==resultado

@pytest.mark.parametrize(["contrasena", "resultado"],
	[
	    ("clave", False),
	    ("CONTRASENA", False),
	    ("12345678", False),
	    ("Abcdefg", False),
	    ("", False),
	    ("A1b2C3d4", False),
	    ("abcd", False),
	    ("1234", False),
	    ("Ab CdEfGhI", False),
	    ("Ab!CdEfGhI ", False),
	    (" Ab!CdEfGhI", False),
	    ("Ab!CdEfGhIJKLMN", False),
	    ("Ab@cdEfG", False),
	    ("Ab@cdEf1 G", False),
	    ("Ab!CdEfGhIJK3LMN", True),
	    ("Abcd12 34!", False),
	    ("Abcd1234!", True),
	]
)
def test_contrasena_correcta(contrasena, resultado):

    assert contrasena_correcta(contrasena)==resultado

@pytest.mark.parametrize(["nombre", "apellido", "usuario", "contrasena", "edad"],
	[
		(None, "dorado", "golden98", "contrasena100", "18"),
		("Nacho", None, "golden98", "contrasena100", "18"),
		("nacho", "dorado", None, "djkggjk&/()?", "25"),
		("nacho", "dorado", "golden98", None, "22"),
		("nachodoorado", "dorado", "golden98", "mypassword", None),
		("nach0", "dorado", "nacho98", "nacho98%&/", "19"),
		("nacho", "dor4do", "nacho98", "nacho98%&/", "19"),
		("nacho", "dorado", "nacho_98", "nacho98%hhj", "26"),
		("nacho", "dorado", "nacho98", "nac98%", "99"),
		("nacho", "dorado", "nacho98", "nacho98hhjh$", "17"),
	]
)
def test_datos_incorrectos(nombre, apellido, usuario, contrasena, edad):

	assert not datos_regitros_correctos(nombre, apellido, usuario, contrasena, edad)

@pytest.mark.parametrize(["nombre", "apellido", "usuario", "contrasena", "edad"],
	[
		("nachodorado", "dorado", "nacho98", "nacHo98%&", "19"),
		("nacho", "dorado", "nacho98", "Nacho98%hhj", "26"),
		("nacho", "dorado", "nacho98", "NAacdhdh98%LL", "99"),
		("nacho", "dorado", "nacho98", "nSGcho98hhjh$", "18"),
	]
)
def test_datos_correctos(nombre, apellido, usuario, contrasena, edad):

	assert datos_regitros_correctos(nombre, apellido, usuario, contrasena, edad)

@pytest.mark.parametrize(["contrasena"],
	[("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_generar_hash_contrasena(contrasena):

	contrasena_hash=generarHash(contrasena)

	assert len(contrasena_hash)==60
	assert contrasena not in contrasena_hash


@pytest.mark.parametrize(["contrasena", "contrasena_mal"],
	[
		("contrasena1234","contrasena123"),
		("123456789","1234567899"),
		("contrasena_secreta","contrasenasecreta")
	]
)
def test_comprobar_hash_contrasena_incorrecta(contrasena, contrasena_mal):

	contrasena_hash=generarHash(contrasena)

	assert not comprobarHash(contrasena_mal, contrasena_hash)


@pytest.mark.parametrize(["contrasena"],
	[("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_comprobar_hash_contrasena_correcta(contrasena):

	contrasena_hash=generarHash(contrasena)

	assert comprobarHash(contrasena, contrasena_hash)