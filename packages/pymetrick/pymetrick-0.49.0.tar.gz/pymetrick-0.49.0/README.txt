PYMETRICK
============
Pymetrick version 0.49.0

Mini libreria de desarrollo web basado en Python 3.x ( TODO EN UNO ), al disponer de muchos de los modulos necesarios dirigido a desarrollos web (templates, session/cookies, routing de solicitudes, gestión BB.DD., rst - reStructuredText, identificacion de conexiones, tratamiento de imagenes, tratamiento de correos,...etc) podremos completar nuestros proyectos facilmente.

No dispone de un servidor de aplicaciones. Por lo que los desarrollos realizados, deberan configurarse con mod_wsgi si se ejecutan en el servidor Apache 2 o bien adaptarlos a otros servidores de aplicaciones disponibles ( CherryPy, Tornado, waitress,... ).

Se aceptan contribuciones de codigo que permitan la adaptacion a desarrollos empresariales, con igual licencia que PYMETRICK.


INDICE DE MODULOS
-----------------

- TEMPLATE o como interpretar plantillas .tpl y transformarlas en HTML5
- DEVICE o como identificar accesos con dispositivos, navegadores, motores e idiomas.
- ROUTING o como manipular direcciones HTTP a funciones ( controller )
- IMAGE o como gestionar imagenes
- SQLDB y DB_SQLITE o como gestionar BB.DD.
- SESSION o como identificar usuarios y seguridad de acceso
- MAIL tratamiento de correo
- EXCHEQUER tratamiento fiscal e identificación (NIF/CIF/NIE/VAT)
- HELPERS o gestion de utilidades universales de uso comun
- RST o reStructuredText gestiona el formato de textos convirtiendolo en html
- COMMON o donde identificar valores universales


TEMPLATE
--------

Realiza la gestion de plantillas ( con extension .tpl ), generando codigo HTML5. Similar a JINJA2 pero mucho mas simple.

A continuación se identifica codigo para realizar plantillas :

<% ..... %>    
Se puede introducir cualquier tipo de informacion, si los datos se separan con el caracter | se enviara como una lista de elementos o si ademas, los elementos estan separados por clave valor con = se enviara un diccionario. La informacion enviada entre estas etiquetas, se procesara en funcion del primer elemento. Si no pudiera ser procesado por el primer elemento, se incluira igual que si se hubiera incluido entre etiquetas {%literal%} {%endliteral%}.
Por ejemplo, para incluir en el bloque \<head\>

             <%title|Prueba Html5%>
             <%author|Fco.Javier Tamarit%>
             <%description|Prueba Html5%>
             <%script|../../web/js/jquery.min.js||text/javascript%>
             <%script|../../web/js/jquery-ui.min.js||text/javascript%>

o para incluir en el bloque \<body\>

             <%type="hidden"|id="sessionID"|value=""%>
             <%type="number"|id="numero"|label="Numero"|placeholder="Introduzca numero"|br=""%>
             <%type="tel"|id="telefono"|label="Telefono"|placeholder="Introduzca telefono"|br=""%>
             <%type="submit"|id="s"|value="Acceso"|size=10%>
             <%type="submit"|id="r"|value="Registrarse"%>

{% ..... %}    
Separa la informacion por bloques, el inicio de bloque se nombrara como {%block body%} y el final como {%endblock body%}. Esto creara una etiqueta \<body\> y al finalizar, otra etiqueta \</body\>. Los bloques permitidos son html, head, body, footer, article, section, aside, form, header, hgroup, table, nav.
Algunos bloques pueden incluir informacion en su etiqueta inicial como :

             {%block html|lang="es"%}
             {%block body|onload="MideScreen()"%}
             {%block form|id="Login",method="POST",action="/input"%}

Observe que los parametros estan separados de la etiqueta mediante |

Los bloques iniciados y no cerrados, se cerraran de forma automatica al finalizar el proceso de la plantilla.

{%literal%} .....  {%endliteral%}
La informacion incluida entre estas dos etiquetas, no tendra ninguna tranformacion, se incluirá exactamente como se haya introducido.

             {%literal%}
             script type="text/javascript">  
                 document.createElement("nav"); 
                 document.createElement("header"); 
                 document.createElement("footer"); 
                 document.createElement("section"); 
                 document.createElement("article"); 
                 document.createElement("aside"); 
                 document.createElement("hgroup");
             </script
             {%endliteral%}



<--!  .....  -->  
La informacion contenida entre estas dos etiquetas, se entendera que corresponde a un comentario y no se procesara en el código resultado.

