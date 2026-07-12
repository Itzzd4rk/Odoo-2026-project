from odoo import fields, models


class EsgProductProfile(models.Model):
    _name = 'esg.product.profile'
    _description = 'Product Sustainability Profile'

    product_id = fields.Many2one('product.product', required=True, ondelete='cascade')
    default_emission_factor_id = fields.Many2one('esg.emission.factor')
    sustainability_notes = fields.Text()
    recyclable = fields.Boolean()

    _sql_constraints = [('esg_product_profile_unique', 'unique(product_id)', 'Only one ESG profile is allowed per product.')]
