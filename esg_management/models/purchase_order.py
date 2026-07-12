from odoo import models
from .esg_tools import setting_enabled


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        result = super().button_confirm()
        if not setting_enabled(self.env, 'auto_emission_calc', False):
            return result
        Carbon = self.env['esg.carbon.transaction']
        for order in self:
            department = self.env['esg.department'].search([('status', '=', 'active')], limit=1)
            # ASSUMPTION: Purchase transactions use the first active ESG department when no departmental analytic mapping exists.
            if not department:
                continue
            for line in order.order_line:
                profile = self.env['esg.product.profile'].search([('product_id', '=', line.product_id.id)], limit=1)
                if profile.default_emission_factor_id:
                    Carbon.create({'source_type': 'purchase', 'source_document_ref': 'purchase.order,%s' % order.id, 'department_id': department.id, 'emission_factor_id': profile.default_emission_factor_id.id, 'quantity': line.product_qty, 'transaction_date': order.date_order.date(), 'is_auto_calculated': True, 'state': 'confirmed'})
        return result
