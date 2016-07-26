# -*- coding: utf-8 -*-

import xmltodict


class Parser(object):

    def __init__(self, *args, **kwargs):
        super(Parser, self).__init__()

    @classmethod
    def xml_to_dict(cls, xml_content):
        return dict(xmltodict.parse(xml_content)['xml'])

    @classmethod
    def dict_to_xml(cls, parmas):
        if not isinstance(parmas, dict):
            raise TypeError('params must be dict')

        xml_content = ['<xml>']
        for k, v in parmas.items():
            if k == 'MediaId':
                xml_content.append('<Image><%s>%s</%s></Image>' % (k, v, k))
            elif isinstance(v, int) or v.isdigit():
                xml_content.append('<%s>%s</%s>' % (k, v, k))
            else:
                xml_content.append('<%s><![CDATA[%s]]></%s>' % (k, v, k))

        xml_content.append('</xml>')
        return ''.join(xml_content)
