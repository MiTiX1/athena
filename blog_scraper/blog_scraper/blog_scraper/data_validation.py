from marshmallow import Schema, fields, ValidationError
from bson import ObjectId


def is_id_valid(id_: str) -> None:
    if not ObjectId.is_valid(id_):
        raise ValidationError(f"'{id_}' is not a valid id")


class InputRunForSchema(Schema):
    blogId = fields.String(required=True, validate=is_id_valid)


class InputRunOnDemandSelectorSchema(Schema):
    cssSelector = fields.String(required=True)
    remove = fields.String(required=False)
    takeBefore = fields.String(required=False)
    takeAfter = fields.String(required=False)


class InputRunOnDemandSelectorsSchema(Schema):
    link = fields.String(required=True)
    title = fields.Nested(InputRunOnDemandSelectorSchema, required=True)
    text = fields.Nested(InputRunOnDemandSelectorSchema, required=True)
    date = fields.Nested(InputRunOnDemandSelectorSchema, required=True)


class InputRunOnDemandSchema(Schema):
    name = fields.String(required=True)
    isSelenium = fields.Boolean(required=True)
    lang = fields.String(required=True)
    startUrl = fields.URL(required=True)
    selectors = fields.Nested(InputRunOnDemandSelectorsSchema, required=True)


input_run_for_schema = InputRunForSchema()
input_run_on_demand_schema = InputRunOnDemandSchema()