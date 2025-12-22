import requests
import json
from igdb.wrapper import IGDBWrapper


def igdb(game_name):

    wrapper = IGDBWrapper("18jlqn68i6l3ysqlrmttocsa6uw2z5", "nu4t36xcmp2z9q28e607s5mj1tl2wf")
    query = f'fields name, summary involved_companies.company.name, involved_companies.publisher, involved_companies.developer; where name = "{game_name}";'
    byte_array = wrapper.api_request(
                'games',
                query
            )
    igdb_result = json.loads(byte_array)
    print(igdb_result)
    

class WikiGet:
    @staticmethod
    def get_content(game: str):
            
        insert_game = game

        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={insert_game}&rvprop=content&format=json&formatversion=2"

        headers = {
            'User-Agent': 'MyWikiTool/1.0 (YourName@example.com)' 
        }

        response = requests.get(url, headers=headers) 
        data = response.json()

            # dive into content key
        wiki_content = data['query']['pages'][0]['revisions'][0]['content']
        
        return wiki_content

    @staticmethod
    def find_dev(wiki_content: str):

        # look for 'developer' string
        dev_name = wiki_content.find("developer")

        # slice characters from that position until X
        dev_string = wiki_content[dev_name: dev_name + 100]

        # identify position of developer name based on [] in json
        first = dev_string.find("[") + 2
        second = dev_string.find("]")
        new_dev = dev_string[first:second]

        # print(f"Developer: {new_dev}")
        
        return new_dev
    

    @staticmethod
    def find_publisher(wiki_content: str):

            # look for 'developer' string
        pub_name = wiki_content.find("publisher")

            # slice characters from that position until X
        pub_string = wiki_content[pub_name: pub_name + 100]

            # identify position of developer name based on [] in json
        first = pub_string.find("[") + 2
        second = pub_string.find("]")
        new_pub = pub_string[first:second]

        # print(f"Publisher: {new_pub}")
        
        return new_pub
    
    @staticmethod
    def find_platform(wiki_content: str):
            # look for 'developer' string
        plat_name = wiki_content.find("platforms =")

            # slice characters from that position until X
        plat_string = wiki_content[plat_name: plat_name + 100]

            # identify position of developer name based on [] in json
        first = plat_string.find("[") + 2

        second = plat_string.find("]")
        new_plat = plat_string[first:second]

        
        return new_plat
    