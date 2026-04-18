# [HU-04] Registrar médico

## 📖 Historia de Usuario

Como administrador

Quiero registrar médicos en el sistema

Para asignarles citas y gestionar su información profesional

## 🔁 Flujo Esperado

* El administrador ingresa los datos del médico desde la interfaz.
* El sistema consume el endpoint `/api/v1/medicos`.
* El backend valida que el médico no esté registrado previamente.
* Se almacena la información del médico en la base de datos.
* Se genera un identificador único para el médico.
* El sistema retorna confirmación del registro.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint POST para registrar médicos.
* [ ] Se valida que el número de licencia no exista previamente.
* [ ] Se validan los campos obligatorios.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu04jsonok"
{
  "mensaje": "Médico registrado correctamente",
  "data": {
    "medico_id": 1,
    "nombre": "Dr. Carlos Ruiz",
    "especialidad": "Cardiología"
  },
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu04jsonerror"
{
  "mensaje": "El médico ya está registrado",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Registro de Médico

* **Método HTTP:** `POST`
* **Ruta:** `/api/v1/medicos`

## 📤 Ejemplo de Respuesta JSON

```json id="hu04jsonexample"
{
  "mensaje": "Médico registrado correctamente",
  "data": {
    "medico_id": 1,
    "nombre": "Dr. Carlos Ruiz",
    "especialidad": "Cardiología"
  },
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu04jsonexample2"
{
  "mensaje": "El médico ya está registrado",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El médico no existe en la base de datos.
* **Acción:** Ejecutar POST `/api/v1/medicos`.
* **Resultado esperado:**

  * Código HTTP 201 Created
  * Médico registrado correctamente
  * Se retorna ID del médico
  * success = true

### ❌ Caso 2:

* **Precondición:** La licencia ya existe.
* **Acción:** Ejecutar POST `/api/v1/medicos`.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** Datos incompletos.
* **Acción:** Ejecutar POST `/api/v1/medicos`.
* **Resultado esperado:**

  * Código HTTP 400
  * Error de validación

## ✅ Definición de Hecho

# Historia: Registro de Médico

## 📦 Alcance Funcional

* [ ] El médico se registra correctamente.
* [ ] Se valida duplicidad de licencia.
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
