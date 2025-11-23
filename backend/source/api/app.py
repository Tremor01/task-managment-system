from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .tasks.api import router as tasks_router
from .labels.api import router as labels_router
from .statuses.api import router as statuses_router
from .priorities.api import router as priorities_router
from .users.api import router as users_router


app = FastAPI(title="Tasks Managment System API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(tasks_router)
app.include_router(labels_router)
app.include_router(statuses_router)
app.include_router(priorities_router)
app.include_router(users_router)

