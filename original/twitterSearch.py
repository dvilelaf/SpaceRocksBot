#!/usr/bin/python3

from musicXmatch import musicXmatch

lyrics = ["A fire a fire, you can only take what you can carry", \
          "All through the magic up here in the night sky", \
          "I'm a shooting star leaping through the skies", \
          "Picture yourself by a rocket. Picture yourself in a glittering silver suit. Picture yourself getting on it.", \
          "Ziggy, Benny and the Jets, take a rocket. We just gotta fly!", \
          "Look out your window I can see his light, if we can sparkle he may land tonight", \
          "And I've been waiting for this moment for all my life.", \
          "And you wake up in the morning, and your head feels twice the size", \
          "And when you wake up, it's a new morning. The sun is shining, it's a new morning", \
          "And all those stars that shine above you, will kiss you every night", \
          "I travel the world and the seven seas"]

songs = [["Snow Patrol", "If there's a rocket tie me to it"], \
         ["Andy Burrows", "Light the Night"], \
         ["Queen", "Don't stop me now"], \
         ["Kaiser Chiefs", "Meanwhile Up In Heaven"], \
         ["Deff Lepard", "Rocket"], \
         ["David Bowie", "Starman"], \
         ["Phil Collins", "In the air tonight"], \
         ["Amy MacDonald", "This is the life"], \
         ["Gerry Rafferty", "Baker Street"], \
         ["INXS", "Mystify"], \
         ["Eurythmics", "Sweet Dreams (Are made of this)"]]

mm = musicXmatch()


for i in range(len(lyrics)):
    print(songs[i][0] + ' - ' + songs[i][1])
    print(mm.get_song_by_lyrics(lyrics[i]))
