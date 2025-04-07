# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import requests
import logging
from datetime import datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class MovieMovie(models.Model):
	_name = 'movie.movie'
	_description = 'Ranking de Peliculas'
	_rec_name = 'movie_title'
	_order = 'ranking_movie'

	movie_title = fields.Char("Título")
	ranking_movie = fields.Integer('Ranking')

	def _cron_consume_api_movie(self):
		if not self.env['ir.config_parameter'].get_param('movies.cl_url_api'):
			self.env['visor.eventos'].create({
				'name': 'ERROR EN CONFIGURACION DE API',
				'date': datetime.now(),
				'response': "NO SE HA INGRESADO LA URL DE LA API A CONSUMIR, COMPLETE LA CONFIGURACION EN AJUSTES PARA REALIZAR EL CONSUMO",
				'state': 'ERROR',
				})
		url = self.env['ir.config_parameter'].get_param('movies.cl_url_api')
		if not self.env['ir.config_parameter'].get_param('movies.cl_api_key'):
			self.env['visor.eventos'].create({
				'name': 'ERROR EN CONFIGURACION DE API',
				'date': datetime.now(),
				'response': "NO SE HA INGRESADO EL API KEY PARA CONSUMIR EL SERVICIO, COMPLETE LA CONFIGURACIÓN EN AJUSTES PARA REALIZAR EL CONSUMO.",
				'state': 'ERROR',
				})
		api_key = self.env['ir.config_parameter'].get_param('movies.cl_api_key')
		params = {
			'api_key': api_key
		}
		r = requests.get(url, params=params)
		if r.status_code == 200:
			json = r.json()
			if not isinstance(json, dict):
				if not isinstance(json, list):
					for line in json:
						if self.env['movie.movie'].search_count([('movie_title', '=', line['movie_title']), ('ranking_movie', '=', int(line['ranking_movie']))], limit=1):
							self.env['visor.eventos'].create({
								'name': 'Hay conexión a API, no se pudo crear pelicula en sistema.',
								'date': datetime.now(),
								'response': 'La Pelicula ya existe en el sistema. respuesta de consumo: %s' % r.json(),
								'state': 'ERROR',
								})
						else:
							movie = self.env['movie.movie'].create({
								'movie_title': line['movie_title'],
								'ranking_movie': int(line['ranking_movie'])
							})
							if movie:
								self.env['visor.eventos'].create({
									'name': 'Consulta exitosa!',
									'date': datetime.now(),
									'response': r.json(),
									'state': 'OK',
									'movie_id': movie.id,
									})
							else:
								self.env['visor.eventos'].create({
									'name': 'Hay conexión a API, no se pudo crear pelicula en sistema.',
									'date': datetime.now(),
									'response': 'Ocurrio un error al crear la pelicula en el sistema. respuesta de consumo: %s' % r.json(),
									'state': 'ERROR',
									})
				else:
					self.env['visor.eventos'].create({
						'name': 'Hay conexión a API, error de datos',
						'date': datetime.now(),
						'response': 'El tipo de dato de la respuesta no es soportado. respuesta de consumo: %s' % r.json(),
						'state': 'ERROR',
						})
			else:
				if self.env['movie.movie'].search_count([('movie_title', '=', json['movie_title']), ('ranking_movie', '=', int(json['ranking_movie']))], limit=1):
					self.env['visor.eventos'].create({
						'name': 'Hay conexión a API, no se pudo crear pelicula en sistema.',
						'date': datetime.now(),
						'response': 'La Pelicula ya existe en el sistema. respuesta de consumo: %s' % r.json(),
						'state': 'ERROR',
						})
				else:
					movie = self.env['movie.movie'].create({
						'movie_title': json['movie_title'],
						'ranking_movie': int(json['ranking_movie'])
					})
					if movie:
						self.env['visor.eventos'].create({
							'name': 'Consulta exitosa!',
							'date': datetime.now(),
							'response': r.json(),
							'state': 'OK',
							'movie_id': movie.id,
							})
					else:
						self.env['visor.eventos'].create({
							'name': 'Hay conexión a API, no se pudo crear pelicula en sistema.',
							'date': datetime.now(),
							'response': 'Ocurrio un error al crear la pelicula en el sistema. respuesta de consumo: %s' % r.json(),
							'state': 'ERROR',
							})			
		else:
			self.env['visor.eventos'].create({
				'name': 'Ocurrio un Error! Status_code %s' % r.status_code,
				'date': datetime.now(),
				'response': r.json(),
				'state': 'ERROR',
				})