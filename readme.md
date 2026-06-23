# API RESTful - Sistema de Votaciones

Esta es una API RESTful desarrollada en Python para gestionar un sistema de votaciones. Permite el registro de votantes y candidatos, garantiza la emisión de un único voto por ciudadano mediante validaciones transaccionales, y genera estadísticas precisas en tiempo real.

## Tecnologías Utilizadas

- **Framework:** FastAPI
- **Lenguaje:** Python 3.10+
- **Base de Datos:** SQLite (para facilitar la ejecución local sin configuración de servidores externos)
- **ORM:** SQLAlchemy
- **Validación de Datos:** Pydantic

---

## ⚙️ Instrucciones para ejecutar el proyecto localmente

Sigue estos pasos para levantar el entorno en tu máquina:

**1. Clonar el repositorio**
\`\`\`bash
git clone <URL_DE_TU_REPOSITORIO_AQUI>
cd <NOMBRE_DE_LA_CARPETA>
\`\`\`

**2. Crear y activar un entorno virtual (Recomendado)**

- En Windows:
  \`\`\`bash
  python -m venv venv
  venv\Scripts\activate
  \`\`\`
- En macOS/Linux:
  \`\`\`bash
  python3 -m venv venv
  source venv/bin/activate
  \`\`\`

**3. Instalar las dependencias**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**4. Ejecutar el servidor web**
\`\`\`bash
uvicorn main:app --reload
\`\`\`

La API estará disponible en `http://127.0.0.1:8000`.
Puedes acceder a la documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

---

## Ejemplos de uso del API (cURL)

A continuación, ejemplos para interactuar con los endpoints principales usando `curl` desde la terminal. También puedes probarlos directamente desde la interfaz de Swagger en la ruta `/docs`.

**1. Registrar un nuevo votante**
\`\`\`bash
curl -X 'POST' \
 'http://127.0.0.1:8000/voters' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -d '{
"name": "Juan Perez",
"email": "juan.perez@email.com"
}'
\`\`\`

**2. Registrar un candidato**
\`\`\`bash
curl -X 'POST' \
 'http://127.0.0.1:8000/candidates' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -d '{
"name": "Maria Gomez",
"party": "Partido Innovación"
}'
\`\`\`

**3. Emitir un voto**
\`\`\`bash
curl -X 'POST' \
 'http://127.0.0.1:8000/votes' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -d '{
"voter_id": 1,
"candidate_id": 1
}'
\`\`\`

---

## Estadísticas Generadas

_A continuación se muestran las capturas de los resultados obtenidos a través del endpoint `/votes/statistics` tras realizar pruebas con múltiples votantes:_

**(Reemplaza este texto por tu imagen: En GitHub, puedes simplemente arrastrar y soltar la imagen aquí al editar el README)**

![Estadísticas de la votación](ruta/a/tu/imagen.png)

---

_Desarrollado por Andrey para prueba técnica._
