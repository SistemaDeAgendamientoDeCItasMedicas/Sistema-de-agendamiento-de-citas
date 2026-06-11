# Sistema de Agendamiento de Citas Médicas

## Descripción del Proyecto

API REST desarrollada con **Python y FastAPI** para la gestión integral de citas médicas. Permite registrar usuarios, autenticarse y administrar citas de manera eficiente, aplicando validaciones de negocio, control de acceso mediante JWT y arquitectura por capas.

---

## Objetivo General

Desarrollar un servicio web que permita la gestión integral de citas médicas, garantizando validaciones de negocio, control de acceso y correcta manipulación de la información mediante endpoints REST.

---

## Funcionalidades Principales

- Registro y autenticación de usuarios con JWT
- Registro de pacientes y médicos
- Agendamiento de citas médicas con validación de disponibilidad
- Consulta y listado de citas con filtros y paginación
- Cancelación de citas con validación de anticipación mínima
- Reprogramación de citas con control de disponibilidad
- Eliminación lógica de citas (soft delete)

---

## Arquitectura del Sistema

El sistema implementa una **arquitectura por capas** con separación clara de responsabilidades:

```
app/
├── api/              # Capa API — Routers y endpoints FastAPI
├── services/         # Capa de Servicios — Lógica de negocio
├── repositories/     # Capa de Repositorios — Acceso a datos
├── domain/           # Capa de Dominio — Modelos Pydantic
├── core/             # Utilidades transversales (JWT, dependencias)
└── main.py           # Punto de entrada de la aplicación
```

| Capa | Responsabilidad |
|------|----------------|
| API | Recibe requests, valida entrada, retorna respuestas HTTP |
| Services | Aplica reglas de negocio y coordina el flujo |
| Repositories | CRUD en memoria (sin base de datos real) |
| Domain | Modelos Pydantic con validaciones de datos |

---

## Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.11 | Lenguaje principal |
| FastAPI | 0.111.0 | Framework web |
| Uvicorn | 0.30.0 | Servidor ASGI |
| Pydantic | 2.7.1 | Validación de datos |
| python-jose | 3.3.0 | Generación y verificación de JWT |
| bcrypt | 4.1.3 | Hash seguro de contraseñas |
| Git / GitHub | — | Control de versiones |
| Swagger UI | — | Documentación automática |

---

## Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/SistemaDeAgendamientoDeCItasMedicas/Sistema-de-agendamiento-de-citas.git
cd Sistema-de-agendamiento-de-citas

# 2. Crear entorno virtual
py -m venv venv
.\venv\Scripts\activate      # Windows
source venv/bin/activate     # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servidor
uvicorn app.main:app --reload
```

Swagger UI disponible en: **http://127.0.0.1:8000/docs**

---

## Endpoints

### [HU-01] Usuarios
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/users` | Registrar usuario |

### [HU-02] Autenticación
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/auth/login` | Iniciar sesión — retorna JWT |

### [HU-03] Pacientes
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/pacientes` | Registrar paciente 🔒 |

### [HU-04] Médicos
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/medicos` | Registrar médico 🔒 |

### [HU-05 al HU-10] Citas
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/citas` | Agendar cita 🔒 |
| `GET` | `/api/v1/citas` | Consultar citas con filtros 🔒 |
| `GET` | `/api/v1/citas/list` | Listar citas con paginación 🔒 |
| `PATCH` | `/api/v1/citas/{id}/cancel` | Cancelar cita 🔒 |
| `PATCH` | `/api/v1/citas/{id}/reschedule` | Reprogramar cita 🔒 |
| `DELETE` | `/api/v1/citas/{id}` | Eliminar cita (soft delete) 🔒 |

🔒 Requiere Bearer Token JWT

---

## Ejemplo de Respuesta

```json
{
  "message": "Appointment scheduled successfully",
  "data": {
    "appointment_id": 1,
    "patient_id": 1,
    "doctor_id": 2,
    "date": "2026-12-15",
    "time": "10:00",
    "reason": "Consulta general",
    "status": "SCHEDULED"
  },
  "success": true
}
```

---

## Seguridad

- Autenticación mediante **Bearer Token JWT** (algoritmo HS256)
- Contraseñas hasheadas con **bcrypt**
- Token con expiración de **3600 segundos (1 hora)**
- Endpoints protegidos validan el token en cada request

---

## Pruebas

Las pruebas fueron realizadas directamente en **Swagger UI**, validando por cada Historia de Usuario:

- ✅ Casos exitosos
- ❌ Validaciones de datos
- ❌ Manejo de errores
- ❌ Control de autenticación

Las evidencias de cada caso de prueba están documentadas en los Pull Requests del repositorio.

---

## Control de Versiones

Se utilizó Git con el siguiente flujo de ramas:

```
main          ← producción / entrega final
staging       ← pre-producción / QA
testing       ← evidencias de pruebas
development   ← base de trabajo
HU-XX-...     ← rama por cada Historia de Usuario
```

Cada HU siguió el flujo:
```
HU-XX → staging → (PR con evidencias) → testing → main
```

---

## Metodología de Trabajo

Se implementó **Kanban** con GitHub Projects, organizando el trabajo en:

| Estado | Descripción |
|--------|-------------|
| To Do | HU pendiente de iniciar |
| In Progress | HU en desarrollo |
| Gestion de Integración | HU en staging |
| Testing | HU en revisión con evidencias |
| Done | HU completada y mergeada |

---

## Autores

Proyecto desarrollado por:

- **Sebastian Andres Garcia Payares** — Desarrollo backend
- **Camilo** — Testing y evidencias

---

## Conclusión

El sistema desarrollado permite la gestión eficiente de citas médicas mediante un enfoque estructurado con arquitectura por capas, validaciones de negocio robustas, autenticación JWT y documentación automática con Swagger. Las 10 historias de usuario fueron implementadas y probadas siguiendo un flujo profesional de desarrollo con Git y Kanban.