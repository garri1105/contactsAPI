import falcon
import falcon.testing
import json
import unittest
from falcon_autocrud.middleware import Middleware
from inkit_project.resources import ContactResource, ContactCollectionResource, AddressResource, AddressCollectionResource, json1_file
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class TestAddress(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    street_address = Column(String(250), nullable=False)
    unit_number = Column(String(250), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    post_code = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False, default="US")

    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship("TestContact", back_populates="address")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TestContact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=True)
    company = Column(String(50), nullable=True)
    notes = Column(String(500), nullable=True)

    address = relationship("TestAddress", uselist=False, back_populates="contact", cascade='all,delete')

    def as_dict(self):
        contact = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        contact.update({'address': self.address.as_dict()})
        return contact


class BaseTestCase(unittest.TestCase):

    def tearDown(self):
        self.db_session.close()
        self.db_engine.dispose()
        json1_file.close()

    def setUp(self):
        super(BaseTestCase, self).setUp()

        self.app = falcon.API(
            middleware=[Middleware()],
        )

        self.db_engine = create_engine('sqlite:///tmp_contacts.db')
        self.db_session = sessionmaker(bind=self.db_engine)()

        self.app.add_route('/contacts', ContactCollectionResource(self.db_engine))
        self.app.add_route('/contacts/{id}', ContactResource(self.db_engine))
        self.app.add_route('/contacts/{id}/address', AddressResource(self.db_engine))
        self.app.add_route('/addresses', AddressCollectionResource(self.db_engine))
        self.app.add_route('/addresses/{id}', AddressResource(self.db_engine))

        Base.metadata.drop_all(self.db_engine)
        Base.metadata.create_all(self.db_engine)

        self.srmock = falcon.testing.StartResponseMock()

    def simulate_request(self, path, *args, **kwargs):
        env = falcon.testing.create_environ(path=path, **kwargs)
        return self.app(env, self.srmock)

    def assertOK(self, response, body=None):
        self.assertEqual(self.srmock.status, '200 OK')
        if body is not None and isinstance(body, dict):
            self.assertEqual(json.loads(response.decode('utf-8')), body)

    def assertCreated(self, response, body=None):
        self.assertEqual(self.srmock.status, '201 Created')
        if body is not None and isinstance(body, dict):
            self.assertEqual(json.loads(response.decode('utf-8')), body)

    def assertBadRequest(self, response, title='Invalid attribute', description='An attribute provided '
                                                                                'for filtering is invalid'):
        self.assertEqual(self.srmock.status, '400 Bad Request')
        self.assertEqual(
            json.loads(response[0].decode('utf-8')),
            {
                'title':        title,
                'description':  description,
            }
        )

    def assertFailValidation(self, response, description):
        self.assertEqual(self.srmock.status, '400 Bad Request')
        self.assertEqual(
            json.loads(response[0].decode('utf-8')),
            {
                'title':        'Failed data validation',
                'description':  description,
            }
        )

    def assertValid(self):
        self.assertNotEqual(self.srmock.status, '400 Bad Request')

    def assertUnauthorized(self, response, description='No credentials supplied'):
        self.assertEqual(self.srmock.status, '401 Unauthorized')
        self.assertEqual(
            json.loads(response[0].decode('utf-8')),
            {
                'title':        'Authentication Required',
                'description':  description,
            }
        )

    def assertForbidden(self, response, description='User does not have access to this resource'):
        self.assertEqual(self.srmock.status, '403 Forbidden')
        self.assertEqual(
            json.loads(response[0].decode('utf-8')),
            {
                'title':        'Permission Denied',
                'description':  description,
            }
        )

    def assertNotFound(self, response):
        self.assertEqual(self.srmock.status, '404 Not Found')
        self.assertEqual(response, [])

    def assertMethodNotAllowed(self, response):
        self.assertEqual(self.srmock.status, '405 Method Not Allowed')
        self.assertEqual(response, [])

    def assertConflict(self, response, description='Unique constraint violated'):
        self.assertEqual(self.srmock.status, '409 Conflict')
        self.assertEqual(
            json.loads(response[0].decode('utf-8')),
            {
                'title':        'Conflict',
                'description':  description,
            }
        )

    def assertUnsupportedMediaType(self, response, description='This API supports only JSON-encoded requests'):
        self.assertEqual(self.srmock.status, '415 Unsupported Media Type')
        self.assertEqual(
            json.loads(response[0].decode('utf-8')),
            {
                'title':        'Unsupported media type',
                'description':  description,
            }
        )

    def assertInternalServerError(self, response):
        self.assertEqual(self.srmock.status, '500 Internal Server Error')
        self.assertEqual(
            json.loads(response[0].decode('utf-8')),
            {
                'title':        'Internal Server Error',
                'description':  'An internal server error occurred',
            }
        )
