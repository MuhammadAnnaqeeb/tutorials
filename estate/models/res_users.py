from odoo import api, fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="user_id",
                                   string="Real Estate Properties",
                                   domain="[ '|',('state', '=', 'new'),('state', '=', 'offer_received')]"
                                   )
