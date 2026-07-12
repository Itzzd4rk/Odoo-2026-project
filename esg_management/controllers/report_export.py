import csv
import io
import xlsxwriter
from odoo import http
from odoo.http import request


class EsgReportExportController(http.Controller):
    @http.route('/esg/report/<int:wizard_id>/xlsx', type='http', auth='user')
    def export_xlsx(self, wizard_id, **kwargs):
        wizard = request.env['esg.report.builder.wizard'].browse(wizard_id).exists()
        if not wizard:
            return request.not_found()
        output = io.BytesIO()
        book = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = book.add_worksheet('ESG Report')
        heading = book.add_format({'bold': True, 'bg_color': '#183A37', 'font_color': '#FFFFFF'})
        for column, title in enumerate(['Pillar', 'Metric', 'Value']):
            sheet.write(0, column, title, heading)
        for row, item in enumerate(wizard._build_report_data()['rows'], 1):
            sheet.write_row(row, 0, [item['pillar'], item['metric'], item['value']])
        sheet.set_column(0, 1, 28)
        sheet.set_column(2, 2, 18)
        book.close()
        return request.make_response(output.getvalue(), headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), ('Content-Disposition', 'attachment; filename="esg-report.xlsx"')])

    @http.route('/esg/report/<int:wizard_id>/csv', type='http', auth='user')
    def export_csv(self, wizard_id, **kwargs):
        wizard = request.env['esg.report.builder.wizard'].browse(wizard_id).exists()
        if not wizard:
            return request.not_found()
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['pillar', 'metric', 'value'])
        writer.writeheader()
        writer.writerows(wizard._build_report_data()['rows'])
        return request.make_response(output.getvalue(), headers=[('Content-Type', 'text/csv; charset=utf-8'), ('Content-Disposition', 'attachment; filename="esg-report.csv"')])
