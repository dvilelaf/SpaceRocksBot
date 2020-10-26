from twitterBot import twitterBot
import sys

bots = {'sirius' : {'name'                : 'sirius',
                    'consumer_key'        : "",
                    'consumer_secret'     : "",
                    'access_token'        : "",
                    'access_token_secret' : ""},

        'bender' : {'name'                : 'bender',
                    'consumer_key'        : "",
                    'consumer_secret'     : "",
                    'access_token'        : "",
                    'access_token_secret' : ""},
}

targets = {'tim' : {'userid'   : '552582271',
                    'username' : "astro_timpeake",
                    'tag'      : "#spacerocks.12"}}


if __name__ == '__main__':
    if len (sys.argv) == 3:
        if sys.argv[1] in bots:

            print('Bot ' + bots[sys.argv[1]]['name'] + ' has started tracking user ' + targets[sys.argv[2]]['username'])
            tb = twitterBot(bots[sys.argv[1]], targets[sys.argv[2]])
            tb.track()

    else:
        print('Arguments do not match')

##magic.12 🎵I travel the world and the seven seas...🎵
