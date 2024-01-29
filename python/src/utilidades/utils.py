import re
from passlib.context import CryptContext

# Funcion para comprobar que el nombre y el apellido es correcto
def nombre_apellido_correcto(nombre:str, apellido:str)->bool:

    return bool(nombre and apellido and nombre.isalpha() and apellido.isalpha())

# Funcion para comprobar que un usuario es correcto
def usuario_correcto(usuario:str)->bool:

    return bool(usuario and usuario.isalnum())

# Funcion para comprobar la edad es correcta
def edad_correcta(edad:str)->bool:

    try:

        edad_entero=int(edad)

        return 18<=edad_entero<100

    except ValueError:

        return False

# Funcion para comprobar que la contraseña es correcta (8 caracteres, mayuscula, minuscula, digito, caracter especial, sin espacio)
def contrasena_correcta(contrasena:str)->bool:

    patron=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

    return bool(re.match(patron, contrasena))

# Funcion para comprobar que los datos del registro son correctos
def datos_regitros_correctos(nombre:str, apellido:str, usuario:str, contrasena:str, edad:str)->bool:

    if nombre is None or apellido is None or usuario is None or contrasena is None or edad is None:

        return False

    return True if nombre_apellido_correcto(nombre, apellido) and usuario_correcto(usuario) and contrasena_correcta(contrasena) and edad_correcta(edad) else False

# Funcion para generar el hash de una contraseña
def generarHash(contrasena:str)->str:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.hash(contrasena)

# Funcion para comprobar el hash y la contraseña
def comprobarHash(contrasena:str, contrasena_hash:str)->bool:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.verify(contrasena, contrasena_hash)