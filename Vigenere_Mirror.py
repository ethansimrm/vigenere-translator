"""
Vigenère Encoder and Decoder with GUI

Written by Ethan Sim
"""

import tkinter

##Dictionary

alpha_num = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9, "K":10, "L":11, "M":12, "N":13, 
             "O":14, "P":15, "Q":16, "R":17, "S":18, "T":19, "U":20, "V":21, "W":22, "X":23, "Y":24, "Z":25}

#Creating this list to save memory when looking up values
alphabet_list = list(alpha_num.keys())

#Helper function to prep plaintext, ciphertext and key for encoding, decoding and keystring building respectively

def message_prepper(message):
    """
    Takes in a string message, and returns a string message_copy, which has no whitespace and is all uppercase.
    """
    message_copy = str(message)
    message_copy = message_copy.replace(" ","") #If we want to preserve spaces, we can add a Boolean flag (but we must strip spaces for keys)
    #Strip punctuation
    message_copy = message_copy.replace("(","").replace(")", "").replace(".", "").replace(",","").replace("'", "").replace('"', "").replace("?", "").replace(":", "").replace("-", "")
    message_copy = message_copy.upper()
    return message_copy         

#Helper function to build a keystring 

def keystring_builder(key, message_length):
    """
    Takes as input a string key and integer message_length, and returns a string keystring.
    """   
    #We need to remove any whitespace from the key
    key_copy = message_prepper(key)    
    #Depending on the length of the plaintext, build the keystring accordingly
    if len(key_copy) > message_length:
        keystring = key_copy[:message_length]
    elif len(key_copy) == message_length:
        keystring = str(key_copy) 
    else:
        keystring = str(key_copy) #Don't mutate the input
        key_letter = 0 
        for letter_idx in range(message_length - len(key_copy)): #This is the number of letters you need to add to make the keystring the same length as the plaintext
            keystring += key_copy[key_letter % len(key_copy)] #As we iterate through the characters, this will go from 0 to len(key) - 1, and back to 0, allowing us to generate our keystring
            key_letter += 1
    return keystring.upper()

##Create a function which can do both encoding and decoding

#First, initialise our encoder and decoder dictionaries - we use this because it's faster to look stuff up in a dictionary - and we will be doing a lot of looking.

encoder_dict = {0:"Plaintext", 1:"encode", 2:"encoded", 3:1}

decoder_dict = {0:"Ciphertext", 1:"decode", 2:"decoded", 3:-1}

#Second, initialise our master dictionary, flag_dict - this will point to both dictionaries above.

flag_dict = {"encode":encoder_dict, "decode":decoder_dict}

#Let's combine both functions into one, using the generic name "message" to replace ciphertext and plaintext.

def basic_vigenere_translator(message, key, flag):
    """
    Takes as input three strings, message, key, and flag, encodes or decodes via the Vigenère method depending on flag, and returns a string output.
    """
    #Sanity checks
    if flag != "encode" and flag != "decode":
        return "ERROR: Flag must either be 'encode' or 'decode'!"
    elif not isinstance(message, str):
        return "ERROR: " + flag_dict[flag][0] + " must be a string!"
    elif not isinstance(key, str):
        return "ERROR: Key must be a string!"
    elif len(key) == 0: #No key means no encoding or decoding
        return message_prepper(message)
    
    #Prepare message for encoding or decoding
    message_copy = message_prepper(message)
    
    #Prepare keystring for encoding or decoding
    keystring = keystring_builder(key, len(message_copy))
    
    #Initialise a pointer which runs across both message_copy and keystring, and encode or decode accordingly
    output = ""
    for idx in range(len(message_copy)):
        if message_copy[idx] not in alphabet_list:
            return "ERROR: I can't " + flag_dict[flag][1] + " this character: " + message_copy[idx] + "\nYour " + flag_dict[flag][2] + " message thus far is: " + output
        elif keystring[idx] not in alphabet_list:
            return "ERROR: You can't use this character in your key: " + keystring[idx] + "\nYour " + flag_dict[flag][2] + " message thus far is: " + output
        else:
            output_letter_code = (alpha_num[message_copy[idx]] + alpha_num[keystring[idx]] * flag_dict[flag][3]) % 26
            output += alphabet_list[output_letter_code]
    return output

