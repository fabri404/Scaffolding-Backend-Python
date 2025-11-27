# Python Backend Scaffold por Capas

Este repositorio contiene un pequeño script de **scaffolding** en Python que genera la estructura base de un proyecto backend con arquitectura por capas, pensada para ser **agnóstica de framework** (puede usarse con FastAPI, Flask, Django como capa de presentación, etc.).

---

## 🧱 Arquitectura generada

Al ejecutar el script se genera una estructura similar a la siguiente:

```text
mi_proyecto/
  app/
    __init__.py

    config/
      __init__.py
      settings.py        # Configuración general
      logging_conf.py    # Configuración de logging

    core/
      __init__.py
      exceptions.py      # Excepciones base
      events.py          # Eventos de dominio / sistema (opcional)

    domain/
      __init__.py
      models.py          # Entidades de dominio
      value_objects.py   # Value objects (opcional)
      repositories.py    # Interfaces de repositorios

    application/
      __init__.py
      dto.py             # DTOs / modelos de entrada/salida
      services.py        # Servicios de aplicación / casos de uso
      commands.py        # Casos de uso orientados a comandos
      queries.py         # Casos de uso orientados a consultas

    infrastructure/
      __init__.py

      db/
        __init__.py
        base.py              # Conexión a BD / ORM (placeholder)
        repositories_impl.py # Implementaciones de repositorios

      http/
        __init__.py
        client.py            # Cliente HTTP externo

    presentation/
      __init__.py

      api/
        __init__.py
        controllers.py   # Controladores / endpoints (API REST)
        schemas.py       # Esquemas de validación (pydantic o similar)

      cli/
        __init__.py
        main.py          # Entrada por línea de comandos

  tests/
    __init__.py
    test_smoke.py        # Test básico para probar que todo importa

  README.md
  requirements.txt       # Dependencias (por ahora vacío / mínimo)
  .env.example           # Variables de entorno de ejemplo
  .gitignore

## Ejecutar el script de scaffolding:

    python scaffold.py