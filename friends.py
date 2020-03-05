episodes_text = "The One After Joey and Rachel Kiss-The One Where Ross is Fine-The One With Ross's Tan-" \
                "The One With the Cake-The One Where Rachel's Sister Babysits-The One With Ross's Grant-" \
                "The One With the Home Study-The One With the Late Thanksgiving-The One With The Birth Mother-" \
                "The One Where Chandler Gets Caught-The One Where The Stripper Cries-The One With Phoebe's Wedding-" \
                "The One Where Joey Speaks French-The One With Princess Consuela-The One Where Estelle Dies-" \
                "The One With Rachel's Going Away Party-The Last One"


episodes = episodes_text.split('-')

Episodes = []
for ep, name in enumerate(episodes):
    Episodes.append(f"{ep+1} - {name}")

EpisodesCopy = Episodes.copy()
cont = 0
for num, ep in enumerate(Episodes):
    EpisodesCopy.insert(num + cont, ep)
    cont += 1


if __name__ == '__main__':
    print(episodes_text)
    print(episodes)
    print(len(episodes))
    print(Episodes)
    print(EpisodesCopy)
    print(len(EpisodesCopy))
    for ep in EpisodesCopy:
        print(ep)
