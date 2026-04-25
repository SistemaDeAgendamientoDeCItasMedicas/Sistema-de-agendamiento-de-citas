
# [HU-02] Iniciar sesión 


## 📖 Historia de Usuario

Como usuario

Quiero iniciar sesión en el sistema

Para acceder de forma segura a mi cuenta y gestionar mis citas médicas


## 🔁 Flujo Esperado

- El usuario ingresa correo electrónico y contraseña desde la interfaz.
- El sistema consume el endpoint /api/v1/auth/login.
- El backend valida que los campos obligatorios estén completos.
- Se valida el formato del correo electrónico.
- Se consulta el usuario en la base de datos por correo.
- Se verifica que el usuario exista.
- Se compara la contraseña ingresada con la contraseña encriptada almacenada (hash).
- Se valida que la cuenta esté activa.
- Se genera un token de autenticación JWT con información del usuario (user_id, rol).
- Se define un tiempo de expiración del token.
- El sistema retorna el token junto con los datos básicos del usuario.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST para autenticación.
- [ ] Se validan los campos obligatorios.
- [ ] Se valida formato de correo electrónico.
- [ ] Se verifica existencia del usuario.
- [ ] Se valida la contraseña mediante hash.
- [ ] Se genera un token JWT válido.
- [ ] Se incluye expiración del token.
- [ ] Se valida estado activo del usuario.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Inicio de sesión exitoso",
  "data": {
    "user_id": 1,
    "email": "usuario@email.com",
    "rol": "USER",
    "token": "jwt_token_ejemplo",
    "expires_in": 3600
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json id="hu02error"
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

````json id="hu02example"
```json
{
  "mensaje": "Inicio de sesión exitoso",
  "data": {
    "user_id": 1,
    "email": "usuario@email.com",
    "rol": "USER",
    "token": "jwt_token_ejemplo",
    "expires_in": 3600
  },
  "success": true
}
```
````

* [ ] Si ocurre error:

```json id="hu02example2"
{
  "mensaje": "Credenciales incorrectas",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El usuario está registrado y activo.
* **Acción:** Ejecutar POST /api/v1/auth/login.
* **Resultado esperado:**

  * Código HTTP 200 OK
  * Token generado correctamente
  * Retorna datos del usuario
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** Contraseña incorrecta.
* **Acción:** Ejecutar POST /api/v1/auth/login.
* **Resultado esperado:**

  * Código HTTP 401 Unauthorized
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** Usuario no existe.
* **Acción:** Ejecutar POST /api/v1/auth/login.
* **Resultado esperado:**

  * Código HTTP 404 Not Found
  * Mensaje: "Usuario no encontrado"

### ❌ Caso 4:

* **Precondición:** Usuario inactivo.
* **Acción:** Ejecutar POST /api/v1/auth/login.
* **Resultado esperado:**

  * Código HTTP 403 Forbidden
  * Mensaje: "Usuario inactivo"

### ❌ Caso 5:

* **Precondición:** Campos vacíos o inválidos.
* **Acción:** Ejecutar POST /api/v1/auth/login.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Validación de campos

### ❌ Caso 6:

* **Precondición:** Error en la base de datos.
* **Acción:** Ejecutar el endpoint bajo fallo.
* **Resultado esperado:**

  * Código HTTP 500 Internal Server Error
  * Mensaje: "Error al iniciar sesión"

## ✅ Definición de Hecho

#Historia: Inicio de Sesión

## 📦 Alcance Funcional

* [ ] El usuario puede autenticarse correctamente
* [ ] Se genera token JWT
* [ ] Se valida estado del usuario

## 🧪 Pruebas Completadas

* [ ] Pruebas de login exitoso
* [ ] Pruebas de credenciales incorrectas
* [ ] Pruebas de usuario inexistente
* [ ] Pruebas de usuario inactivo
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Propósito del endpoint
  * Generación de token JWT
  * Expiración del token
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 401 para credenciales incorrectas
* [ ] Se devuelve código HTTP 403 para usuario inactivo
* [ ] Se devuelve código HTTP 404 para usuario no encontrado
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica



