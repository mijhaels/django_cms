# contentflow

Sistema de Gestión de Contenidos

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

## Comandos básicos
## Despliegue
- Para la creación del stack, abra un terminal en la raíz del proyecto y ejecute lo siguiente para el desarrollo local:

      $ docker-compose -f local.yml build

- Para la ejecución del stack, ejecute el siguiente comando:

      $ docker-compose -f local.yml up      
### Configuración de los usuarios

- Para crear una **cuenta de usuario normal**, sólo tienes que ir a Regístrate y rellenar el formulario. Una vez que lo envíes, verás una página "Verifica tu dirección de correo electrónico". Ve a tu consola para ver un mensaje simulado de verificación de correo electrónico. Copie el enlace en su navegador. Ahora el correo electrónico del usuario debería estar verificado y listo para funcionar.

- Para crear una **cuenta de super usuario**, utiliza este comando:

      $ docker compose -f local.yml run --rm django python manage.py createsuperuser

Para mayor comodidad, puedes mantener a tu usuario normal conectado en Chrome y a tu superusuario conectado en Firefox (o similar), de modo que puedas ver cómo se comporta el sitio para ambos tipos de usuarios.

#### Correr los tests con pytest
- Para llevar a cabo la acción utilice este comando:

      $ docker compose -f local.yml run --rm django pytest
