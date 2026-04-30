
# [HU-03] Registrar paciente 


## 📖 Historia de Usuario

Como administrador

Quiero registrar pacientes en el sistema

Para gestionar su información y poder asignarles citas médicas


## 🔁 Flujo Esperado

- El administrador ingresa los datos del paciente (nombre, documento, correo, teléfono) desde la interfaz.
- El sistema consume el endpoint /api/v1/pacientes.
- El backend valida la autenticación mediante token JWT.
- Se validan los campos obligatorios.
- Se valida el formato del documento (numérico y longitud válida).
- Se valida el formato del correo electrónico.
- Se valida el formato del número telefónico.
- Se valida que el documento no esté registrado previamente.
- Se valida que el correo no esté registrado previamente.
- Se asigna un estado inicial al paciente (ACTIVO).
- Se almacena la información del paciente en la base de datos.
- Se genera un identificador único para el paciente.
- Se registra la fecha de creación.
- El sistema retorna confirmación del registro.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST para registrar pacientes.
- [ ] Se requiere autenticación mediante JWT.
- [ ] Se validan los campos obligatorios.
- [ ] Se valida formato de documento, correo y teléfono.
- [ ] Se valida que el documento no exista previamente.
- [ ] Se valida que el correo no exista previamente.
- [ ] Se asigna un estado inicial al paciente.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Paciente registrado correctamente",
  "data": {
    "paciente_id": 1,
    "nombre": "Maria Lopez",
    "documento": "123456789",
    "estado": "ACTIVO"
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json id="hu03error"
{
  "mensaje": "El paciente ya está registrado",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Registro de Paciente

* **Método HTTP:** `POST`
* **Ruta:** `/api/v1/pacientes`

## 📤 Ejemplo de Respuesta JSON

````json id="hu03example"
```json
{
  "mensaje": "Paciente registrado correctamente",
  "data": {
    "paciente_id": 1,
    "nombre": "Maria Lopez",
    "documento": "123456789",
    "estado": "ACTIVO"
  },
  "success": true
}
```
````

* [ ] Si ocurre error:

```json id="hu03example2"
{
  "mensaje": "El paciente ya está registrado",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El paciente no existe en la base de datos.
* **Acción:** Ejecutar POST /api/v1/pacientes.
* **Resultado esperado:**

  * Código HTTP 201 Created
  * Paciente registrado correctamente
  * Retorna ID del paciente
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** Documento ya registrado.
* **Acción:** Ejecutar POST /api/v1/pacientes.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje de duplicidad
  * success = false

### ❌ Caso 3:

* **Precondición:** Correo ya registrado.
* **Acción:** Ejecutar POST /api/v1/pacientes.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje de duplicidad

### ❌ Caso 4:

* **Precondición:** Formato de documento inválido.
* **Acción:** Ejecutar POST /api/v1/pacientes.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Validación de formato

### ❌ Caso 5:

* **Precondición:** Token inválido o no enviado.
* **Acción:** Ejecutar endpoint sin autenticación.
* **Resultado esperado:**

  * Código HTTP 401 Unauthorized

### ❌ Caso 6:

* **Precondición:** Error en la base de datos.
* **Acción:** Ejecutar endpoint bajo fallo.
* **Resultado esperado:**

  * Código HTTP 500 Internal Server Error
  * Mensaje: "Error al registrar paciente"

## ✅ Definición de Hecho

#Historia: Registro de Paciente

## 📦 Alcance Funcional

* [ ] El paciente se registra correctamente
* [ ] Se valida duplicidad de documento y correo
* [ ] Se asigna estado inicial al paciente

## 🧪 Pruebas Completadas

* [ ] Pruebas de registro exitoso
* [ ] Pruebas de duplicidad
* [ ] Pruebas de validación de datos
* [ ] Pruebas de autenticación
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Propósito del endpoint
  * Validaciones aplicadas
  * Estructura de datos
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 401 para autenticación
* [ ] Se devuelve código HTTP 409 para duplicidad
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica

## Dependencias

- Depende de: HU-01 Registrar usuario
