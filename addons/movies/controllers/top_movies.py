# Part of Odoo. See LICENSE file for full copyright and licensing details

import json

from odoo.http import Controller, request, route


class TopMovies(Controller):

    @route('/api/top_movies', type='json', auth='public', methods=['GET'], website=True)
    def get_combination_info_website(self):
        movies = request.env['movie.movie'].sudo().search([], order='ranking_movie desc', limit=10)
        return movies
