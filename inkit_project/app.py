from sqlalchemy import create_engine
import falcon
from falcon_autocrud.middleware import Middleware
from .resources import ContactCollectionResource, ContactResource, AddressResource, AddressCollectionResource

db_engine = create_engine('sqlite:///contacts.db')

app = falcon.API(
    middleware=[Middleware()],
)

app.add_route('/contacts', ContactCollectionResource(db_engine))
app.add_route('/contacts/{id}', ContactResource(db_engine))
app.add_route('/contacts/{id}/address', AddressResource(db_engine))
app.add_route('/addresses', AddressCollectionResource(db_engine))
app.add_route('/addresses/{id}', AddressResource(db_engine))
