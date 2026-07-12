from odoo import api, fields, models


class EsgDepartment(models.Model):
    _name = 'esg.department'
    _description = 'ESG Department'
    _parent_store = True
    _rec_name = 'complete_name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    head_id = fields.Many2one('hr.employee', string='Department Head')
    parent_id = fields.Many2one('esg.department', index=True, ondelete='restrict')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('esg.department', 'parent_id')
    member_ids = fields.One2many('hr.employee', 'esg_department_id', string='Members')
    employee_count = fields.Integer(compute='_compute_employee_count')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active', required=True)
    complete_name = fields.Char(compute='_compute_complete_name', recursive=True, store=True)

    _sql_constraints = [('esg_department_code_unique', 'unique(code)', 'The ESG department code must be unique.')]

    @api.depends('member_ids')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = len(record.member_ids)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for record in self:
            record.complete_name = '%s / %s' % (record.parent_id.complete_name, record.name) if record.parent_id else record.name
