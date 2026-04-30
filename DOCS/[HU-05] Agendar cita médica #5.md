
# [HU-05] Agendar cita médica 


## 📖 Historia de Usuario

Como administrador

Quiero agendar una cita médica

Para asignar un paciente a un médico en una fecha y hora específica cumpliendo las reglas del sistema


## 🔁 Flujo Esperado

- El administrador ingresa los datos de la cita (paciente_id, medico_id, fecha, hora) desde la interfaz.
- El sistema consume el endpoint /api/v1/citas.
- El backend valida la autenticación mediante token JWT.
- Se validan los campos obligatorios.
- Se valida el formato de fecha (YYYY-MM-DD) y hora (HH:mm).
- Se valida que la fecha no sea anterior a la fecha actual.
- Se valida que el paciente y el médico existan en la base de datos.
- Se valida que el médico tenga disponibilidad en el horario solicitado.
- Se valida que el paciente no tenga otra cita en el mismo horario.
- Se valida que la hora esté dentro del horario laboral permitido (ej: 08:00 – 18:00).
- Se define una duración estándar de la cita (ej: 30 minutos).
- Se verifica que no exista solapamiento de citas en ese rango de tiempo.
- Se registra la cita en la base de datos con estado inicial "PROGRAMADA".
- Se genera un identificador único para la cita.
- El sistema retorna confirmación del agendamiento.


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST para agendar citas.
- [ ] Se requiere autenticación mediante JWT.
- [ ] Se validan los campos obligatorios.
- [ ] Se valida formato de fecha y hora.
- [ ] Se valida que la fecha sea futura.
- [ ] Se valida existencia de paciente y médico.
- [ ] Se valida disponibilidad del médico.
- [ ] Se evita duplicidad de citas en el mismo horario.
- [ ] Se valida horario laboral del médico.
- [ ] Se controla solapamiento de citas.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Cita agendada correctamente",
  "data": {
    "cita_id": 1,
    "paciente_id": 1,
    "medico_id": 2,
    "fecha": "2026-05-10",
    "hora": "10:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
````

* [ ] Si ocurre error, el backend retorna:

```json
{
  "mensaje": "El médico no está disponible en ese horario",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Agendar Cita Médica

* **Método HTTP:** `POST`
* **Ruta:** `/api/v1/citas`

## 📤 Ejemplo de Respuesta JSON

````json
```json
{
  "mensaje": "Cita agendada correctamente",
  "data": {
    "cita_id": 1,
    "paciente_id": 1,
    "medico_id": 2,
    "fecha": "2026-05-10",
    "hora": "10:00",
    "estado": "PROGRAMADA"
  },
  "success": true
}
```
````

* [ ] Si ocurre error, el backend retorna:

```json
{
  "mensaje": "El médico no está disponible en ese horario",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1:

* **Precondición:** El paciente y el médico existen y están disponibles.
* **Acción:** Ejecutar el endpoint POST /api/v1/citas.
* **Resultado esperado:**

  * Código HTTP 201 Created
  * Cita registrada con estado "PROGRAMADA"
  * Retorna ID de la cita
  * Campo success = true

### ❌ Caso 2:

* **Precondición:** Fecha en el pasado.
* **Acción:** Ejecutar el endpoint POST /api/v1/citas.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje: "No se permiten fechas pasadas"

### ❌ Caso 3:

* **Precondición:** Médico ocupado en ese horario.
* **Acción:** Ejecutar el endpoint POST /api/v1/citas.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje de conflicto de horario

### ❌ Caso 4:

* **Precondición:** Paciente con cita en el mismo horario.
* **Acción:** Ejecutar el endpoint POST /api/v1/citas.
* **Resultado esperado:**

  * Código HTTP 409 Conflict
  * Mensaje de duplicidad de cita

### ❌ Caso 5:

* **Precondición:** Hora fuera del horario laboral.
* **Acción:** Ejecutar el endpoint POST /api/v1/citas.
* **Resultado esperado:**

  * Código HTTP 400 Bad Request
  * Mensaje: "Horario fuera de rango permitido"

### ❌ Caso 6:

* **Precondición:** Token inválido o no enviado.
* **Acción:** Ejecutar el endpoint sin autenticación.
* **Resultado esperado:**

  * Código HTTP 401 Unauthorized

### ❌ Caso 7:

* **Precondición:** Error en la base de datos.
* **Acción:** Ejecutar el endpoint bajo fallo.
* **Resultado esperado:**

  * Código HTTP 500 Internal Server Error
  * Mensaje: "Error al agendar la cita"

## ✅ Definición de Hecho

#Historia: Agendar Cita Médica

## 📦 Alcance Funcional

* [ ] Se agenda la cita correctamente
* [ ] Se valida disponibilidad del médico
* [ ] Se valida existencia de paciente y médico
* [ ] Se controla el estado de la cita

## 🧪 Pruebas Completadas

* [ ] Pruebas de agendamiento exitoso
* [ ] Pruebas de conflicto de horarios
* [ ] Pruebas de validación de fechas
* [ ] Pruebas de autenticación
* [ ] Pruebas de errores del sistema

## 📄 Documentación Técnica

* [ ] Endpoint documentado en Swagger / OpenAPI
* [ ] Se describe:

  * Propósito del endpoint
  * Validaciones aplicadas
  * Estados de la cita
  * Ejemplo de respuesta exitosa
  * Ejemplo de error

## 🔐 Manejo de Errores

* [ ] Se devuelve código HTTP 400 para validaciones
* [ ] Se devuelve código HTTP 401 para autenticación
* [ ] Se devuelve código HTTP 409 para conflictos de horario
* [ ] Se devuelve código HTTP 500 para errores internos
* [ ] El campo `mensaje` contiene información clara y específica

## Dependencias

- Depende de: HU-02 Iniciar sesión
- Depende de: HU-03 Registrar médico
- Depende de: HU-04 Registrar paciente
