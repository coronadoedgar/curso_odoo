# -*- coding: utf-8 -*-

from odoo import api, models, fields


class InvoiceSunatWizard(models.TransientModel):

    _name = 'invoice.sunat.wizard'

    @api.multi
    def invoice_confirm(self):
        id_invoice = self.env.context.get('active_id')
        obj_invoice = self.env['invoice.sunat'].browse(id_invoice)
        obj_invoice.update({
            'date_approved': fields.Datetime.now(),
            'state': 'done'
        })
