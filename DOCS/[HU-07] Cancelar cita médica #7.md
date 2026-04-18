# [HU-07] Cancelar cita médica

## 📖 Historia de Usuario

Como paciente

Quiero cancelar una cita médica

Para liberar el espacio en la agenda del médico

## 🔁 Flujo Esperado

* El paciente selecciona la cita que desea cancelar.
* El sistema consume el endpoint `/api/v1/citas/{id}`.
* El backend valida que la cita exista.
* Se verifica que la cita no esté cancelada previamente.
* Se valida que la cita sea futura.
* Se actualiza el estado de la cita a "CANCELADA".
* El sistema retorna confirmación de la cancelación.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint PATCH para cancelar citas.
* [ ] Se valida que la cita exista.
* [ ] No se permite cancelar citas ya canceladas.
* [ ] No se permite cancelar citas pasadas.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu07jsonok"
{
  "mensaje": "Cita cancelada correctamente",
  "data": {
    "cita_id": 1,
    "estado": "CANCELADA"
  },
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu07jsonerror"
{
  "mensaje": "No es posible cancelar la cita",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Cancelar Cita

* **Método HTTP:** `PATCH`
* **Ruta:** `/api/v1/citas/{id}`

## 📤 Ejemplo de Respuesta JSON

```json id="hu07jsonexample"
{
  "mensaje": "Cita cancelada correctamente",
  "data": {
    "cita_id": 1,
    "estado": "CANCELADA"
  },
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu07jsonexample2"
{
  "mensaje": "No es posible cancelar la cita",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** La cita existe y es futura.
* **Acción:** Ejecutar PATCH `/api/v1/citas/1`.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Estado actualizado a CANCELADA
  * success = true

### ❌ Caso 2:

* **Precondición:** La cita ya está cancelada.
* **Acción:** Ejecutar PATCH `/api/v1/citas/1`.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** La cita ya ocurrió.
* **Acción:** Ejecutar PATCH `/api/v1/citas/1`.
* **Resultado esperado:**

  * Código HTTP 400
  * Operación no permitida

### ❌ Caso 4:

* **Precondición:** La cita no existe.
* **Acción:** Ejecutar PATCH `/api/v1/citas/999`.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje de error

## ✅ Definición de Hecho

# Historia: Cancelación de Cita

## 📦 Alcance Funcional

* [ ] Permite cancelar citas correctamente.
* [ ] Valida estado y fecha.

## 🧪 Pruebas Completadas

* [ ] Pruebas de cancelación exitosa
* [ ] Pruebas de validación de estado
* [ ] Pruebas de citas pasadas

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros para el usuario
