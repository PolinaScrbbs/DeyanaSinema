from fastapi import FastAPI

from .auth.router import router as authRouter
from .film.router import router as filmRouter
from .session.router import router as sessionRouter
from .ticket.router import router as ticketRouter
from .reservation.router import router as reservationRouter

app = FastAPI(
    title="Kittens API", description="A Test Task About Kittens", version="1.0.0"
)

app.include_router(authRouter, tags=["Auth"])
app.include_router(filmRouter, tags=["Film"])
app.include_router(sessionRouter, tags=["Session"])
app.include_router(ticketRouter, tags=["Ticket"])
app.include_router(reservationRouter, tags=["Reservation"])