##Testing Suite

def test_vigenere(translator_function):
    """
    This will run our Vigenère translator (translator_function) against a selection of varying inputs, and compare the outputs to a model answer.
    """
    
    #Assess edge cases first
    assert translator_function("","","") == "ERROR: Flag must either be 'encode' or 'decode'!", "Test 1 failed: input '', '', ''"
    assert translator_function(123, "", "encode") == "ERROR: Plaintext must be a string!", "Test 2 failed: input 123, '', 'encode'"
    assert translator_function("", 123, "encode") == "ERROR: Key must be a string!", "Test 3 failed: input '', 123, 'encode'"
    assert translator_function("test", "", "encode") == "TEST", "Test 4 failed: input 'test', '', 'encode'"
    assert translator_function("", "testkey", "encode") == "", "Test 5 failed: input '', 'testkey', 'encode'"
    assert translator_function(123, "", "decode") == "ERROR: Ciphertext must be a string!", "Test 6 failed: input 123, '', 'decode'"
    assert translator_function("fake_plaintext", "testkey", "encode") == "ERROR: I can't encode this character: _\nYour encoded message thus far is: YECX", "Test 7 failed: input 'fake_plaintext', 'testkey', 'encode'"
    assert translator_function("fake_plaintext", "f@kekey", "encode") == "ERROR: You can't use this character in your key: @\nYour encoded message thus far is: K", "Test 8 failed: input 'fake_plaintext', 'f@kekey', 'encode'"
    assert translator_function("fake_plaintext", "testkey", "decode") == "ERROR: I can't decode this character: _\nYour decoded message thus far is: MWSL", "Test 9 failed: input 'fake_plaintext', 'testkey', 'decode'"
    assert translator_function("fake_plaintext", "f@kekey", "decode") == "ERROR: You can't use this character in your key: @\nYour decoded message thus far is: A", "Test 10 failed: input 'fake_plaintext', 'f@kekey', 'decode'"
   
    #Assess encoding and decoding capability
    assert translator_function("This is a test message", "test key", "encode") == "MLALSWYMIKMWIQLEYX", "Test 11 failed: input 'This is a test message', 'test key', 'encode'"
    assert translator_function("MLALSWYMIKMWIQLEYX", "test key", "decode") == "THISISATESTMESSAGE", "Test 12 failed: input 'MLALSWYMIKMWIQLEYX', 'test key', 'decode'"
    
    print("Congratulations! 12/12 tests passed!")
    
test_vigenere(basic_vigenere_translator)

##GUI Creation

from tkinter import * #This gives us direct access to all public names within tkinter without needing to call tkinter.this, tkinter.that, etc.

vig_gui = Tk() #Initialises our GUI window - its name is vig_gui
vig_gui.title('Vigenère Translator') #Changes title

##First, we need some welcome text so the user knows what this is and what to do.

welcome_text = Text(vig_gui, height = 2, width = 100) #This is our text box
welcome_text.pack(side = TOP) #Our welcome text will be at the top of the window
welcome_text.insert("1.0","Welcome to my Vigenère Translator!\nSelect either Encode or Decode, put your message and key in, and hit Translate!") #Inserts at the first character (0) of the first line (1)

##Our translator function does two mutually exclusive things, so we need mutually exclusive options - radio buttons will work best.

