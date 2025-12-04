{
    'name': 'Estate',
    'version': '17.0.1.0',
    'sequence': -99,
    'depends': ['base','mail','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/site_views.xml',
        'views/main_unit_views.xml',
        'views/sub_unit_views.xml',
        'views/booking_views.xml',
        'views/partner_views.xml'
    ],
    'application': False,
    'installable': True,
}
