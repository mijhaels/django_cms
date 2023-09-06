 .. _permisos:

Permisos
======================================================================
**Campos**
----------------------------------------------------------------------
Los objetos de **Permisos** tienen los siguientes campos:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class **models.Permission**

**nombre**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Requerido. 255 caracteres o menos. Ejemplo: 'Puede eliminar usuarios'

**tipo_contenido**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Requerido. Una referencia a la tabla de base de datos django_content_type, que contiene un registro para cada modelo instalado.

**codigo**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Requerido. 100 caracteres o menos. Ejemplo: 'eliminar_usuario'

.. 
   :members:
   :noindex:
