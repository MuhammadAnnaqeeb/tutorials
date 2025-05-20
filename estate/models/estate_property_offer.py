from odoo.exceptions import UserError
from odoo import _, api, fields, models
from datetime import date, timedelta, datetime

from odoo.tools import float_compare


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _sql_constraints = [
        ('check_offer_price', 'CHECK( price > 0)',
         'A property offer price should be strictly positive')
    ]
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)

    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = offer_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - offer_date).days



    @api.model
    def create(self, vals):
        if vals.get('price') and vals.get('property_id'):
            prop = self.env['estate.property'].browse(vals['property_id'])
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals['price'], max_offer, precision_rounding=0.01) < 0:
                    raise UserError("The offer must be equal to or higher than %.2f" % max_offer)
            prop.state = 'offer_received'
        return super().create(vals)

    def action_accept(self):
        if self.mapped('property_id').state == 'offer_accepted':
            raise UserError(_('Can not accept multiple offers'))
        return self.mapped('property_id').write({
            'state': 'offer_accepted',
            'buyer_id': self.partner_id,
            'selling_price': self.price
        }) and self.write({'state': 'accepted'})

    def action_refuse(self):
        return self.write({'state': 'refused'})