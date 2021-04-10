EG Butler (c)
=============
Powered by Emtec Group

# Gesti&oacute;n de solicitudes

**EG Butler** permite la gesti&oacute;n de solicitudes de provisionamiento de m&aacute;quinas virtuales en la soluci&oacute;n IaaS para le cliente ***AGUAS ANDINAS***

## Proceso de Aprovisionamiento Autom&aacute;tico

Es el proceso que permite provisionar los recursos requeridos para implementar una m&aacute;quina virtual en la plataforma IaaS de ***AGUAS ANDINAS***, para lo cual se crea una solicitud con el m&iacute;nimo indispensable de datos requeridos para esta creaci&oacute;n, esta solicitud est&aacute; sujeta a aprobaci&oacute;n antes del inicio del provisionamiento autom&aacute;tico, una vez aprobada la solicitud **EG Butler** orquesta la creaci&oacute;n de la m&aacute;quina virtual en la plataforma **Iaas**, inicia el monitoreo de disponibilidad via **EG Monitor** (c) y activa la tarificaci&oacute;n de servicios seg&uacute;n los recursos provisionados usando **EG Collector** (c).

En este proceso se consieran 2 roles principales:

### Solicitante

Usuario autorizado para solicitar provisionamiento de m&aacute;quinas virtuales, estos usuarios est&aacute;n predefinidos y se identifican en el sistema usando una combinaci&oacute;n de nombre de usuario y contrase&ntilde;a.

### Aprobador

Usuario autorizado para modificar y aprobar las solicitudes de m&aacute;quinas virtuales ingresadas por los Solicitantes

**EG Butler** pone a disposici&oacute;n de los usuarios del sistema una interfaz de usuario dise&ntilde;ada para ser simple e intuitiva, todo se inicia con la identificaci&oacute;n del usuario:

<img src="/home/gvalera/GIT/EG-Butler-Tools/code/src/app/static/img/butler_login.png">

Una vez identificado, el usuario tiene acceso a las funciones generales del sistema de acuerdo al perfil asignado a su rol en el proceso, para los roles ***Solicitante*** y ***Aprobador***, sendas opciones de men&uacute; se habilitan y el usuario centraliza sus acciones usando estas opciones principales.

<img src="/static/img/request_list.png">

El listado de solicitudes permite la visualizaci&oacute;n de las solicitudes de forma que puedan gestionarse usando siempre una vista familiar.

A partir de esta visualizaci&oacute;n el usuario tiene funciones generales de acuerdo a su perfil:

Para el Solicitante:

Acci&oacute;n | Descripci&oacute;n
------------- | ------------------
|
**Retorno**   | Regresa a la pantalla anterior, deja sin efecto cualquier acci&oacute;n vigente |
|
**Nueva**     | Creaci&oacute;n de una nueva solicitud |
|
**Principal** | Regresa apantalla principal del sistema, deja sin efecto cualquier acci&oacute;n en curso |

Para el Aprobador

Acci&oacute;n | Descripci&oacute;n
------        | ------------------
|
**Retorno**   | Regresa a la pantalla anterior, deja sin efecto cualquier acci&oacute;n vigente
|
**Nueva**     | Creaci&oacute;n de una nueva solicitud
|
**Principal** | Regresa a la pantalla principal del sistema, deja sin efecto cualquier acci&oacute;n en curso

El listado de solicitudes permite acciones directas sobre cada solicitud identificada por un n&uacute;mero de solicitud, las herramientas consideradas son:

Acci&oacute;n      | Descripci&oacute;n
-------------      | ------------------
|
**Detalle**        | Muestra el detalle de la solicitud. El nivel de detalle esta especificado seg&uacute;n el rol del usuario.
|
**Edici&oacute;n** | Visualiza el formulario de modificaci&oacute;n de la solicitud, este permitir&aacute; la edici&oacute;n de los detalles y/o estado de la solicitud dependiendo del rol del usuario y el estado vigente de la solicitud.

## Edici&oacute;n de Una Solicitud

<img src="/home/gvalera/GIT/EG-Butler-Tools/code/src/app/static/img/request_form.png">

**EG Butler** esta dise&ntilde;ado para minimizar los datos requeridos para un provisionamiento efectivo de m&aacute;quinas virtuales en la plataforma IaaS de ***AGUAS ANDINAS***. El Usuario puede modificar los datos requeridos por una solicitud de acuerdo a los siguientes criterios:

Campo                      | Descripci&oacute;n
-----                      | -----------
|
**Nombre**                 | Nombre asociado a la m&aacute;quina virtual, este identificador ser&aacute; utilizado como base para crear el identificador &uacute;nico en toda la plataforma IaaS y la integraci&oacute; con los otros m&oacute;dulos **EG Suite**
|
**CPU**                    | N&uacute;mero de CPUs virtuales a provisionar en la m&aacute;quina virtual durante el proceso de provisionamiento inicial autom&aacute;tico.
|
**RAM**                    | Cantidad de memoria virtual en GB a provisionar en la m&aacute;quina virtual durante el proceso de provisionamiento inicial autom&aacute;tico.
|
**Centro de Costo**        | Agrupamiento utilizado para distribuci&oacute;n de costos de recursos aprovisionados , esta distribuci&oacute;n se utiliza durante el proceso de tarificaci&oacute;n. los ***"centros de costo"*** se listar&aacute;n como opciones aqui, seg&uacute;n sean implementados en la infraestructura IaaS.
|
**Tipo de Disco**          | Especifica el tipo de almacenamiento a utilizar en el aprovisionamiento, solo se usar&aacute; un solo tipo de almacenamiento por cada maquina virtual, el cual aplicar&aacute; para todos los discos virtuales que se provisionen, los tipos se listar&aacute;n como opciones aqui pudiendo ser HDD,SSD,... seg&uacute;n sean implementados en la infraestructura IaaS.  
|
**Discos**                 | Matriz con la opci&oacute;n para provisionar hasta 12 discos en la primera solicitud, a cada disco se le puede asignar un tama&ntilde;o en GB de almacenamiento y opcionalmente indicar una imagen de disco a cargar autom&aacute;ticamente en el proceso de creaci&oacute;n.

