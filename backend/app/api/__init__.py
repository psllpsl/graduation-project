from .auth import router as auth_router
from .patients import router as patients_router
from .appointments import router as appointments_router
from .dialogues import router as dialogues_router
from .knowledge import router as knowledge_router
from .stats import router as stats_router

__all__ = [
    "auth_router",
    "patients_router",
    "appointments_router",
    "dialogues_router",
    "knowledge_router",
    "stats_router",
]
