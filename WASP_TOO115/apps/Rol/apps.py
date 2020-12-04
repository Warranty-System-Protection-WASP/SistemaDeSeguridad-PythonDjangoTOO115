from django.apps import AppConfig
from django.db import connection

class RolConfig(AppConfig):
    name = 'Rol'
    def ready(self):
        with connection.cursor() as cursorVerificacion:
            try:
                cursorVerificacion.execute("SELECT * FROM ALL_TABLES WHERE TABLE_NAME = 'ROL_OPCIONCRUD' FETCH FIRST 1 ROWS ONLY;")
                existeRolOpcion=cursorVerificacion.fetchone()
            except:
                pass

        with connection.cursor() as cursor:
            if(existeRolOpcion!=None):
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
