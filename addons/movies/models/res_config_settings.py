# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cl_url_api = fields.Char("URL API", config_parameter='movies.cl_url_api')
    cl_api_key = fields.Char("API KEY", config_parameter='movies.cl_api_key')