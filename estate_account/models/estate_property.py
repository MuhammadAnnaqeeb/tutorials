from odoo import models, Command


class Property(models.Model):
    _name = "estate.property"
    _inherit = "estate.property"

    def action_sold(self):
        # print("overriden method")
        journal = (
            self.env["account.journal"].sudo().search([("type", "=", "sale")], limit=1)
        )
        current_user = self.env.user
        for prop in self:
            print(" reached ".center(100, "="))
            self.env["account.move"].check_access("create")
            account_move = self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "line_ids": [
                        Command.create(
                            {
                                "name": "6% of the selling price",
                                "quantity": "1",
                                "price_unit": 0.06 * prop.selling_price,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administration fees",
                                "quantity": "1",
                                "price_unit": "100.00",
                            }
                        ),
                    ],
                }
            )
        return super().action_sold()
