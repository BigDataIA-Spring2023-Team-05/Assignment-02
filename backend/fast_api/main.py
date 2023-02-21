from fastapi import FastAPI, status, Response, HTTPException
import uvicorn
from routers import user

app =  FastAPI()

app.include_router(user.router)

@app.get('/')
def index():
    return 'Success! APIs are working!'



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

 