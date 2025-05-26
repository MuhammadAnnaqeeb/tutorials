from email.policy import default

from dateutil.utils import today

from odoo.exceptions import UserError, ValidationError
from odoo import _, api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    


    _name = "estate.property"
    _description = "Real Estate Property"
    _sql_constraints = [
        ('check_expected_price', 'CHECK( expected_price > 0)',
         'A property expected price should be strictly positive'),
        ('check_selling_price', 'CHECK( selling_price > 0)',
         'A property selling price should be strictly positive')
    ]
    _order = "id desc"

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string="Status",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="The state of the real estate property",
        required=True,
        copy=False,
        default='new'
    )
    name = fields.Char(required=True, string="Title")
    postcode = fields.Char()
    three_months_later = date.today() + relativedelta(months=3)

    date_availability = fields.Date(string="Available from", default=three_months_later, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities"
    )

    description = fields.Text()

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_id', string="Property Offers")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids")
    def _compute_best_price(self):
        for prop in self:
            if prop.offer_ids  and (offers := prop.offer_ids.mapped('price')) :
                prop.best_price = max(0, max(offers))
                if prop.state == 'new':
                    prop.state = 'offer_received'
            else:
                prop.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None



    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for prop in self:
            if (not float_is_zero(prop.selling_price, precision_digits=2) and
                    float_compare(prop.selling_price, 0.9 * prop.expected_price, precision_digits=2) == -1):
                raise ValidationError("Selling Price Can not be less than 90% of expected price")


    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_canceled(self):
        for prop in self:
            if prop.state not in ['new', 'canceled']:
                raise UserError("Cannot delete property unless new or cancelled.")

    def action_sold(self):
        if 'canceled' in self.mapped('state'):
            raise UserError(_('Canceled properties can not be sold'))
        return self.write({'state': 'sold'})

    def action_cancel(self):
        if 'sold' in self.mapped('state'):
            raise UserError(_('Sold properties can not be canceled'))
        return self.write({'state': 'canceled'})