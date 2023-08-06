import random
import string


# Generate a random string
# with 32 characters.
# https://www.geeksforgeeks.org/generating-random-ids-python/
def random_id():
    random_id_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    return random_id_str


def obj_type_serialize(obj: object):
    """ Returns class name. To be used with Schema.obj_type field.

    :param obj:
    :return:
    """

    return obj.__class__.__name__


def obj_type_deserialize(value):
    """ Returns class name. To be used with Schema.obj_type field.

    :param value:
    :return:
    """

    return value