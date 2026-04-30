
# [HU-04] Registrar médico 


## 📖 Historia de Usuario

Como administrador

Quiero registrar médicos en el sistema

Para gestionar su información y asignarles citas médicas


## 🔁 Flujo Esperado

- El administrador ingresa los datos del médico desde la interfaz.
- El sistema consume el endpoint /api/v1/medicos.
- El backend valida que los campos obligatorios estén completos.
- Se valida el formato del documento y del correo.
- El backend verifica que el médico no esté registrado previamente.
- Se almacena la información del médico en la base de datos.
- Se genera un identificador único para el médico.
- El sistema retorna confirmación del registro.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST para registrar médicos.
- [ ] Se validan los campos obligatorios.
- [ ] Se valida que el documento no exista previamente.
- [ ] Se valida formato de datos (documento, correo).
- [ ] Se genera un identificador único para el médico.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Médico registrado correctamente",
  "data": {
    "medico_id": 1,
    "nombre": "Dr. Juan Perez"
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json
{
  "mensaje": "El médico ya está registrado",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Registro de Médico

* **Método HTTP:** `POST`
* **Ruta:** `/api/v1/medicos`

## 📤 Ejemplo de Respuesta JSON

````json
```json
{
  "mensaje": "Médico registrado correctamente",
  "data": {
    "medico_id": 1,
    "nombre": "Dr. Juan Perez"
  },
  "success": true
}
```
````

* [ ] Si ocurre error, el backend retorna:

```json
{
  "mensaje": "El médico ya está registrado",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El médico no existe en la base de datos.
* **Acción:** Ejecutar el endpoint POST /api/v1/medicos.
* **Resultado esperado:**

  * Código HTTP 201 Created
  * Médico registrado correctamente
  * Retorna ID del médico
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** El documento del médico ya existe.
* **Acción:** Ejecutar el endpoint POST /api/v1/medicos.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** Campos vacíos o inválidos.
* **Acción:** Ejecutar el endpoint POST /api/v1/medicos.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Validación de campos

### ❌ Caso 4:

* **Precondición:** Error en la base de datos.
* **Acción:** Ejecutar el endpoint bajo condiciones de fallo.
* **Resultado esperado:**

  * Código HTTP 500 Internal Server Error
  * Mensaje: "Error al registrar el médico"

## ✅ Definición de Hecho

#Historia: Registro de Médico

## 📦 Alcance Funcional

* [ ] El médico se registra correctamente
* [ ] Se valida duplicidad de documento
* [ ] Se almacena en base de datos

## 🧪 Pruebas Completadas

* [ ] Se ejecutaron pruebas de registro exitoso
* [ ] Se validaron casos de duplicidad
* [ ] Se probaron validaciones de entrada
* [ ] Se probaron errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Propósito del endpoint
  * Campos de entrada y salida
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara para el usuario

## Dependencias

- Depende de: HU-01 Registrar usuario
