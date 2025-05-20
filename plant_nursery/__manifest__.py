{
    'name': 'Plant Nursery',
    'version': '1.0',
    'category': 'Toools',
    'summary': 'Plants and customers management',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        #'data/data.xml',
        'views/nursery_plant_views.xml',
        'views/nursery_customer_views.xml',
        'views/nursery_order_views.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'css': [],
    'installable':True,
    'auto_install':False,
    'application':True,
    'images':[
        'static/description/icon.png'
    ],

}