import nltk
import os
import time
from playsound import playsound

# Ensure that the required NLTK data is available
nltk.download('cmudict')

# Load CMU Pronouncing Dictionary (ARPAbet)
arpabet_dict = nltk.corpus.cmudict.dict()

# Define the directory where your ARPAbet MP3 files are stored
sound_directory = 'arpabet_sounds'  # Modify this to your actual folder path

# Function to convert text to ARPAbet
def text_to_arpabet(text):
    words = text.split()
    arpabet_words = []
    
    for word in words:
        word_lower = word.lower()
        if word_lower in arpabet_dict:
            arpabet_words.append(' '.join(arpabet_dict[word_lower][0]))  # Take the first pronunciation
        else:
            arpabet_words.append(word)  # If no ARPAbet found, keep the word as is
    
    return ' '.join(arpabet_words)

# Function to play ARPAbet phonemes
def play_arpabet(arpabet_text):
    phonemes = arpabet_text.split()
    
    for phoneme in phonemes:
        # Check if the phoneme has a corresponding MP3 file
        mp3_file = f"{phoneme.upper()}.mp3"
        mp3_path = os.path.join(sound_directory, mp3_file)
        
        if os.path.exists(mp3_path):
            print(f"Playing: {phoneme}")
            playsound(mp3_path)
        else:
            print(f"Warning: No MP3 file found for phoneme {phoneme}")

# Main function to take input text and produce speech
def main():
    text = input("Enter text: ")
    arpabet_text = text_to_arpabet(text)
    print(f"ARPAbet Text: {arpabet_text}")
    play_arpabet(arpabet_text)

if __name__ == "__main__":
    main()
