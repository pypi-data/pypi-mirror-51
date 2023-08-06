import pytest
from testfixtures import compare

from src import schema, fields


def test__get_instance_vars():
    class TestObject:

        def __init__(self):
            self.int_a = 0
            self.int_b = 0

    obj_cls = TestObject

    res = schema._get_instance_variables(obj_cls)

    assert res == ["int_a", "int_b"]


@pytest.mark.skip
def test__get_instance_vars_nested_init():
    class TestObject:

        def _nested_init(self):
            self.int_c = 0

        def __init__(self):
            self.int_a = 0
            self.int_b = 0
            self._nested_init()

    obj_cls = TestObject

    res = schema._get_instance_variables(obj_cls)
    # print(res)
    assert res == ["int_a", "int_b", "int_c"]


def test__get_field_vars():
    """
    Tests that _get_field_vars returns a dictionary of expected Field objects.
    """

    # class TestObject:
    #
    #     def __init__(self):
    #         self.int_a = 0
    #         self.int_b = 0

    # obj_cls = TestObject

    field_vars = schema._get_field_vars(["int_a", "int_b"],
                                        fd=["int_a", "int_b"])

    def field_comparator(x, y, _):
        """
        Test fixture for comparing two fields.Field objects
        """
        if x.load_from != y.load_from:
            return "x != y since x.load_from: {} != y.load_from: {}".format(
                x.load_from, y.load_from
            )

    compare(

        field_vars, {
            "int_a": fields.Raw(load_from="intA"),
            "int_b": fields.Raw(load_from="intB"),
        }, comparers={fields.Field: field_comparator}

    )


def test_set_attr():
    """
    Tests that generate_schema returns a schema that has the ability to
        set instance variables based on keys of different format in the
        dictionary provided in schema.load(d)
    """

    class TestObject(object):

        def __init__(self):
            super().__init__()
            self.int_a = 0
            self.int_b = 0

        @classmethod
        def get_fields(cls):
            return ["int_a", "int_b"]

        def __new__(cls, *args, **kwargs):
            instance = super().__new__(cls, *args, **kwargs)
            return instance

    s = schema.generate_schema(TestObject)

    # print(s)

    obj = s.load({
        "intA": 1,
        "intB": 2
    }).data

    assert obj.int_a == 1
    assert obj.int_b == 2

    # TODO: test that no extraneous attributes are set


def test_conversion():
    """
    Tests that "camelCase" key used in Firestore converts to "snake_case"
        target instance variable names.
    """

    res = schema.firestore_key_to_attr_name("intA")
    assert res == "int_a"

    r_res = schema.attr_name_to_firestore_key("int_a")
    assert r_res == "intA"
