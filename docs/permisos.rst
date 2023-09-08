 .. _permisos:

Permisos
======================================================================
.. class:: models.Permission

    .. attribute:: nombre

        Requerido. 255 caracteres o menos. Ejemplo: 'Puede eliminar usuarios'

    .. attribute:: tipo_contenido

        Requerido. Una referencia a la tabla de base de datos django_content_type, que contiene un registro para cada modelo instalado.
      
    .. attribute:: codigo

      Requerido. 100 caracteres o menos. Ejemplo: 'eliminar_usuario'
    

.. 
   :members:
   :noindex:
