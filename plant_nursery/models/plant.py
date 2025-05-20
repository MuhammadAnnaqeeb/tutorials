from odoo.exceptions import UserError
from odoo import api,fields, models

class Plant(models.Model):
    _name = 'nursery.plant'
    _description = 'Plant'

    image = fields.Binary("Plant Image", attachment=True)

    name = fields.Char("Plant Name")
    price = fields.Float()
    order_ids=fields.One2many(comodel_name="nursery.order",
                              inverse_name="plant_id",
                              string="Orders")
    order_count =  fields.Integer(compute='_compute_order_count',
                                  store=True,
                                  string="Total sold")
    number_in_stock = fields.Integer()

    @api.constrains('order_count', 'number_in_stock')
    def _check_available_in_stock(self):
        for plant in self:
            if plant.number_in_stock and plant.order_count > plant.number_in_stock:
                raise UserError("There is only %s %s in stock but %s were sold"
                    % (plant.number_in_stock, plant.name,plant.order_count))


    @api.depends('order_ids')
    def _compute_order_count(self):
        for plant in self:
            plant.order_count = len(plant.order_ids)