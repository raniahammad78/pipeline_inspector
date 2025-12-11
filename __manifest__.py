{
    'name': 'Pipeline Inspector',
    'version': '18.0',
    'author': 'Rania Hammad',
    'category': 'Industries',
    'summary': 'Module for managing pipeline inspections.',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/dashboard_data.xml',
        'views/pipeline_inspector_views.xml',
        'views/dashboard_views.xml',
        'reports/pipeline_report.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
