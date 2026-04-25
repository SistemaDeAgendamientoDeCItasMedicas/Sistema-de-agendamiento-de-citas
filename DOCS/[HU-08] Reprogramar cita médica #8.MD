
# [HU-08] Reprogramar cita médica 


## 📖 Historia de Usuario

Como administrador

Quiero reprogramar una cita médica

Para cambiar la fecha y hora de una cita existente sin perder su información


## 🔁 Flujo Esperado

- El administrador selecciona la cita a reprogramar desde la interfaz.
- El sistema consume el endpoint /api/v1/citas/{cita_id}.
- El backend valida la autenticación mediante token JWT.
- Se valida que el identificador de la cita exista.
- Se consulta la cita en la base de datos.
- Se valida que la cita exista.
- Se valida que la cita no esté cancelada ni finalizada.
- El administrador envía nueva fecha y hora.
- Se validan los campos obligatorios (fecha, hora).
- Se valida el formato de fecha (YYYY-MM-DD) y hora (HH:mm).
- Se valida que la nueva fecha no sea anterior a la actual.
- Se valida que el médico tenga disponibilidad en el nuevo horario.
- Se valida que no exista solapamiento con otras citas.
- Se valida que el paciente no tenga otra cita en el mismo horario.
- Se valida que la hora esté dentro del horario laboral permitido.
- Se actualizan los datos de la cita en la base de datos.
- Se mantiene el estado de la cita como "PROGRAMADA".
- Se registra la fecha de modificación.
- El sistema retorna confirmación de la reprogramación.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint PUT o PATCH para reprogramar citas.
- [ ] Se requiere autenticación mediante JWT.
- [ ] Se valida que la cita exista.
- [ ] Se valida estado de la cita (no cancelada ni finalizada).
- [ ] Se validan fecha y hora.
- [ ] Se valida disponibilidad del médico.
- [ ] Se evita solapamiento de citas.
- [ ] Se valida horario laboral.
- [ ] Se mantiene consistencia de datos.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Cita reprogramada correctamente",
  "data": {
    "cita_id": 1,
    "fecha": "2026-05-15",
    "hora": "11:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json id="hu08error"
{
  "mensaje": "No es posible reprogramar la cita",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Reprogramar Cita Médica

* **Método HTTP:** `PUT` (reemplazo completo) o `PATCH` (recomendado)
* **Ruta:** `/api/v1/citas/{cita_id}`

## 📤 Ejemplo de Respuesta JSON

````json id="hu08example"
```json
{
  "mensaje": "Cita reprogramada correctamente",
  "data": {
    "cita_id": 1,
    "fecha": "2026-05-15",
    "hora": "11:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
```
````

* [ ] Si ocurre error:

```json id="hu08example2"
{
  "mensaje": "No es posible reprogramar la cita",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** La cita existe y está en estado "PROGRAMADA".
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Fecha y hora actualizadas correctamente
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** La cita no existe.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje: "Cita no encontrada"

### ❌ Caso 3:

* **Precondición:** Cita cancelada o finalizada.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje: "No se puede reprogramar la cita"

### ❌ Caso 4:

* **Precondición:** Médico no disponible en el nuevo horario.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje de conflicto de horario

### ❌ Caso 5:

* **Precondición:** Fecha en el pasado.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje: "Fecha inválida"

### ❌ Caso 6:

* **Precondición:** Token inválido o no enviado.
* **Acción:** Ejecutar endpoint sin autenticación.
* **Resultado esperado:**

  * Código HTTP 401 Unauthorized

### ❌ Caso 7:

* **Precondición:** Error en la base de datos.
* **Acción:** Ejecutar endpoint bajo fallo.
* **Resultado esperado:**

  * Código HTTP 500 Internal Server Error
  * Mensaje: "Error al reprogramar la cita"

## ✅ Definición de Hecho

#Historia: Reprogramar Cita Médica

## 📦 Alcance Funcional

* [ ] Se reprograma la cita correctamente
* [ ] Se valida disponibilidad del médico
* [ ] Se mantiene consistencia de la cita

## 🧪 Pruebas Completadas

* [ ] Pruebas de reprogramación exitosa
* [ ] Pruebas de conflictos de horario
* [ ] Pruebas de validación de fechas
* [ ] Pruebas de autenticación
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Reglas de reprogramación
  * Validaciones aplicadas
  * Estados de la cita
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 401 para autenticación
* [ ] Se devuelve código HTTP 404 para recurso no encontrado
* [ ] Se devuelve código HTTP 409 para conflictos de horario o estado
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica

