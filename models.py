from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

Base = declarative_base()

class Sexo(enum.Enum):
    MASCULINO = "M"
    FEMININO = "F"

class NivelAtividade(enum.Enum):
    SEDENTARIO = "sedentario"
    LEVE = "leve"
    MODERADO = "moderado"
    INTENSO = "intenso"
    MUITO_INTENSO = "muito_intenso"

class Medicao(Base):
    __tablename__ = 'medicoes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    sexo = Column(Enum(Sexo), nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    nivel_atividade = Column(Enum(NivelAtividade), nullable=False)
    imc = Column(Float, nullable=False)
    percentual_gordura = Column(Float, nullable=False)
    massa_magra = Column(Float, nullable=False)
    gasto_calorico_basal = Column(Float, nullable=False)
    gasto_calorico_total = Column(Float, nullable=False)
    ingestao_agua = Column(Float, nullable=False)
    data_medicao = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Medicao(nome='{self.nome}', data='{self.data_medicao}')>"

# Criar engine e sessão
engine = create_engine('sqlite:///imc_calculator.db')
Session = sessionmaker(bind=engine)

# Criar todas as tabelas
Base.metadata.create_all(engine) 