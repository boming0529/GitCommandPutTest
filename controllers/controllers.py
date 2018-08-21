# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.web.http import request


class SurveyExtend(http.Controller):
    """extend survey feature"""

    @http.route(['/survey_extend/print/<model("survey.survey"):survey>',
                 '/survey_extend/print/<model("survey.survey"):survey>/<string:token>'],
                type='http', auth="public", website=True)
    def view(self, survey, token=None, **post):
        """print survey to pdf
        Arguments:
            survey {[model]} -- survey.survey model
            **post {[dict]} -- other parameter
        Keyword Arguments:
            token {[string]} -- token for this user_line (default: {None})
        Returns:
            [application/pdf] -- print pdf or http status code 404
        """
        if survey:
            if token:
                user_input = survey.user_input_ids.search(
                    [('token', '=', token)])
                # user_input = http.request.env['survey.user_input'].search([('token', '=', token)])
                pdf = http.request.env['report'].sudo().with_context(set_viewport_size=True).get_pdf(
                    user_input, 'survey_extend.survey_report_user_print')
            else:
                pdf = http.request.env['report'].sudo().with_context(
                    set_viewport_size=True).get_pdf(survey, 'survey_extend.survey_report_print')
            pdfhttpheaders = [('Content-Type', 'application/pdf'),
                              ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        return request.not_found()
