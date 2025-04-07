# Part of Odoo. See LICENSE file for full copyright and licensing details

import json

from odoo.http import Controller, request, route


class TopMovies(Controller):

    @route('/api/top_movies', type='json', auth='public', website=True)
    def get_combination_info_website(self):
        movies = request.env['movie.movie'].sudo().search([], order='ranking_movie desc', limit=10) # Retornar los 10 registros ordenados de manera descendente
        movie_list = []
        for movie in movies:
            movie_list.append({
                'id': movie.id,
                'movie_title': movie.movie_title,
                'ranking_movie': movie.ranking_movie,
            })
        return json.dumps(movie_list) # Retorna Json
