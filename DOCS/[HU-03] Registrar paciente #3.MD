# [HU-03] Registrar paciente

## 📖 Historia de Usuario

Como administrador

Quiero registrar pacientes en el sistema

Para gestionar su información y asignarles citas médicas

## 🔁 Flujo Esperado

* El administrador ingresa los datos del paciente desde la interfaz.
* El sistema consume el endpoint `/api/v1/pacientes`.
* El backend valida que el paciente no esté registrado previamente.
* Se almacena la información del paciente en la base de datos.
* Se genera un identificador único para el paciente.
* El sistema retorna confirmación del registro.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint POST para registrar pacientes.
* [ ] Se valida que el documento no exista previamente.
* [ ] Se validan los campos obligatorios.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu03jsonok"
{
  "mensaje": "Paciente registrado correctamente",
  "data": {
    "paciente_id": 1,
    "nombre": "Maria Lopez"
  },
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu03jsonerror"
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

```json id="hu03jsonexample"
{
  "mensaje": "Paciente registrado correctamente",
  "data": {
    "paciente_id": 1,
    "nombre": "Maria Lopez"
  },
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu03jsonexample2"
{
  "mensaje": "El paciente ya está registrado",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El paciente no existe en la base de datos.
* **Acción:** Ejecutar POST `/api/v1/pacientes`.
* **Resultado esperado:**

  * Código HTTP 201 Created
  * Paciente registrado correctamente
  * Se retorna ID del paciente
  * success = true

### ❌ Caso 2:

* **Precondición:** El documento ya existe.
* **Acción:** Ejecutar POST `/api/v1/pacientes`.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** Datos incompletos.
* **Acción:** Ejecutar POST `/api/v1/pacientes`.
* **Resultado esperado:**

  * Código HTTP 400
  * Error de validación

## ✅ Definición de Hecho

# Historia: Registro de Paciente

## 📦 Alcance Funcional

* [ ] El paciente se registra correctamente.
* [ ] Se valida duplicidad de documento.
* [ ] Se almacena en base de datos.

## 🧪 Pruebas Completadas

* [ ] Pruebas de registro exitoso
* [ ] Pruebas de duplicidad
* [ ] Pruebas de validación

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros para el usuario
