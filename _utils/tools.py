from bs4             import BeautifulSoup
from my_tables       import ark_server_rcon
from my_tables.base  import Session
from rcon            import select_data
import _utils
import requests

url_battlemetrics = "https://www.battlemetrics.com/servers/ark/"

session = Session()

def get_status_servers(p_id_link_server):

    proxies  = {"http:":"131.161.105.42"}

    r = requests.get(url_battlemetrics + p_id_link_server, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')

    server_title = soup.find_all('h2')
    server_title = list(list(server_title)[0])[0]

    list_return = soup.find_all(class_='col-md-6 server-info')
    table_exit = list(list_return)[0]
    tags = list(table_exit)[1]

    server_rank = str(list(tags)[1])
    server_rank = server_rank.replace("<dd>#", "")
    server_rank = server_rank.replace("</dd>", "")

    players_online = str(list(tags)[3])
    players_online = players_online.replace("<dd>", "")
    players_online = players_online.replace("</dd>", "")

    server_address = str(list(tags)[5])
    server_address = server_address.replace("<dd>", "")
    server_address = server_address.replace("</dd>", "")
    server_address = server_address.replace("<!-- -->", "")
    server_address = server_address.replace("<br/>", "")
    x = server_address.find("(Game Port)")
    y = server_address.find("(Query Port)")
    server_address = server_address[x+11:y-1]

    server_status = str(list(tags)[7])
    server_status = server_status.replace("<dd>", "")
    server_status = server_status.replace("</dd>", "")

    table_exit = list(list_return)[0]
    tags = list(table_exit)[2]
    table_exit_2 = list(tags)[0]

    server_map = list(list(table_exit_2)[1])[0]
    day_of_server = list(list(table_exit_2)[3])[0]
    official_server = list(list(table_exit_2)[5])[0]
    mods_table = list(list(table_exit_2)[7])[0]
    #mods_count = list(list(mods_table)[0])[0]

    #mods_list = list(mods_table)[1]

    server_details =                  "\n```     Server Title: " + server_title
    server_details = server_details + "\n              Rank: " + server_rank
    server_details = server_details + "\n    Players online: " + players_online
    server_details = server_details + "\n    Server Address:" + server_address
    server_details = server_details + "\n            Status: " + str(server_status)
    server_details = server_details + "\n               Map: " + server_map
    server_details = server_details + "\n       In-game Day: " + day_of_server
    server_details = server_details + "\n   Official Server: " + official_server
    #server_details = server_details + "\n        Mods Count: " + mods_count

    #cont = 1
    #for x in mods_list:
    #    server_details =server_details+"\n           Mod " + str(cont) + ": " + x.text
    #    cont += 1

    server_details = server_details + "```"
    
    return server_details

if __name__ == '__main1__':
    id_link_server = ["3571188", "3571191", "3527688", "3527628", "3572561", "3527689", "3527629", "3527632"]

    status = ''
    for x in id_link_server:
        status = get_status_servers(x)
        if status.find("online") > 0:
            status = status.replace("online", ":white_check_mark:online")
        else:
            status = status.replace("offline", ":no_entry:offline")
    