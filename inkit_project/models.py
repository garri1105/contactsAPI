from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
DB_URI = 'sqlite:///contacts.db'


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    street_address = Column(String(250), nullable=False)
    unit_number = Column(String(250), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    post_code = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False, default="US")

    contact_id = Column(Integer, ForeignKey('contacts.id',  ondelete="CASCADE"))
    contact = relationship("Contact", back_populates="address")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=True)
    company = Column(String(50), nullable=True)
    notes = Column(String(500), nullable=True)

    address = relationship("Address", uselist=False, back_populates="contact", passive_deletes=True)

    def as_dict(self):
        contact = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        contact.update({'address': self.address.as_dict()})
        return contact


if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
