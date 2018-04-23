from __future__ import absolute_import
from falcon_autocrud.resource import CollectionResource, SingleResource
from inkit_project.models import *
import json

import falcon
import jsonschema


json1_file = open('inkit_project/post_schema.json')
json1_str = json1_file.read()
post_schema = json.loads(json1_str)


def validate_json(instance):
    try:
        jsonschema.validate(instance, post_schema, format_checker=jsonschema.FormatChecker())
    except jsonschema.ValidationError as e:
        raise falcon.HTTPBadRequest(
            'Failed data validation',
            description=e.message
        )


def validate_content_type(req, resp, resource, params):
    if req.method in ['POST', 'PUT', 'PATCH'] and (req.content_type is None or 'application/json' not in req.content_type):
        raise falcon.HTTPUnsupportedMediaType('This API supports only JSON-encoded requests. Make sure the '
                                              'Content-Type header is set appropiately')

    if req.method in ['POST', 'PUT']:
        validate_json(req.context['doc'])


class ContactCollectionResource(CollectionResource):
    model = Contact
    allow_subresources = True
    methods = ['GET', 'POST']

    @falcon.before(validate_content_type)
    def on_post(self, req, resp, *args, **kwargs):
        if isinstance(req.context['doc'], list):
            contacts = req.context['doc']
            for contact in contacts:
                req.context['doc'] = contact
                super(ContactCollectionResource, self).on_post(req, resp, *args, **kwargs)

        else:
            super(ContactCollectionResource, self).on_post(req, resp, *args, **kwargs)

    def after_get(self, req, resp, collection, *args, **kwargs):
        req.context['result'] = [resource.as_dict() for resource in collection]


class ContactResource(SingleResource):
    model = Contact
    methods = ['GET', 'PATCH', 'DELETE', 'PUT']

    @falcon.before(validate_content_type)
    def on_put(self, req, resp, *args, **kwargs):
        super(ContactResource, self).on_put(req, resp, *args, **kwargs)

    @falcon.before(validate_content_type)
    def on_patch(self, req, resp, *args, **kwargs):
        super(ContactResource, self).on_patch(req, resp, *args, **kwargs)

    def after_get(self, req, resp, resource, *args, **kwargs):
        req.context['result'] = resource.as_dict()


class AddressCollectionResource(CollectionResource):
    model = Address
    methods = ['GET']

    def after_get(self, req, resp, collection, *args, **kwargs):
        req.context['result'] = [resource.as_dict() for resource in collection]


class AddressResource(SingleResource):
    model = Address
    methods = ['GET']

    def after_get(self, req, resp, resource, *args, **kwargs):
        req.context['result'] = resource.as_dict()
