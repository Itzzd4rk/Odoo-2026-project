from odoo import models


class CustomEsgReport(models.AbstractModel):
    _name = 'report.esg_management.report_custom_esg'
    _description = 'Custom ESG QWeb Report'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['esg.report.builder.wizard'].browse(docids).exists()
        return wizard._build_report_data()
