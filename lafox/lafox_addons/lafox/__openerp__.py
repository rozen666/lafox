# -*- coding: utf-8 -*-
{
    'name': "La Fox",
    'summary': """
        Sistema de para la integración de los
    procesos de La Fox""",

    'description': """
        Sistematización de los procesos de inventarios, ventas, asistencias, etc,
    para la Fox  deshabilitar stock.quant.multicompany
    """,

    'author': "BPMTech",
    'category': 'LaFox',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base','stock', 'mail','account','account_accountant','hr','website'],
    #'depends': ['base','stock', 'mail','account','account_accountant','hr','website'],
    # always loaded
    'data': [
        'data/lafox_data.xml',
        'data/lafox_sequence.xml',
        'view/lafox_view.xml',
        'view/lafox_ventas_view.xml',
        'view/lafox_configuracion.xml',
        'data/lafox_crontab.xml',
        'data/email_templates.xml',
        'security/lafox_security.xml',
        'security/ir.model.access.csv',
        'view/menu_hide_view.xml',
        # 'view/homepage.xml',
    ],
    'js': [],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
