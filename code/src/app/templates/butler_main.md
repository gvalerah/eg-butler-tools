<style>
  table { border-collapse: collapse; }
  table th, table td { padding: 5px; border: solid 1px #777; }
  table th { background-color: lightblue; }
</style>
EG Butler (c)
=============
Potenciado por Emtec Group

<a href="#" onclick="history.go(-1)"><img src="/static/img/back.png"  color=yellow width="32" height="32" title="" alt="Add"></a>
<hr>
**Tabla de contenido**

[TOC]

<hr>
# Gestión de solicitudes

**EG Butler** permite la gestión de solicitudes de aprovisionamiento de máquinas virtuales en la solución IaaS para el cliente ***AGUAS ANDINAS***

## Proceso de Aprovisionamiento Automático

Es el proceso que permite aprovisionar los recursos requeridos para implementar una máquina virtual en la plataforma IaaS de ***AGUAS ANDINAS***, para lo cual se crea una solicitud con el mínimo indispensable de datos requeridos para esta creación, esta solicitud está sujeta a aprobación antes del inicio del aprovisionamiento automático, una vez aprobada la solicitud **EG Butler** orquesta la creación de la máquina virtual en la plataforma **Iaas**, inicia el monitoreo de disponibilidad via **EG Monitor** (c) y activa la tarificación de servicios según los recursos aprovisionados usando **EG Collector** (c).

El primer paso es conectarse al sistema via la pagina principal:

<img src="/static/img/butler_main.png">

Luego de identificarse el usuario tendra acceso a las funciones segun su rol:

En este proceso se consieran 2 roles principales:

### Solicitante

Usuario autorizado para solicitar aprovisionamiento de máquinas virtuales, estos usuarios están predefinidos y se identifican en el sistema usando una combinación de nombre de usuario y contrase&ntilde;a.

<img src="/static/img/butler_menu_user.png">

### Aprobador

Usuario autorizado para modificar y aprobar las solicitudes de máquinas virtuales ingresadas por los Solicitantes

<img src="/static/img/butler_menu_approver.png">

**EG Butler** pone a disposición de los usuarios del sistema una interfaz de usuario dise&ntilde;ada para ser simple e intuitiva, todo se inicia con la identificación del usuario:

<img src="/static/img/butler_login.png">

Una vez identificado, el usuario tiene acceso a las funciones generales del sistema de acuerdo al perfil asignado a su rol en el proceso, para los roles ***Solicitante*** y ***Aprobador***, sendas opciones de menú se habilitan y el usuario centraliza sus acciones usando estas opciones principales.

<img src="/static/img/butler_select_requests.png">

El listado de solicitudes permite la visualización de las solicitudes de forma que puedan gestionarse usando siempre una vista familiar.

A partir de esta visualización el usuario tiene funciones generales de acuerdo a su perfil:

####Para el Solicitante:

**Acción** | **icono** | **Descripción** |
----------------- | --------- |----------------------  |
**Retorno**   | <img src="/static/img/back.png" width=32> | Regresa a la pantalla anterior, deja sin efecto cualquier acción vigente |
**Nueva**     | <img src="/static/img/add.png" width=32>  | Creación de una nueva solicitud |
**Principal** | <img src="/static/img/home.png" width=32>  | Regresa apantalla principal del sistema, deja sin efecto cualquier acción en curso | 
**Descarga**  | <img src="/static/img/download.png" width=32"> | Permite descargar la lista de solicitudes en formato MS Excel de inmediato con la relacion de todas las solicitudes del usuario |

####Para el Aprobador

**Acción** | **icono**  | **Descripción** |
----------------- | ---------  | ---------------------- |
**Retorno**       | <img src="/static/img/back.png" width=32> | Regresa a la pantalla anterior, deja sin efecto cualquier acción vigente |
**Nueva**         | <img src="/static/img/add.png" width=32>  | Creación de una nueva solicitud |
**Principal**     | <img src="/static/img/home.png" width=32>  | Regresa a la pantalla principal del sistema, deja sin efecto cualquier acción en curso |
**Descarga**      | <img src="/static/img/download.png" width=32> | Permite descargar la lista de solicitudes en formato MS Excel de inmediato, la relación estará limitada por el tipo de solicitud vigente |

El listado de solicitudes permite acciones directas sobre cada solicitud identificada por un número de solicitud, las herramientas consideradas son:

**Acción** | **icono** | **Descripción** |
----------------- | --------- | ---------------------- |
**Detalle** | <img src="/static/img/search.png" width=32> | Muestra el detalle de la solicitud. El nivel de detalle esta especificado según el rol del usuario. |
**Edición** | <img src="/static/img/edit.png" width=32> | Visualiza el formulario de modificación de la solicitud, este permitirá la edición de los detalles y/o estado de la solicitud dependiendo del rol del usuario y el estado vigente de la solicitud. |

## Edición de Una Solicitud

<img src="/static/img/butler_form_request_01.png">
<img src="/static/img/butler_form_request_02.png">

**EG Butler** esta dise&ntilde;ado para minimizar los datos requeridos para un aprovisionamiento efectivo de máquinas virtuales en la plataforma IaaS de ***AGUAS ANDINAS***. El Usuario puede modificar los datos requeridos por una solicitud de acuerdo a los siguientes criterios:

**Campo**                  | **Descripción** | 
---------                  | ---------------------- |
**Nombre**                 | Nombre asociado a la máquina virtual, este identificador será utilizado como base para crear el identificador único en toda la plataforma IaaS y la integració con los otros módulos ***EG Suite***|
**CPU cores por socket**   | Número de CPUs virtuales por aprovisionar en cada socket asignado a la la máquina virtual durante el proceso de aprovisionamiento inicial automático. El número total de nucleos de proceso será el producto de CPU cores por socket * # de sockets|
**Sockets**                | Número de sockets virtuales por aprovisionar en la máquina virtual durante el proceso de aprovisionamiento inicial automático.|
**RAM**                    | Cantidad de memoria virtual en GB por aprovisionar en la máquina virtual durante el proceso de aprovisionamiento inicial automático.|
**Corporativa**            | Dirección corporativa dentro de la estructura de ***AGUAS ANDINAS*** a la cual se relacionará la Máquina Virtual.|
**Gerencia**               | Gerencia o dirección dentro de la estructura de ***AGUAS ANDINAS*** a la cual se relacionará la Máquina Virtual.|
**Ambiente**               | Cada Máquina Virtual debe asociarse a un ambiente de trabajo especáfico, esto permite agrupar las máquinas y gestionarlas apropiadaente. El ambiente definido asocia automáticamente la MV a un ***Projecto*** y a una **Categoría** específicos, estas asociaciones permiten organizar el flujo de trabajo con la MV y determinarán el listado de Redes Virtuales disponibles para la MV en el momento de aprovisionamiento.|
**Tipo de Disco**          | Especifica el tipo de almacenamiento a utilizar en el aprovisionamiento, solo se usará un solo tipo de almacenamiento por cada maquina virtual, el cual aplicará para todos los discos virtuales que se aprovisionen, los tipos se listarán como opciones aqui pudiendo ser HDD,SSD,... según sean implementados en la infraestructura IaaS.  |
**Centro de Costo**        | La combinación de las selección de Corporativo,Gerencia,Ambiente y Tipo de Disco permiten asociar la Máquina Virtual a un centro de costo específico, esto se hace automáticamente y permitirá la distribución eficiente de los cargos asociados al uso de la MV durante el proceso de Tarificación.|
**Subredes**               | Cada Máquina Virtual  Matriz con la opción para aprovisionar hasta 12 discos en la primera solicitud, a cada disco se le puede asignar un tama&ntilde;o en GB de almacenamiento y opcionalmente indicar una imagen de disco a cargar automáticamente en el proceso de creación.
**Cluster**               | Cada Máquina Virtual debe aprovisionarse en un Cluster, agrupamiento de ervidores específico, las opciones disponibles se presentarán en esta opción de selección multiple|
**Cópias de Seguridad** | Por defecto las MV incluyen políticas de respaldo para contar con copias locales y remotas en caso de contingencia, estas opciones pueden ser deshabilitadas en el momento de creaciín de la MV|
**CDROM**                 | Por Defecto las MV incluyen la aprovisión de una unidad de disco óptico virtual, esto permite "montar" imagenes específicas durante la vida útil de la MV|
**Subredes** | Cada MV pruede aprovisionarse con hasta 4 tarjetas de red virtuales (vNIC), cada NIC estará asociada a una VLAN de las disponibles para el proyecto especificado, si las VLAN cuentan con DHCP activado se puede esperar que la MV cuente con dirección IP asignada automáticamente durante el proceso de aprovisionamiento.
**Imagen de Arranque**    | Cada MV puede ser creada incluyendo una **imagen inicial de arranque**, en caso de definirse esta se asignará al primer disco aprovisionado, el tama&ntilde;o de este primer disco sera ajustado para tener como mínimo lo requerido por la imagen. La implementación por defecto para ***AGUAS ANDINAS*** requiere que estas imagenes esten en formato UEFI de tal forma que las MV quede encendida en el momento de aprovisión|
**Discos**                 | Matriz con la opción para aprovisionar hasta 12 discos en la primera solicitud, a cada disco se le puede asignar un tama&ntilde;o en GB de almacenamiento. Para el primer disco opcionalmente se asociará la **Imagen inicial de arranque** (boot image) en el proceso de creación.|
**Requerimiento Especial** | Los requerimientos de creación de cada MV pueden diferir en algunos caso particulares, de ser necesario el solicitante o el aprobador pueden poblar este campo con instrucciones específicas a ejecutarse por el equipo de soporte de LUMEN durante el proceso de aprovisionamiento.


####Una vez definidos los valores requeridos el usuario tiene las siguientes opciones:


**Opción** | **Descripción** |
----------------- | ---------------------- |
**Grabar** | Guardar los datos nuevos o modificados segun corresponda, en el caso del **Solicitante** iterará entre una nueva solicitud o las modificaciones a una existente antes de ser ***completada***.
**Completado** | Los solicitantes, cuando ya no deseen modificar su solicitud pueden ***"completarla"***, en este momento quedará a disposición de los aprobadores para ser ***Revisada***, ***Rechazada*** o ***Aprobada***.
**Eliminar** | Los solicitantes pueden cancelar su solicitud siempre y cuando no haya sido aun gestionada por un aprobador (***Revisada***, ***Rechazada*** o ***Aprobada***)
**Cancelar** | Abortar cualquier modificación realizada a los campos de la solicitud, no cambia el estado de la solicitud y se retorna a la pantalla del listado de solicitudes correspondiente. 
**Rechazar** | Los aprobadores pueden rechazar una solicitud si esta no cumple con los requisitos administrativos correspondientes o en su defecto recibe una petición por parte de un soliictante que ha decidido eliminar la solicitud pero esta ya ha sido ***Revisada*** por un **Aprobador**. Este es un estado final y la solicitud no puede proseguir.
**Aprobar** | Los aprobadores después de revisar la solicitud deciden si la aprueban, ejecutada esta acción se activa el proceso de aprovisionamiento automático, el avance del proceso puede ser seguido consultando el estado de una solicitud específica via el listado de solicitudes correspondientes.
**Retorno** | En diversas ocaciones y según el perfil del usuario, es posible que no existan acciones específicas que afecten el estado de la solicitud, es así que la única opción posible se retornar a la pantalla anterior. 

## Visualización de la solicitud

<img src="/static/img/butler_report_request.png">

Esta vista permite visualizar el estado general de una solicitud incluyendo historial de estado, también muestra una estimación del costo mensual aproximado a cargar por cada máquina virtual aprovisionada, esta estimación se hace en función del tarifario vigente y considerando el aprovisionamiento de los recursos especificados en la solicitud por un periodo de treinta dias calendarios.

## Matriz de Estados

Una solicitud tiene un ciclo de vida que representa las diversas etapas que deben cumplirse en el proceso de solicitud de tal forma que todo este listo antes de activar el aprovisionamiento automático de recursos:

<img src="/static/img/request_states.png">

Es así que una solicitud puede ***"navegar"*** entre los siguientes estados:

Estado         | Descripción |
-------------- | ------------------ |
**Creada**     | El solicitante ha definido las características de la máquina virtual deseada asi como los detalles asociados al agrupamiento correspondiente para el proceso de distribución de la facturación. La Solicitud se mantiene en estado ***Creada*** a pesar de las modificaciones que el usuario le haga. Esta puede ser modificada tantas veces com el usuario requieran antes de someterla a aprobació
**Cancelada**  | El solicitante ha abortado el proceso de solicitud, el registro de la misma queda disponible por consulta y auditoria, sin embargo este es un estado final, la solicitud no procederá a ningún estado futuro. El **Solicitante** puede eliminar la solicitud hasta antes que sea gestionada por un **Aprobador** (***Revisada***,***Aprobada*** o ***Rechazada***).
**Solicitada** | El solicitante ha completado las modificaciones a su solicitud y la somete a aprobación. Una vez en este estado, la solicitud puede ser gestionada solo por el Aprobador quien puede modificarla (**Revisada**) , rechazarla o aprobarla.
**Revisada**   | La solicitud ha sido modificada por el **Aprobador**, en términos de recursos y distribución para facturación, estas revisiones pueden darse tantas veces como sea requerido, el solicitante no puede cancelar una solicitud una vez revisada o promovida a estados superiores (***Aprobada*** o ***Rechazada***)
**Rechazada**  | La solitud ha sido rechazada por el aprobador, Este es un estado final.
**Aprobada**   | La solicitud ha sido aprobada y queda en proceso de aprovisionamiento automático, futuros estados son gestionados automáticamente por **EG Butler** hasta llegar a un estado final (***Completada*** o ***Error***)

<hr>

# Migraciones

La función de Migraciones esta orientada a facilitar el proceso de mover grupos de máquinas virtuales desde un Cluster de la solución IaaS de ***AGUAS ANDINAS*** hacia otro. Esta operación se realiza bajo diversas circunstancias como por ejemplo pruebas de planes de recuperación de desastres (DRP).

## Interfaz de Grupos de Migración

Esta pantalla es a principal para esta función, su objetivo principal es administrar los "Grupos de Migración" facilitando una serie de funciones orientadas a su gestión y preparación para la migración efectiva. Acontinuación definiremos al gunos conceptos que nos permitan interpretar luego las especificaciones de la funcionalidad provista.

### Grupo de Migración

Un Grupo de Migración no es mas que una entidad que agrupa a una o mas máquinas virtuales que residen (están aprovisionadas) en un mismo Cluster. Esta agrupación tiene como objetivo tratar a este grupo de máquinas en simultaneo al momento de hacer una migración entre diferentes clusters.

Todo Grupo de Migración tiene como atributos:

**Atributo** | **Descripción**
-------- | -----------
**Identificador único** | Lo gestiona EG Butler y sirve para identificar al GM dentro del contexto de la aplicación.
**Nombre**              | Lo crea el cliente según sus requerimientos para identificar claramente la funcion del grupo o las caracteristicas de asociación
**Cluster de origen**   | Cluster donde estan aprovisionadas las máquinas virtuales objeto de migración.
**Cluster de destino**  | Cluster hacia donde deberán ser migradas las máquinas virtuales.
**Listado de máquinas virtuales** |  Al menos una máquina virtual debe estar incluida en este listado, una vez incluida una máquina en esta lista EG Butler verifica periodicamente su estado y capacidad de ser migrada.

### Cluster

Un Cluster (Racimo) es un equipo parte de la infraestructura IaaS de ***AGUAS ANDINAS***, en cada Cluster residen (están aprovisionadas) las máquinas virtuales de la solución y es desde ellos y hacia ellos donde las máquinas virtuales son migradas. 

### Proyecto

Cada Máquna virtual esta asociada a un "Proyecto" esta es una asociación administrativa para efectos de identificación de la smáquinas virtuales, es un atributo que EG Butler actualiza periódicamente.

### Protección

La Protección (Protection Domain) de una MV esta determinada por una serie de reglas que determinan cuando y hacia donde se deben hacer réplicas de los datos asociados a una máquina virtual para efectos de respaldo. Para que una máquina virtual pueda ser migrada debe contar con un esquema de protección definido. Los detalles se representan en agendas (schedules) de replicación.

### Agenda

Una agenda determina el tipo (horario, diario, semanal, mensual) el intervalo y la retención de las réplicas que deben ejecutarse para los datos de una MV. Para que una máquina virtual pueda ser migrada debe contar con al menos una agenda de replicación que pueda usarse durante el proceso de migración.

### Réplica

Cada réplica es una copia diferencial de los datos de una máquina virtual durante un period de tiempo determinado por su agenda. Para ejecutarse la igración deben existir réplicas de la MV a migrar, el tiempo de replicacion depende del tamaño de estas réplicas y puede extenderse si la última tiene mas de 60 minutos de ejecutadas.

A continuación una vista de la interfaz: 

<img src="/static/img/butler-migration-groups.png" width=75% align=center>

Esta vista es muy intuitiva, a continuación la exploraremos por partes para ir detallando la funcionalidad:

#### Area de mensajes

En la parte superior objervamos el area de "Mensajes" aqui se recibirá retroalimentación sobre el resultado de las acciones que se ejecuten y se indicará información relevante, mensajes de éxito, advertencias y errores en "Cajas de mensaje" como la que se muestra.

Luego se ven los detalles y botones de acción asociados a los grupos de migración y máquinas virtuales los describiremos por subgrupos:

#### Vista

**Acción**  | **Objeto**  | **Descripción**
:--------:  | :--------:  | -----------
**Retorno** | **<img src="/static/img/back.png" width=32>**  | Regresa a la vista anterior
**Inicio**  | **<img src="/static/img/home.png" width=32>**    | Regresa a la pantalla principal del sistema

#### Grupo de Migración

**Acción** | **Objeto**  | **Descripción**
:--------: | :---------: | -----------
**Buscar** | **<img src="/static/img/search.png" width=32>**  | Permite seleccionar un nuevo grupo de migración por nombre. Al pulsar esta opción se despliega una caja de selección que permite buscar y escoger un Grupo de Migración de entre todos los disponibles en EG Butler.
**Crear** | **<img src="/static/img/add.png" width=32>**   | Permite crear un nuevo Grupo de MIgración. Al pulsar esta opción se despliega una caja de entrada que permite ingresar un nombre para el nuevo grupo de migración, una vez ingresado EG Butler crea un nuevo grupo con los atributos por defecto y una lista de máqunas virtuales vacia.
**Clonar** | **<img src="/static/img/clone.png" width=32>**  | Esta opción permite "clonar" el grupo de migración en curso en uno completamente nuevo. al pulsar la opción se despliega una caja de texto con un nombre sugerido el cual puede ser editado por el usuario. Esta opción es muy util para generar grupos de migración "simétricos" ya que incluye en el nuevo grupo toda la lista de las máquinas virtuales del grupo de origen. Un ejemplo típico es para crear el grupo de igracion de "regreso" a partir del grupo de migracion de "ida"
**Editar** | **<img src="/static/img/edit.png" width=32>**   | Esta opción permite editar el nombre de un grupo de migración existente. Al pulsar esta opción se despliega una caja de texto que permite editar el nombre del Grupo de Migración en curso. 
**Cambio** | **<img src="/static/img/butler-migration-switch-button.png">** | Este botón de acción permite cambiar el cluster de origen por el de destino y viceversa, muy util para completar la configuracion de un grupo de migración por diferentes razones. Un ejemplo básico es para ajustar el "sentido" de la migracion para un Grupo de Migración recientemente clonado. 
**Cluster de Origen** | campo de selección múltiple | Este campo es de selección multiple y permite escoger el cluster que se usará como "origen" en el proceso de migración de este grupo, se selecciona cualquiera de los clusters disponibles en el sistema.
**Cluster de Destino** | campo de selección múltiple | Este campo es de selección multiple y permite escoger el cluster que se usará como "destino" en el proceso de migración de este grupo, se selecciona cualquiera de los clusters disponibles en el sistema, no puede ser igual al clustar de origen.

#### Listado de máquinas virtuales

**Acción** | **Objeto** | **Descripción**
:--------: | :--------: | -----------
**Agregar** | **<img src="/static/img/add.png" width=32>**   | Esta opción permite asociar una nueva maquina virtual al listado de máquinas del grupo. Al pulsarse esta opción se despliega un cuadro de selección que ofrece los nombres de todas las máquinas virtuales en la solución IaaS de ***AGUAS ANDINAS***, al escoger una de ellas esta es automáticamente asociada al grupo de migración. 
**Seleccionar** | **<img src="/static/img/butler-migration-checkbox.png">** | Esta caja de "chequeo" permite incluir o excluir una MV en particular de las opciones de validacion y posterior migración del grupo. Al pulsar en la caja correspondiente a una máquina virtual se esta encendiendo y apagando esta opción.
**Eliminar** | **<img src="/static/img/delete.png" width=32>** | Esta opción permite des-asociar una máquina virtual del grupo. Al pulsar esta opción la máquina virtual deja de verse en el listado de máquinas virtuales asociadas al grupo de migración.

La tabla de máquinas virtuales brinda una gran cantidad de información que puede ser interpretada rápidamente por el operador sin necesidad de "validar" el grupo de migración, el estado de cada campo en la ultima actualozacion nos da información relevante, asi tenemos:

<img src="/static/img/butler-migration-vm-list.png">

**Campo**              | **Descripcion**
---------------------- | ---------------
**Máquinas virtuales** | Nombre de la máquina virtual
**Cluster**            | Cluster donde reside la máquina virtual. Si esta en color rojo, entonces este no coincide con el cluster de origen y por tanto la migración no se puede ejecutar para esta  máquina virtual
**Proyecto**           | Nombre del proyecto asociado a la máquina virtual. Debe coincidir con el cluster donde está aprovisionada la máquina virtual.
**Encendido**          | Estado de energia d ela máquina virtual. Debe estar apagada para poder migrarse, de lo contrario la migración no puede proceder.
**Protección**         | Indica nombre de Protección (Protection domain) asociada a esta máquina virtual, si no existe se considera un error, se indica en color rojo y la migración no puede proceder
**Agendas**            | Indica en número de agendas disponibles para la máquina virtual, si existe alguna la migración puede proceder de lo contrario se considera un error.
**Réplica**            | Indica la última fecha/hora de replica de la máquina virtual, si no existe se indica y se indica como advertencia, si existe y el tiempo de creación es mas antiguo que una hora entonces se indica como advertencia en color naranja.
**Migrar**            | Esta casilla de chequeo es el único campo de la lista de máquinas que puede editarse directamente. Cuando está chequeado la máquina virtual está "seleccionada" para migración, de lo contrario no será considerada en la validación ni en la eventual migración del grupo. El estado se salva usando el botón de acción "Salvar".

#### Acciones

**Acción**  | **Objeto**   | **Descripción**
:---------: | :----:       | -----------
**Salvar** | **<img src="/static/img/butler-migration-save-button.png">**   | Este botón de acción salva cambios que se realicen sobre el grupo de migracion y que esten pendientes de almacenamiento (chequeo de migración, por ejemplo)
**Eliminar** | **<img src="/static/img/butler-migration-delete-button.png">** | Este botón de acción permite eliminar completamente el grupo de migración en curso incluyedo sus asociaciones a máquinas virtuales vigentes.
**Validar** | **<img src="/static/img/butler-migration-validate-button.png">**  | Este botón de acción permite validar el estado actual del grupo de migración y de su listado de máquinas virtuales y su potencialidad de migración, si todas las condiciones se cumplen se informa en el área de mensajes y se activa el botón "Migrar", de lo contrario se informa al usuario de las condiciones no cumpidas.
**Migrar** | **<img src="/static/img/butler-migration-migrate-button.png">**   | Este boton de acción solo se visualiza luego de una "Validación" exitosa, al seleccionarlo se inicia el proceso de migración para todas las máquinas "seleccionadas" de la lista y se redirecciona  automáticamente hacia las vistas de retro-alimentación y reporte del proceso.

<hr>

## Interfaz de Migración

El objetivo de esta pantalla es brindar retroalimentación al usuario durante el proceso de migración, en esta se visualizan las acciones que EG Butler esta tomando para procurar migrar todas las máquinas seleccionadas ejecutando reintentos de ser necesario hasta estar seguro que el proceso ha concluido o se ha excedifo el tiempo máximo determinado por el sistema para esta acción.

<img src="/static/img/butler-migration-feedback.png" width=50%>

<hr>

## Interfaz de Reporte

Al final del proceso se muestra un resumen de lo ejecutado y del resultado obtenido, la interpretación es muy sencilla y deja claro el estado general de migración de cada máquina virtual y del grupo de migración en su conjunto.

<img src="/static/img/butler-migration-report.png" width=50%>

<hr>
