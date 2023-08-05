# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UDFResponse(Model):
    """UDFResponse.

    :param udf_id:
    :type udf_id: int
    :param name:
    :type name: str
    :param udf_type:
    :type udf_type: str
    :param data_type:
    :type data_type: ~energycap.sdk.models.DataTypeResponse
    :param display_order:
    :type display_order: int
    :param udf_select_values:
    :type udf_select_values:
     list[~energycap.sdk.models.UDFSelectValueResponse]
    :param count:
    :type count: int
    """

    _attribute_map = {
        'udf_id': {'key': 'udfId', 'type': 'int'},
        'name': {'key': 'name', 'type': 'str'},
        'udf_type': {'key': 'udfType', 'type': 'str'},
        'data_type': {'key': 'dataType', 'type': 'DataTypeResponse'},
        'display_order': {'key': 'displayOrder', 'type': 'int'},
        'udf_select_values': {'key': 'udfSelectValues', 'type': '[UDFSelectValueResponse]'},
        'count': {'key': 'count', 'type': 'int'},
    }

    def __init__(self, udf_id=None, name=None, udf_type=None, data_type=None, display_order=None, udf_select_values=None, count=None):
        super(UDFResponse, self).__init__()
        self.udf_id = udf_id
        self.name = name
        self.udf_type = udf_type
        self.data_type = data_type
        self.display_order = display_order
        self.udf_select_values = udf_select_values
        self.count = count
