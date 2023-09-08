 .. _roles:

Roles
======================================================================
.. class:: models.Group

    .. attribute:: nombre

        Obligatorio. 150 caracteres o menos. Se permite cualquier carácter. Ejemplo: 'Super Usuarios'

    .. attribute:: permisos

         Campo many-to-many a :ref:`Permisos <Permisos>`:

         .. code-block::

            group.permissions.set([permission_list])
            group.permissions.add(permission, permission, ...)
            group.permissions.remove(permission, permission, ...)         
            group.permissions.clear()

.. 
   :members:
   :noindex:
