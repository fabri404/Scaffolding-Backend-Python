import os
from pathlib import Path
from textwrap import dedent

def create_file(path: Path, content: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(dedent(content).lstrip("\n"), encoding="utf-8")
        print(f"CREATED: {path}")
    else:
        print(f"SKIPPED (exists): {path}")

def create_project_scaffold(project_name: str):
    root = Path(project_name)
    root.mkdir(exist_ok=True)

    # ---------- Archivos raíz ----------
    create_file(
        root / "README.md",
        f"""
        # {project_name}

        Proyecto backend en Python con arquitectura por capas (domain, application, infrastructure, presentation).
        """
    )

    create_file(
        root / "requirements.txt",
        """
        # Añade aquí dependencias como:
        # fastapi
        # pydantic
        # sqlalchemy
        """
    )

    create_file(
        root / ".env.example",
        """
        APP_ENV=development
        APP_DEBUG=true
        DATABASE_URL=sqlite:///./app.db
        """
    )

    create_file(
        root / ".gitignore",
        """
        __pycache__/
        .venv/
        .env
        *.pyc
        .mypy_cache/
        .pytest_cache/
        """
    )

    # ---------- app/__init__.py ----------
    create_file(
        root / "app" / "__init__.py",
        """
        \"\"\"Entry point del paquete principal de la aplicación.\"\"\"
        """
    )

    # ---------- CONFIG ----------
    create_file(
        root / "app" / "config" / "__init__.py",
        """
        \"\"\"Módulo de configuración de la aplicación.\"\"\"
        """
    )

    create_file(
        root / "app" / "config" / "settings.py",
        """
        \"\"\"Configuración base de la aplicación.

        En un proyecto real podrías usar pydantic-settings o similar.
        \"\"\"

        import os

        class Settings:
            APP_NAME: str = "BackendApp"
            APP_ENV: str = os.getenv("APP_ENV", "development")
            DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
            DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

        settings = Settings()
        """
    )

    create_file(
        root / "app" / "config" / "logging_conf.py",
        """
        \"\"\"Configuración de logging estándar.\"\"\"

        import logging
        import logging.config

        DEFAULT_LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": "INFO",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            },
        }

        def setup_logging():
            logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
        """
    )

    # ---------- CORE ----------
    create_file(
        root / "app" / "core" / "__init__.py",
        """
        \"\"\"Elementos centrales compartidos (excepciones, eventos, etc.).\"\"\"
        """
    )

    create_file(
        root / "app" / "core" / "exceptions.py",
        """
        \"\"\"Excepciones base de la aplicación.\"\"\"

        class AppError(Exception):
            \"\"\"Excepción base de la aplicación.\"\"\"

        class NotFoundError(AppError):
            \"\"\"Recurso no encontrado.\"\"\"

        class ValidationError(AppError):
            \"\"\"Error de validación de datos de entrada.\"\"\"
        """
    )

    create_file(
        root / "app" / "core" / "events.py",
        """
        \"\"\"Eventos de dominio / sistema (opcional).\"\"\"

        from dataclasses import dataclass
        from datetime import datetime

        @dataclass
        class DomainEvent:
            name: str
            occurred_at: datetime
        """
    )

    # ---------- DOMAIN ----------
    create_file(
        root / "app" / "domain" / "__init__.py",
        """
        \"\"\"Entidades de dominio, value objects e interfaces de repositorios.\"\"\"
        """
    )

    create_file(
        root / "app" / "domain" / "models.py",
        """
        \"\"\"Entidades de dominio (reglas de negocio).\"\"\"

        from dataclasses import dataclass
        from datetime import datetime
        from typing import Optional

        @dataclass
        class BaseEntity:
            id: Optional[int]
            created_at: datetime
            updated_at: datetime

        @dataclass
        class User(BaseEntity):
            username: str
            email: str
        """
    )

    create_file(
        root / "app" / "domain" / "value_objects.py",
        """
        \"\"\"Value objects del dominio (opcional).\"\"\"

        from dataclasses import dataclass

        @dataclass(frozen=True)
        class EmailAddress:
            value: str
        """
    )

    create_file(
        root / "app" / "domain" / "repositories.py",
        """
        \"\"\"Interfaces de repositorios del dominio.\"\"\"

        from abc import ABC, abstractmethod
        from typing import List, Optional
        from .models import User

        class UserRepository(ABC):
            @abstractmethod
            def get_by_id(self, user_id: int) -> Optional[User]:
                raise NotImplementedError

            @abstractmethod
            def list_all(self) -> List[User]:
                raise NotImplementedError

            @abstractmethod
            def save(self, user: User) -> User:
                raise NotImplementedError

            @abstractmethod
            def delete(self, user_id: int) -> None:
                raise NotImplementedError
        """
    )

    # ---------- APPLICATION ----------
    create_file(
        root / "app" / "application" / "__init__.py",
        """
        \"\"\"Capa de aplicación: casos de uso / servicios.\"\"\"
        """
    )

    create_file(
        root / "app" / "application" / "dto.py",
        """
        \"\"\"DTOs para entrada/salida de la capa de aplicación.\"\"\"

        from dataclasses import dataclass

        @dataclass
        class UserCreateDTO:
            username: str
            email: str

        @dataclass
        class UserDTO:
            id: int
            username: str
            email: str
        """
    )

    create_file(
        root / "app" / "application" / "services.py",
        """
        \"\"\"Servicios de aplicación: orquestan dominio + repositorios.\"\"\"

        from typing import List
        from app.domain.repositories import UserRepository
        from app.application.dto import UserCreateDTO, UserDTO
        from app.domain.models import User
        from datetime import datetime

        class UserService:
            def __init__(self, repo: UserRepository):
                self.repo = repo

            def create_user(self, data: UserCreateDTO) -> UserDTO:
                now = datetime.utcnow()
                user = User(
                    id=None,
                    username=data.username,
                    email=data.email,
                    created_at=now,
                    updated_at=now,
                )
                saved = self.repo.save(user)
                return UserDTO(id=saved.id, username=saved.username, email=saved.email)

            def list_users(self) -> List[UserDTO]:
                users = self.repo.list_all()
                return [UserDTO(id=u.id, username=u.username, email=u.email) for u in users]
        """
    )

    create_file(
        root / "app" / "application" / "commands.py",
        """
        \"\"\"Casos de uso tipo comando (crear/actualizar/eliminar).\"\"\"
        """
    )

    create_file(
        root / "app" / "application" / "queries.py",
        """
        \"\"\"Casos de uso tipo consulta (lecturas).\"\"\"
        """
    )

    # ---------- INFRASTRUCTURE ----------
    create_file(
        root / "app" / "infrastructure" / "__init__.py",
        """
        \"\"\"Implementaciones técnicas (BD, HTTP, caches, etc.).\"\"\"
        """
    )

    # DB
    create_file(
        root / "app" / "infrastructure" / "db" / "__init__.py",
        """
        \"\"\"Infraestructura de base de datos.\"\"\"
        """
    )

    create_file(
        root / "app" / "infrastructure" / "db" / "base.py",
        """
        \"\"\"Configuración de base de datos (placeholder).

        Aquí podrías configurar SQLAlchemy, por ejemplo.
        \"\"\"
        """
    )

    create_file(
        root / "app" / "infrastructure" / "db" / "repositories_impl.py",
        """
        \"\"\"Implementaciones concretas de repositorios usando BD.\"\"\"

        from typing import List, Optional
        from app.domain.repositories import UserRepository
        from app.domain.models import User

        class InMemoryUserRepository(UserRepository):
            \"\"\"Implementación simple en memoria (útil para tests / prototipos).\"\"\"

            def __init__(self):
                self._data = {}
                self._next_id = 1

            def get_by_id(self, user_id: int) -> Optional[User]:
                return self._data.get(user_id)

            def list_all(self) -> List[User]:
                return list(self._data.values())

            def save(self, user: User) -> User:
                if user.id is None:
                    user.id = self._next_id
                    self._next_id += 1
                self._data[user.id] = user
                return user

            def delete(self, user_id: int) -> None:
                self._data.pop(user_id, None)
        """
    )

    # HTTP
    create_file(
        root / "app" / "infrastructure" / "http" / "__init__.py",
        """
        \"\"\"Clientes HTTP externos (APIs de terceros).\"\"\"
        """
    )

    create_file(
        root / "app" / "infrastructure" / "http" / "client.py",
        """
        \"\"\"Cliente HTTP simple (placeholder).\"\"\"

        import requests

        class HttpClient:
            def get(self, url: str, **kwargs):
                return requests.get(url, **kwargs)
        """
    )

    # ---------- PRESENTATION ----------
    create_file(
        root / "app" / "presentation" / "__init__.py",
        """
        \"\"\"Capa de presentación: API, CLI, etc.\"\"\"
        """
    )

    # API
    create_file(
        root / "app" / "presentation" / "api" / "__init__.py",
        """
        \"\"\"Módulo para exponer la API (REST, GraphQL, etc.).\"\"\"
        """
    )

    create_file(
        root / "app" / "presentation" / "api" / "schemas.py",
        """
        \"\"\"Esquemas de validación para la API (placeholder).\"\"\"
        """
    )

    create_file(
        root / "app" / "presentation" / "api" / "controllers.py",
        """
        \"\"\"Controladores / endpoints de la API (placeholder).

        Aquí podrías montar FastAPI, Flask, etc.
        \"\"\"
        """
    )

    # CLI
    create_file(
        root / "app" / "presentation" / "cli" / "__init__.py",
        """
        \"\"\"Entrada por línea de comandos.\"\"\"
        """
    )

    create_file(
        root / "app" / "presentation" / "cli" / "main.py",
        """
        \"\"\"Punto de entrada CLI básico.\"\"\"

        import argparse
        from app.infrastructure.db.repositories_impl import InMemoryUserRepository
        from app.application.services import UserService
        from app.application.dto import UserCreateDTO

        def main():
            parser = argparse.ArgumentParser(description="CLI de ejemplo")
            parser.add_argument("--username", required=True)
            parser.add_argument("--email", required=True)
            args = parser.parse_args()

            repo = InMemoryUserRepository()
            service = UserService(repo)
            user_dto = service.create_user(UserCreateDTO(username=args.username, email=args.email))
            print(f"Usuario creado: {user_dto}")

        if __name__ == "__main__":
            main()
        """
    )

    # ---------- TESTS ----------
    create_file(
        root / "tests" / "__init__.py",
        ""
    )

    create_file(
        root / "tests" / "test_smoke.py",
        """
        def test_imports():
            # Test mínimo para comprobar que los imports básicos funcionan
            import app
            import app.domain.models
            import app.application.services
            assert True
        """
    )

    print(f"\nEstructura completa creada en: {root.resolve()}")

if __name__ == "__main__":
    # Cambia el nombre del proyecto si quieres
    create_project_scaffold("mi_proyecto_backend")
