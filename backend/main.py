from fastapi import FastAPI

DEBUG = True

app = FastAPI()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=DEBUG)
