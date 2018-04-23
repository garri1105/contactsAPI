from falcon_autocrud.resource import CollectionResource, SingleResource
from inkit_project.models import *


class ContactCollectionResource(CollectionResource):
    model = Contact
    allow_subresources = True
    methods = ['GET', 'POST']

    def after_get(self, req, resp, collection, *args, **kwargs):
        req.context['result'] = [resource.as_dict() for resource in collection]


class ContactResource(SingleResource):
    model = Contact
    methods = ['GET', 'PATCH', 'DELETE']

    def after_get(self, req, resp, resource, *args, **kwargs):
        req.context['result'] = [resource.as_dict()]


class AddressResource(SingleResource):
    model = Address
    methods = ['GET']
