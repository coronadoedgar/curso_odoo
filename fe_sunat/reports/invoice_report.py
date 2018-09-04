# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class InvoiceReport(models.Model):

    _name = 'invoice.report'

    _auto = False

    _rec_name = 'number'

    number = fields.Char(
        string='Número'
    )
    partner_id = fields.Many2one(
        comodel_name='partner.base',
        string='Id Cliente'
    )
    partner_name = fields.Char(
        string='Cliente'
    )
    date = fields.Date(
        comodel_name='Fecha'
    )
    date_approved = fields.Datetime(
        comodel_name='Fecha Aprobado'
    )
    total = fields.Float(
        string='Total'
    )

    def _select(self):
        select_str = """
            SELECT
                inv.id as id,
                inv.name as number,
                pb.id as partner_id,
                pb.name as partner_name,
                inv.date,
                inv.date_approved,
                inv.total as total
        """
        return select_str

    def _from(self):
        from_str = """
            invoice_sunat inv
            left join partner_base pb on pb.id = inv.partner_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY inv.id, total, pb.id, partner_name, number, inv.date, inv.date_approved
        """
        return group_by_str

    @api.model_cr
    def init(self):
        print "table name >>>>>", self._table

        tools.drop_view_if_exists(self.env.cr, self._table)
        value_view = """CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
        )""" % (self._table, self._select(), self._from(), self._group_by())
        print "sql value view", self.env.cr.mogrify(value_view)
        self.env.cr.execute(value_view)
