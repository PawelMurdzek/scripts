# Morse Code dictionary for encoding
TEXT_TO_MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '-': '-....-', '&': '.-...',
    '@': '.--.-.'
}

def text_to_morse(text):
    """
    Converts English text to Morse code.

    Args:
        text (str): The English text to convert to Morse code.

    Returns:
        str: The Morse code representation with letters separated by spaces
             and words separated by ' / '.
    """
    morse_message = ""
    
    # Split text into words
    words = text.upper().split()
    
    for word in words:
        morse_word = ""
        for char in word:
            if char in TEXT_TO_MORSE_DICT:
                morse_word += TEXT_TO_MORSE_DICT[char] + " "
            else:
                # For characters not in the dictionary, add a placeholder
                morse_word += "? "
        
        # Remove the trailing space and add the word to the message
        morse_message += morse_word.strip() + " / "
    
    # Remove the final " / " and return
    return morse_message.strip(" / ")

if __name__ == "__main__":
    print("--- Text to Morse Code Converter ---")
    print("Supported characters: A-Z, 0-9, . , ? / ( ) - & @")
    
    text_message = input("\nEnter the text to convert to Morse code: ")
    
    morse_code = text_to_morse(text_message)
    
    print("\nMorse code:")
    print(morse_code)
    
    print("\nNote: Letters are separated by spaces, words are separated by ' / '")
    print("Unknown characters are represented by '?'")