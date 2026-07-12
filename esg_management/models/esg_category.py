from odoo import fields, models


class EsgCategory(models.Model):
    _name = 'esg.category'
    _description = 'ESG Category'

    name = fields.Char(required=True)
    type = fields.Selection([('csr_activity', 'CSR Activity'), ('challenge', 'Challenge')], required=True)
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active', required=True)
