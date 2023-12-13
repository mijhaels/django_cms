Puesta en marcha localmente con Docker
======================================================================

Prerequisitos
----------------------------------------------------------------------
- `Docker desktop <https://docs.docker.com/desktop/>`__
- `Git <https://git-scm.com/downloads>`__

Antes de empezar
----------------------------------------------------------------------
Clonar el repositorio

 .. code-block:: python

    $ git clone https://github.com/Andythem23/django_cms.git

Creación de Stack
----------------------------------------------------------------------
Esto puede tardar un poco, especialmente la primera vez que ejecute este comando en particular en su sistema de desarrollo.

Abra un terminal en la raíz del proyecto y ejecute lo siguiente para el desarrollo local:

 .. code-block:: python

   $ docker-compose -f local.yml build

Generalmente, si quieres emular el entorno de producción utiliza **production.yml** en su lugar. Y esto es cierto para cualquier otra acción que pueda necesitar realizar: siempre que se requiera un cambio, ¡simplemente hágalo!

Ejecución del Stack
----------------------------------------------------------------------
Esto levanta tanto Django como PostgreSQL. La primera vez que se ejecuta puede tardar un poco en iniciarse, pero las siguientes ejecuciones se producirán rápidamente.
 .. code-block:: python

   $ docker-compose -f local.yml up

Ejecución de comandos de administración de Django
----------------------------------------------------------------------
Como con cualquier comando shell que deseemos ejecutar en nuestro contenedor, esto se hace utilizando el comando **docker-compose -f local.yml run --rm**:
 .. code-block:: python

   $ docker compose -f local.yml run --rm django python manage.py makemigrations
   $ docker compose -f local.yml run --rm django python manage.py migrate
   $ docker compose -f local.yml run --rm django python manage.py createsuperuser

Aquí, **Django** es el servicio de destino contra el que estamos ejecutando los comandos. Además, ten en cuenta que **docker exec** no funciona para ejecutar comandos de gestión.

Ejecución de comandos de calidad de codigo:
----------------------------------------------------------------------
A continuación se demuestran los comandos a ser utilizados para optimizar la calidad de código

Se utiliza para formatear todos los archivos .py
 .. code-block:: python

   $ docker compose -f local.yml run --rm django black .

Se utiliza para linting de los archivos .py
 .. code-block:: python
   
   $ docker compose -f local.yml run --rm django flake8 

Se utiliza para para ordenar los imports
 .. code-block:: python
   
   $ docker compose -f local.yml run --rm django isort .

Se utiliza para hacer linting de los archivos .html
 .. code-block:: python
      
   $ docker compose -f local.yml run --rm django djlint . --lint 
   
Se utiliza para formatear todos los archivos .html
 .. code-block:: python
   
   $ docker compose -f local.yml run --rm django djlint . --reformat

Ejecución de comandos de restauración de base de datos:
----------------------------------------------------------------------
A continuación se demuestran los comandos a ser utilizados para restaurar la base de datos.

Tener en cuenta que el único contenedor que debe estar arriba es el de **postgres**.

 .. code-block:: python

   $ docker compose -f local.yml up -d postgres

Para crear un backup, se ejecuta el siguiente comando
 .. code-block:: python
   
   $ docker compose -f local.yml exec postgres backup

Para listar los backups existentes, se ejecuta el siguiente comando: 
 .. code-block:: python
   
   $ docker compose -f local.yml exec postgres backups

Para copiar backups de un contenedor a un directorio local, se ejecuta el siguiente comando:
 .. code-block:: python
   
   $ docker cp <container_id>:/backups <local_dir>

Por ejemplo, dado 9c5c3f055843 es el ID del contenedor copiar todas las copias de seguridad a un directorio local, se ejecuta el siguiente comando:
 .. code-block:: python
   
   $ docker cp 9c5c3f055843:/backups ./backups

Para copiar backups de un directorio local a un contenedor, se ejecuta el siguiente comando:
 .. code-block:: python
   
   $ docker cp <local_dir> <container_id>:/backups

Por ejemplo, dado 9c5c3f055843 es el ID del contenedor copiar todas las copias de seguridad a un directorio local, se ejecuta el siguiente comando:
 .. code-block:: python
      
   $ docker cp ./backups 9c5c3f055843:/backups

Para restaurar un backup existente, se ejecuta el siguiente comando:
 .. code-block:: python
   
   $ docker compose -f local.yml exec postgres restore backup_2023_03_13T09_05_07.sql.gz

Ejecución de comandos de pruebas unitarias:
----------------------------------------------------------------------
A continuación se demuestran los comandos a ser utilizados para las pruebas unitarias.

Para ejecutar las pruebas unitarias, se ejecuta el siguiente comando:
 .. code-block:: python
   
   $ docker compose -f local.yml run --rm django pytest

Puede ejecutar el pytest con cobertura de código escribiendo el siguiente comando:
 .. code-block:: python
      
   $ docker compose -f local.yml run --rm django coverage run -m pytest

Para ver el informe de cobertura de código, se ejecuta el siguiente comando:
 .. code-block:: python
      
   $ docker compose -f local.yml run --rm django coverage report
.. 
   :members:
   :noindex:

