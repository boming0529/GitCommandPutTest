# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from openerp import models, fields, api


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
            IsPrint {[boolean]} -- Is Print pdf or not
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
        if question.type == "matrix_text":
            for row_label in question.labels_ids_2:
                for col_label in question.labels_ids:
                    if '%s_%s_%s' % (answer_tag, row_label.id, col_label.id) in answer:
                        string = str(answer['%s_%s_%s' % (
                            answer_tag, row_label.id, col_label.id)][0])
                        _parent = soup.find('',
                                            {'name': '%s_%s_%s' % (answer_tag, row_label.id, col_label.id)}).parent
                        try:
                            width = soup.find('th', {'data-id': col_label.id})['style'] if \
                                soup.find('th', {'data-id': col_label.id}) else ''
                            if width != '':
                                _parent["style"] = 'word-break: break-all; %s' % (
                                    width)
                            soup.find('',
                                      {'name': '%s_%s_%s' % (answer_tag, row_label.id, col_label.id)}).parent.string = string
                        except:
                            soup.find('',
                                      {'name': '%s_%s_%s' % (answer_tag, row_label.id, col_label.id)}).parent.string = string
                    else:
                        _parent = soup.find('',
                                            {'name': '%s_%s_%s' % (answer_tag, row_label.id, col_label.id)}).parent
                        _parent.string = ''
            try:
                thspan = soup.find('thead').find('tr').find('th')['style']
                for th in soup.find('tbody').find('tr').find_all('th'):
                    th['style'] = thspan
            except:
                thspan = None
        return soup

    @api.multi
    def get_answer(self, ret, answer_tag):
        """get this answer_tag answer
        Arguments:
            ret {[dict]} -- all answer
            answer_tag {[string]} -- mapping current input name
        """
        return {k: v for k, v in ret.items() if answer_tag in k}
