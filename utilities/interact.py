

def checkInput(tocontinue, tocancel):
    given = '****'
    while given != tocontinue and given != tocancel: 
        given = input(f'Continue ({tocontinue}) or Abort ({tocancel})')
    if given == tocancel:
        print('Killing program')
        exit()
    if given == tocontinue:
        print('continuing program')
        return True