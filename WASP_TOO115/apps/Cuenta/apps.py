from django.apps import AppConfig
import logging
from django.db import connection


class CuentaConfig(AppConfig):
    name = 'Cuenta'
'''
SELECT *
FROM   all_tables
WHERE  num_rows > 1

TABLE_NAME
'''