de_en_flag = StringVar() #Tell tkinter what type of variable this is: a StringVar object is a container which takes in strings
de_en_flag.set("encode") #We set this variable to have the value "encode" first, so we don't inadvertently fill both radio buttons - comment this out to see what I mean
Radiobutton(vig_gui, text = "Encode", variable = de_en_flag, value = "encode").pack(anchor = N, pady = (10,0)) #By clicking on the button, we change the value of de_en_flag
Radiobutton(vig_gui, text = "Decode", variable = de_en_flag, value = "decode").pack(anchor = N, pady = (0,10)) #Anchor controls where the text is postioned within morse_gui - options are N, NW, etc. and CENTER.
#The pady option takes in either a single integer or a tuple - adds the specified amount of vertical space to the top and bottom.

##After selecting their option, the user needs to know where to put their message in.

input_text_msg = Text(vig_gui, height = 1, width = 23)
input_text_msg.pack(side = TOP)
input_text_msg.insert("1.0", "Put your message below!")

##We then create the space in which the user can put their message in.

user_input_message = Entry(vig_gui, width = 100)
user_input_message.pack(side = TOP, pady = 15)

##Skip this for now --------- (1)

#After repeated usage, I needed some way to quickly remove large messages, given the limited size of the user input box.

def clear_message():
    user_input_message.delete(0, END) #Clears user input box

clear_button_msg = Button(vig_gui, text = 'Clear Message', width = 25, command = clear_message)
clear_button_msg.pack(side = TOP, pady = (0,15))

##The user also needs to know where to put their key in.

input_text_key = Text(vig_gui, height = 1, width = 19)
input_text_key.pack(side = TOP)
input_text_key.insert("1.0", "Put your key below!")

##We then create the space in which the user can put their key in.

user_input_key = Entry(vig_gui, width = 100)
user_input_key.pack(side = TOP, pady = 15)

##Now, we need to find some way of initiating the encoding or decoding process. 

def start_translator(de_en_flag): #This allows us to create conditional additions to the GUI
    if de_en_flag == "encode":
        output_text.replace("1.0", END, basic_vigenere_translator(user_input_message.get(), user_input_key.get(), de_en_flag)) #Removes all characters in the box (from 1.0 to the end) and puts the specified string in
    elif de_en_flag == "decode":
        output_text.replace("1.0", END, basic_vigenere_translator(user_input_message.get(), user_input_key.get(), de_en_flag))
#Note that output_text (where the output will be displayed) has not been defined yet - this is okay, because the function has not yet been called.

##Skip this for now --------- (3)

#Aesthetically, I wanted to put the buttons below the key input box side-by-side, in the centre.
#The best solution for this was to create a frame to hold them both, and position that frame between the user input and the output. This is where "code echoes order" helps a lot.
        
main_frame = Frame(vig_gui)
main_frame.pack(side = TOP)

##Now we need to let the user call start_translator. We need a start button.

start_button = Button(vig_gui, text = 'Translate!', width = 25, command = lambda: start_translator(de_en_flag.get())) 
#This lambda will use the StringVar object's get() method to return its current value, then pass it to start_translator
start_button.pack(in_ = main_frame, side = LEFT)

##Skip this for now --------- (2)

#After repeated usage, I needed some way to quickly remove large keys, given the limited size of the user input box.

def clear_key():
    user_input_key.delete(0, END) #Clears key input box

clear_button_key = Button(vig_gui, text = 'Clear Key', width = 25, command = clear_key)
clear_button_key.pack(in_ = main_frame, side = RIGHT, padx = (20,0))

##We then need to display the output to the user.

output_text = Text(vig_gui, height = 10, width = 100)
output_text.pack(side = TOP, pady = 15)

##Finally, we need some way of neatly exiting the window.

exit_button = Button(vig_gui, text='Exit', width=25, command=vig_gui.destroy) #Adds exit button to terminate gui
exit_button.pack(side = TOP, pady = (0,15)) #Our exit button will be on the bottom of the window

##Once we're done, let's run the GUI!

vig_gui.mainloop() #This starts the GUI

## Go to points (1) and (2). 

## Go to point (3).