Una vez definidos los valores requeridos el usuario tiene las siguientes opciones:

Opci&oacute;n | Descripci&oacute;n
---           | ---
|
**Grabar** | Guardar los datos nuevos o modificados segun corresponda, en el caso del **Solicitante** iterar&aacute; entre una nueva solicitud o las modificaciones a una existente antes de ser ***completada***.
|
**Completado** | Los solicitantes, cuando ya no deseen modificar su solicitud pueden ***"completarla"***, en este momento quedar&aacute; a disposici&oacute;n de los aprobadores para ser ***Revisada**, ***Rechazada*** o ***Aprobada***.
|
**Eliminar** | Los solicitantes pueden cancelar su solicitud siempre y cuando no haya sido aun gestionada por un aprobador (***Revisada***, ***Rechazada*** o ***Aprobada***)
|
**Cancelar** | Abortar cualquier modificaci&oacute;n realizada a los campos de la solicitud, no cambia el estado de la solicitud y se retorna a la pantalla del listado de solicitudes correspondiente. 
|
**Rechazar** | Los aprobadores pueden rechazar una solicitud si esta no cumple con los requisitos administrativos correspondientes o en su defecto recibe una petici&oacute;n por parte de un soliictante que ha decidido eliminar la solicitud pero esta ya ha sido ***Revisada*** por un **Aprobador**. Este es un estado final y la solicitud no puede proseguir.
|
**Aprobar** | Los aprobadores despu&eacute;s de revisar la solicitud deciden si la aprueban, ejecutada esta acci&oacute;n se activa el proceso de provisionamiento autom&aacute;tico, el avance del proceso puede ser seguido consultando el estado de una solicitud espec&iacute;fica via el listado de solicitudes correspondientes.
|
**Retorno** | En diversas ocaciones y seg&uacute;n el perfil del usuario, es posible que no existan acciones espec&iacute;ficas que afecten el estado de la solicitud, es as&iacute; que la &uacute;nica opci&oacute;n posible se retornar a la pantalla anterior. 

## Visualizaci&oacute;n de la solicitud

<img src="/home/gvalera/GIT/EG-Butler-Tools/code/src/app/static/img/request_show.png">

Esta vista permite visualizar el estado general de una solicitud incluyendo historial de estado, tambi&eacute;n muestra una estimaci&oacute;n del costo mensual aproximado a cargar por cada m&aacute;quina virtual provisionada, esta estimaci&oacute;n se hace en funci&oacute;n del tarifario vigente y considerando el provisionamiento de los recursos especificados en la solicitud por un periodo de treinta dias calendarios.

## Matriz de Estados

Una solicitud tiene un ciclo de vida que representa las diversas etapas que deben cumplirse en el proceso de solicitud de tal forma que todo este listo antes de activar el provisionamiento autom&aacute;tico de recursos:

<img src="/home/gvalera/GIT/EG-Butler-Tools/code/src/app/static/img/request_states.png">

Es as&iacute; que una solicitud puede ***"navegar"*** entre los siguientes estados:

Estado         | Descripci&oacute;n
-------------- | ------------------
|
**Creada**     | El solicitante ha definido las caracter&iacute;sticas de la m&aacute;quina virtual deseada asi como los detalles asociados al agrupamiento correspondiente para el proceso de distribuci&oacute;n de la facturaci&oacute;n. La Solicitud se mantiene en estado ***Creada*** a pesar de las modificaciones que el usuario le haga. Esta puede ser modificada tantas veces com el usuario requieran antes de someterla a aprobaci&oacute;
|
**Cancelada**  | El solicitante ha abortado el proceso de solicitud, el registro de la misma queda disponible por consulta y auditoria, sin embargo este es un estado final, la solicitud no proceder&aacute; a ning&uacute;n estado futuro. El **Solicitante** puede eliminar la solicitud hasta antes que sea gestionada por un **Aprobador** (***Revisada***,***Aprobada*** o ***Rechazada***).
|
**Solicitada** | El solicitante ha completado las modificaciones a su solicitud y la somete a aprobaci&oacute;n. Una vez en este estado, la solicitud puede ser gestionada solo por el Aprobador quien puede modificarla (**Revisada**) , rechazarla o aprobarla.
|
**Revisada**   | La solicitud ha sido modificada por el **Aprobador**, en t&eacute;rminos de recursos y distribuci&oacute;n para facturaci&oacute;n, estas revisiones pueden darse tantas veces como sea requerido, el solicitante no puede cancelar una solicitud una vez revisada o promovida a estados superiores (***Aprobada*** o ***Rechazada***)
|
**Rechazada**  | La solitud ha sido rechazada por el aprobador, Este es un estado final.
|
**Aprobada**   | La solicitud ha sido aprobada y queda en proceso de provisionamiento autom&aacute;tico, futuros estados son gestionados autom&aacute;ticamente por **EG Butler** hasta llegar a un estado final (***Completada*** o ***Error***)

