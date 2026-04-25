
# [HU-09] Listar citas médicas 


## 📖 Historia de Usuario

Como administrador

Quiero listar las citas médicas registradas

Para visualizar de forma organizada la agenda general del sistema


## 🔁 Flujo Esperado

- El administrador solicita el listado de citas desde la interfaz.
- El sistema consume el endpoint /api/v1/citas/list.
- El backend valida la autenticación mediante token JWT.
- Se reciben parámetros de paginación (page, size).
- Se valida que los parámetros de paginación sean numéricos y válidos.
- Se establece un tamaño máximo permitido por página (ej: 50 registros).
- Se consulta la base de datos.
- Se obtienen todas las citas registradas.
- Se ordenan los resultados por fecha y hora (ascendente).
- Se aplica paginación sobre los resultados.
- Se construyen los metadatos de paginación.
- El sistema retorna la lista de citas junto con la información de paginación.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET para listar citas.
- [ ] Se requiere autenticación mediante JWT.
- [ ] Se implementa paginación obligatoria.
- [ ] Se valida límite máximo de registros por página.
- [ ] Se ordenan los resultados por fecha y hora.
- [ ] Se optimiza la consulta para evitar sobrecarga.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Listado de citas obtenido correctamente",
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
    "total_records": 100,
    "total_pages": 10
  },
  "success": true
}
````

* [ ] Si no existen datos, el backend retorna:

```json id="hu09nodata"
{
  "mensaje": "No existen citas registradas",
  "data": [],
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Listar Citas Médicas

* **Método HTTP:** `GET`
* **Ruta:** `/api/v1/citas/list`
* **Parámetros:**

  * page (número de página)
  * size (cantidad de registros por página)

## 📤 Ejemplo de Respuesta JSON

````json id="hu09example"
```json
{
  "mensaje": "Listado de citas obtenido correctamente",
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
    "total_records": 100,
    "total_pages": 10
  },
  "success": true
}
```
````

* [ ] Si no existen datos:

```json id="hu09example2"
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
* **Acción:** Ejecutar GET /api/v1/citas/list?page=1&size=10.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Retorna lista paginada
  * Campo success = true

### ✅ Caso 2:

* **Precondición:** Existen más registros que el tamaño de página.
* **Acción:** Ejecutar GET /api/v1/citas/list?page=2&size=10.
* **Resultado esperado:**

  * Retorna segunda página de resultados

### ❌ Caso 3:

* **Precondición:** No existen citas registradas.
* **Acción:** Ejecutar GET /api/v1/citas/list.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Lista vacía
  * success = false

### ❌ Caso 4:

* **Precondición:** Parámetros inválidos (page o size negativos).
* **Acción:** Ejecutar GET /api/v1/citas/list?page=-1.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje de validación

### ❌ Caso 5:

* **Precondición:** Tamaño de página excede el límite permitido.
* **Acción:** Ejecutar GET /api/v1/citas/list?size=1000.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje: "Tamaño de página excede el límite permitido"

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
  * Mensaje: "Error al listar citas"

## ✅ Definición de Hecho

#Historia: Listar Citas Médicas

## 📦 Alcance Funcional

* [ ] Se listan citas correctamente
* [ ] Se implementa paginación
* [ ] Se optimiza la consulta

## 🧪 Pruebas Completadas

* [ ] Pruebas de listado exitoso
* [ ] Pruebas de paginación
* [ ] Pruebas de validación de parámetros
* [ ] Pruebas de autenticación
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Parámetros de paginación
  * Límite de registros
  * Ordenamiento
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 401 para autenticación
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica

