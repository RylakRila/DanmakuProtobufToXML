# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
from protocol_buffer.dm_pb2 import DmSegMobileReply
from google.protobuf.json_format import MessageToDict

def get_sessdata():
    r"""
    Get the sessdata in the cookie of www.bilibili.com from cookie.json file.
    
    Cookie.json file is required and must store the cookies in json format beforehand.
    """
    
    with open("cookie.json", "r", encoding="utf-8") as temp:
        bili_cookies = json.load(temp)
    
    # search for the sessdata, make its name and value same as a string with format of http request header of cookie, and return it
    for cookie in bili_cookies:
        if cookie['name'] == "SESSDATA":
            header_cookie = f"{cookie['name']}={cookie['value']};"
            break
        
    return header_cookie

def dm_history(oid, date):
    r"""
    get and translate the seg.so binary file to a list of dictionary and return it. 
    
    oid: 
        the cid of the video of which you want the danmaku in www.bilibili.com
    
    date: 
        the date of the danmaku history
    """
    # url to get the seg.so binary file of history danmaku
    url_history=f"https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={oid}&date={date}"
    
    # get the sessdata of cookie in http header format
    header_cookie = get_sessdata()
    
    # set the header dictionary for http request
    headers = {
        'cookie': header_cookie
    }
    
    # Send a GET request to history danmaku url with correct cookie info in header
    bili_response = requests.get(url_history, headers=headers)
    
    # the binary file retrieve from history danmaku url needs to be converted to human readable message using related protocol buff methods 
    DM = DmSegMobileReply()
    DM.ParseFromString(bili_response.content)
    
    #convert protobuf message to a dictionary
    data_dict = MessageToDict(DM)
    return data_dict['elems']

def dm_list_to_xml(dm_list:list, oid, date):
    r"""
    Convert dictionaries of danmaku information in the list to xml file.
    
    dm_list:
        the list of dictionary of danmaku information returned by dm_history() function.
    
    oid:
        the cid of the video of which you want the danmaku in www.bilibili.com. It will be part of the name of final xml file. 
    
    date:
        the specific date of the history danmaku in www.bilibili.com. It will be part of the name of final xml file.
    """
    # basic xml information of danmaku
    pre_info = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    i_tag = "<i>\n</i>"
    chat_server = "<chatserver>chat.bilibili.com</chatserver>"
    chat_id = f"<chatid>{oid}</chatid>"
    
    # make output folder
    if not os.path.exists("output"):
        os.mkdir("output")
    
    # converting part
    with open(f"output/{oid}.{date}.xml", "w", encoding="utf-8") as xml_file:
        xml_file.write(f"{pre_info}{i_tag}") # write basic information of xml file and <i></i> tag
    
    with open(f"output/{oid}.{date}.xml", "r+", encoding="utf-8") as xml_file:
        contents = xml_file.readlines() # read the lines in the xml file and return it as a list called 'contents'
        contents[0] = contents[0][:-1] # cut the link breaker behind the <i> tag in the purpose of formatting
        contents.insert(-1, chat_server) # insert other basic informations before the last elements of the list
        contents.insert(-1, chat_id) # same as above
        
        '''
        A for loop iterating each dictionary in the danmaku list. Retrieve values in the dictionary and append them to a string storing previous bilibili xml <d> tag, which means danmaku. Insert these strings before the last elements of contents list. 
        
        Because the “pool” information would not appear in the danmaku information dictionary except that it's on the subtitle pool or special pool for sure, a condition ternary operator is implemented in the position of pool information. 
        Same for the progress, color information.
        '''
        for dm_dict in dm_list:
            dm_line = f"<d p=\"" +\
                f"{(dm_dict['progress'] / 1000) if (dm_dict.__contains__('progress')) else '0.00000'}," +\
                f"{dm_dict['mode']},{dm_dict['fontsize']}," +\
                f"{dm_dict['color'] if (dm_dict.__contains__('color')) else '0'}," +\
                f"{dm_dict['ctime']}," +\
                f"{dm_dict['pool'] if (dm_dict.__contains__('pool')) else '0'}," +\
                f"{dm_dict['midHash']},{dm_dict['id']}\">" +\
                f"{dm_dict['content']}</d>"
            
            contents.insert(-1, dm_line)
    
    # overwrite the xml with every elements in the list seperated by line breaks
    with open(f"output/{oid}.{date}.xml", "w", encoding="utf-8") as xml_file:    
        xml_file.write("\n".join(contents))

if __name__ == '__main__':
    oid = sys.argv[1]
    date = sys.argv[2]
    dm_list = dm_history(oid, date)
    dm_list_to_xml(dm_list, oid, date)
    