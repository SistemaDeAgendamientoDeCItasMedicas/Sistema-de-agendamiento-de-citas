
# [HU-01] Registrar usuario 


## 📖 Historia de Usuario

Como usuario

Quiero registrarme en el sistema

Para poder acceder a los servicios médicos de forma segura


## 🔁 Flujo Esperado

- El usuario ingresa nombre, correo electrónico y contraseña desde la interfaz.
- El sistema consume el endpoint /api/v1/users.
- El backend valida la autenticación (si aplica para registro restringido por rol).
- Se validan los campos obligatorios (nombre, correo, contraseña).
- Se valida el formato del correo electrónico.
- Se valida que la contraseña cumpla políticas de seguridad (mínimo 8 caracteres, combinación de letras y números).
- Se valida que el correo no esté registrado previamente.
- Se aplica encriptación segura a la contraseña (hash con algoritmo seguro, ej: bcrypt).
- Se asigna un rol por defecto (ej: USER).
- Se almacena la información del usuario en la base de datos.
- Se genera un identificador único para el usuario.
- Se registra la fecha de creación del usuario.
- El sistema retorna confirmación del registro.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST para registrar usuarios.
- [ ] Se validan los campos obligatorios.
- [ ] Se valida formato de correo electrónico.
- [ ] Se valida política de seguridad de contraseña.
- [ ] Se valida que el correo no exista previamente.
- [ ] La contraseña se almacena encriptada.
- [ ] Se asigna un rol por defecto al usuario.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Usuario registrado correctamente",
  "data": {
    "user_id": 1,
    "email": "usuario@email.com",
    "rol": "USER"
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json
{
  "mensaje": "El correo ya está registrado",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Registro de Usuario

* **Método HTTP:** `POST`
* **Ruta:** `/api/v1/users`

## 📤 Ejemplo de Respuesta JSON

````json
```json
{
  "mensaje": "Usuario registrado correctamente",
  "data": {
    "user_id": 1,
    "email": "usuario@email.com",
    "rol": "USER"
  },
  "success": true
}
```
````

* [ ] Si ocurre error:

```json
{
  "mensaje": "El correo ya está registrado",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El usuario no existe en la base de datos.
* **Acción:** Ejecutar POST /api/v1/users.
* **Resultado esperado:**

  * Código HTTP 201 Created
  * Usuario registrado correctamente
  * Retorna ID del usuario
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** El correo ya existe.
* **Acción:** Ejecutar POST /api/v1/users.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje de error
  * success = false

### ❌ Caso 3:

* **Precondición:** Contraseña no cumple política de seguridad.
* **Acción:** Ejecutar POST /api/v1/users.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje: "La contraseña no cumple los requisitos de seguridad"

### ❌ Caso 4:

* **Precondición:** Campos vacíos o inválidos.
* **Acción:** Ejecutar POST /api/v1/users.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Validación de campos

### ❌ Caso 5:

* **Precondición:** Error en la base de datos.
* **Acción:** Ejecutar el endpoint bajo condiciones de fallo.
* **Resultado esperado:**

  * Código HTTP 500 Internal Server Error
  * Mensaje: "Error al registrar usuario"

## ✅ Definición de Hecho

#Historia: Registro de Usuario

## 📦 Alcance Funcional

* [ ] El usuario se registra correctamente
* [ ] Se valida duplicidad de correo
* [ ] Se almacena la contraseña encriptada
* [ ] Se asigna rol al usuario

## 🧪 Pruebas Completadas

* [ ] Pruebas de registro exitoso
* [ ] Pruebas de duplicidad
* [ ] Pruebas de validación de contraseña
* [ ] Pruebas de validación de campos
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Propósito del endpoint
  * Validaciones aplicadas
  * Política de contraseñas
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 409 para duplicidad
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica

## Dependencias

- No tiene dependencias.


