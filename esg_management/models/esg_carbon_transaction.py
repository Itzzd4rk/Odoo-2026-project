from odoo import api, fields, models


class EsgCarbonTransaction(models.Model):
    _name = 'esg.carbon.transaction'
    _description = 'Carbon Transaction'
    _order = 'transaction_date desc, id desc'

    name = fields.Char(required=True, copy=False, readonly=True, default='New')
    source_type = fields.Selection([('purchase', 'Purchase'), ('manufacturing', 'Manufacturing'), ('expense', 'Expense'), ('fleet', 'Fleet')], required=True)
    source_document_ref = fields.Reference(selection=[('purchase.order', 'Purchase Order'), ('mrp.production', 'Manufacturing Order'), ('hr.expense', 'Expense'), ('fleet.log', 'Fleet Log')])
    department_id = fields.Many2one('esg.department', required=True, ondelete='restrict')
    emission_factor_id = fields.Many2one('esg.emission.factor', required=True, ondelete='restrict')
    quantity = fields.Float(required=True)
    calculated_emissions = fields.Float(compute='_compute_calculated_emissions', store=True, digits=(16, 6))
    transaction_date = fields.Date(required=True, default=fields.Date.today)
    is_auto_calculated = fields.Boolean(readonly=True, default=False)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('esg.carbon.transaction') or 'New'
        return super().create(vals_list)

    @api.depends('quantity', 'emission_factor_id.factor_value')
    def _compute_calculated_emissions(self):
        for record in self:
            record.calculated_emissions = record.quantity * record.emission_factor_id.factor_value

    def action_confirm(self):
        self.write({'state': 'confirmed'})
