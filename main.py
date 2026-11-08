from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models
import auth_routes, users, posts

Base.metadata.create_all(bind=engine)
app = FastAPI(title='Social Network API', version='1.0.0')
# For production, restrict this to your actual frontend origins.
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5500', 'http://127.0.0.1:5500', 'http://localhost:8000'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(auth_routes.router)
app.include_router(users.router)
app.include_router(posts.router)

@app.get('/')
def root():
    return {'message': 'Social Network API is running', 'docs': '/docs'}
