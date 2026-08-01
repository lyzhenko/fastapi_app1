import uvicorn
from fastapi import FastAPI

from app.routers import bookings, hotels

app = FastAPI()
app.include_router(hotels.router)
app.include_router(bookings.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
