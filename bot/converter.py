from models import Message, engine
from sqlalchemy.orm import Session
from sqlalchemy import select


with Session(engine) as session:
	messages = session.execute(select(Message.content)).scalars().all()

res = '\n'.join(messages)
with open('list.txt', 'w') as f:
	f.write(res)
