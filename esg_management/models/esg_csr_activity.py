from odoo import api, fields, models


class EsgCsrActivity(models.Model):
    _name = 'esg.csr.activity'
    _description = 'CSR Activity'

    name = fields.Char(required=True)
    description = fields.Text()
    category_id = fields.Many2one('esg.category', domain=[('type', '=', 'csr_activity')])
    department_id = fields.Many2one('esg.department')
    date = fields.Date()
    status = fields.Selection([('planned', 'Planned'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned', required=True)
    participation_ids = fields.One2many('esg.employee.participation', 'activity_id')
    participant_count = fields.Integer(compute='_compute_participant_count')

    @api.depends('participation_ids')
    def _compute_participant_count(self):
        for record in self:
            record.participant_count = len(record.participation_ids)
