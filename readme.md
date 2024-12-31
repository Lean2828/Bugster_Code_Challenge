# Proyecto: Bugster APP

## Introducción

**Bugster APP** es una solución diseñada para gestionar eventos, historias de usuario y generar pruebas automatizadas utilizando Playwright. El proyecto permite integrar datos y optimizar flujos de trabajo mediante una arquitectura escalable basada en microservicios. 

La aplicación está construida sobre una arquitectura que le permite ser extensible y escalable, utilizando tecnologías como **FastAPI**, **MongoDB** y **Pydantic**.

---

## Instrucciones de Instalación y Ejecución

### Requisitos Previos

- **Docker**: Asegúrate de tener Docker instalado en tu sistema.
- **Docker Compose**: Debe estar configurado (viene integrado en Docker Desktop para Windows y macOS).

---

### Instalación y Ejecución

1. **Clona el repositorio**:
    ```bash
    git clone [URL_DEL_REPOSITORIO]
    cd Bugster_Code_Challenge
    ```

2. **Levanta la aplicación con Docker Compose**:
    ```bash
    docker-compose up --build
    ```

3. **Accede a los servicios**:
    - **Microservicio de eventos (event_service)**: [http://localhost:8000](http://localhost:8000)
    - **Microservicio de historias (story_service)**: [http://localhost:8001](http://localhost:8001)
    - **Microservicio de pruebas (test_service)**: [http://localhost:8002](http://localhost:8002)
    - **Mongo Express (UI de MongoDB)**: [http://localhost:8081](http://localhost:8081)

---

### Parar la Aplicación

Para detener los servicios y eliminar los contenedores creados:

```bash
docker-compose down
```

## Documentación de la API

FastAPI proporciona una documentación interactiva automática disponible en `/docs`. La API ofrece los siguientes endpoints principales:

Si la aplicación está corriendo se puede visualizar la documentación en estos links
**Documentación Event service**
    http://127.0.0.1:8000/docs
  
**Documentación Story service**
    http://127.0.0.1:8001/docs

**Documentación Tests service**
    http://127.0.0.1:8002/docs

### Detalle de Endpoints

- **Microservicio de Eventos (`/v1/events`)**:
  - `POST /v1/events/`: Procesa y guarda eventos en la base de datos. Realiza validaciones detalladas de los datos de entrada.

    **Ejemplo de request**:
    ```json
    {
        "event": "Test Event",
        "properties": {
            "distinct_id": "user-123",
            "session_id": "session-456",
            "$current_url": "https://example.com/page",
            "$host": "example.com",
            "$pathname": "/page",
            "$browser": "Chrome",
            "$device": "Desktop",
            "$screen_height": 1080,
            "$screen_width": 1920,
            "eventType": "click",
            "elementType": "button",
            "elementText": "Submit",
            "timestamp": "2024-12-30T00:00:00Z",
            "x": 100,
            "y": 200,
            "mouseButton": 0,
            "ctrlKey": false,
            "shiftKey": false,
            "altKey": false,
            "metaKey": false
        }
    }
    ```

    **Ejemplo de respuesta**:
    ```json
    {
        "status": "success",
        "message": "1 eventos procesados correctamente."
    }
    ```

### Endpoints del Microservicio **Stories**

- **`GET /v1/stories/`**
  - **Descripción**: Devuelve todas las historias almacenadas en la base de datos.
  - **Parámetros opcionales**:
    - `session_id` (str): Filtra historias por el ID de la sesión.
    - `story_id` (str): Filtra historias por el ID de la historia.
  - **Respuesta**: Lista de historias con sus atributos.
      ```json
    {
        "stories": [
            {
                "id": "story-56676925-6e55-4072-98db-ca544bd3dbb5",
                "session_id": "fcc95c16-28ae-4bc5-bead-cf052ab87cef",
                "title": "User Story 56676925-6e55-4072-98db-ca544bd3dbb5",
                "startTimestamp": "2024-10-10T22:53:05.563Z",
                "endTimestamp": "2024-10-10T22:53:18.547Z",
                "initialState": {
                    "url": "https://www.bugster.app/dashboard"
                },
                "finalState": {
                    "url": "https://www.bugster.app/testCases"
                },
                "actions": [
                    {
                        "type": "click",
                        "target": "div",
                        "value": "71.43%Pass Rate21Tests",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "span",
                        "value": "",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "a",
                        "value": "User Stories",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "a",
                        "value": "Test Cases",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "a",
                        "value": "Test Cases",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "span",
                        "value": "Test Cases",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "div",
                        "value": "EEyeonic projectHomeUser StoriesTest CasesMy Project",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "a",
                        "value": "Test Cases",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "div",
                        "value": "NameStatusSourceFeatureG.4.1. Grant Reclaim TestPassedChrome extensionToken GrantG.4. Grant Test fro...",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "svg",
                        "value": "",
                        "url": null
                    },
                    {
                        "type": "click",
                        "target": "svg",
                        "value": "",
                        "url": null
                    }
                ],
                "networkRequests": []
            }
        ]
    } 
    ``` 

- **`POST /v1/stories/`**
  - **Descripción**: Permite crear nuevas historias o actualizar las existentes.
  - **Body**:
    ```json
    {
      "id": "string",
      "session_id": "string",
      "title": "string",
      "content": "string",
      "tags": ["string"]
    }
    ```
  - **Respuesta**: Confirmación de creación o actualización.


- **`GET /v1/stories/patterns`**
  - **Descripción**: Analiza las historias almacenadas e identifica patrones comunes.
  - **Respuesta**: Resumen de patrones encontrados.
    ```json
    {
        "interaction_with_highlighted_content": {
            "story-56676925-6e55-4072-98db-ca544bd3dbb5": 3
        },
        "ambiguous_interaction": {
            "story-56676925-6e55-4072-98db-ca544bd3dbb5": 1
        },
        "navigation_to_section": {
            "story-56676925-6e55-4072-98db-ca544bd3dbb5": 4
        },
        "repeated_click": {
            "story-56676925-6e55-4072-98db-ca544bd3dbb5": 1
        },
        "ui_icon_interaction": {
            "story-56676925-6e55-4072-98db-ca544bd3dbb5": 2
        }
    }
    ```

---

### Endpoints del Microservicio **Tests**

- **`GET /v1/tests/`**
  - **Descripción**: Lista los scripts de prueba generados.
  - **Respuesta**: Test generado para playwright
    ```json

    {
        "story_id": "story-56676925-6e55-4072-98db-ca544bd3dbb5",
        "test_script": "from playwright.sync_api import sync_playwright\n\ndef test_generated():\n    with sync_playwright() as p:\n        browser = p.chromium.launch()\n        page = browser.new_page()\n        page.locator('div').click()\n        page.locator('span').click()\n        page.locator('a').click()\n        page.locator('a').click()\n        page.locator('a').click()\n        page.locator('span').click()\n        page.locator('div').click()\n        page.locator('a').click()\n        page.locator('div').click()\n        page.locator('svg').click()\n        page.locator('svg').click()\n        browser.close()"
    },
    {
        "story_id": "story-12345",
        "test_script": "from playwright.sync_api import sync_playwright\n\ndef test_generated():\n    with sync_playwright() as p:\n        browser = p.chromium.launch()\n        page = browser.new_page()\n        page.locator('button').click()\n        browser.close()"
    }

    ```


---

## Explicación de Decisiones de Diseño

### Arquitectura

Se optó por una arquitectura basada en microservicios debido a los siguientes beneficios:

1. **Escalabilidad**: Cada microservicio puede escalar de manera independiente.
2. **Modularidad**: Facilita el mantenimiento y la incorporación de nuevas funcionalidades.

### Microservicios Implementados

1. **Microservicio de Eventos (`/v1/events`)**:
   - Gestión de carga y procesamiento de eventos.
2. **Microservicio de Historias (`/v1/stories`)**:
   - Gestión de historias de usuario.
3. **Microservicio de Tests (`/v1/tests`)**:
   - Generación de pruebas automatizadas con Playwright.

### Capas

Cada microservicio se organiza internamente en tres capas principales:

- **Capa de Dominio**:
  - Manejo de las rutas y validaciones de entrada/salida.
- **Capa de Aplicación**:
  - Contiene la lógica de negocio y la aplicación de casos de uso.
- **Capa de Infraestructura**:
  - Interacción con la base de datos.

---

## Trade-offs Considerados

### Carga en `POST /v1/events/`
- **Ventaja**: El procesamiento inicial reduce la carga en los métodos `GET`, lo que mejora la experiencia del cliente.
- **Desventaja**: Incrementa el tiempo de respuesta del método `POST`.

### Carga en capa de Aplicación
- **Ventaja**: Se tiene una lógica de negocio "robusta", para cumplir el requerimiento de accuracy por sobre velocidad. 
- **Desventaja**: Si la solución requiere escalabilidad, se tiene que poner mucho foco en mantener eficientes los algoritmos y el procesamiento dentro de esta capa.

### Decisión de utilizar MongoDB
- **Ventaja**: Flexibilidad en el manejo de datos no estructurados, y puede escalar horizontalmente si se lo requiere.
- **Desventaja**: Puede requerir índices adicionales para mejorar el rendimiento en consultas complejas.

---

## Áreas de Mejora Identificadas

1. **Implementación de Caché**:
   - Utilizar Redis para almacenar resultados procesados y reducir la carga en la base de datos.

2. **Integración de Kafka**:
   - Incorporar un sistema de mensajería para manejar la ingesta de eventos de manera más eficiente.

3. **Mejoras en la Generación de Tests**:
   - Explorar el uso de LLMs para detectar patrones de comportamiento en las historias, y para hacer mas robusta la generación y ejecución de tests.

4. **Ampliación de Pruebas Automatizadas**:
   - Aumentar la cobertura de pruebas unitarias e integración para garantizar la estabilidad del sistema.

---

## Testing
- Para el testing se dispone de un archivo **test.bat**, en la raíz del proyecto. Al ejecutar el archivo se realizan testeos básicos de funcionamiento del endpoint.
- También se disponibiliza el archivo **Bugster.postman_collection.rar**. Se puede importar en Postman para realizar pruebas manuales de los endpoints.

---

## Conclusión
- Se deja en funcionamiento la aplicación cumpliendo con los requerimientos solicitados, teniendo en cuenta que puede ser un prototipo evolutivo y se puede adaptar a nuevas funcionalidades e integrarse fácilmente con otros sistemas.