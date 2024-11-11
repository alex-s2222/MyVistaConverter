from fastapi import FastAPI
import uvicorn

from .routes import converter



def create_app():

    app = FastAPI(title="Elegant Fiber Labs")

    return app


app = create_app()
app.include_router(converter.router,  tags=['converter'],  prefix='/api/converter')


@app.get("/", description="hello")
async def test():
    return {"test": "good"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
