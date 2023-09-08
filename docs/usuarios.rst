 .. _usuarios:

Usuarios
======================================================================



.. autoclass:: django_cms.users.models::User
   :members:

   .. attribute:: username_validator

      Validador de nombre de usuario

   .. attribute:: username

      Nombre de usuario
      
   .. attribute:: first_name

      Nombre del usuario   

   .. attribute:: last_name
            
      Apellido del usuario

   .. attribute:: email

      Email del usuario    

   .. attribute:: is_staff

      Indica si el usuario es staff

   .. attribute:: is_active

      Indica si el usuario esta activo

   .. attribute:: date_joined
      
      Fecha de registro del usuario 

   .. attribute:: objects
            
      Objeto de tipo UserManager

   .. attribute:: EMAIL_FIELD
            
      Campo de email

   .. attribute:: USERNAME_FIELD
               
      Campo de nombre de usuario

   .. attribute:: REQUIRED_FIELDS
            
      Campos requeridos   

   .. method:: clean(self)
            
      Limpia el usuario

   .. method:: get_full_name(self)

      Devuelve el nombre completo del usuario

   .. method:: get_short_name(self)

      Devuelve el nombre corto del usuario

   .. method:: email_user(self, subject, message, from_email=None, **kwargs)
            
      Envia un email al usuario
