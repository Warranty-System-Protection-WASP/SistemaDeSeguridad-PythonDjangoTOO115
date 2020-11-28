from django.apps import AppConfig
import logging
from django.db import connection


class CuentaConfig(AppConfig):
    name = 'apps.Cuenta'
    def ready(self):
        with connection.cursor() as cursorVerificacion:
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'CUENTA_USUARIO' FETCH FIRST 1 ROWS ONLY;")
                existeUsuario=cursorVerificacion.fetchone()
            except:
                pass

        with connection.cursor() as cursor:
            if(existeUsuario!=None):
                cursor.execute("SELECT COUNT(*) FROM CUENTA_USUARIO")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO CUENTA_USUARIO (PASSWORD, LAST_LOGIN, NOMUSUARIO, PASSCODE, IS_BLOQUEADO, CONTADORINTENTOS, IS_ACTIVE, SOLICITUD, NOMBRE, APELLIDO, FECHANACIMIENTO, CORREO, TELEFONO, DUI, NIT, ISSS, NUP, SALARIO, GENERO, ESTADOCIVIL, DIRECCION, NUMCASA, COLONIA) VALUES('pbkdf2_sha256$216000$3eV7aGYpIlRH$TGj6vyx4oCODWXHJxwKyg4zrsMqzVeY1gMIWOx6z87I=',NULL, 'admin', 1507,0,0,1, 'A','admin','admin', to_date('1996-06-09', 'yyyy-mm-dd'),'vabcruz96@gmail.com','63141818','053733490','06140906961090','123456789','123456789012',500.0,'femenino', 'soltero','Colonia La Fuente Pasaje El Manantial Comasagua La Libertad', 6, 'La Fuente');")
