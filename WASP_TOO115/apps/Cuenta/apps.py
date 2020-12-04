from django.apps import AppConfig
import logging
from django.db import connection


class CuentaConfig(AppConfig):
    name = 'apps.Cuenta'
    def ready(self):
        with connection.cursor() as cursorVerificacion:
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'CUENTA_DEPARTAMENTO' FETCH FIRST 1 ROWS ONLY;")
                existeDepartamento=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'CUENTA_MUNICIPIO' FETCH FIRST 1 ROWS ONLY;")
                existeMunicipio=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'CUENTA_USUARIO' FETCH FIRST 1 ROWS ONLY;")
                existeUsuario=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'ROL_OPCIONCRUD' FETCH FIRST 1 ROWS ONLY;")
                existeOpcion=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'UNIDADORGANIZACIONAL_UNIDA4EEA' FETCH FIRST 1 ROWS ONLY;")
                existeUnidad=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'ROL_ROL' FETCH FIRST 1 ROWS ONLY;")
                existeRolOpcion=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'ROL_ROLOPCION' FETCH FIRST 1 ROWS ONLY;")
                existeRol=cursorVerificacion.fetchone()
            except:
                pass

        with connection.cursor() as cursor:
            if(existeDepartamento!=None):
                cursor.execute("SELECT COUNT(*) FROM CUENTA_DEPARTAMENTO")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(1,'San Salvador');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(2,'La Libertad');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(3,'Chalatenango');")
            if(existeMunicipio!=None):
                cursor.execute("SELECT COUNT(*) FROM CUENTA_MUNICIPIO")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (IDMUNICIPIO, NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES(1,'San Salvador', 1);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (IDMUNICIPIO, NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES(2,'Ciudad Delgado', 1);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (IDMUNICIPIO, NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES(3,'Comasagua', 2);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (IDMUNICIPIO, NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES(4,'Tamanique', 2);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (IDMUNICIPIO, NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES(5,'Tepecoyo', 2);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (IDMUNICIPIO, NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES(6,'San José Las Flores', 3);")
            if(existeUsuario!=None):
                cursor.execute("SELECT COUNT(*) FROM CUENTA_USUARIO")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):

                    cursor.execute("INSERT INTO CUENTA_USUARIO (PASSWORD, LAST_LOGIN, NOMUSUARIO, PASSCODE, IS_BLOQUEADO, CONTADORINTENTOS, IS_ACTIVE, SOLICITUD, NOMBRE, APELLIDO, FECHANACIMIENTO, CORREO, TELEFONO, DUI, NIT, ISSS, NUP, SALARIO, GENERO, ESTADOCIVIL, MUNICIPIO_ID, NUMCASA, CALLE, COLONIA) VALUES('pbkdf2_sha256$216000$3eV7aGYpIlRH$TGj6vyx4oCODWXHJxwKyg4zrsMqzVeY1gMIWOx6z87I=',NULL, 'admin', '$pbkdf2-sha256$29000$3RsDwBhDKKW01rrXeq917g$MPi8zq254FVo8ZAKVnysLxcHoXbgyRdO131tfiBaxwY',0,0,1, 'A','admin','admin', to_date('1996-06-09', 'yyyy-mm-dd'),'vabcruz96@gmail.com','63141818','053733490','06140906961090','123456789','123456789012',500.0,'femenino', 'soltero', 1, 6, 'Rafael Hernández','La Fuente');")
            if(existeOpcion!=None):
                cursor.execute("SELECT COUNT(*) FROM ROL_OPCIONCRUD")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(11,'Consultar Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(12,'Crear Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(13,'Modificar Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(14,'Eliminar Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(21,'Consultar Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(22,'Crear Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(23,'Modificar Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(24,'Eliminar Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(31,'Consultar Usuario');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(33,'Modificar Usuario');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(34,'Eliminar Usuario');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (NUMCRUD, DESCRIPCRUD) VALUES(34,'Eliminar Usuario');")

            '''if(existeUnidad!=None):
                cursor.execute("SELECT COUNT(*) FROM UNIDADORGANIZACIONAL_UNIDA4EEA")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO UNIDADORGANIZACIONAL_UNIDA4EEA (NOMBREUNIDAD, DESCRIPUNIDAD) VALUES(1,'Departamento De Recursos Humanos');")

            if(existeRol!=None):
                cursor.execute("SELECT COUNT(*) FROM ROL_ROL")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO ROL_ROL (NOMBREROL, DESCRIPROL, UNIDAD_ID) VALUES('Jefe De Recursos Huamnos','Administrador del sistema.',1);")

            if(existeRolOpcion!=None):
                cursor.execute("SELECT COUNT(*) FROM ROL_ROLOPCION")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(1,1);")'''
