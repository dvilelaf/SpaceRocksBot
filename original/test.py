from musicXmatch import musicXmatch

mm = musicXmatch()

lyrics = "Tonight I'm gonna have myself a real good time"


song_list = mm.get_song_list_by_lyrics(lyrics)

print('Select one of the following options: ')

for i in range(len(song_list)):
    print('[{:>2}'.format(i) + '] : ' + song_list[i][1] + ' by ' + song_list[i][0])

option = ''

while option is '' :
    inp = input('\n>> ')
    if inp:
        option = int(inp)
        if option >= len(song_list):
            option = ''

    if option is '':
        print("Please select a valid option")


print(type(option))
print(option)
