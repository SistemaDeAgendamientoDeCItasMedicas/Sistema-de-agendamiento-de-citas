# [HU-06] Consultar cita médica

## 📖 Historia de Usuario

Como usuario

Quiero consultar una cita médica

Para conocer los detalles de la atención programada

## 🔁 Flujo Esperado

* El usuario ingresa el identificador de la cita desde la interfaz.
* El sistema consume el endpoint `/api/v1/citas/{id}`.
* El backend valida que la cita exista.
* Se consulta la información en la base de datos.
* El sistema retorna los datos completos de la cita.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint GET para consultar citas.
* [ ] Se valida que la cita exista.
* [ ] Se valida que el identificador sea correcto.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu06jsonok"
{
  "mensaje": "Cita consultada correctamente",
  "data": {
    "cita_id": 1,
    "paciente_id": 1,
    "medico_id": 1,
    "fecha": "2026-03-25",
    "hora": "10:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu06jsonerror"
{
  "mensaje": "La cita no existe",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Consultar Cita

* **Método HTTP:** `GET`
* **Ruta:** `/api/v1/citas/{id}`

## 📤 Ejemplo de Respuesta JSON

```json id="hu06jsonexample"
{
  "mensaje": "Cita consultada correctamente",
  "data": {
    "cita_id": 1,
    "paciente_id": 1,
    "medico_id": 1,
    "fecha": "2026-03-25",
    "hora": "10:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu06jsonexample2"
{
  "mensaje": "La cita no existe",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** La cita existe en la base de datos.
* **Acción:** Ejecutar GET `/api/v1/citas/1`.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Se retorna la información de la cita
  * success = true

### ❌ Caso 2:

* **Precondición:** La cita no existe.
* **Acción:** Ejecutar GET `/api/v1/citas/999`.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** ID inválido.
* **Acción:** Ejecutar GET `/api/v1/citas/abc`.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Error de validación

## ✅ Definición de Hecho

# Historia: Consulta de Cita Médica

## 📦 Alcance Funcional

* [ ] Permite consultar citas correctamente.
* [ ] Retorna información completa.

## 🧪 Pruebas Completadas

* [ ] Pruebas de consulta exitosa
* [ ] Pruebas de cita inexistente
* [ ] Pruebas de validación

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros para el usuario
