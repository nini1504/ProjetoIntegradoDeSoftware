from fastapi import FastAPI, status, Depends
from schemas import Message
import models
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/mensagens", status_code=status.HTTP_201_CREATED)
def criar_mensagens(newMessage: Message, db_session: Session = Depends(get_db)):
    msg_created = models.Model_Message(**newMessage.model_dump())
    db_session.add(msg_created)
    db_session.commit()
    db_session.refresh(msg_created)
    return {"Mensagem": msg_created}
