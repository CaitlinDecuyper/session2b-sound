import csv
import os
from pydub import AudioSegment, silence
from pydub.playback import play
AudioSegment.converter = "D:\\ffmpeg\\bin\\ffmeg.exe"


# We have three conditions: High Frequency (HF), Low Frequency (LF), and Non-Words (NW).
# All words for each condition are stored in one .wav file.
# Your task is to:
#       split the words on the silence
#       make sure they all have the same loudness
#       save them in a folder corresponding to their condition (folder names: HF, LF, NW)


path_to_repository =  "K:\\PhD\\IMPRScourses\\Python\\session2b-sound"

# This piece of code is here to help you.
# It reads a text file with information about the stimuli you are going to split (names & condition),
# and returns a dictionary named 'stimuli' with condition as key, and the word itself as value.
# Use this dictionary to name the files you have to save.
stimuli_info = open(os.path.join(path_to_repository, "lexdec_stimuli.txt"))
stimuli_reader = csv.reader(stimuli_info, delimiter=',')
headers = next(stimuli_reader, None)

# Create the dictionary
stimuli = {}
for stimulus in stimuli_reader:
    if stimulus[2] not in stimuli.keys():
        stimuli[stimulus[2]] = list()
    stimuli[stimulus[2]].append(stimulus[3])

# Put them in alphabetical order
for condition, words in stimuli.items():
    sort = sorted(words)
    stimuli[condition] = sort

# change the non-word condition name
stimuli["NW"] = stimuli.pop("none") # none was old name

# Now you have the stimulus names. Let's take a look at the dictionary:
print(stimuli)

# YOUR CODE HERE.

sound_folder =  "K:\\PhD\\IMPRScourses\\Python\\session2b-sound\\raw" # folder with raw sound files
conditions = ["HF", "LF", "NW"] # 3 conditions
target_volume = -6 # target volume for normalized files

for condition in conditions: # do everything for all 3 conditions

    # create folder to save edited recordings (if that folder does not exist yet)
    conditionfolder = "K:\\PhD\\IMPRScourses\\Python\\session2b-sound\\" + condition
    if not os.path.isdir(conditionfolder):
        os.mkdir(conditionfolder)

    # open long recording with all words
    raw_file = condition + "_recording.wav
    path_raw = os.path.join(sound_folder, raw_file)
    sound_raw = AudioSegment.from_wav(path_raw)

    # split into words based on silence
    list_words = silence.split_on_silence(sound_raw, min_silence_len=200, silence_thresh=-50)

        # normalize (individual) recordings and save
        for i in range(len(list_words)):
        sound_word = list_words[i]
        change = target_volume - sound_word.dBFS
        target_sound = sound_word.apply_gain(change)
        filename = stimuli[condition][i] + '.wav'
        target_sound_path = os.path.join(conditionfolder, filename)
        sound.export(target_sound_path, format='wav')


# Some hints:
# 1. Where are the stimuli?
# 2. How loud do you want your stimuli to be? Store it in a variable
# 3. Where do you want to save your files? Make separate folders for the conditions.
# 4. Do you normalize the volume for the whole sequence or for separate words? Why (not)? Try it if you like :)
# 5. You can check whether your splitting worked by playing the sound, or by printing the length of the resulting list
# 6. Use the index of the word [in the list of words you get after splitting]
# to get the right text from the dictionary.
# 7. Recall you can plot your results to see what you have done.
# Good luck!



