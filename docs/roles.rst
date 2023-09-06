 .. _roles:

Roles
======================================================================
**Campos**
----------------------------------------------------------------------
Los objetos de **Roles** tienen los siguientes campos:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class **models.Group**

**nombre**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obligatorio. 150 caracteres o menos. Se permite cualquier carácter. Ejemplo: 'Super Usuarios'

**permisos**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Campo many-to-many a Permisos:

.. code-block::

   group.permissions.set([permission_list])
   group.permissions.add(permission, permission, ...)
   group.permissions.remove(permission, permission, ...)
   group.permissions.clear()
