
# [HU-10] Eliminar cita médica 


## 📖 Historia de Usuario

Como administrador

Quiero eliminar una cita médica

Para remover registros que no deben permanecer en el sistema manteniendo la integridad de la información


## 🔁 Flujo Esperado

- El administrador selecciona la cita a eliminar desde la interfaz.
- El sistema consume el endpoint /api/v1/citas/{cita_id}.
- El backend valida la autenticación mediante token JWT.
- Se valida que el identificador de la cita exista.
- Se consulta la cita en la base de datos.
- Se valida que la cita exista.
- Se valida que la cita no esté finalizada.
- Se valida que la cita no esté en proceso (ej: en atención).
- Se aplica eliminación lógica (soft delete) marcando el registro como inactivo.
- Se actualiza el estado de la cita a "ELIMINADA".
- Se registra la fecha y hora de eliminación.
- Se conserva el historial para auditoría.
- El sistema retorna confirmación de la eliminación.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint DELETE para eliminar citas.
- [ ] Se requiere autenticación mediante JWT.
- [ ] Se valida que la cita exista.
- [ ] Se valida que la cita no esté finalizada.
- [ ] Se aplica eliminación lógica (soft delete).
- [ ] Se registra auditoría de eliminación.
- [ ] Se mantiene integridad de datos.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Cita eliminada correctamente",
  "data": {
    "cita_id": 1,
    "estado": "ELIMINADA"
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json id="hu10error"
{
  "mensaje": "No es posible eliminar la cita",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Eliminar Cita Médica

* **Método HTTP:** `DELETE`
* **Ruta:** `/api/v1/citas/{cita_id}`

## 📤 Ejemplo de Respuesta JSON

````json id="hu10example"
```json
{
  "mensaje": "Cita eliminada correctamente",
  "data": {
    "cita_id": 1,
    "estado": "ELIMINADA"
  },
  "success": true
}
```
````

* [ ] Si ocurre error:

```json id="hu10example2"
{
  "mensaje": "No es posible eliminar la cita",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** La cita existe y está en estado "PROGRAMADA".
* **Acción:** Ejecutar DELETE /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Estado actualizado a "ELIMINADA"
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** La cita no existe.
* **Acción:** Ejecutar DELETE /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje: "Cita no encontrada"

### ❌ Caso 3:

* **Precondición:** Cita finalizada.
* **Acción:** Ejecutar DELETE /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje: "No se puede eliminar una cita finalizada"

### ❌ Caso 4:

* **Precondición:** Cita en proceso.
* **Acción:** Ejecutar DELETE /api/v1/citas/{cita_id}.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje: "No se puede eliminar una cita en proceso"

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
  * Mensaje: "Error al eliminar la cita"

## ✅ Definición de Hecho

#Historia: Eliminar Cita Médica

## 📦 Alcance Funcional

* [ ] Se elimina la cita correctamente (lógica)
* [ ] Se valida estado de la cita
* [ ] Se conserva historial para auditoría

## 🧪 Pruebas Completadas

* [ ] Pruebas de eliminación exitosa
* [ ] Pruebas de restricciones de estado
* [ ] Pruebas de autenticación
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Eliminación lógica (soft delete)
  * Estados de la cita
  * Reglas de eliminación
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 401 para autenticación
* [ ] Se devuelve código HTTP 404 para recurso no encontrado
* [ ] Se devuelve código HTTP 409 para conflictos de estado
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica

## Dependencias

- Depende de: HU-02 Iniciar sesión
- Depende de: HU-05 Agendar cita médica


