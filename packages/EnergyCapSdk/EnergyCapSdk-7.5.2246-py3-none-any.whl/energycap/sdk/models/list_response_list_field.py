# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ListResponseListField(Model):
    """ListResponseListField.

    :param field_id: Column/Filter Identifier
    :type field_id: int
    :param width: Width of the column
    :type width: int
    :param display_order: Order of the column
    :type display_order: int
    :param sortable: Is the column sortable?
    :type sortable: bool
    :param caption: Caption for the column/filter
    :type caption: str
    :param sort_direction: Sort direction "asc" or "desc"
    :type sort_direction: str
    :param sort_order: Sort order for the column
    :type sort_order: int
    :param data_type_code: Type of Data in this column
    :type data_type_code: str
    :param required_output: Is this column a required column?
    :type required_output: bool
    :param visible: Is this column currently visible?
    :type visible: bool
    """

    _attribute_map = {
        'field_id': {'key': 'fieldId', 'type': 'int'},
        'width': {'key': 'width', 'type': 'int'},
        'display_order': {'key': 'displayOrder', 'type': 'int'},
        'sortable': {'key': 'sortable', 'type': 'bool'},
        'caption': {'key': 'caption', 'type': 'str'},
        'sort_direction': {'key': 'sortDirection', 'type': 'str'},
        'sort_order': {'key': 'sortOrder', 'type': 'int'},
        'data_type_code': {'key': 'dataTypeCode', 'type': 'str'},
        'required_output': {'key': 'requiredOutput', 'type': 'bool'},
        'visible': {'key': 'visible', 'type': 'bool'},
    }

    def __init__(self, field_id=None, width=None, display_order=None, sortable=None, caption=None, sort_direction=None, sort_order=None, data_type_code=None, required_output=None, visible=None):
        super(ListResponseListField, self).__init__()
        self.field_id = field_id
        self.width = width
        self.display_order = display_order
        self.sortable = sortable
        self.caption = caption
        self.sort_direction = sort_direction
        self.sort_order = sort_order
        self.data_type_code = data_type_code
        self.required_output = required_output
        self.visible = visible
