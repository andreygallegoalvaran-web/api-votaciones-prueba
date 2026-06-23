# API RESTful - Sistema de Votaciones (Prueba Técnica)

Este proyecto es una API RESTful desarrollada para gestionar un sistema de votaciones seguro y confiable. Cumple con todos los requisitos técnicos establecidos, garantizando la integridad de los datos, la unicidad del voto por ciudadano y la generación de estadísticas precisas en tiempo real.

## Características Principales y Validaciones

El sistema cumple con las siguientes restricciones exigidas:

- **Integridad de Roles:** Un ciudadano registrado como votante no puede ser candidato, y viceversa.
- **Voto Único:** El sistema bloquea transaccionalmente cualquier intento de voto duplicado por parte de un mismo elector.
- **Validación de Datos:** Uso de `Pydantic` para asegurar que los correos electrónicos tengan el formato correcto y los datos requeridos no estén vacíos.
- **Manejo de Errores:** Respuestas HTTP claras (400 Bad Request, 404 Not Found) para guiar al usuario o al frontend sobre por qué falló una petición.

## Stack Tecnológico

- **Framework Web:** FastAPI (Elegido por su rendimiento, asincronía nativa y generación automática de documentación).
- **Lenguaje:** Python 3.10+
- **Base de Datos:** SQLite (Garantiza una ejecución local inmediata sin necesidad de configurar contenedores o servidores externos).
- **ORM:** SQLAlchemy
- **Validación:** Pydantic & email-validator

## Estructura del Proyecto

El código sigue una arquitectura limpia separando responsabilidades:

```text
api-votaciones-prueba/
├── activos/             # Evidencias y capturas de funcionamiento
├── src/                 # Código fuente principal de la API
│   ├── database.py      # Configuración y conexión del motor SQLite
│   ├── main.py          # Endpoints, controladores y lógica de negocio
│   ├── models.py        # Modelos de entidades de base de datos
│   └── schemas.py       # Esquemas de validación de entrada/salida
├── readme.md            # Documentación técnica
└── requisitos.txt       # Dependencias exactas del proyecto
```
ota: para ingresar a la API de Sistema de Votaciones ingresa por este enlace http://127.0.0.1:8000/docs
