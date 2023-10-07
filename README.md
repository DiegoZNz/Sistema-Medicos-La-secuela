# Sistema-Medicos-La-secuela
Proyecto de sistema médico de la materia de Programación Orientada a Objetos, del 6to cuatrimestre de la carrera de Ingeniería en Sistemas Computacionales de la Universidad Politécnica de Querétaro

**La calificación final del proyecto fue 10**

Herramientas usadas:

Flask, python, bootstrap, html, css, javascript, sweetalerts, mysql

Requerimientos Funcionales de la aplicación web

Se necesita una aplicación web para un centro médico, que requiere
automatizar algunos procesos para el procesamiento de la información:

Procesos:

1. Login:

a. Control de acceso solicitando RFC del Médico y Contraseña

2. Administración Médicos:

a. CRUD para la administración de los usuarios que pueden
acceder al sistema

b. Datos del médico obligatorios RFC, Nombre completo, Cedula
profesional, correo, password (cifrado), rol (Medico Admin y Medico)

c. Solo el Usuario con Rol Medico Admin puede acceder a este
modulo

4. Expediente de pacientes:

a. En este módulo el medico registrara a los pacientes que asistan
al consultorio para generar su expediente

b. Datos obligatorios que lleva el Expediente: Médico que atiende,
Nombre completo del paciente, Fecha de nacimiento

c. Datos opcionales: Enfermedades crónicas, Alergias, Antecedentes
familiares


4. Cita Exploración y diagnóstico:

a. En el módulo el medico registrara el resultado de la exploración
al paciente y el diagnostico

b. Exploración: El medico seleccionara el paciente previamente
registrado captura los siguientes datos de la exploración; Fecha
,Peso, Altura, Temperatura, Latidos por minuto , saturación de
oxigeno glucosa, La edad del paciente se calcula en base a la
fecha de nacimiento

c. Diagnóstico: En este apartado el medico registra los Síntomas,
Dx (Diagnostico), Tratamiento (medicamentos e indicaciones)
también es necesario un apartado para solicitud de Estudios en
caso de requerirlo

d. Receta: Después de guardar los resultado de la cita el sistema
generara una receta con los datos del médico que atiende

e. La receta debe tener la posibilidad debe descargada en PDF

5. Consultar pacientes:

a. En este apartado se puede consultar los pacientes y sus
respectivos expedientes

b. El medico solo puede ver los pacientes que atiende

c. Se tiene la opción para editar los siguientes datos del
expediente: Nombre completo del paciente, Fecha de
nacimiento, enfermedades crónicas, Alergias y Antecedentes
familiares

6. Consultar citas:

a. Este módulo tiene como objetivo consultar todas las citas que a
tenido el paciente, así como la posibilidad de una re impresión
de la receta en caso de ser necesario

b. La consulta de los pacientes puede ser filtrada por nombre del
paciente y/o fecha de la cita

Requerimientos no funcionales de la aplicación web:

1. Proteger las rutas como método de seguridad

2. Cuidar la estética del proyecto

3. Tener en cuenta la usabilidad de las interfaces para el mejor
desempeño
de la aplicación

4. Mensajes de información siempre visibles y claros para el usuario
