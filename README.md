# SpaceRocksBot
A very simple Twitter bot written in Python that guesses song names and artists from lyrics inside tweets.

This bot participated in the [Space Rocks contest](https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Principia/spacerocks) organized by the European Space Agency in 2015-2016 and [won](https://twitter.com/esaoperations/status/693092778310516737?s=20) one of the patches (#12).

![patch](https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2015/10/spacerocks_patch/15641423-1-eng-GB/SpaceRocks_patch_pillars.jpg)

Basically, the astronaut Tim Peake would tweet some lyrics from a song of his choice. The first person to guess the song and reply to his tweet in the format "Artist - Song #spacerocks" would get one of the 75 patches. This bot [won](https://twitter.com/esaoperations/status/693092778310516737?s=20) number 12.

The bot would listen to Tim's Twitter Feed, analyze new tweets looking for the #spacerocks hashtag, strip the lyrics down and use MusixMatch API to get a list of candidate songs. Then, it would reply to Tim's tweet in the needed format, with a 0.5 second delay to avoid raising suspicions.

Included is the original version, which is a quick-and-dirty one from a total Python newbie (I do not recommend trying to make much sense of it), and a posterior rewrite in a few lines of code.