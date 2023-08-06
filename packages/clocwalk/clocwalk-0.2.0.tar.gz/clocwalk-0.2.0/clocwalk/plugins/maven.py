# coding: utf-8

import os
import glob
import requests

from xml.etree import ElementTree
from lxml import html

from clocwalk.lib.data import logger

__product__ = 'Java'
__version__ = '0.2'

WHITE_LIST = [
    'global', 'project.build.sourceEncoding'
]
NAMESPACES = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}


def _get_properties(xml_doc):
    """
    get properties
    :param xml_doc:
    :return:
    """
    result = {}
    prop_list = xml_doc.find(".//xmlns:properties", namespaces=NAMESPACES)

    if prop_list is not None:
        for item in prop_list:
            name = item.tag
            name = name.replace('{http://maven.apache.org/POM/4.0.0}', '')
            value = item.text.strip() if item.text else ''
            result[name] = value
    return result


def _get_maven_version(groupId, artifactId, timeout):
    """
    get new version
    :param groupId: com.thetransactioncompany
    :param artifactId: cors-filter
    :param timeout:
    :return:
    """
    result = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    try:
        logger.debug('Start checking the latest version of {0}/{1} ...'.format(groupId, artifactId))
        if groupId and artifactId:

            xpath_list = [
                '//*[@id="maincontent"]/div[4]/table/tbody[1]/tr/td[2]/a',
                '//*[@id="maincontent"]/div[5]/table/tbody[1]/tr[1]/td[2]/a',
                '//*[@id="snippets"]/div/div/div/table/tbody[1]/tr[1]/td[1]/a',
                '//*[@id="snippets"]/div/div/div/table/tbody[1]/tr[1]/td[2]/a',
            ]

            url = 'https://mvnrepository.com/artifact/{0}/{1}'.format(groupId, artifactId)
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                dom = html.fromstring(resp.text)
                for item in xpath_list:
                    try:
                        ele_version = dom.xpath(item)[0]
                        result = ele_version.text
                        break
                    except:
                        result = ''

    except Exception as ex:
        logger.warning(ex)

    return result


def _get_dependencies(xml_doc, relative_path_file='pom.xml', skipNewVerCheck=False, timeout=5, tag_filter=[]):
    """

    :param xml_doc:
    :param relative_path_file:
    :param skipNewVerCheck:
    :return:
    """

    def _get_ele_text(ele):
        try:
            result = ele.text
            if result.startswith('$'):
                pass
            return result
        except:
            return ''

    result = []
    deps = xml_doc.findall(".//xmlns:dependencies", namespaces=NAMESPACES)

    if deps is not None:
        properties_list = _get_properties(xml_doc)
        for item in deps:
            for dependency in item.getchildren():
                # print item.tag, item.text, item.tail
                artifactId = dependency.find("xmlns:artifactId", namespaces=NAMESPACES)
                version = dependency.find("xmlns:version", namespaces=NAMESPACES)
                tag = dependency.find("xmlns:groupId", namespaces=NAMESPACES)
                if tag is not None and (_get_ele_text(tag).startswith('${')):
                    continue
                ver = _get_ele_text(version)
                if ver and ver.startswith('${'):
                    k = ver.replace('${', '').replace('}', '')
                    if k in properties_list:
                        ver = properties_list[k]
                    else:
                        # TODO
                        pass
                if not skipNewVerCheck:
                    new_version = _get_maven_version(_get_ele_text(tag), _get_ele_text(artifactId), timeout)
                else:
                    new_version = ''
                _tag = _get_ele_text(tag)
                if _tag in tag_filter:
                    continue
                result.append({
                    'name': _get_ele_text(artifactId),
                    'version':  ver,
                    'tag':  _tag,
                    'origin': relative_path_file,
                    'parent_origin': '',
                    'new_version': new_version
                })

    return result


def start(**kwargs):
    """
    :param kwargs:
    :return:
    """
    code_dir = kwargs.get('code_dir', '')
    file_name = kwargs.get('file_name', 'pom.xml')
    skipNewVerCheck = kwargs.get('skipNewVerCheck', False)
    tag_filter = kwargs.get('tag_filter', [])
    timeout = kwargs.get('timeout', 3)

    properties = []

    result_file_list = glob.glob(os.path.join(code_dir, file_name)) + \
        glob.glob(os.path.join(code_dir, '**', file_name)) + \
        glob.glob(os.path.join(code_dir, '*', '*', file_name)) + \
        glob.glob(os.path.join(code_dir, '*', '*', '*', file_name))

    result = []

    for item in result_file_list:

        # FIXME
        relative_path = item.replace('{0}'.format(code_dir), '')
        relative_path = relative_path[1:] if relative_path.startswith('/') else relative_path

        tree = ElementTree.parse(item)
        doc_root = tree.getroot()
        reVal = _get_dependencies(doc_root, relative_path, skipNewVerCheck, timeout, tag_filter)

        if 'pom.xml' == relative_path:  # root
            properties = _get_properties(doc_root)
        result.extend(reVal)


    for item in result:
        if not item['version'] or item['version'].startswith('${'):
            version_key = item['version'].replace('${', '').replace('}', '')
            if version_key in properties:
                item['version'] = properties[version_key]
                item['parent_origin'] = 'pom.xml'


    return result

