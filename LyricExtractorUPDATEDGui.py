import lyricsgenius
import customtkinter
from tkinter import messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) # Used for displaying the emotion bar chart
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

from selenium import webdriver

from nrclex import NRCLex

sns.set_style('darkgrid')
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class LyricGUI:
    def __init__(self):          
        self.root = customtkinter.CTk()
        self.root.title('Lyrics Extractor')

        self.root.state('zoomed') # Opens the maximized tkinter window

        self.api_key = '2CVDvKiySOViYtn79C3izKrUQ5ONyZU-HIpPf1GMwYQgCO5NXTjVpuJcEQqMSjGn'
        self.genius = lyricsgenius.Genius(self.api_key, verbose=False, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])

        # Create a main frame
        self.title_frame = customtkinter.CTkFrame(self.root)
        self.title_frame.pack(fill='both')

        self.option_frame = customtkinter.CTkFrame(self.root)
        self.option_frame.pack()

        self.main_frame = customtkinter.CTkScrollableFrame(self.root)
        self.main_frame.pack(fill='both', expand='yes')

        # Displays the title
        self.title = customtkinter.CTkLabel(self.title_frame, text='LYRICS GENERATOR', font=('Arial', 45))
        self.title.pack(pady=5) 

        # Displays the option menu
        self.option_menu_1 = customtkinter.CTkOptionMenu(self.option_frame, values=['Lyrics Generator', 'Emotions Generator'], command=self.switch_mode)
        self.option_menu_1.grid(row=0, column=0, padx=10, pady=5, sticky='NESW')
        self.option_menu_1.set('Lyrics Finder')

        # Changes the appearance mode of the screen based on what option the user clicks
        self.option_menu_2 = customtkinter.CTkOptionMenu(self.option_frame, values=['Light', 'Dark'], command=self.switch_appearance)
        self.option_menu_2.grid(row=0, column=1, padx=10, pady=5)
        self.option_menu_2.set('Toggle Light/Dark Appearance')

        # Displays the question and the entry box for the user's song and artist choice ONTO THE SCROLLABLE FRAME
        self.song_choice_label = customtkinter.CTkLabel(self.main_frame, text='What song do you want to listen to?', font=('Arial', 25))
        self.song_choice_label.pack(pady=10) 

        self.song_choice = customtkinter.CTkEntry(self.main_frame)
        self.song_choice.pack()

        self.artist_choice_label = customtkinter.CTkLabel(self.main_frame, text='Who is the artist?', font=('Arial', 25))
        self.artist_choice_label.pack(pady=10)

        self.artist_choice = customtkinter.CTkEntry(self.main_frame)
        self.artist_choice.pack()

        # Displays the button that says "Generate Lyrics" ONTO THE SCROLLABLE FRAME
        self.generate_lyrics = customtkinter.CTkButton(self.main_frame, text='Generate Lyrics!', font=('Arial', 30), command=self.show_lyrics)
        self.generate_lyrics.pack(pady=20)

        # Controls whether or not there are lyrics already present in the GUI
        self.generate_lyrics_counter = 1

        # Controls whether or not there is a Selenium Chrome Browser currently running
        self.youtube_lyrics_counter = 1

        # Displays the button that says "Clear All Lyrics" ONTO THE SCROLLABLE FRAME. 
        self.clear_lyrics = customtkinter.CTkButton(self.main_frame, text='Clear All Lyrics', font=('Arial', 30), command=self.clear_lyrics_func)
        self.clear_lyrics.pack(pady=10)

        # Displays the button that says "YouTube Lyrics" ONTO THE SCROLLABLE FRAME. 
        self.yt_lyrics = customtkinter.CTkButton(self.main_frame, text='YouTube Lyrics', font=('Arial', 30), command=self.show_youtube_lyrics)
        self.yt_lyrics.pack(pady=10)

        # Boolean for whether or not the "Clear Lyrics" button was clicked or not
        self.clear_lyrics_clicked = False

        # Closes the GUI window when the user hits the "X" button 
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.root.mainloop()

    def show_lyrics(self):
        # If the "Clear Lyrics" button has already been clicked, then reset the generate lyrics counter back to 1
        # because the GUI is empty now.
        if self.clear_lyrics_clicked == True:
            self.generate_lyrics_counter = 1

        try:
        # Only display the lyrics once before exiting the loop
        # If there are lyrics present in the GUI, then the user can't enter in another song because generate_lyrics_counter = 2
            while self.generate_lyrics_counter < 2:
                self.song = self.genius.search_song(self.song_choice.get(), self.artist_choice.get())

                # I need to figure out how to remove the annoying numbers at the end of the lyrics.
                # IDK HOW TO DO THIS YET THOUGH!
                
                self.song_lyrics = customtkinter.CTkLabel(self.main_frame, 
                                            # Gets rid of the unnecessary strings in the beginning of the lyrics and gets rid of the annoying "Embed" string at the end
                                            text=self.song.lyrics.replace('[', '\n[').replace(self.song.lyrics[0:self.song.lyrics.index('[')], '').replace('Embed', ''), 
                                            font=('Arial', 13)) 

                self.song_lyrics.pack(pady=30)

                self.clear_lyrics_clicked = False # Change this boolean back to False because there are lyrics present in the GUI now

                self.generate_lyrics_counter += 1 # Increase the generate_lyrics_counter variable so the loop ends and the user can't input multiple song lyrics at the same time

        except: # prints out "Song was not found" if the song is not found by the lyricsgenius API
           print('This song was not found!')
           self.clear_lyrics_clicked = True # Resets the boolean back to True so that the user CAN'T click on "Clear Lyrics"
           self.generate_lyrics_counter = 1 # Resets the lyric counter to 1 so the user can print out another song

    def show_youtube_lyrics(self):
        # while self.youtube_lyrics_counter < 2: 
        self.song_choice_words = self.song_choice.get().split() 
        self.artist_choice_words = self.artist_choice.get().split()

        self.song_choice_full_str = '+'.join(self.song_choice_words)
        self.artist_choice_full_str = '+'.join(self.artist_choice_words)

        self.driver = webdriver.Chrome()
        self.driver.get('https://www.youtube.com/results?search_query=' + self.song_choice_full_str + '+' + self.artist_choice_full_str + '+lyrics')
        self.driver.maximize_window()

    def generate_lyrics_clicker_counter():
        pass

    def on_closing(self):
        # If the user presses on "Yes", then the tkinter window will close.
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            self.root.destroy() # Closes the tkinter window

    def clear_lyrics_func(self):
        if self.clear_lyrics_clicked == False:
            self.clear_lyrics_clicked = True # Change the boolean to True because there are no lyrics present in the GUI
            self.song_lyrics.destroy()
    
    def switch_appearance(self, choice):
        customtkinter.set_appearance_mode(choice)

    def switch_mode(self, choice):
        if choice == 'Emotions Generator':
            # Sets the boolean for the "Clear Emotions" button to FALSE
            self.clear_emotions_clicked = False
            
            # Removes the "Generate Lyrics!" and "Clear All Lyrics" button when the user clicks on "Emotions Generator"
            self.generate_lyrics.destroy()
            self.clear_lyrics.destroy()

            # Removes the "YouTube Lyrics" button when the user clicks on "Emotions Generator"
            self.yt_lyrics.destroy()

            # Destroys the title so that I can update the text without the title showing up twice
            self.title.destroy() 

            # If there are song lyrics present in the GUI when the user switches to "Emotions Generator", then DELETE THE LYRICS!
            if self.clear_lyrics_clicked == False and self.generate_lyrics_counter == 2:
                self.song_lyrics.destroy()
        

            self.title = customtkinter.CTkLabel(self.title_frame, text='EMOTIONS GENERATOR', font=('Arial', 45))
            self.title.pack(pady=5) 

            self.generate_emotions = customtkinter.CTkButton(self.main_frame, text='Generate Emotions!', font=('Arial', 30), command=self.show_emotions)
            self.generate_emotions.pack(pady=20)

            # Controls whether or not the bar plot is already present in the GUI
            self.generate_emotions_counter = 1

            self.clear_emotions = customtkinter.CTkButton(self.main_frame, text='Clear All Emotions', font=('Arial', 30), command=self.clear_emotions_func)
            self.clear_emotions.pack(pady=10)

        if choice == 'Lyrics Generator':
            # Sets the boolean for the "Clear Lyrics" button to FALSE
            self.clear_lyrics_clicked = False

            # Delete all these elements so that I can easily update the labels when the user clicks back on "Lyrics Finder"
            self.generate_emotions.destroy()
            self.clear_emotions.destroy()
            # Destroys the title so that I can update the text without the title showing up twice
            self.title.destroy()
            
            # If the emotion bar chart is still present in the GUI and the user switches to "Lyrics Generator", then DELETE THE BAR CHART!
            if self.clear_emotions_clicked == False and self.generate_emotions_counter == 2:
                self.widget.destroy()

            self.title = customtkinter.CTkLabel(self.title_frame, text='LYRICS GENERATOR', font=('Arial', 45))
            self.title.pack(pady=5) 

            self.generate_lyrics = customtkinter.CTkButton(self.main_frame, text='Generate Lyrics!', font=('Arial', 30), command=self.show_lyrics)
            self.generate_lyrics.pack(pady=20)

            # Controls whether or not there are lyrics already present in the GUI
            self.generate_lyrics_counter = 1

            # Displays the button that says "Clear All Lyrics" ONTO THE SCROLLABLE FRAME. 
            self.clear_lyrics = customtkinter.CTkButton(self.main_frame, text='Clear All Lyrics', font=('Arial', 30), command=self.clear_lyrics_func)
            self.clear_lyrics.pack(pady=10)

            # Displays the button that says "YouTube Lyrics" ONTO THE SCROLLABLE FRAME. 
            self.yt_lyrics = customtkinter.CTkButton(self.main_frame, text='YouTube Lyrics', font=('Arial', 30), command=self.show_youtube_lyrics)
            self.yt_lyrics.pack(pady=10)

    def show_emotions(self):
        if self.clear_emotions_clicked == True:
            self.generate_emotions_counter = 1
        
        try:
            while self.generate_emotions_counter < 2:
                self.song = self.genius.search_song(self.song_choice.get(), self.artist_choice.get())

                # The NRCLex object takes in the song lyrics so that I can analyze the main emotions 
                self.emotion = NRCLex(self.song.lyrics.replace('[', '\n[').replace(self.song.lyrics[0:self.song.lyrics.index('[')], '').replace('Embed', ''))

                # Gets all the different emotions into one list
                self.emotions_list = list(self.emotion.raw_emotion_scores.keys())

                # Gets all the counts of the emotions into another list
                self.emotions_count_list = list(self.emotion.raw_emotion_scores.values())

                # Creates a dictionary using the 2 previous lists
                self.emotions_dict = {'Emotion': self.emotions_list, 'Emotion Count': self.emotions_count_list}

                # Creates a pandas DataFrame from the emotions dictionary and sorts the values in ascending order
                self.emotions_df = pd.DataFrame(self.emotions_dict)
                self.emotions_df = self.emotions_df.sort_values(by='Emotion Count', ascending=True)

                self.fig, self.ax = plt.subplots(figsize=(10,5))
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
                self.widget = self.canvas.get_tk_widget()
                self.widget.pack(padx=10, pady=10)
                
                self.ax.barh(self.emotions_df['Emotion'], self.emotions_df['Emotion Count'])
                self.ax.set_ylabel('Emotion Classification')
                self.ax.set_xlabel('Emotion Count')

                self.canvas.draw()

                self.clear_emotions_clicked = False # Change this boolean back to False because the bar chart is already present in the GUI now

                self.generate_emotions_counter += 1 # Increase the generate_emotions_counter variable so the loop ends and the user can't input multiple bar charts at the same time

        except:
            print('This song was not found!')
            self.clear_emotions_clicked = True # Resets the boolean back to True so that the user CAN'T click on "Clear Emotions"
            self.generate_emotions_counter = 1 # Resets the emotion counter to 1 so the user can print out another bar chart

    def clear_emotions_func(self):
        if self.clear_emotions_clicked == False:
            self.clear_emotions_clicked = True
            self.widget.destroy()

LyricGUI()