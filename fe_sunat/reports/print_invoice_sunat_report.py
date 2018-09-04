# -*- coding: utf-8 -*-

from odoo import api, models


class ReportInvoiceSunat(models.AbstractModel):

    _name = 'report.fe_sunat.report_invoice_sunat'

    @api.model
    def get_report_values(self, docids, data=None):
        list_obj_inv = self.env['invoice.sunat'].browse(docids)
        obj_company = self.env.user.company_id
        list_data = self.build_data(list_obj_inv)
        docargs = {
            'docs': list_data,
            'company': obj_company
        }
        return docargs

    def build_data(self, list_obj):
        list_data = []
        for obj in list_obj:
            igv = self.calc_igv(obj.total)
            list_data.append({
                'name': obj.name,
                'partner_name': obj.partner_id.name or '',
                'date': obj.date or '',
                'date_approved': obj.date_approved or '',
                'total': obj.total or 0.0,
                'igv': igv or 0.0,
                'line_ids': obj.invoice_line_ids or []
            })
        print "list_data", list_data
        return list_data

    def calc_igv(self, total):
        igv = total * 0.18
        return igv
