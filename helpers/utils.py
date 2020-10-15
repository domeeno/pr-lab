import json
import csv
from xml.etree import cElementTree as ElementTree

from logs.log import default_logger

DATA = {}
ROW = 0
COLUMNS = []
MIME_TYPE = ['application/xml', 'text/csv', 'application/x-yaml']


def data_collector(data):
    global ROW
    collected_data = {}
    data_json = json.loads(data)

    if 'mime_type' not in data_json:
        DATA.update(data_json)


def select_query(query):
    list_of_values = []
    for values in DATA['data']:
        list_of_values.append(values[query.replace('select ', '')])
    return DATA['data'].encode()


def csv_to_dict(data):
    dictionary_friendly_string = ""
    csv_dict = {}
    values = []

    rows = data.split('\n')

    columns = list(rows[0].split(","))

    for index, row in enumerate(rows):
        if index == 0:
            continue

        values.append(rows[index].split(','))

    index = ROW
    index = index + 1
    dictionary_friendly_string = dictionary_friendly_string + "{" + str(index) + ": "

    del values[-1]
    print(values)
    for index, value in enumerate(values):

        dictionary_friendly_string = dictionary_friendly_string + "{"
        for string, column in zip(value, columns):
            dictionary_friendly_string = dictionary_friendly_string + '"' + column + '": ' + '"' + string + '"' + ', '
        index = index + 1
        if index != len(value) - 1:
            dictionary_friendly_string = dictionary_friendly_string + "}, " + str(index) + ": "
        else:
            dictionary_friendly_string = dictionary_friendly_string + "}"
            break

    dictionary_friendly_string = dictionary_friendly_string + "}"
    print(dictionary_friendly_string)
    return json.loads(dictionary_friendly_string)


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
