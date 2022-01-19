import random
import turtle
import requests

T = turtle.Turtle()
WORD = requests.get('https://www.mit.edu/~ecprice/wordlist.10000')
N = random.randint(1, 10000)
WRONG_GUESSES = 0           # counter: how many wrong guesses the player has accumulated
GUESSES = []                # list containing all the wrong guesses the player made. Allows player to guess again if they already guessed the wrong letter without losing another point.
GOOD_GUESSES = []           # list containing all the good guesses the player has made. Allows player to guess again if they already guesses that letter.


# Drawing hangman
def circle():
    T.circle(30)
    T.pu()

def body():
    T.rt(270)
    T.pd()
    T.fd(200)


def right_arm():
    T.goto(-50,-100)
    T.lt(45)
    T.fd(60)

def left_arm():
    T.goto(-50,-100)
    T.rt(90)
    T.fd(60)
    T.pu()

def right_leg():
    T.goto(-50,-200)
    T.pd()
    T.rt(290)
    T.fd(60)

def left_leg():
    T.goto(-50,-200)
    T.rt(40)
    T.fd(60)

def box():
    T.pu()
    T.goto(-200,-200)
    T.pd()
    T.fd(100)
    T.rt(90)
    T.fd(50)
    T.rt(90)
    T.fd(100)
    T.rt(90)
    T.fd(50)
    T.rt(90)
    T.fd(50)
    T.lt(90)
    T.fd(200)
    T.rt(90)
    T.fd(100)
    T.rt(180)


def word_selection(n, word):
    # API connection that iterates through each line of the webpage
    # Stores each line in a list
    lst = []
    for i in word.iter_lines():
        lst += [i]

    if len(lst[n].decode('UTF-8')) < 3:
        n = random.randint(1, 10000)
    return list(lst[n].decode('UTF-8'))
SELECTION = word_selection(N, WORD)
CORRECT_GUESSES = list(len(SELECTION) * "_")    # displays all the correct guesses to players. Initilialized to start with the same amount of underscores as the length of the word.
print(' '.join(CORRECT_GUESSES))
LETTER = input(str('Please pick a lower case letter: '))


# define correct letters by using a set
def cl_set(function):
    return set(function)
CORRECT = cl_set(SELECTION)

# adds correct letters in proper order, leaving unguessed letters as '_'
def correct_letter(letter, selection, correct, correct_guesses, good_guesses):
    good_guesses.append(letter)
    correct.remove(letter)
    index = []
    for i in range(len(selection)):
        if selection[i] == letter:
            index.append(i)
    for i in index:
        correct_guesses[i] = letter
    correct_guesses = ' '.join(correct_guesses)
    print(correct_guesses)
    correct_guesses = list(correct_guesses.replace(' ',''))
    index.clear()

# draw hangman after each wrong guess
def hangman(wrong_guesses):
    if wrong_guesses == 1:
        circle()
    elif wrong_guesses == 2:
        body()
    elif wrong_guesses == 3:
        right_arm()
    elif wrong_guesses == 4:
        left_arm()
    elif wrong_guesses == 5:
        right_leg()
    elif wrong_guesses == 6:
        left_leg()


def win_lose(letter, selection, correct, correct_guesses, good_guesses, wrong_guesses, guesses):
    while wrong_guesses != 6:
        if len(letter) > 1 or (chr(97) > letter > chr(122)):
            if letter == ''.join(selection):
                print('You guessed the word!')
                break
            else:
                letter = input(str('Please pick a lower case letter: '))

        if letter not in selection:
            if letter in guesses:
                letter = input(str("You\'ve already picked that letter! Pick again: "))
            if letter not in guesses:
                wrong_guesses += 1
                guesses.append(letter)
                hangman(wrong_guesses)
                if wrong_guesses == 6:
                    print("You lost... The word was", ''.join(selection), ".")
                    break
                letter = input(str('Not correct, guess again: '))

        elif letter in good_guesses:
            letter = input(str('You\'ve already picked that letter! Pick again: '))

        if letter in correct:
            correct_letter(letter, selection, correct, correct_guesses, good_guesses)
            if len(correct) == 0:
                print('You guessed the word!')
                break
            else:
                letter = input(str('Nice! What\'s your next pick?: '))

def main():
    box()
    win_lose(LETTER, SELECTION, CORRECT, CORRECT_GUESSES, GOOD_GUESSES, WRONG_GUESSES, GUESSES)

main()

# SOURCES:
    # list of words: https://www.mit.edu/~ecprice/wordlist.10000
    # inter_lines(): https://docs.python-requests.org/en/master/user/advanced/?highlight=iter_lines
    # decoding bytes to strings: https://www.studytonight.com/post/significance-of-prefix-b-in-a-string-in-python
    # turtle module: https://realpython.com/beginners-guide-python-turtle/
    # turtle methods: https://docs.python.org/3/library/turtle.html
