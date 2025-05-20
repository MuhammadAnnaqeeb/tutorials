
from odoo import _,models, fields, api
from odoo.exceptions import UserError

class Order(models.Model):
    _name= 'nursery.order'
    _description =  'Nursery Order'

    name =  fields.Char(
        'Reference', default = lambda self: _('New'), required=True, states={'draft:'}
    )
    plant_id = fields.Many2one("nursery.plant", required=True)
    customer_id = fields.Many2one("nursery.customer")
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Canceled')
    ], default='draft', group_expand="_expand_states")
    last_modification=fields.Datetime(readonly=True)

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def write(self, values):
        #helper to "YYYY-MM-DD"
        values['last_modification'] = fields.Datetime.now()

        return super(Order,self).write(values)

    def unlink(self):
        #self is a recordset
        for order in self:
            if order.state=='confirm':
                raise UserError("You can not delete confirmed orders")

        return super(Order,self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']
                ).next_by_code('plant.order') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('plant.order') or _('New')
        return super(Order, self).create(vals)
