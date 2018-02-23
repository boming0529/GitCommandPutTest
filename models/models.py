# -*- coding: utf-8 -*-
import logging
from bs4 import BeautifulSoup
from openerp import models, fields, api
from openerp.addons.survey.controllers.main import dict_soft_update


_logger = logging.getLogger(__name__)


class SurveyExtends(models.Model):
    """extend survey question"""

    _inherit = 'survey.question'

    description_before = fields.Html('Content_before', sanitize=False)
    description_after = fields.Html('Content_after', sanitize=False)
    description_question = fields.Html('Content_question', sanitize=False)

    @api.multi
    def override_render_description(self, question_id, answer_tag, answer):
        """Re-render the HTML of the description
        Decorators:
            api.multi
        Arguments:
            question_id {[int]} -- current question id
            answer_tag {[string]} -- mapping current input name
            answer {[dict]} -- mapping current input value
        Returns:
            [string] -- return Html string
        """

        question = self.search([('id', '=', question_id)])[0]
        soup = BeautifulSoup(question.description_question, 'html.parser')
        ele_input = soup.find(
            '', {'name': answer_tag, 'class': 'form-control'})
        simple_val = str(answer[answer_tag][0]) if answer_tag in answer else ''
        if question.type == 'free_text':
            ele_input.append(BeautifulSoup(simple_val, 'html.parser'))
        if question.type in ('textbox', 'numerical_box', 'datetime'):
            ele_input['value'] = simple_val
        ele_s_input = soup.select("input[name^=" + answer_tag + "]")

        if question.type == 'simple_choice':
            ele_select = soup.select("select[name^=" + answer_tag + "]")
            for item in ele_select:
                if str(item['value']) == simple_val:
                    item.select(
                        'option[value="' + simple_val + '"]')['selected'] = '1'
        if question.type in ('simple_choice', 'multiple_choice'):
            for item in ele_s_input:
                if [x for x in answer[answer_tag] if str(x) == str(item['value'])]:
                    item['checked'] = 'checked'
        if question.type == 'matrix':
            for row_label in question.labels_ids_2:
                for col_label in answer['%s_%s' % (answer_tag, row_label.id)]:
                    soup.find('input',
                              {'name': '%s_%s' % (answer_tag, row_label.id) if
                               question.matrix_subtype == 'simple' else
                               '%s_%s_%s' % (
                                   answer_tag, row_label.id, col_label),
                               'value': col_label})['checked'] = 'checked'
        return soup

    @api.multi
    def get_answer(self, ret, answer_tag):
        """[summary]
        
        Arguments:
            ret {[dict]} -- all answer
            answer_tag {[type]} -- [description]
        """

        return {k: v for k, v in ret.items() if answer_tag in k}


class survey_user_input(models.Model):
    _inherit = 'survey.user_input'

    @api.multi
    def get_the_answer(self, token):
        ret = {}
        ids = self.search([('token', '=', token)])
        for answer in ids.user_input_line_ids:
            if not answer.skipped:
                answer_tag = '%s_%s_%s' % (
                    answer.survey_id.id, answer.page_id.id, answer.question_id.id)
                answer_value = None
                if answer.answer_type == 'free_text':
                    answer_value = answer.value_free_text
                elif answer.answer_type == 'text' and answer.question_id.type == 'textbox':
                    answer_value = answer.value_text
                elif answer.answer_type == 'text' and answer.question_id.type != 'textbox':
                    # here come comment answers for matrices, simple choice and multiple choice
                    answer_tag = "%s_%s" % (answer_tag, 'comment')
                    answer_value = answer.value_text
                elif answer.answer_type == 'number':
                    answer_value = answer.value_number.__str__()
                elif answer.answer_type == 'date':
                    answer_value = answer.value_date
                elif answer.answer_type == 'suggestion' and not answer.value_suggested_row:
                    answer_value = answer.value_suggested.id
                elif answer.answer_type == 'suggestion' and answer.value_suggested_row:
                    answer_tag = "%s_%s" % (
                        answer_tag, answer.value_suggested_row.id)
                    answer_value = answer.value_suggested.id
                elif answer.answer_type == 'matrix_text' and answer.value_suggested_row:
                    answer_tag = "%s_%s_%s" % (
                        answer_tag, answer.value_suggested_row.id, answer.value_suggested.id)
                    answer_value = answer.value_free_text
                if answer_value:
                    dict_soft_update(ret, answer_tag, answer_value)
                else:
                    _logger.warning(
                        "[survey] No answer has been found for question %s marked as non skipped" % answer_tag)
        return ret
