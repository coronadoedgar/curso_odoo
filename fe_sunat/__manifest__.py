# -*- coding: utf-8 -*-

{
    'name': 'FE SUNAT',
    'version': '0.1',
    'category': 'Accounting',
    'summary': 'Invoice Sunat',
    'description': """
Addons demo with format FE
    """,
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        'views/trees.xml',
        'views/forms.xml',
        'views/searchs.xml',
        'reports/invoice_sunat_report_view.xml',
        'reports/print_invoice_sunat_template.xml',
        'reports/print_invoice_sunat_report.xml',
        'views/actions.xml',
        'views/menus.xml',
        'views/wizards.xml',
    ],
    'installable': True,
    'auto_install': False,
}
