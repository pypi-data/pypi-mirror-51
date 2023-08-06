"""
Some examples are inspired by firestore documentations, some copyright
    conditions of the firestore documentations apply to code on this page.

    https://firebase.google.com/docs/firestore/query-data/queries
"""

import pytest
from google.cloud.firestore import Query

from flask_boiler.config import Config
from flask_boiler.context import Context as CTX

from flask_boiler.firestore_object import FirestoreObjectClsFactory
from flask_boiler.domain_model import DomainModel
from flask_boiler.schema import Schema
from flask_boiler import fields

config = Config(
    app_name="gravitate-dive-testing",
    debug=True,
    testing=True,
    certificate_filename="gravitate-dive-testing-firebase-adminsdk-g1ybn-2dde9daeb0.json"
)
CTX.read(config)
assert CTX.firebase_app.project_id == "gravitate-dive-testing"


class CitySchema(Schema):
    city_name = fields.Raw(load_from="name", dump_to="name")

    country = fields.Raw(load_from="country", dump_to="country")
    capital = fields.Raw(load_from="capital", dump_to="capital")


class CityBase(DomainModel):
    _collection_name = "City"


class MunicipalitySchema(CitySchema):
    pass


Municipality = FirestoreObjectClsFactory.create(
    name="Municipality",
    schema=MunicipalitySchema,
    base=CityBase,
)


class StandardCitySchema(CitySchema):
    city_state = fields.Raw(load_from="state", dump_to="state")
    regions = fields.Raw(many=True)


StandardCity = FirestoreObjectClsFactory.create(
    name="StandardCity",
    schema=StandardCitySchema,
    base=CityBase
)


def setup_cities():

    sf = StandardCity.create(doc_id="SF")
    sf.city_name, sf.city_state, sf.country, sf.capital, sf.regions = \
        'San Francisco', 'CA', 'USA', False, ['west_coast', 'norcal']
    sf.save()

    la = StandardCity.create(doc_id="LA")
    la.city_name, la.city_state, la.country, la.capital, la.regions = \
        'Los Angeles', 'CA', 'USA', False, ['west_coast', 'socal']
    la.save()

    dc = Municipality.create(doc_id="DC")
    dc.city_name, dc.country, dc.capital = 'Washington D.C.', 'USA', True
    dc.save()

    tok = Municipality.create(doc_id="TOK")
    tok.city_name, tok.country, tok.capital = 'Tokyo', 'Japan', True
    tok.save()

    beijing = Municipality.create(doc_id="BJ")
    beijing.city_name, beijing.country, beijing.capital = \
        'Beijing', 'China', True
    beijing.save()


def test_subclass_same_collection():
    """
    Tests that subclasses of a class can be stored in the same collection.
    :return:
    """

    expected_dict = {
        'Washington D.C.': {
            'name': 'Washington D.C.',
            'country': 'USA',
            'capital': True,
            'obj_type': "Municipality",
            'doc_id': 'DC',
            'doc_ref': 'City/DC'
        },
        'San Francisco': {
            'name': 'San Francisco',
            'state': 'CA',
            'country': 'USA',
            'capital': False,
            'regions': ['west_coast', 'norcal'],
            'obj_type': "StandardCity",
            'doc_id': 'SF',
            'doc_ref': 'City/SF'
        },
        'Los Angeles': {
            'name': 'Los Angeles',
            'state': 'CA',
            'country': 'USA',
            'capital': False,
            'regions': ['west_coast', 'socal'],
            'obj_type': "StandardCity",
            'doc_id': 'LA',
            'doc_ref': 'City/LA'
        }

    }

    res_dict = dict()

    for obj in CityBase.where("country", "==", "USA"):
        d = obj.to_dict()
        res_dict[d["name"]] = d

    assert res_dict['Washington D.C.'] == expected_dict['Washington D.C.']
    assert res_dict['San Francisco'] == expected_dict['San Francisco']
    assert res_dict['Los Angeles'] == expected_dict['Los Angeles']


def test_where_with_kwargs():
    """
    Tests that subclasses of a class can be stored in the same collection.
    :return:
    """

    expected_dict = {
        'Washington D.C.': {
            'name': 'Washington D.C.',
            'country': 'USA',
            'capital': True,
            'obj_type': "Municipality",
            'doc_id': 'DC',
            'doc_ref': 'City/DC'
        },
        'San Francisco': {
            'name': 'San Francisco',
            'state': 'CA',
            'country': 'USA',
            'capital': False,
            'regions': ['west_coast', 'norcal'],
            'obj_type': "StandardCity",
            'doc_id': 'SF',
            'doc_ref': 'City/SF'
        },
        'Los Angeles': {
            'name': 'Los Angeles',
            'state': 'CA',
            'country': 'USA',
            'capital': False,
            'regions': ['west_coast', 'socal'],
            'obj_type': "StandardCity",
            'doc_id': 'LA',
            'doc_ref': 'City/LA'
        }

    }

    res_dict = dict()

    for obj in CityBase.where(country="USA"):
        d = obj.to_dict()
        res_dict[d["name"]] = d

    assert res_dict['Washington D.C.'] == expected_dict['Washington D.C.']
    assert res_dict['San Francisco'] == expected_dict['San Francisco']
    assert res_dict['Los Angeles'] == expected_dict['Los Angeles']

