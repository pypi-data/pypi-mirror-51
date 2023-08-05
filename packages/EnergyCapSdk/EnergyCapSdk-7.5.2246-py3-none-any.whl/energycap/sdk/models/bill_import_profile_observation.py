# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillImportProfileObservation(Model):
    """BillImportProfileObservation.

    :param column_index:  <span class='property-internal'>Required</span>
     <span class='property-internal'>Must be between 1 and 2147483647</span>
    :type column_index: int
    :param observation_type_code:  <span
     class='property-internal'>Required</span>
    :type observation_type_code: str
    :param caption:  <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type caption: str
    :param unit_code:  <span class='property-internal'>Required</span>
    :type unit_code: str
    """

    _validation = {
        'column_index': {'required': True, 'maximum': 2147483647, 'minimum': 1},
        'observation_type_code': {'required': True},
        'caption': {'required': True, 'max_length': 32, 'min_length': 0},
        'unit_code': {'required': True},
    }

    _attribute_map = {
        'column_index': {'key': 'columnIndex', 'type': 'int'},
        'observation_type_code': {'key': 'observationTypeCode', 'type': 'str'},
        'caption': {'key': 'caption', 'type': 'str'},
        'unit_code': {'key': 'unitCode', 'type': 'str'},
    }

    def __init__(self, column_index, observation_type_code, caption, unit_code):
        super(BillImportProfileObservation, self).__init__()
        self.column_index = column_index
        self.observation_type_code = observation_type_code
        self.caption = caption
        self.unit_code = unit_code
