{
    'name': 'PDP Consent & Agreement Management', 
    'summary': 'PDP Consent & Agreement Management',
    'description': '''
        PDP Consent & Agreement Management
    ''',
    'version': '0.1',
    'category': 'Uncategorized',
    'license': 'LGPL-3', 
    'author': 'PT. Tunas Ridean / Yogabpp',
    'depends': ['base'],
    'data': [
    'security/ir.model.access.csv',
    'views/consent_agreement_views.xml',
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/consent_agreement_views.xml',
        'data/pdp_consent_sequence.xml',
    ]
    # only loaded in demonstration mode
}