{%extend fichero_template.tpl%}
La etiqueta {%extend se empleara para incluir un fichero con formato de plantilla en la plantilla que se esta procesando. De forma que no se repita el mismo codigo en todas las plantillas y pueda unificarse en un solo fichero de plantilla externo. El nombre de fichero no puede contener espacios.

{%merge fichero_externo.txt%}
La etiqueta {%merge también importa un fichero externo, pero su contenido no sera procesado y se incluira tal cual se importe. El nombre de fichero no puede contener espacios.


{{  .....  }}  
Los datos incluidos entre doble llave, se consideran variables o funciones a procesar, que igualmente deben devolver un valor.
             
DEVICE
------

A partir del 'user-agent' proporcionado por el cliente, es posible identificar : S.O., navegador, motor, idiomas admitidos, dispositivo origen y adaptar la respuesta.

ROUTING
-------

Con su ayuda, se construyen las reglas de actuacion ante las posibles solicitudes de los clientes, permitiendo respuestas flexibles en funcion de parametros dinamicos.

Importar routing:

from pymetrick.routing import *

Primero debe crear una ruta al subdominio de la siguiente forma :

        rules_web = Map(default_subdomain='www',redirect_defaults='/')

        Las rutas a páginas se crean de la siguiente forma :

        rules_web.add(rule='/login',controller='login')
        rules_web.add(rule='/login/nada',controller='login')
        rules_web.add(rule='/login/nada/todo',controller='login')
        rules_web.add(rule='/registro',controller='registro')
        rules_web.add(rule='/prueba',controller='prueba')

        Ahora, cuando busque una ruta debe indicarlo como :

        rules_web.match('login')
        rules_web.match('/login/nada/todo')
        rules_web.match('/varios')

        esto ejecutara el controlador parametrizado.

        Si la ruta obtenida del cliente, contiene datos del tipo
        '/auth?user=javier&passw=tonto'
        se eliminaran para evaluar correctamente la ruta

        Y si no existe la ruta, devolvera 404 y podremos redirigirlo
        if rules_web.match('/no_existe')=="404":
           rules_web.match('/')
        ''')

IMAGE
-----

Este modulo permite la adaptacion o manipulacion de las imagenes a cualquier necesidad, desde el peso de las imagenes hasta su formato.

Importar Image:

from pymetrick.image import *

Utilidades con imagenes :
        image_size(__path__) Comprueba las dimensiones de la imagen.

        image_resize(__path__,__factor__=1,__resized_path__='') Convierte fichero de imagen a un tamaÃ±o diferente, ademas es posible cambiar el tipo de imagen de png, jpeg o gif a otro cuando se renombra el fichero de imagen resultante.

        strip_metadata(image_path,newImage=None) Elimina los metadatos EXIF de una imagen, guardando en el mismo nombre de imagen o bien en otra imagen nueva.

        image2html('logo.png') Devuelve una imagen en base64 como un string de forma que se pueda utilizar como imagen embebida en css o html.

        image2base64('logo.png') Devuelve una imagen en base64 extendido  ( file_name$string_base64).

        image_download('http://nadadenada.com/coche.png', '/img/coche_2.png') Descarga una imagen desde una url con <urllib> y permite renombrar el fichero.

        image_checksums('logo.png') Devuelve un hash como un string que identifica la imagen para ser comparada con otras imagenes.

        image_compare(file1,file2) Devuelve 0 si las imagenes comparadas son iguales, en caso contrario devolvera un valor distinto de 0.
        
        image_qrcode('/home/content.png'logo.png') Devuelve datos/informacion en formato qrcode como imagen png

SQLDB 
--------

Facilita la creacion, modificacion, solicitud y eliminacion de tablas o datos al servidor MySQL, gestionando adecuadamente la conexion y permisos.

DB_SQLITE
---------

Facilita la creacion, modificacion, solicitud y eliminacion de tablas o datos en una bb.dd. SQLite.

SESSION
-------

Con el modulo SESSION se introduce la identificacion de las conexiones de los usuarios.

MAIL
-----

Con el modulo MAIL se gestiona el correo electronico.

Parametros necesarios :  

    sendMail()
        _sender       - str  -  enviado desde
        _to           - list -  enviar a
        _cc           - list -  enviar copias
        _bcc          - list -  enviar copias ocultas
        _subject      - str  -  asunto
        _text         - str  -  text/plain del mensaje
        _html         - str  -  text/html  del mensaje
        _user         - str  -  usuario
        _password     - str  -  password
        _smtpserver   - str  -  servidor
        _port         - str  -  puerto
        _files        - list -  ficheros adjuntos
        _output       - str  -  el contenido del mensaje se grabara como un fichero

    getMail()
        _user         - str  -  usuario
        _password     - str  -  password
        _imapserver   - str  -  servidor IMAP
        _pop3server   - str  -  servidor POP3
        _port         - str  -  puerto
        _criteria     - str  -   
                        ALL - devuelve todos los mensajes que coinciden con el resto del criterio
                        ANSWERED - coincide con los mensajes con la bandera \\ANSWERED establecida
                        BCC "cadena" - coincide con los mensajes con "cadena" en el campo Bcc:
                        BEFORE "fecha" - coincide con los mensajes con Date: antes de "fecha"
                        BODY "cadena" - coincide con los mensajes con "cadena" en el cuerpo del mensaje
                        CC "cadena" - coincide con los mensajes con "cadena" en el campo Cc:
                        DELETED - coincide con los mensajes borrados
                        FLAGGED - coincide con los mensajes con la bandera \\FLAGGED establecida (algunas veces referidos como Importante o Urgente)
                        FROM "cadena" - coincide con los mensajes con "cadena" en el campo From:
                        KEYWORD "cadena" - coincide con los mensajes con "cadena" como palabra clave
                        NEW - coincide con los mensajes nuevos
                        OLD - coincide con los mensajes antiguos
                        ON "fecha" - coincide con los mensajes con Date: coincidiendo con "fecha"
                        RECENT - coincide con los mensajes con la bandera \\RECENT establecida
                        SEEN - coincide con los mensajes que han sido leídos (la bandera \\SEEN esta estabecido)
                        SINCE "fecha" - coincide con los mensajes con Date: despues de "fecha"
                        SUBJECT "cadena" - coincide con los mensajes con "cadena" en Subject:
                        TEXT "cadena" - coincide con los mensajes con el texto "cadena"
                        TO "cadena" - coincide con los mensajes con "cadena" en To:
                        UNANSWERED - coincide con los mensajes que no han sido respondidos
                        UNDELETED - coincide con los mensajes que no estan eliminados
                        UNFLAGGED - coincide con los mensajes que no tienen bandera
                        UNKEYWORD "cadena" - coincide con los mensajes que no tienen la palabra clave "cadena"
                        UNSEEN - coincide con los mensajes que aun no han sido leidos
        _outputdir    - str  -

    deleteIMAP()
        _user         - str  -  usuario
        _password     - str  -  password
        _imapserver   - str  -  servidor IMAP
        _port         - str  -  puerto
        _folder       - str  -  carpeta a tratar

    timeZone(zona)

EXCHEQUER
---------

Con el modulo EXCHEQUER pueden introducirse datos identificativos fiscales en las transacciones comerciales, asi como validar
las identificaciones aportadas segun reglas de cada pais.

HELPERS
-------

Se admiten todas las clases o funciones que por su funcionalidad, puedan compartirse entre los restantes modulos o no tengan un fin funcional asociado a los restantes modulos.

             
RST o reStructuredText
----------------------

A partir de ficheros con extension .rst y codificados como un reStructuredText se obtienen ficheros HTML5 completos o HTML5 parciales que completaran otros ficheros HTML5 principales.


COMMON
------

Proporciona listas de valores universales para todos los modulos.

VERSIONES
---------

Las versiones estables se indicaran con numero de version par. Las versiones en desarrollo y que incorporen caracteristicas experimentales se numeraran con version impar.


Ver 0.01     21/09/2012  Licencia GPLv3  - en desarrollo -
    Los inicios de desarrollo se han realizado sobre un RASPBERRY PI 512Mb RAM, 1 Ghz CPU y SD de 64 Gb, evolucionando satisfactoriamente. El objetivo es 
    obtener una libreria simple, completa y funcional. El software instalado sobre la misma plataforma es MYSQL 5 y servidor APACHE 5 incorporando mod_wsgi.

Ver 0.02     20/08/2015  Licencia GPLv3  - version estable -

Ver 0.48.4   15/12/2018  Licencia GPLv3  - version estable -

Ver 0.49.0   26/08/2019  Licencia GPLv3  - version estable - 
    

CREDITOS O COLABORACIONES
-------------------------

Cualquier desarrollo aportado a PYMETRICK debe cumplir unas normas de calidad y deben ser debidamente documentados en su codigo antes de aprobar su incorporarcion a esta libreria, debiendo respetar la licencia GPLv3. En la cabecera  'CREDITS' de los modulos afectados por mejoras o nuevos desarrollos, se incorporara el reconocimiento a su desarrollador o colaboracion.
