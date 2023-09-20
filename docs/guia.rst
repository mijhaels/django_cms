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

.. 
   :members:
   :noindex:

