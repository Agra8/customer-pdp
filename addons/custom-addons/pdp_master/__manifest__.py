{
    "name":"PDP Master",
    "version":"0.1",
    "author":"PDP",
    "website":"",
    "category":"Uncategorized",
    "description": """
        PDP Master 
    """,
    "depends":["base", "hr"],
    "data":[
            'security/ir.model.access.csv',
            'views/master_pdp_view.xml',
            # 'views/hr_job_view.xml',
            'views/res_country_view.xml',
            'views/res_city_view.xml',
            'views/res_kecamatan_view.xml',
            'views/res_kelurahan_view.xml'
              ]
}