# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp import http
from openerp.addons.web.http import request


class SurveyExtend(http.Controller):

    @http.route(['/survey_extend/print/<model("survey.survey"):survey>', '/survey_extend/print/<model("survey.survey"):survey>/<string:token>'], type='http', auth="public", website=True)
    def view(self, survey, token=None, **post):
        if survey:
            if token:
                user_input = survey.user_input_ids.search([('token', '=', token)])
                # user_input = http.request.env['survey.user_input'].search([('token', '=', token)])
                pdf = http.request.env['report'].sudo().with_context(set_viewport_size=True).get_pdf(user_input, 'survey_extend.survey_report_user_print')
            else:
                pdf = http.request.env['report'].sudo().with_context(set_viewport_size=True).get_pdf(survey, 'survey_extend.survey_report_print')
            pdfhttpheaders = [('Content-Type', 'application/pdf'),
                              ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        return request.not_found()
