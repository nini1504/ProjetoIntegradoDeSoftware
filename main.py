from fastapi import FastAPI, status, Depends, Request
from schemas import Message
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    messages = db.query(models.Model_Message).all()
    return templates.TemplateResponse("index.html",{"request": request, "messages": messages})


@app.post("/mensagens", status_code=status.HTTP_201_CREATED)
def criar_mensagens(newMessage: Message, db_session: Session = Depends(get_db)):
    msg_created = models.Model_Message(**newMessage.model_dump())
    db_session.add(msg_created)
    db_session.commit()
    db_session.refresh(msg_created)
    return {"Message": msg_created}
