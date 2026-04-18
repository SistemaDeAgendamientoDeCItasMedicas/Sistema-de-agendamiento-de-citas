# [HU-09] Listar citas médicas

## 📖 Historia de Usuario

Como usuario

Quiero listar mis citas médicas

Para visualizar todas mis citas programadas

## 🔁 Flujo Esperado

* El usuario accede a la opción de consultar citas.
* El sistema consume el endpoint `/api/v1/citas`.
* El backend valida la identidad del usuario.
* Se consultan las citas asociadas al usuario en la base de datos.
* El sistema retorna una lista de citas.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint GET para listar citas.
* [ ] Se valida la autenticación del usuario.
* [ ] Se retornan únicamente las citas asociadas al usuario.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu09jsonok"
{
  "mensaje": "Listado de citas obtenido correctamente",
  "data": [
    {
      "cita_id": 1,
      "fecha": "2026-03-25",
      "hora": "10:00",
      "estado": "PROGRAMADA"
    },
    {
      "cita_id": 2,
      "fecha": "2026-04-01",
      "hora": "09:00",
      "estado": "CANCELADA"
    }
  ],
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu09jsonerror"
{
  "mensaje": "No se pudieron obtener las citas",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Listar Citas

* **Método HTTP:** `GET`
* **Ruta:** `/api/v1/citas`

## 📤 Ejemplo de Respuesta JSON

```json id="hu09jsonexample"
{
  "mensaje": "Listado de citas obtenido correctamente",
  "data": [
    {
      "cita_id": 1,
      "fecha": "2026-03-25",
      "hora": "10:00",
      "estado": "PROGRAMADA"
    }
  ],
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu09jsonexample2"
{
  "mensaje": "No se pudieron obtener las citas",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El usuario tiene citas registradas.
* **Acción:** Ejecutar GET `/api/v1/citas`.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Lista de citas retornada
  * success = true

### ❌ Caso 2:

* **Precondición:** El usuario no tiene citas.
* **Acción:** Ejecutar GET `/api/v1/citas`.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Lista vacía
  * success = true

### ❌ Caso 3:

* **Precondición:** Usuario no autenticado.
* **Acción:** Ejecutar GET `/api/v1/citas`.
* **Resultado esperado:**

  * Código HTTP 401 Unauthorized
  * Mensaje de error

## ✅ Definición de Hecho

# Historia: Listado de Citas

## 📦 Alcance Funcional

* [ ] Permite visualizar citas del usuario.
* [ ] Maneja listas correctamente.

## 🧪 Pruebas Completadas

* [ ] Pruebas de listado con datos
* [ ] Pruebas de listado vacío
* [ ] Pruebas de autenticación

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen parámetros de entrada y salida

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros para el usuario
