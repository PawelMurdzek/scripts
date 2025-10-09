# Morse Code dictionary for translation
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6',
    '--...': '7', '---..': '8', '----.': '9', '.-.-.-': '.',
    '--..--': ',', '..--..': '?', '-..-.': '/', '-.--.': '(',
    '-.--.-': ')', '-....-': '-', '.-...': '&', '.--.-.': '@'
}

def morse_to_text(morse_code):
    """
    Translates a string of Morse code to English text.

    Args:
        morse_code (str): The Morse code string. It's assumed that
                          letters are separated by a single space ' '
                          and words are separated by a forward slash '/'.

    Returns:
        str: The translated English text.
    """
    translated_message = ""
    
    # Split the morse code into words
    words = morse_code.strip().split(' / ')
    
    for word in words:
        # Split each word into letters
        letters = word.split(' ')
        for morse_char in letters:
            if morse_char in MORSE_CODE_DICT:
                translated_message += MORSE_CODE_DICT[morse_char]
            elif morse_char == "":
                continue # Ignore multiple spaces
            else:
                translated_message += '?' # Placeholder for unknown code
        
        # Add a space after each word
        translated_message += ' '
        
    return translated_message.strip()

if __name__ == "__main__":
    print("--- Morse Code to Text Translator ---")
    print("Enter Morse code. Use spaces between letters and ' / ' between words.")
    example = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
    print(f"Example: '{example}' translates to 'HELLO WORLD'")
    
    morse_message = input("\nEnter the Morse code to translate: ")
    
    translated_text = morse_to_text(morse_message)
    
    print("\nTranslated text:")
    print(translated_text)
