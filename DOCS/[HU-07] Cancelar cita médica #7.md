
# [HU-07] Cancelar cita médica 


## 📖 Historia de Usuario

Como administrador

Quiero cancelar una cita médica

Para liberar el espacio en la agenda y mantener actualizada la disponibilidad de los médicos


## 🔁 Flujo Esperado

- El administrador selecciona la cita a cancelar desde la interfaz.
- El sistema consume el endpoint /api/v1/citas/{cita_id}.
- El backend valida la autenticación mediante token JWT.
- Se valida que el identificador de la cita exista.
- Se consulta la cita en la base de datos.
- Se valida que la cita exista.
- Se valida que la cita no esté previamente cancelada.
- Se valida que la cita no esté finalizada.
- Se valida que la cancelación se realice con una anticipación mínima (ej: 1 hora antes).
- Se actualiza el estado de la cita a "CANCELADA".
- Se registra la fecha y hora de cancelación.
- Se actualiza la disponibilidad del médico en ese horario.
- El sistema retorna confirmación de la cancelación.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint DELETE o PATCH para cancelar citas.
- [ ] Se requiere autenticación mediante JWT.
- [ ] Se valida que la cita exista.
- [ ] Se valida que la cita no esté cancelada previamente.
- [ ] Se valida que la cita no esté finalizada.
- [ ] Se valida política de tiempo mínimo para cancelación.
- [ ] Se actualiza el estado de la cita correctamente.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Cita cancelada correctamente",
  "data": {
    "cita_id": 1,
    "estado": "CANCELADA"
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json id="hu07error"
{
  "mensaje": "No es posible cancelar la cita",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Cancelar Cita Médica

* **Método HTTP:** `PATCH` (recomendado) o `DELETE`
* **Ruta:** `/api/v1/citas/{cita_id}`

## 📤 Ejemplo de Respuesta JSON

````json id="hu07example"
```json
{
  "mensaje": "Cita cancelada correctamente",
  "data": {
    "cita_id": 1,
    "estado": "CANCELADA"
  },
  "success": true
}
```
````

* [ ] Si ocurre error:

```json id="hu07example2"
{
  "mensaje": "No es posible cancelar la cita",
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
  * Estado actualizado a "CANCELADA"
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** La cita no existe.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje: "Cita no encontrada"

### ❌ Caso 3:

* **Precondición:** Cita ya cancelada.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje: "La cita ya está cancelada"

### ❌ Caso 4:

* **Precondición:** Cita finalizada.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje: "No se puede cancelar una cita finalizada"

### ❌ Caso 5:

* **Precondición:** Cancelación fuera del tiempo permitido.
* **Acción:** Ejecutar PATCH /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje: "Tiempo límite de cancelación excedido"

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
  * Mensaje: "Error al cancelar la cita"

## ✅ Definición de Hecho

#Historia: Cancelar Cita Médica

## 📦 Alcance Funcional

* [ ] Se cancela la cita correctamente
* [ ] Se valida estado de la cita
* [ ] Se actualiza disponibilidad del médico

## 🧪 Pruebas Completadas

* [ ] Pruebas de cancelación exitosa
* [ ] Pruebas de estados inválidos
* [ ] Pruebas de tiempo de cancelación
* [ ] Pruebas de autenticación
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Estados de la cita
  * Reglas de cancelación
  * Validaciones aplicadas
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 401 para autenticación
* [ ] Se devuelve código HTTP 404 para recurso no encontrado
* [ ] Se devuelve código HTTP 409 para conflictos de estado
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica

