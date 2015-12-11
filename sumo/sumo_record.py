# -*- coding: utf-8 -*-
import re
import os
import sys
import robotparser #for check a wbe page can be fetched or not
import datetime
import time
import json
from urllib2 import urlopen, Request
from collections import OrderedDict

from lxml import etree

from constants import BASE_URL
from constants import EACH_DAY_URL
from constants import HEADER
from constants import GZIP_HEADER
from constants import WIN_LOSE_TYPE_DICT

dir_name = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_name + '/../')
from py_utils import compress


def save_total_record_json(data):
    # Save info into json file
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    output_dir = 'output/%s/total/' % data['date']
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_dir + date_str + '.json', 'w+') as f:
        doc_str = json.dumps(data)
        f.write(doc_str + '\n')


def save_single_record_json(day, data):
    # Save info into json file
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    output_dir = 'output/%s/day_%s/' % (data['date'], str(day).zfill(2))
    #output_dir = 'output/%s/day_%2d/' % (data['date'], day)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_dir + date_str + '.json', 'w+') as f:
        doc_str = json.dumps(data)
        f.write(doc_str + '\n')


class SumoRecord(object):
    def __init__(self):
        pass


    def printd(self):
        pass


    def get_total_record(self):
        """ Get total record from starting day to now during current season

        Returns:
            OrderedDict: with total record and date

            "record":"9勝6敗",
            "competitor_list":[],
            "win_lose_list":[],
            "name":"鶴竜",
            "rank":"横綱"

        """
        #raw_HTML_data = self.__get_HTML_data(BASE_URL)
        raw_HTML_data = self.__get_gzip_HTML_data(BASE_URL)
        result_data = self.__parse_total_record(raw_HTML_data)
        return result_data


    def get_single_day_record(self, day=1):
        """ Get single day record during current season.

        Args:
            day(int): The

        Returns:

        """
        if day < 1 or day > 15:
            raise ValueError('Day is invalid, day should be 1 to 15')

        url = EACH_DAY_URL % day
        raw_HTML_data = self.__get_gzip_HTML_data(url)
        result_data = self.__parse_single_day_record(raw_HTML_data)
        return result_data


    def __get_HTML_data(self, url):
        """  """
        req = Request(url, None, HEADER)
        page = urlopen(req)
        return page.read()


    def __get_gzip_HTML_data(self, url):
        """  """
        req = Request(url, None, GZIP_HEADER)
        gzip_page = urlopen(req)
        data = compress.ungzip_html(gzip_page)
        return data


    def __parse_total_record(self, web_page_data):
        """  """
        total_record = OrderedDict()

        # Get date
        tree = etree.HTML(web_page_data)
        date = tree.xpath('//*/div[@id="content"]/div[@id="mainContent"]/p[@class="mdDate"]')
        total_record['date'] = date[0].text.strip()

        # Get east result
        east_result = self.__parse_total_record_by_side(tree, True)
        for index in xrange(len(east_result)):
            total_record["E" + str(index+1)] = east_result[index]

        # Get west result
        west_result = self.__parse_total_record_by_side(tree, False)
        for index in xrange(len(west_result)):
            total_record["W" + str(index+1)] = west_result[index]

        return total_record


    def __parse_total_record_by_side(self, xml_tree, is_east=True):
        """  """
        each_elements = None
        if is_east:
            each_elements = xml_tree.xpath('//*/div[@id="east"]/table[@class="main "]/tr')
        else:
            each_elements = xml_tree.xpath('//*/div[@id="west"]/table[@class="main "]/tr')

        result = []
        # Get each player name, rank, and total record with competitor
        for index in xrange(0, len(each_elements), 2):

            single_player_data = {}

            player_info = each_elements[index].xpath('td[@class="player bBnone"]/div/dl')
            record_info = each_elements[index].xpath('td/img')
            competitor_info = each_elements[index+1].xpath('td')

            if len(player_info) == 1:
                info = self.get_retr_list(player_info[0])
                single_player_data['rank'] = info[0]
                single_player_data['name'] = info[1]
                single_player_data['record'] = info[2]

            wb_record = [WIN_LOSE_TYPE_DICT.get(i.get('alt')) for i in record_info]
            single_player_data['win_lose_list'] = wb_record

            # Get competitor info and order
            com_record = [i.text if i.text else "" for i in competitor_info]
            single_player_data['competitor_list'] = com_record

            result.append(single_player_data)

        return result


    def __parse_single_day_record(self, web_page_data):
        """  """
        single_day_record = OrderedDict()

        # Get date
        tree = etree.HTML(web_page_data)
        date = tree.xpath('//*/div[@id="content"]/div[@id="mainContent"]/div[@class="mdSection1"]/p[@class="mdDate"]')
        single_day_record['date'] = date[0].text.strip()

        # Get game result, the first item is label, so ignore it
        game_result = tree.xpath('//*/div[@id="content"]/div[@id="mainContent"]/div[@class="mdSection1"]/table[@class="mdTable1"]/tr')
        parse_result_list = self.__parse_game_result_list(game_result)
        for index in xrange(len(parse_result_list)):
            single_day_record["Game" + str(index+1)] = parse_result_list[index]

        return single_day_record


    def __parse_game_result_list(self, game_result):
        """ """

        parse_result_list = []

        for index in xrange(1, len(game_result)):
            single_basho_data = {}
            each_basho_info = game_result[index].xpath('td')

            # Each basho has five elements.
            # First competitor info, win/lose, winning skill, win/lose, second competitor
            single_basho_data['first_competitor_info'] = self.get_retr_list(each_basho_info[0])
            single_basho_data['first_competitor_result'] = WIN_LOSE_TYPE_DICT.get(each_basho_info[1].xpath('img')[0].get('alt'))
            single_basho_data['winning_skill'] = each_basho_info[2].text
            single_basho_data['second_competitor_result'] = WIN_LOSE_TYPE_DICT.get(each_basho_info[3].xpath('img')[0].get('alt'))
            single_basho_data['second_competitor_info'] = self.get_retr_list(each_basho_info[4])

            parse_result_list.append(single_basho_data)

        return parse_result_list


    @staticmethod
    def get_retr_list(nodes):
        """  """
        return filter(None, [i.strip() for i in nodes.itertext()])



######## Main Start ########
if __name__=="__main__":

    sumo_record = SumoRecord()

    # total_result = sumo_record.get_total_record()
    # save_total_record_json(total_result)

    try:
        day_one_result = sumo_record.get_single_day_record(0)
    except ValueError as err:
        print err

    try:
        day_one_result = sumo_record.get_single_day_record(17)
    except ValueError as err:
        print err

    day_one_result = sumo_record.get_single_day_record(1)
    save_single_record_json(1, day_one_result)

    day_one_result = sumo_record.get_single_day_record(13)
    save_single_record_json(13, day_one_result)

    print "DONE"
