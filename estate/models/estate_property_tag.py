from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)',
         'A property tag name must be unique')
    ]
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
