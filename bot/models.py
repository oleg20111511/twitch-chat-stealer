from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import registry
import settings as bs

mapper_registry = registry()
Base = mapper_registry.generate_base()
engine = create_engine(bs.DATABASE_URL, future=True)


class Message(Base):
	__tablename__ = 'message'

	id = Column(Integer, primary_key=True)
	source = Column(String)
	sender = Column(String)
	content = Column(String)

	def __repr__(self):
		return f"Message(id={self.id!r}, source={self.source!r}, sender={self.sender!r}, content={self.content!r})"


Base.metadata.create_all(engine)
