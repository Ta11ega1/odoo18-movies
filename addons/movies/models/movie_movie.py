# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import requests
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class MovieMovie(models.Model):
    _name = 'movie.movie'
    _rec_name = 'movie_title'
    _order = 'ranking_movie'

    movie_title = fields.Char("Título")
    ranking_movie = fields.Integer('Ranking')

    def _cron_consume_api_movie(self):
        api_key = 'ZN-BE0NeUFPRYdYrRZf7CQ'
        url = 'https://random-data-api.com/api/v3/projects/a2bebcc5-69e3-4b4e-b8c0-4a2f4306f0da'
        data = {
            "api-key": api_key
        }
        r = requests.get(url, json=data)
        _logger.warning(r.status_code)
        _logger.info(r.json())
        if r.status_code == 200:
            self.env['visor.eventos'].create({
                'name': 'Consulta exitosa!',
                'date': datetime.now(),
                'response': r.json(),
                'state': 'OK',
                })
        else:
            self.env['visor.eventos'].create({
                'name': 'Ocurrio un Error!',
                'date': datetime.now(),
                'response': r.json(),
                'state': 'ERROR',
                })