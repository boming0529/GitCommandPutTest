# -*- coding: utf-8 -*-

from openerp import models, fields, api


class survey_extends(models.Model):
    _inherit = 'survey.question'

    # Mytest
    description_before = fields.Html('Content_before')
    description_after = fields.Html('Content_after')