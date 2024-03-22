import pygame
import cv2 as cv

# Define drum sounds and map them to regions (adjust coordinates as needed)
drum_sounds = {
    ((50, 340), (150, 350)): "snare",  # Region 1: Kick drum
    ((500, 340), (600, 350)): "crash",  # Region 2: Snare drum
    ((150, 440), (300, 450)): "tom-1",  # Region 3: Closed hi-hat
    ((350, 440), (500, 450)): "tom-2",  # Region 4: Open hi-hat
}

# load all sounds
pygame.mixer.init()
sounds = [pygame.mixer.Sound("sounds/" + sound + ".mp3") for sound in drum_sounds.values()]
channels = [pygame.mixer.Channel(i) for i in range(len(sounds))]  # Create a channel for each sound


playing_channels = [None]*len(sounds)  # To keep track of the currently playing sound


def display_drum(frame):
    for region in drum_sounds.keys():
        cv.rectangle(frame, region[0], region[1], (255, 0, 0), 3)
        image = cv.putText(frame, drum_sounds[region], (region[0][0], region[0][1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)

    return frame


def play_drum(x, y):

    i = 0
    for region in drum_sounds.keys():
        
        try:
            # play sounds if in region and no sound is playing
            # if (cx > region[0][0] and cx < region[1][0]) and (cy > region[0][1] and cy < region[1][1]) and not playing_channels[i]:
            if (x > region[0][0] and x < region[1][0]) and (y > region[0][1] and y < region[1][1]):
                playing_channels[i] = channels[i]
                playing_channels[i].play(sounds[i])
                # print(playing_channels)
        except:
            pass
        i += 1







# ###### Made by Tashadur Rahman  #######