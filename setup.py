from setuptools import setup, find_packages

setup(
    name="mall-admin-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "alembic",
        "pymysql",
        "aioredis",
        "celery",
        "python-dotenv",
    ],
) 