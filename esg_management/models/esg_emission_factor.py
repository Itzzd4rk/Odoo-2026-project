from odoo import fields, models


class EsgEmissionFactor(models.Model):
    _name = 'esg.emission.factor'
    _description = 'Emission Factor'
    _order = 'effective_date desc, id desc'

    name = fields.Char(required=True)
    activity_type = fields.Selection([('purchase', 'Purchase'), ('manufacturing', 'Manufacturing'), ('expense', 'Expense'), ('fleet', 'Fleet')], required=True)
    unit = fields.Char(help='For example: kg CO2e / litre')
    factor_value = fields.Float(required=True, digits=(16, 6))
    effective_date = fields.Date()
    active = fields.Boolean(default=True)

    def unlink(self):
        self.write({'active': False})
        return True
