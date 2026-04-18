# [HU-01] Registrar usuario

## Historia de Usuario

Como paciente del sistema de agendamiento de citas médicas
Quiero registrarme proporcionando mis datos personales y credenciales de acceso
Para poder acceder a la plataforma y gestionar mis citas médicas de manera segura

## Flujo Esperado

* El usuario ingresa nombre, correo electrónico y contraseña desde la interfaz.
* El sistema consume el endpoint `/api/v1/users`.
* El backend valida que el correo no esté registrado.
* Se almacena la información del usuario en la base de datos.
* Se genera un identificador único para el usuario.
* El sistema retorna confirmación del registro.

## Criterios de Aceptación

### 1. Estructura y lógica del servicio

* [ ] Se expone un endpoint POST para registrar usuarios.
* [ ] Se valida que el correo no exista previamente.
* [ ] Se validan los campos obligatorios.

### 2. Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Usuario registrado correctamente",
  "data": {
    "user_id": 1,
    "email": "usuario@email.com"
  },
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json
{
  "mensaje": "El correo ya está registrado",
  "success": false
}
```

## Notas Técnicas

* Validación de datos en backend.
* Uso de base de datos relacional para persistencia.
* Generación de identificador único por usuario.

## Endpoint – Registro de Usuario

* Método HTTP: `POST`
* Ruta: `/api/v1/users`

## Ejemplo de Respuesta JSON

```json
{
  "mensaje": "Usuario registrado correctamente",
  "data": {
    "user_id": 1,
    "email": "usuario@email.com"
  },
  "success": true
}
```

## Requisitos de Pruebas

## Casos de Prueba Funcional

### Caso 1: Registro exitoso

* Precondición: El usuario no existe en la base de datos.
* Acción: Ejecutar POST `/api/v1/users`.
* Resultado esperado:

  * Código HTTP 201 Created
  * Usuario registrado correctamente
  * Retorna ID del usuario
  * Campo success = true

### Caso 2: Correo duplicado

* Precondición: El correo ya existe.
* Acción: Ejecutar POST `/api/v1/users`.
* Resultado esperado:

  * Código HTTP 400 Bad Request
  * Mensaje de error
  * success = false

### Caso 3: Campos vacíos

* Precondición: Campos obligatorios no diligenciados.
* Acción: Ejecutar POST `/api/v1/users`.
* Resultado esperado:

  * Código HTTP 400
  * Validación de campos

## Definición de Hecho

### Alcance Funcional

* [ ] El usuario se registra correctamente.
* [ ] Se valida duplicidad de correo.
* [ ] Se almacena en base de datos.

### Pruebas Completadas

* [ ] Pruebas de registro exitoso
* [ ] Pruebas de duplicidad
* [ ] Pruebas de validación

### Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

### Manejo de Errores

* [ ] Se retorna código HTTP adecuado
* [ ] Mensajes claros para el usuario
