# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import requests
import logging

_logger = logging.getLogger(__name__)

class VisorEventos(models.Model):
    _name="visor.eventos"

    name = fields.Char('Nombre de Servicio')
    date = fields.Datetime('Fecha de ejecución')
    response = fields.Text('Respuesta')
    state = fields.Selection([('OK', 'CORRECTO'),
                              ('ERROR', 'OCURRIO UN ERROR')], string="Estado")