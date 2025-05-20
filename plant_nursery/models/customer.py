from odoo import models, fields, api

class Customer(models.Model):
    _name = 'nursery.customer'

    name=fields.Char("Customer Name", required=True)
    email=fields.Char(help="To receive the newsletter ")
    mobile = fields.Char('Mobile')
    image=fields.Binary('Photo', attachment=True)
    address= fields.Char('Address')
    country_id=fields.Many2one('res.country', string='Country')
    partner_id=fields.Many2one('res.partner',string='Customer Address')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.image_1920:
                self.image= self.partner_id.image_1920
            if self.partner_id.email:
                self.email= self.partner_id.mobile
            if self.partner_id.country_id:
                self.country_id=self.partner_id.country_id.id
            if not self.address:
                self.address = self.partner_id.with_context(show_address_only=True)._get_name()
