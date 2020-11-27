from ankiconnectTest import invoke
import argparse
import csv

def getDeckInfo(deck):
    if deck not in invoke('deckNames'):
        return None, None

    deckID = invoke('deckNamesAndIds')[deck]
    query = 'deck:'+deck
    deckSize = len(invoke('findCards', query=query))

    return deckID, deckSize
    
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--deck', 
                    help='deck name',
                    action='store')

parser.add_argument('-a', '--action', 
                    help='what do you want to do?',
                    choices=['add', 'addcsv'])

parser.add_argument('-t', '--tag',
                    help='if adding a csv, assign 1 tag to all cards',
                    action='store')

parser.add_argument('-i', '--info',
                    help='get info on deck(s)',
                    action='store')

args = parser.parse_args()

if args.info:
    if args.info == 'all':
        args.info = invoke('deckNames')
    else:
        args.info = [args.info]
    for deck in args.info:
        deckID, deckSize = getDeckInfo(deck)
        print('Deck Name: {}'.format(deck))
        print('Deck ID: {}'.format(deckID))
        print('Deck Size: {}'.format(deckSize))

if args.action == 'add':
    if args.deck in invoke('deckNames'):
        while True:
            cardFront = input('Front of card: ')
            if cardFront == 'q' or cardFront == 'quit': break
            cardBack  = input('Back of card: ')
            if cardBack == 'q' or cardFront == 'quit': break
            
            print('Confirm add to {0}?'.format(args.deck))
            confirm = input('y/n/f/b: ')
            while confirm != 'y':
                if confirm == 'n': break
                if confirm == 'f': cardFront = input('Front of card: ')
                elif confirm == 'b': cardBack = input('Back of card: ')
                print('Confirm add to {0}?'.format(args.deck))
                confirm = input('y/n/f/b: ')

            if confirm == 'y':
                cardID = invoke('addNote', note= {           
                        "options": {"allowDuplicate": False},
                        'deckName':args.deck, 'modelName':'Basic',
                        'fields': {'Front':cardFront, 'Back':cardBack},
                        'tags':[]
                        }                       
                    )
                
                print(cardID)

    else: print('{} is not a deck'.format(args.deck))
    
elif args.action == 'addcsv':
    if args.deck in invoke('deckNames'):
        # if csv file in os.path:
        csv_name = 'C:/Users/sludj/Documents/notes/offline/ankify.csv'

        tags = [args.tag] if args.tag else []
        with open(csv_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #for row in csv_reader: print(row)
            for front, back in csv_reader:
                cardID = invoke('addNote', note= {           
                    "options": {"allowDuplicate": False},
                    'deckName':args.deck, 'modelName':'Basic',
                    'fields': {'Front':front, 'Back':back},
                    'tags':tags
                    }                       
                )
                print(cardID)
            print('Successfully added cards.')
        

