from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DECIMAL, Column, String
from PatternFinder import engine

Base = declarative_base()
# engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres'
#                        , echo=True)

class Pattern(Base):
    __tablename__ = 'patterns'
    fixed = Column(String)
    fixedvalue = Column(String)
    variable = Column(String)
    aggfunction = Column(String)
    aggvalue = Column(String)
    pattern = Column(String)
    metric = Column(DECIMAL)


def addPattern(fixed, fixedvalue, variable, aggfunction, aggvalue,
               pattern, metric):
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    new_pattern = Pattern(fixed=fixed, fixedvalue=fixedvalue,
                          variable=variable, aggfunction=aggfunction,
                          aggvalue=aggvalue, pattern=pattern, metric=metric)
    session.add(new_pattern)
    session.commit()
