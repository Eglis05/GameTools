import requests

top_amount = 71

if __name__ == "__main__":
    link = "https://technotal.com/shinobi_warfare/ranking-arena.php"
    webp = requests.get(link).text
    players = []
    for i in range(1, top_amount + 1):
        if i > 1 and i % 20 == 1:
            link = "https://technotal.com/shinobi_warfare/ranking-arena.php?page=" + str(i//20)
            webp = requests.get(link).text

        i_player_str = "<td>" + str(i) + "</td>"
        i_player = webp.find(i_player_str) + len(i_player_str)

        end_str = "</span>"
        end = webp.find(end_str, i_player)

        start_str = "'>"
        start = webp.find(start_str, i_player) + len(start_str)

        player_i = webp[start: end]
        players.append(str(i) + ": " + player_i)
    print(len(players))
    print(players)
