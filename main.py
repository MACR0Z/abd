from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Table, Column, Integer, String, create_engine, ForeignKey

# <dbms>[+<driver>]://<user>:<pass>@<host>[:<port>][/<database>]
URL="mysql+mysqlconnector://aluno:senha@127.0.0.1:3306/orm"
engine = create_engine(url=URL)

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("materia_id", ForeignKey("materia.id")),
    Column("classe_id", ForeignKey("classe.id")),
)
matricula = Table(
    "matricula",
    Base.metadata,
    Column("aluno_id", ForeignKey("aluno.id")),
    Column("sala_id", ForeignKey("sala.id")),
)

class Trabalho(Base):
    __tablename__ = "trabalho"
    id = Column(Integer, primary_key=True)
    entrega = Column(String(150), nullable=False)
    materia_id = Column(Integer, ForeignKey('materia.id'))
    materia = relationship('Materia')

class Materia(Base):
    __tablename__ = "materia"
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    trabalhos = relationship(Trabalho)

class Aluno(Base):
    __tablename__ = "aluno"
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    classe_id = Column(Integer, ForeignKey('classe.id'))
    classe = relationship('Classe')

class Sala(Base):
    __tablename__ = "sala"
    id = Column(Integer, primary_key=True)
    numero = Column(String(150), nullable=False)
    matriculas = relationship('Aluno', secondary=matricula)

class Classe(Base):
    __tablename__ = "classe"
    id = Column(Integer, primary_key=True)
    ano = Column(String(150), nullable=False)

    prof_id = Column(Integer, ForeignKey('professor.id'))
    prof = relationship('Professor')
    alunos = relationship(Aluno)
    materias = relationship('Materia', secondary=association_table)


class Professor(Base):
    __tablename__ = "professor"
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    classes = relationship(Classe)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

professor = Professor(nome="lucas")
classe = Classe(ano="1º", prof=professor)
aluno = Aluno(nome="marcos", classe=classe)
materia = Materia(nome="adb")
trabalho = Trabalho(entrega="20/11/22", materia=materia)
sala = Sala(numero="9ºB")

Session = sessionmaker(engine)

with Session.begin() as session:
    session.add(materia)
    session.add(sala)
    session.add(aluno)
    session.commit()

