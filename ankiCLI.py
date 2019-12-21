from ankiconnectTest import invoke
import argparse

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
                    choices=['add','remove', 'changeVariables'])

parser.add_argument('-i', '--info',
                    help='get info on deck(s)',
                    action='append')

args = parser.parse_args()

if args.info:
    for deck in args.info:
        deckID, deckSize = getDeckInfo(deck)
        print('Deck Name: {}'.format(deck))
        print('Deck ID: {}'.format(deckID))
        print('Deck Size: {}'.format(deckSize))

if args.action == 'add':
    if args.deck:
        while True:
            cardFront = input('Front of card: ')
            if cardFront == 'q' or cardFront == 'quit': break
            cardBack  = input('Back of card: ')
            if cardBack == 'q' or cardFront == 'quit': break
            
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

elif args.action == 'changeVariables':
    if args.deck:
        if args.deck == 'all':
            pass
        else:          
            query = 'deck:'+args.deck
            cardIDS = invoke('findCards', query=query)
        for card in invoke('cardsInfo', cards=cardIDS):
            if '[fmla]' in card['answer'] and '[\fmla]' in card['answer']:
                pass
