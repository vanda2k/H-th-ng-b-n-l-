# -*- coding: utf-8 -*-
{
    'name': 'RetailToy',
    'version': '1.0',
    'summary': 'Retail Toy',
    'sequence': 1,
    'author': 'Thao',
    'description': """
        Retail Management Odoo
    """,
    'category': 'Other',
    'website': '',
    'depends': ['base','mail','uom'],
    'data': [
        'views/product_view.xml',
        'views/category_view.xml',
        'views/unit_view.xml',
        'views/employee_view.xml',
        'views/position_view.xml',
        'views/department_view.xml',
        'views/inventory_view.xml',
        'views/partner_view.xml',
        'views/industry_view.xml',
        'views/purchase_view.xml',
        'views/purchase_order_line_view.xml',
        'views/point_session_view.xml',
        'views/order_view.xml',
        'views/sale_order_line_view.xml',
        'security/security_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
}