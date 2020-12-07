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
                existeRol=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'ROL_ROLOPCION' FETCH FIRST 1 ROWS ONLY;")
                existeRolOpcion=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'ROL_ROLUSUARIO' FETCH FIRST 1 ROWS ONLY;")
                existeRolUsuario=cursorVerificacion.fetchone()
            except:
                pass
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'CUENTA_PREGUNTA' FETCH FIRST 1 ROWS ONLY;")
                existePregunta=cursorVerificacion.fetchone()
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
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(4,'SonSonate');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(5,'Santa Ana');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(6,'Ahuachapan');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(7,'Usulutan');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(8,'San Vicente');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(9,'Morazan');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(10,'San Miguel');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(11,'La Union');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(12,'Cabañas');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(13,'Cuscatlan');")
                    cursor.execute("INSERT INTO CUENTA_DEPARTAMENTO (IDDEPARTAMENTO, NOMDEPARTAMENTO) VALUES(14,'La Paz');")
            if(existeMunicipio!=None):
                cursor.execute("SELECT COUNT(*) FROM CUENTA_MUNICIPIO")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES('San Salvador', 1);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES('Ciudad Delgado', 1);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES('Comasagua', 2);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES('Tamanique', 2);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES('Tepecoyo', 2);")
                    cursor.execute("INSERT INTO CUENTA_MUNICIPIO (IDMUNICIPIO, NOMMUNICIPIO, DEPARTAMENTO_ID) VALUES(3000, 'San José Las Flores', 3);")
            if(existeUsuario!=None):
                cursor.execute("SELECT COUNT(*) FROM CUENTA_USUARIO")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):

                    cursor.execute("INSERT INTO CUENTA_USUARIO (PASSWORD, LAST_LOGIN, NOMUSUARIO, PASSCODE, IS_BLOQUEADO, CONTADORINTENTOS, IS_ACTIVE, SOLICITUD, NOMBRE, APELLIDO, FECHANACIMIENTO, CORREO, TELEFONO, DUI, NIT, ISSS, NUP, SALARIO, GENERO, ESTADOCIVIL, MUNICIPIO_ID, NUMCASA, CALLE, COLONIA) VALUES('pbkdf2_sha256$216000$3eV7aGYpIlRH$TGj6vyx4oCODWXHJxwKyg4zrsMqzVeY1gMIWOx6z87I=',NULL, 'admin', '$pbkdf2-sha256$29000$3RsDwBhDKKW01rrXeq917g$MPi8zq254FVo8ZAKVnysLxcHoXbgyRdO131tfiBaxwY',0,0,1, 'A','admin','admin', to_date('1996-06-09', 'yyyy-mm-dd'),'vabcruz96@gmail.com','63141818','053733490','06140906961090','123456789','123456789012',500.0,'femenino', 'soltero', 3000, 6, 'Rafael Hernández','La Fuente');")
            if(existeOpcion!=None):
                cursor.execute("SELECT COUNT(*) FROM ROL_OPCIONCRUD")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(1, 11,'Consultar Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(2, 12,'Crear Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(3, 13,'Modificar Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(4, 14,'Eliminar Puesto De Trabajo');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(5, 21,'Consultar Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(6, 22,'Crear Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(7, 23,'Modificar Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(8, 24,'Eliminar Unidad Organizacional');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(9, 31,'Consultar Usuario');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(10, 33,'Modificar Usuario');")
                    cursor.execute("INSERT INTO ROL_OPCIONCRUD (ID, NUMCRUD, DESCRIPCRUD) VALUES(11, 34,'Eliminar Usuario');")
            if(existeUnidad!=None):
                cursor.execute("SELECT COUNT(*) FROM UNIDADORGANIZACIONAL_UNIDA4EEA")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO UNIDADORGANIZACIONAL_UNIDA4EEA (NOMBREUNIDAD, DESCRIPUNIDAD) VALUES('Departamento De Recursos Humanos', 'Encargados de la gestion del sistema');")
            if(existeRol!=None):
                cursor.execute("SELECT COUNT(*) FROM ROL_ROL")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO ROL_ROL (ID, NOMBREROL, DESCRIPROL, UNIDAD_ID) VALUES(1, 'Jefe De Recursos Huamnos','Administrador del sistema.',1);")
            if(existeRolOpcion!=None):
                cursor.execute("SELECT COUNT(*) FROM ROL_ROLOPCION")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(1, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(2, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(3, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(4, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(5, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(6, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(7, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(8, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(9, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(10, 1);")
                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID, IDROL_ID) VALUES(11, 1);")
            if(existeRolUsuario!=None):
                cursor.execute("SELECT COUNT(*) FROM ROL_ROLUSUARIO")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO ROL_ROLUSUARIO (IS_ACTIVO, FECHA_INICIO, IDEMPLEADO_ID, IDROL_ID) VALUES(1, sysdate, 'admin', 1);")
            if(existePregunta!=None):
                cursor.execute("SELECT COUNT(*) FROM CUENTA_PREGUNTA")
                cantidad = cursor.fetchone()
                if(cantidad[0]==0):
                    cursor.execute("INSERT INTO CUENTA_PREGUNTA (NUMPREGUNTA, PREGUNTA) VALUES(1, '¿Cuál es tu lugar favorito?');")
                    cursor.execute("INSERT INTO CUENTA_PREGUNTA (NUMPREGUNTA, PREGUNTA) VALUES(2, '¿Cuál es el nombre de tu amigo de infancia?');")
                    cursor.execute("INSERT INTO CUENTA_PREGUNTA (NUMPREGUNTA, PREGUNTA) VALUES(3, '¿Cuál es el nombre de tu primera mascota?');")
                    cursor.execute("INSERT INTO CUENTA_PREGUNTA (NUMPREGUNTA, PREGUNTA) VALUES(4, '¿Cuál es el nombre de tu primera escuela donde estudiaste?');")
                    cursor.execute("INSERT INTO CUENTA_PREGUNTA (NUMPREGUNTA, PREGUNTA) VALUES(5, '¿Dónde nació tu abuela?');")
                    cursor.execute("INSERT INTO CUENTA_PREGUNTA (NUMPREGUNTA, PREGUNTA) VALUES(6, '¿Dónde se conocieron tus padres?');")
