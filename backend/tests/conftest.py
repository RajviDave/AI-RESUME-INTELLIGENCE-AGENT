import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/resume_intelligence_test",
)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
