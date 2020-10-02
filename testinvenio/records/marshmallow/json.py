# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 alzp.
#
# testInvenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function
import uuid
import invenio_pidstore
import invenio_records_rest
#import kwargs as kwargs
from invenio_jsonschemas import current_jsonschemas
from invenio_records_rest.schemas import Nested, StrictKeysMixin
from invenio_records_rest.schemas.fields import DateString, GenFunction, \
    PersistentIdentifier, SanitizedUnicode
from invenio_rest.serializer import BaseSchema
from marshmallow import fields, missing, validate, INCLUDE
from invenio_oaiserver.minters import oaiid_minter
from invenio_oaiserver.provider import OAIIDProvider
from testinvenio.records.api import Record
#from invenio_pidstore.models import PersistentIdentifier

def bucket_from_context(_, context):
    """Get the record's bucket from context."""
    record = (context or {}).get('record', {})
    return record.get('_bucket', missing)


def files_from_context(_, context):
    """Get the record's files from context."""
    record = (context or {}).get('record', {})
    return record.get('_files', missing)


def files_from_context(_, context):
    """Get the record's files from context."""
    record = (context or {}).get('record', {})
    return record.get('_files', missing)


def schema_from_context(_, context):
    """Get the record's schema from context."""
    record = (context or {}).get('record', {})
    return record.get(
        "_schema",
        current_jsonschemas.path_to_url(Record._schema)
    )


class PersonIdsSchemaV1(StrictKeysMixin):
    """Ids schema."""

    source = SanitizedUnicode()
    value = SanitizedUnicode()


class OaiSchemaV1(BaseSchema):
    """Resource type schema."""
    #id =  OAIIDProvider.create()
    #id = PersistentIdentifier()
    id = fields.Str()
    sets = fields.List(fields.Str)
    updated = fields.Str()

    # @validates_schema
    # def validate_data(self, data, **kwargs):
    #     """Validate resource type."""
    #     validate_entry('resource_type', data)


class ContributorSchemaV1(StrictKeysMixin):
    """Contributor schema."""

    ids = fields.Nested(PersonIdsSchemaV1, many=True)
    name = SanitizedUnicode(required=True)
    role = SanitizedUnicode()
    affiliations = fields.List(SanitizedUnicode())
    email = fields.Email()


class MetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    id = PersistentIdentifier()
    title = SanitizedUnicode()
    fileName = SanitizedUnicode()
    fileType = SanitizedUnicode()
    owner = fields.Integer()
    keywords = fields.List(SanitizedUnicode(), many=True)
    publication_date = DateString()
    contributors = Nested(ContributorSchemaV1, many=True)
    _schema = GenFunction(
        attribute="$schema",
        data_key="$schema",
        deserialize=schema_from_context,  # to be added only when loading
    )
    _oai = Nested(OaiSchemaV1)

    class Meta:
        unknown = INCLUDE

class RecordSchemaV1(StrictKeysMixin):
    """Record schema."""
    _oai = Nested(OaiSchemaV1)
    metadata = fields.Nested(MetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = invenio_records_rest.schemas.fields.PersistentIdentifier()
    files = GenFunction(
        serialize=files_from_context, deserialize=files_from_context)

    class Meta:
        unknown = INCLUDE
