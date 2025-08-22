from fastapi import APIRouter


def setup(app):
    router = APIRouter()

    @router.get("/plugin/hello")
    def hello():
        return {"msg": "hi"}

    app.include_router(router)
