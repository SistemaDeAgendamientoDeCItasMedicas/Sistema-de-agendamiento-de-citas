
# [HU-06] Consultar cita médica 


## 📖 Historia de Usuario

Como administrador

Quiero consultar las citas médicas registradas

Para visualizar la información de las citas y gestionar la agenda médica


## 🔁 Flujo Esperado

- El administrador solicita la consulta de citas desde la interfaz.
- El sistema consume el endpoint /api/v1/citas.
- El backend valida la autenticación mediante token JWT.
- Se validan los parámetros opcionales de búsqueda (fecha, paciente_id, medico_id, estado).
- Se valida el formato de fecha (YYYY-MM-DD) en caso de ser enviado.
- Se construye la consulta dinámica con filtros aplicados.
- El sistema consulta la base de datos.
- Se obtienen los registros de citas que cumplen los filtros.
- Se ordenan los resultados por fecha y hora (ascendente o descendente).
- Se implementa paginación (page, size).
- Se retorna la lista de citas junto con metadatos de paginación.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET para consultar citas.
- [ ] Se requiere autenticación mediante JWT.
- [ ] Se permiten filtros por fecha, paciente, médico y estado.
- [ ] Se valida formato de fecha.
- [ ] Se implementa paginación.
- [ ] Se ordenan los resultados correctamente.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Consulta de citas exitosa",
  "data": [
    {
      "cita_id": 1,
      "paciente_id": 1,
      "medico_id": 2,
      "fecha": "2026-05-10",
      "hora": "10:00",
      "estado": "PROGRAMADA"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "total_records": 1,
    "total_pages": 1
  },
  "success": true
}
````

* [ ] Si no existen datos, el backend retorna:

```json id="hu06nodata"
{
  "mensaje": "No existen citas registradas",
  "data": [],
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Consultar Citas Médicas

* **Método HTTP:** `GET`
* **Ruta:** `/api/v1/citas`
* **Parámetros opcionales:**

  * fecha (YYYY-MM-DD)
  * paciente_id
  * medico_id
  * estado
  * page
  * size

## 📤 Ejemplo de Respuesta JSON

````json id="hu06example"
```json
{
  "mensaje": "Consulta de citas exitosa",
  "data": [
    {
      "cita_id": 1,
      "paciente_id": 1,
      "medico_id": 2,
      "fecha": "2026-05-10",
      "hora": "10:00",
      "estado": "PROGRAMADA"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "total_records": 1,
    "total_pages": 1
  },
  "success": true
}
```
````

* [ ] Si no existen datos:

```json id="hu06example2"
{
  "mensaje": "No existen citas registradas",
  "data": [],
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** Existen citas registradas.
* **Acción:** Ejecutar GET /api/v1/citas.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Retorna lista de citas
  * Campo success = true

### ✅ Caso 2:

* **Precondición:** Existen citas con filtro aplicado.
* **Acción:** Ejecutar GET /api/v1/citas?fecha=2026-05-10.
* **Resultado esperado:**

  * Retorna solo citas de la fecha indicada

### ❌ Caso 3:

* **Precondición:** No existen citas.
* **Acción:** Ejecutar GET /api/v1/citas.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Lista vacía
  * success = false

### ❌ Caso 4:

* **Precondición:** Formato de fecha inválido.
* **Acción:** Ejecutar GET /api/v1/citas?fecha=10-05-2026.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje: "Formato de fecha inválido"

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
  * Mensaje: "Error al consultar citas"

## ✅ Definición de Hecho

#Historia: Consultar Citas Médicas

## 📦 Alcance Funcional

* [ ] Se consultan citas correctamente
* [ ] Se aplican filtros dinámicos
* [ ] Se implementa paginación

## 🧪 Pruebas Completadas

* [ ] Pruebas de consulta general
* [ ] Pruebas de filtros
* [ ] Pruebas de paginación
* [ ] Pruebas de autenticación
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Parámetros de búsqueda
  * Paginación
  * Estructura de respuesta
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 401 para autenticación
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica
