# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PartnerBase(models.Model):

    _name = 'partner.base'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    type = fields.Selection(
        selection=[
            ('customer', 'cliente'),
            ('supplier', 'proveedor')
        ],
        string='Tipo',
        required=True
    )


class InvoiceSunat(models.Model):

    _name = 'invoice.sunat'

    name = fields.Char(
        string=u'Número',
        required=True
    )
    date = fields.Date(
        string='Fecha'
    )
    date_approved = fields.Datetime(
        string='Fecha Aprobado'
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('done', 'Validado'),
            ('account', 'Contabilizado'),
            ('cancel', 'Cancelado')
        ],
        string='Estado',
        default='draft'
    )
    partner_id = fields.Many2one(
        comodel_name='partner.base',
        required=True,
        domain=[('type', '=', 'customer')],
        string='Cliente'
    )
    invoice_line_ids = fields.One2many(
        comodel_name='invoice.sunat.line',
        inverse_name='invoice_id',
        string='Líneas Facturables'
    )
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True
    )

    @api.one
    @api.depends('invoice_line_ids.sub_total')
    def _compute_total(self):
        total = 0
        for obj_line in self.invoice_line_ids:
            total += obj_line.sub_total
        self.total = total

    @api.multi
    def action_confirm(self):
        form = self.env.ref('fe_sunat.view_invoice_sunat_wizard', False)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Confirmar Factura',
            'res_model': 'invoice.sunat.wizard',
            'views': [(form.id, 'form')],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form.id,
            'target': 'new',
        }

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'

    @api.multi
    def action_account(self):
        self.state = 'account'

    @api.multi
    def action_back(self):
        self.state = 'draft'


class InvoiceSunatLine(models.Model):

    _name = 'invoice.sunat.line'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Producto',
        required=True
    )
    name = fields.Char(
        string='Descripción',
        required=True
    )
    invoice_id = fields.Many2one(
        comodel_name='invoice.sunat'
    )
    qty = fields.Integer(
        string='Cantidad',
        required=True,
        default=1
    )
    price = fields.Float(
        string='Precio'
    )
    sub_total = fields.Float(
        string='SubTotal',
    )
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Validado'),
        ('account', 'Contabilizado'),
        ('cancel', 'Cancelado')
    ], string='Estado', default='draft',
        related='invoice_id.state'
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        name = '-'
        price = 0
        sub_total = 0
        if self.product_id.default_code:
            name = self.product_id.default_code
            price = self.product_id.lst_price
            sub_total = price * self.qty

        self.update({
            'name': name,
            'price': price,
            'sub_total': sub_total
        })


class TicketSunat(models.Model):

    _name = 'ticket.sunat'
    _inherit = 'invoice.sunat'

    description = fields.Text(
        string=u'Descripción'
    )


class Partner(models.Model):

    _inherit = 'res.partner'

    base_partner_id = fields.Many2one(
        string='Cliente Sunat',
        comodel_name='partner.base',
        domain=[('type', '=', 'customer')]
    )


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    invoice_sunat_ids = fields.Many2many(
        string='Factura Sunat',
        comodel_name='invoice.sunat',
        compute='_compute_invoice',
        store='True'
    )

    @api.one
    @api.depends('partner_id')
    def _compute_invoice(self):
        obj_partner = self.partner_id.base_partner_id
        list_invoice_ids = []
        if obj_partner:
            list_obj_invoice = self.env['invoice.sunat'].search([
                ('partner_id', '=', obj_partner.id)
            ])
            list_invoice_ids = map(lambda x: x.id, list_obj_invoice)
        self.invoice_sunat_ids = list_invoice_ids
