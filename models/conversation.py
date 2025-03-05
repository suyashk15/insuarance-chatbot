from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    state = Column(String, nullable=True)

# Database setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
