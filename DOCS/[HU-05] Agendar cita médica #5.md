# [HU-05] Agendar cita médica

## 📖 Historia de Usuario

Como paciente

Quiero agendar una cita médica

Para recibir atención con un médico en una fecha y hora específica

## 🔁 Flujo Esperado

* El paciente selecciona un médico desde la interfaz.
* El paciente selecciona una fecha y hora disponible.
* El sistema consume el endpoint `/api/v1/citas`.
* El backend valida que el paciente y el médico existan.
* El sistema valida que el horario esté disponible.
* Se registra la cita en la base de datos.
* Se asigna un estado inicial "PROGRAMADA".
* El sistema retorna confirmación del agendamiento.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint POST para agendar citas.
* [ ] Se valida que el paciente exista.
* [ ] Se valida que el médico exista.
* [ ] Se valida disponibilidad del horario.
* [ ] No se permiten fechas pasadas.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu05jsonok"
{
  "mensaje": "Cita agendada correctamente",
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

```json id="hu05jsonerror"
{
  "mensaje": "El horario no está disponible",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Agendar Cita

* **Método HTTP:** `POST`
* **Ruta:** `/api/v1/citas`

## 📤 Ejemplo de Respuesta JSON

```json id="hu05jsonexample"
{
  "mensaje": "Cita agendada correctamente",
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

```json id="hu05jsonexample2"
{
  "mensaje": "El horario no está disponible",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El paciente y el médico existen y el horario está disponible.
* **Acción:** Ejecutar POST `/api/v1/citas`.
* **Resultado esperado:**

  * Código HTTP 201 Created
  * Cita registrada correctamente
  * Estado "PROGRAMADA"
  * success = true

### ❌ Caso 2:

* **Precondición:** El horario ya está ocupado.
* **Acción:** Ejecutar POST `/api/v1/citas`.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** Fecha en el pasado.
* **Acción:** Ejecutar POST `/api/v1/citas`.
* **Resultado esperado:**

  * Código HTTP 400
  * Error de validación

### ❌ Caso 4:

* **Precondición:** El paciente o médico no existen.
* **Acción:** Ejecutar POST `/api/v1/citas`.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje de error

## ✅ Definición de Hecho

# Historia: Agendar Cita Médica

## 📦 Alcance Funcional

* [ ] Permite agendar citas correctamente.
* [ ] Valida disponibilidad.
* [ ] Asigna estado inicial.

## 🧪 Pruebas Completadas

* [ ] Pruebas de agendamiento exitoso
* [ ] Pruebas de conflictos de horario
* [ ] Pruebas de validación de fechas

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros para el usuario
