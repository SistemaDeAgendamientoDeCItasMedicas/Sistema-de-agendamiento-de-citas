# [HU-10] Eliminar cita médica

## 📖 Historia de Usuario

Como administrador

Quiero eliminar una cita médica

Para remover registros inválidos o innecesarios del sistema

## 🔁 Flujo Esperado

* El administrador selecciona la cita que desea eliminar.
* El sistema consume el endpoint `/api/v1/citas/{id}`.
* El backend valida que la cita exista.
* Se elimina el registro de la base de datos.
* El sistema retorna confirmación de la eliminación.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint DELETE para eliminar citas.
* [ ] Se valida que la cita exista.
* [ ] Solo usuarios con rol administrador pueden eliminar citas.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu10jsonok"
{
  "mensaje": "Cita eliminada correctamente",
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu10jsonerror"
{
  "mensaje": "No se pudo eliminar la cita",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Eliminar Cita

* **Método HTTP:** `DELETE`
* **Ruta:** `/api/v1/citas/{id}`

## 📤 Ejemplo de Respuesta JSON

```json id="hu10jsonexample"
{
  "mensaje": "Cita eliminada correctamente",
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu10jsonexample2"
{
  "mensaje": "No se pudo eliminar la cita",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** La cita existe y el usuario es administrador.
* **Acción:** Ejecutar DELETE `/api/v1/citas/1`.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Cita eliminada correctamente
  * success = true

### ❌ Caso 2:

* **Precondición:** La cita no existe.
* **Acción:** Ejecutar DELETE `/api/v1/citas/999`.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje de error

### ❌ Caso 3:

* **Precondición:** Usuario sin permisos.
* **Acción:** Ejecutar DELETE `/api/v1/citas/1`.
* **Resultado esperado:**

  * Código HTTP 403 Forbidden
  * Acceso denegado

## ✅ Definición de Hecho

# Historia: Eliminación de Cita

## 📦 Alcance Funcional

* [ ] Permite eliminar citas correctamente.
* [ ] Controla permisos de usuario.

## 🧪 Pruebas Completadas

* [ ] Pruebas de eliminación exitosa
* [ ] Pruebas de permisos
* [ ] Pruebas de inexistencia

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros para el usuario
