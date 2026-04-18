# [HU-02] Iniciar sesión

## 📖 Historia de Usuario

Como usuario

Quiero iniciar sesión en el sistema

Para acceder a mi cuenta y gestionar mis citas médicas

## 🔁 Flujo Esperado

* El usuario ingresa su correo electrónico y contraseña desde la interfaz.
* El sistema consume el endpoint `/api/v1/auth/login`.
* El backend valida las credenciales en la base de datos.
* Se genera un token de autenticación (JWT).
* El sistema retorna acceso autorizado al usuario.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

* [ ] Se expone un endpoint POST para autenticación.
* [ ] Se validan las credenciales del usuario.
* [ ] Se genera un token de sesión válido.

### 2. 📆 Estructura de la información

* [ ] Se responde con la siguiente estructura en JSON:

```json id="hu02jsonok"
{
  "mensaje": "Inicio de sesión exitoso",
  "data": {
    "user_id": 1,
    "token": "jwt_token_ejemplo"
  },
  "success": true
}
```

* [ ] Si ocurre error, el backend retorna:

```json id="hu02jsonerror"
{
  "mensaje": "Credenciales incorrectas",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Autenticación de Usuario

* **Método HTTP:** `POST`
* **Ruta:** `/api/v1/auth/login`

## 📤 Ejemplo de Respuesta JSON

```json id="hu02jsonexample"
{
  "mensaje": "Inicio de sesión exitoso",
  "data": {
    "user_id": 1,
    "token": "jwt_token_ejemplo"
  },
  "success": true
}
```

* [ ] Si ocurre error:

```json id="hu02jsonexample2"
{
  "mensaje": "Credenciales incorrectas",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El usuario está registrado.
* **Acción:** Ejecutar POST `/api/v1/auth/login`.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Token generado correctamente
  * Acceso permitido
  * success = true

### ❌ Caso 2:

* **Precondición:** Credenciales incorrectas.
* **Acción:** Ejecutar POST `/api/v1/auth/login`.
* **Resultado esperado:**

  * Código HTTP 401 Unauthorized
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** Campos vacíos.
* **Acción:** Ejecutar POST `/api/v1/auth/login`.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Validación de campos

## ✅ Definición de Hecho

# Historia: Inicio de Sesión

## 📦 Alcance Funcional

* [ ] El usuario puede autenticarse correctamente.
* [ ] Se genera token de acceso.

## 🧪 Pruebas Completadas

* [ ] Pruebas de login exitoso
* [ ] Pruebas de error
* [ ] Pruebas de validación

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describen entradas y salidas

## 🔐 Manejo de Errores

* [ ] Se retornan códigos HTTP adecuados
* [ ] Mensajes claros al usuario
