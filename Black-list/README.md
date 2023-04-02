Descripcion del componente user-management:
- Es el microservicio permite gestionar y validar la identidad de usuarios por medio de tokens.
- Cuenta con un metodo Post que permite crear un usuario con los datos brindados el cual valida que el nombre debe ser unico al igual que el correo.
- Cuenta con un metodo post que nos permite generar un token para el usuario al que le corresponde el username y la contraseña.
- Cuenta con un metodo Get que permite retornar los datos de un usurio al que le pertenece el token.
- Cuenta con un metodo Get que nos permite validar la salud del servicio.