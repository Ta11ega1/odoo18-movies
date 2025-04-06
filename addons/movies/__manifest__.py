# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Movies',
    'version': '1.0',
    'category': 'Personalizacion',
    'summary': 'Consumo de api externa de Peliculas',
    'description': """
Se consume una api externa cada x tiempo donde se rescata el país y se guarda en una tabla en el sistema.
Se disponibiliza una api de consumo donde permite obtener el top 10 de peliculas registradas en el sistema.
Se registra los consumos de la api de peliculas en el visor de eventos.
    """,
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/movie_movie_views.xml',
        'views/movies_menus.xml',  # Last because referencing actions defined in previous files
        'views/visor_eventos_views.xml',
        'views/visor_eventos_menus.xml',
        'data/cron.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'assets': {
    },
}