# Sistema de Agendamiento de Citas Médicas

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un Web Service REST para la gestión de citas médicas, permitiendo a los usuarios registrarse, autenticarse y administrar citas de manera eficiente.

El sistema está diseñado bajo principios de arquitectura REST, facilitando la comunicación entre cliente y servidor mediante el uso de endpoints HTTP y estructuras de datos en formato JSON.

---

## Objetivo General

Desarrollar un servicio web que permita la gestión integral de citas médicas, garantizando validaciones de negocio, control de acceso y correcta manipulación de la información.

---

## Funcionalidades Principales

* Registro de usuarios
* Autenticación mediante credenciales
* Registro de pacientes
* Registro de médicos
* Agendamiento de citas médicas
* Consulta de citas
* Cancelación de citas
* Reprogramación de citas
* Listado de citas por usuario
* Eliminación de citas (administrador)

---

## Arquitectura del Sistema

El sistema sigue una arquitectura basada en servicios REST, donde cada funcionalidad es expuesta mediante endpoints HTTP.

Se implementa una separación de responsabilidades entre:

* Controladores (gestión de solicitudes HTTP)
* Servicios (lógica de negocio)
* Repositorios (acceso a datos)

Además, se contempla el uso de autenticación mediante tokens (JWT) para proteger los endpoints.

---

## Tecnologías Utilizadas

* Lenguaje: Java / Node.js (según tu implementación)
* Framework: Spring Boot / Express
* Base de datos: MySQL / PostgreSQL
* Control de versiones: Git y GitHub
* Pruebas: Postman

---

## Estructura del Proyecto

```bash
src/
 ├── controllers/
 ├── services/
 ├── repositories/
 ├── models/
 └── config/
```

---

## Endpoints Principales

### Autenticación

* POST `/api/v1/auth/login`

### Usuarios

* POST `/api/v1/users`

### Pacientes

* POST `/api/v1/pacientes`

### Médicos

* POST `/api/v1/medicos`

### Citas

* POST `/api/v1/citas`
* GET `/api/v1/citas/{id}`
* GET `/api/v1/citas`
* PATCH `/api/v1/citas/{id}`
* PUT `/api/v1/citas/{id}`
* DELETE `/api/v1/citas/{id}`

---

## Ejemplo de Respuesta

```json id="readmejson1"
{
  "mensaje": "Cita agendada correctamente",
  "data": {
    "cita_id": 1,
    "fecha": "2026-03-25",
    "hora": "10:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
```

---

## Seguridad

El sistema contempla el uso de autenticación mediante tokens JWT, los cuales deben ser enviados en cada solicitud a los endpoints protegidos.

---

## Pruebas

Las pruebas del sistema fueron realizadas utilizando Postman, validando:

* Casos exitosos
* Validaciones de datos
* Manejo de errores
* Respuestas del servidor

---

## Control de Versiones

Se utilizó Git como sistema de control de versiones, implementando el uso de ramas:

* main
* development
* feature/*

Se gestionaron los cambios mediante Pull Requests, asegurando revisión de código y correcta integración.

---

## Metodología de Trabajo

Se implementó una metodología basada en Kanban, organizando el trabajo en:

* Backlog
* En progreso
* En pruebas
* Finalizado

Cada funcionalidad fue desarrollada como una historia de usuario independiente.

---

## Autor

Proyecto desarrollado por:

* Sebastian Andres Garcia Payares

---

## Conclusión

El sistema desarrollado permite la gestión eficiente de citas médicas mediante un enfoque estructurado, validando reglas de negocio y asegurando la integridad de la información.

Además, el uso de buenas prácticas de desarrollo y control de versiones permite que el sistema sea escalable y mantenible.
