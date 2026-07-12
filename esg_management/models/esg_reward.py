from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EsgReward(models.Model):
    _name = 'esg.reward'
    _description = 'ESG Reward'

    name = fields.Char(required=True)
    description = fields.Text()
    points_required = fields.Integer(required=True)
    stock = fields.Integer(required=True, default=0)
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active', required=True)

    @api.constrains('stock')
    def _check_nonnegative_stock(self):
        if any(reward.stock < 0 for reward in self):
            raise ValidationError('Reward stock cannot be negative.')
