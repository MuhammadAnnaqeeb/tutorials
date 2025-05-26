from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description = "Real Estate Property Type"
    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)',
        'A property type name must be unique')
    ]
    _order = "name"

    name=fields.Char(required=True)
    property_ids=fields.One2many("estate.property",inverse_name="property_type_id",string="Properties")
    sequence=fields.Integer('Sequence',default=1, help="Used to order properties.")

    offer_ids=fields.One2many("estate.property.offer", inverse_name='property_type_id')

    offer_count=fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            if type_offer_ids:=self.mapped('offer_ids') :
                record.offer_count = len(type_offer_ids)
            else:
                record.offer_count = 0



