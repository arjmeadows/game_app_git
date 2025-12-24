import navigation
import json
from dotenv import load_dotenv
from igdb.wrapper import IGDBWrapper
import os
import config

def igdb(game_name):
        
    wrapper = IGDBWrapper(config.TWITCH_CLIENT_ID, config.TWITCH_TOKEN)
    query = f'fields name, summary, url, platforms.name, involved_companies.company.name, involved_companies.publisher, involved_companies.developer; where name = "{game_name}";'

    try:
        byte_array = wrapper.api_request(
                    'games',
                    query
                )

        igdb_result = json.loads(byte_array)
        return igdb_result[0]
    
    except:
        print(f"{game_name} not found on Internet Game Database")
        navigation.main_menu()


def find_summary(game_name: str):
    result = igdb(game_name)
    summary = result["summary"]
    return summary 


def find_dev(game_name: str):
    result = igdb(game_name)
    for list in result["involved_companies"]:
        for key, value in list.items():
            if key == "developer" and value == True:
                return list["company"]["name"]


def find_publisher(game_name: str):
    result = igdb(game_name)
    for list in result["involved_companies"]:
        for key, value in list.items():
            if key == "publisher" and value == True:
                return list["company"]["name"]


def find_platform(game_name):
    platform_list = ""         
    result = igdb(game_name)
    for list in result["platforms"]:
        for key, value in list.items():
            if key == "name":
                platform_list += f"{value}\n"
    
    return platform_list


def find_url(game_name: str):
    result = igdb(game_name)
    summary = result["url"]
    return summary 

