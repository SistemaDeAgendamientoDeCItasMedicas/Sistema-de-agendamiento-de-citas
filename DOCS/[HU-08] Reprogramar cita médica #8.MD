# [HU-08] Reprogramar cita médica

## 📖 Historia de Usuario

Como paciente

Quiero reprogramar una cita médica

Para cambiar la fecha u hora de mi atención

## 🔁 Flujo Esperado

* El paciente selecciona la cita que desea modificar.
* El usuario ingresa la nueva fecha y hora.
* El sistema consume el endpoint `/api/v1/citas/{id}`.
* El backend valida que la cita exista.
* Se verifica que la cita no esté cancelada.
* Se valida que la nueva fecha no sea pasada.
* Se valida disponibilidad del nuevo horario.
* Se actualizan los datos de la cita en la base de datos.
* El sistema retorna confirmación de la reprogramación.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint PUT o PATCH para reprogramar citas.
* [ ] Se valida que la cita exista.
* [ ] No se permite modificar citas canceladas.
* [ ] Se valida disponibilidad del nuevo horario.
* [ ] No se permiten fechas pasadas.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu08jsonok"
{
  "mensaje": "Cita reprogramada correctamente",
  "data": {
    "cita_id": 1,
    "fecha": "2026-04-10",
    "hora": "11:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu08jsonerror"
{
  "mensaje": "No es posible reprogramar la cita",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Reprogramar Cita

* **Método HTTP:** `PUT` o `PATCH`
* **Ruta:** `/api/v1/citas/{id}`

## 📤 Ejemplo de Respuesta JSON

```json id="hu08jsonexample"
{
  "mensaje": "Cita reprogramada correctamente",
  "data": {
    "cita_id": 1,
    "fecha": "2026-04-10",
    "hora": "11:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu08jsonexample2"
{
  "mensaje": "No es posible reprogramar la cita",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** La cita existe y el nuevo horario está disponible.
* **Acción:** Ejecutar PUT/PATCH `/api/v1/citas/1`.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Fecha y hora actualizadas
  * success = true

### ❌ Caso 2:

* **Precondición:** El horario ya está ocupado.
* **Acción:** Reprogramar cita.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje de error

### ❌ Caso 3:

* **Precondición:** Cita cancelada.
* **Acción:** Reprogramar cita.
* **Resultado esperado:**

  * Operación no permitida

### ❌ Caso 4:

* **Precondición:** Fecha inválida o pasada.
* **Acción:** Reprogramar cita.
* **Resultado esperado:**

  * Error de validación

## ✅ Definición de Hecho

# Historia: Reprogramación de Cita

## 📦 Alcance Funcional

* [ ] Permite modificar fecha y hora.
* [ ] Valida disponibilidad.
* [ ] Mantiene consistencia de datos.

## 🧪 Pruebas Completadas

* [ ] Pruebas de reprogramación exitosa
* [ ] Pruebas de conflicto de horario
* [ ] Pruebas de validación

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros para el usuario
