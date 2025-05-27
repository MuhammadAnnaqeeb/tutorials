# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'estate',
    'version': '16.0',
    'category': 'Real Estate/Brokerage',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'description': "",
    'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base'
    ],
    'data': [
        
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

    ],
    'demo': [
    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
}