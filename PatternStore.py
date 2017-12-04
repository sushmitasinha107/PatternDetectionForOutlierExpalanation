from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DECIMAL, Column, String, Integer
import PatternFinder as pf

Base = declarative_base()
# engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres'
#                        , echo=True)

class Pattern(Base):
    __tablename__ = 'patterns'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fixed = Column(String)
    fixedvalue = Column(String)
    variable = Column(String)
    aggfunction = Column(String)
    aggvalue = Column(String)
    pattern = Column(String)
    metric = Column(DECIMAL)


def addPattern(fixed, fixedvalue, variable, aggfunction, aggvalue,
               pattern, metric):
    Base.metadata.create_all(pf.engine)

    Session = sessionmaker(bind=pf.engine)
    session = Session()
    new_pattern = Pattern(fixed=fixed, fixedvalue=fixedvalue,
                          variable=variable, aggfunction=aggfunction,
                          aggvalue=aggvalue, pattern=pattern, metric=metric)
    session.add(new_pattern)
    session.commit()
