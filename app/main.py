from pickle import load
from fastapi.middleware.cors import CORSMiddleware
from app.helpers import get_prediction
from fastapi import FastAPI
from pydantic import BaseModel


mnb = load(open('./app/models/mnb.pkl', 'rb'))
vectorizer = load(open('./app/models/vectorizer.pkl', 'rb'))


# Post Model
class Post(BaseModel):
    source: str
    content: str


# create app
app = FastAPI()

# add CORS middleware
origins = [
    "http://127.0.0.1:5173/",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def predict_credibility(post: Post):
    print(post)
    result = get_prediction(post.source, post.content, mnb, vectorizer)
    return result
