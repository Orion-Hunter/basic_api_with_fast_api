from .container import Container
from .settings import Settings

settings = Settings()


container = Container()

# ---É aqui que configuramos o injetor de dependências para ler o arquivo .env
container.config.from_pydantic(settings)  # type: ignore

container.database()
