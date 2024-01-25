import pygame
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # used to hide the annoying welcome message from pygame

WIDTH, HEIGHT = 390, 200 # This is the width and height of the main window
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # WIN is the main window 
play_next = pygame.USEREVENT + 0
dont_play_next = pygame.USEREVENT + 1

# The buttons on the window. They are located in a subfolder
# Each button icon is 50 X 50 pixels
play_button    = pygame.image.load("Icons/play.png")
pause_button   = pygame.image.load("Icons/pause.png")
stop_button    = pygame.image.load("Icons/stop.png")
forward_button = pygame.image.load("Icons/forward.png")
back_button    = pygame.image.load("Icons/back.png")
volume_up      = pygame.image.load("Icons/volume_up.png")
volume_down    = pygame.image.load("Icons/volume_down.png")
mute_button    = pygame.image.load("Icons/mute.png")



def song_import(): # This is the same import function we've been using

    song_list = []
    for filename in os.listdir("Songs/"):
        if filename.endswith(".mp3"):
            song_list.append("Songs/" + filename)
    song_list.sort()
    return song_list

def get_next_last(playlist, song):
    i = playlist.index(song)
    if i == 0:
        i_next = i + 1
        i_last = len(playlist) - 1
    elif i == len(playlist) - 1:
        i_next = 0
        i_last = i - 1
    else:
        i_next = i + 1
        i_last = i - 1
    return playlist[i_next], playlist[i_last]


def mp3_command(x, y, song, playlist, p):
    # This function determines which playback function to run
    # x and y are the coordinates on the window where the mouse clicked.
    # song is the song currently playing/loaded
    # playlist is the list of songs
    # p is a boolean that tracks whether playback is paused

    # since each icon is 50 pixels tall, they all have a y range of 50 - 100.
    # If someone clicks antwhere other than the above range, then the function does nothing
    #if y < 50 or y > 100:
        #return song, p
    if y >= 50 and y <= 100:
        next_song, last_song = get_next_last(playlist, song)

        # BACK
        if x >= 50 and x <= 100: 
            pygame.mixer.music.set_endevent(dont_play_next)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.set_endevent(dont_play_next)
            pygame.mixer.music.load(last_song)
            pygame.mixer.music.play()
            return last_song, p

        # PAUSE
        elif x >= 130 and x <= 180 and pygame.mixer.music.get_busy() and not p:
            pygame.mixer.music.pause()
            p = True

        # UNPAUSE
        elif x >= 130 and x <= 180 and p:
            pygame.mixer.music.unpause()
            p = False

        # PLAY
        elif x >= 130 and x <= 180 and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            p = False

        # STOP
        elif x >= 210 and x <= 260 and pygame.mixer.music.get_busy():
            pygame.mixer.music.set_endevent(dont_play_next)
            pygame.mixer.music.stop()
            song = playlist[0]
            p = False

        # SKIP
        elif x >= 290 and x <= 340:
            pygame.mixer.music.set_endevent(dont_play_next)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.load(next_song)
                pygame.mixer.music.play()
                return next_song, p
            else:
                pygame.mixer.music.load(next_song)
                return next_song, p
    elif y >= 120 and y <= 170:
        # mute
        if x >= 50 and x <= 100:
            current_volume = 0.0
            pygame.mixer.music.set_volume(current_volume)
        # volume up
        elif x >= 130 and x <= 180:
            current_volume = pygame.mixer.music.get_volume()
            if current_volume == 0.0: 
                pass
            else: 
                current_volume -= 0.125
                pygame.mixer.music.set_volume(current_volume)
        # volume down
        elif x >= 190 and x <= 240:
            current_volume = pygame.mixer.music.get_volume()
            if current_volume >= 1.0: 
                pass
            else: 
                current_volume += 0.125
                pygame.mixer.music.set_volume(current_volume)

    return song, p


def draw_window(song_title):
    WIN.fill((255, 255, 255)) # Draws the window

    # The .blit() function draws the icons on the window
    WIN.blit(back_button, (50, 50))
    if(pygame.mixer.music.get_busy()):
        WIN.blit(pause_button, (130, 50))
    else:
        WIN.blit(play_button, (130, 50))
    WIN.blit(stop_button, (210, 50))
    WIN.blit(forward_button, (290, 50))
    WIN.blit(mute_button, (50, 120))
    WIN.blit(volume_down, (130, 120))
    WIN.blit(volume_up, (210, 120))
    pygame.draw.line(WIN, (0, 0, 0), (290, 170), (340, 170))
    volume = pygame.mixer.music.get_volume()
    # volume level rectangles
    vol_x = 300
    vol_y = 164
    vol_w = 30
    vol_h = 4
    i = 0.125
    j = 0
    while i <= volume:
        if volume == 0.0:
            break
        if i == 1.0:
            pygame.draw.rect(WIN, (255, 0, 0), (vol_x, vol_y, vol_w, vol_h))
        else:
            pygame.draw.rect(WIN, (0, 0, 0), (vol_x, vol_y, vol_w, vol_h))
        vol_y -= 6
        i += 0.125
    song_title = song_title.strip("Songs/")
    pygame.display.set_caption("Now Playing: " + song_title)
    pygame.display.update() # This updates the window
# ----------------------------------------------------------
def main():
    pygame.mixer.init() # initialize the player
    songs = song_import() # The song playlist
    current_song = songs[0] # defaults current song to the first song in the playlist
    running = True # Boolean used to keep the main loop running
    mousex = 0     # The X position of the mouse
    mousey = 0     # The Y position of the mouse
    paused = False # Used to determine if the player is paused
    pygame.mixer.music.set_endevent(play_next)
    pygame.mixer.music.set_volume(.5)
    while running: # Handles events, updates the game state, and draws the game state to the screen
        mouseClicked = False # Used to track mouse-click events. Must be reset to False every loop
        for event in pygame.event.get(): #Executes code for every event that has happened since the last iteration of the game loop.
            if event.type == pygame.QUIT: # If the program is closed, exit the loop
                running = False
            elif event.type == pygame.MOUSEBUTTONUP: # Checks to see if the mouse button was clicked
                mousex, mousey = event.pos # The XY coordinates where the mouse was clicked
                mouseClicked = True
                current_song, paused = mp3_command(mousex, mousey, current_song, songs, paused) # Determine function to execute
            elif event.type == play_next:
                next_song, last_song = get_next_last(songs, current_song)
                pygame.mixer.music.load(next_song)
                pygame.mixer.music.play()
                current_song = next_song
                pass
            elif event.type == dont_play_next:
                pass
        pygame.mixer.music.set_endevent(play_next)

                
        draw_window(current_song)
    pygame.quit()
    SystemExit()

if __name__ == "__main__": main()