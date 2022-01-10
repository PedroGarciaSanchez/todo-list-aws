import decimal
import json


# This is a workaround for: http://bugs.python.org/issue16535
# PGS: the json module has incomplete support for decimals
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):      # pylint: disable=E0202
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
