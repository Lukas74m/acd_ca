from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "mariadb+mariadbconnector://user:pass@localhost:3306/testdb", echo=True
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


""" Base.metadata.create_all(engine)

with Session() as session:
    session.add_all(
        [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com"),
        ]
    )
    session.commit() """

with Session() as session:
    users = session.query(User).all()
    for user in users:
        print(f"{user.id}: {user.name} ({user.email})")
