#Import of the library 'tkinter' which is need to create a GUI and some of its sublibraries so the filesystem can be used.
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

#Import of the class Analysis which represents the next level of the GUI where the user can analyze comments. 
from marketing_department_tool_analysis_class import Analysis

#Declaration of the class 'GUI_Control'.
class GUI_Control:

    #Declaration of the '_init__' method.
    def __init__(self):

        #Creates the window of the GUI and its title.
        self.window = tk.Tk()
        self.window.title("Customer Sentiment Analysis Tool")

        #Configuration of the rows and columns of the windows which are 800 pixels in size and grows with the window of the user makes it bigger ('weight = 1').
        self.window.rowconfigure(0, minsize = 800, weight = 1)
        self.window.columnconfigure(1, minsize = 800, weight = 1)

        #Creation of space for different buttons inside the window, that have an raised appearance ('RAISED'), are 2 pixels thick ('bd = 2') and defines the size of these spaces. 
        self.frame_buttons_start_menu = tk.Frame(self.window, relief = tk.RAISED, bd = 2, width = 250, height = 800)
        self.frame_buttons_analysis_menu = tk.Frame(self.window, relief = tk.RAISED, bd = 2, width = 250, height = 800)
        self.frame_buttons_faq_menu = tk.Frame(self.window, relief = tk.RAISED, bd = 2, width = 250, height = 800)
        self.frame_buttons_analysis_class = tk.Frame(self.window, relief = tk.RAISED, bd = 2, width = 250, height = 800)

        #The spaces for the buttons are kept as they are and to not change with the windows. 
        self.frame_buttons_start_menu.grid_propagate(False)
        self.frame_buttons_analysis_menu.grid_propagate(False)
        self.frame_buttons_faq_menu.grid_propagate(False)
        self.frame_buttons_analysis_class.grid_propagate(False)

        #Execute of the next function of this class where all the buttons are declared.
        self.create_widget_gui_control()

    #Declaration of the function.
    def create_widget_gui_control(self):

        #Creates the buttons of 'frame_buttons_start_menu' with its names and commands that are executes when clicked.
        #'command = self.analysis_menu' for going to the next menu and 'command = self.window.destroy' for terminating the window, ending therefore the program. 
        button_analysis_menu = tk.Button(self.frame_buttons_start_menu, text = "Analysis Menu", command = self.analysis_menu)
        button_faq_menu = tk.Button(self.frame_buttons_start_menu, text = "FAQ", command = self.faq_menu)
        button_leave_program = tk.Button(self.frame_buttons_start_menu, text = "Exit", command = self.window.destroy)
        
        #Determines the position of the buttons with 'row' and 'column', 'ew' means the button is stretched from east to west, 'padx' and 'pady' define a distance of 5 pixels to its surroundings. 
        button_analysis_menu.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
        button_faq_menu.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
        button_leave_program.grid(row = 2, column = 0, sticky = "ew", padx = 5)

        #Creates the buttons of 'frame_buttons_faq_menu' with the same properties as above. First 'button' is a label though just for information that gets broken into a new line after 230 pixels.
        #New is the 'tk.Entry' button which serves as an input field for the program to interact with the user.
        button_disclaimer = tk.Label(self.frame_buttons_faq_menu, text = "Chose option by entering the according number in the field below.", wraplength = 230)
        self.entry_field_faq = tk.Entry(self.frame_buttons_faq_menu)
        button_return_from_faq_to_start = tk.Button(self.frame_buttons_faq_menu, text = "Go Back", command = self.start_menu)

        #Determines the position of the buttons that belong to the 'frame_buttons_faq_menu' with the same properties as above. 
        button_disclaimer.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
        self.entry_field_faq.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
        button_return_from_faq_to_start.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the buttons together with the determination of their position. 'Command' is more complex as it is used to call function of other classes.
        button_compare_albums = tk.Button(self.frame_buttons_analysis_menu, text = "Compare albums", command = lambda:
                                     Analysis(frame_buttons_analysis_class = self.frame_buttons_analysis_class, frame_buttons_analysis_menu = self.frame_buttons_analysis_menu, picture_placeholder = self.picture_placeholder).compare_albums())
        button_compare_albums.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)

        button_analyze_comments = tk.Button(self.frame_buttons_analysis_menu, text = "Analyse comments", command = lambda:
                                     Analysis(frame_buttons_analysis_class = self.frame_buttons_analysis_class, frame_buttons_analysis_menu = self.frame_buttons_analysis_menu, picture_placeholder = self.picture_placeholder).analyse_comments())
        button_analyze_comments.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)

        button_single_comment = tk.Button(self.frame_buttons_analysis_menu, text = "Analyse a single comment", command = lambda:
                                     Analysis(frame_buttons_analysis_class = self.frame_buttons_analysis_class, frame_buttons_analysis_menu = self.frame_buttons_analysis_menu, picture_placeholder = self.picture_placeholder).analyse_a_single_comment())
        button_single_comment.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)

        button_return_to_start_menu = tk.Button(self.frame_buttons_analysis_menu, text = "Go Back", command = self.start_menu)
        button_return_to_start_menu.grid(row = 3, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of a text field at position 0 (row) and 1 (column) stretching into each direction (north, south, east, west)
        self.picture_placeholder = tk.Text(self.window)
        self.picture_placeholder.grid(row = 0, column = 1, sticky = "nsew")

        #Execution of the 'start_menu' to show the user the start menu. 
        self.start_menu()

    #Declaration of the 'start_menu' function.
    def start_menu(self):

        #'forget' method to let all other frames disappear and show only the 'start_menu'-frame.
        self.frame_buttons_analysis_menu.grid_forget()
        self.frame_buttons_faq_menu.grid_forget()
        self.frame_buttons_start_menu.grid(row = 0, column = 0, sticky = "ns")

    #Declaration of the 'analysis_menu' function.
    def analysis_menu(self):

        #'forget' method to let all other frames disappear and show only the 'analysis_menu'-frame.
        self.frame_buttons_start_menu.grid_forget()
        self.frame_buttons_analysis_menu.grid(row = 0, column = 0, sticky = "ns")

    #Declaration of the 'faq_menu'.
    def faq_menu(self, event = None):

        #As long as the 'event' variable is 'None' display the menu options. 
        if event == None:

            self.frame_buttons_start_menu.grid_forget()
            self.frame_buttons_faq_menu.grid(row = 0, column = 0, sticky = "ns")

            self.picture_placeholder.insert(tk.END, "1. What is this software for?\n")
            self.picture_placeholder.insert(tk.END, "2. What emotions can be recognized?\n")
            self.picture_placeholder.insert(tk.END, "3. What do I need for the program to work?\n")
            self.picture_placeholder.insert(tk.END, "4. Where can I download the libraries?\n")
            self.picture_placeholder.insert(tk.END, "5. And where do I get the trained model from?\n")
            self.picture_placeholder.insert(tk.END, "6. Is there anything else I have to take into account?\n")
            self.picture_placeholder.insert(tk.END, "7. Where can I get more information?\n")

            #Calling this function 'faq_menu' if the enter button is pressed after entering something in the input field called 'entry_field' (explained above).
            self.entry_field_faq.bind("<Return>", self.faq_menu)

        #This part is executed when the event is not 'None'.
        else:

            #Getting the user input with 'get' and assigning it to the variable 'user_input'.
            user_input = self.entry_field_faq.get()

            #When the input is '1' or '1.' then...
            if user_input == "1" or user_input == "1.":

                #...'delete' to empty the text field, 'insert' to show the according answer. Remember this is a FAQ section. 
                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "This software can be used to analyze reviews or comments and classify what kind of emotion these reviews represent.\n")
                self.picture_placeholder.insert(tk.END, "Type 'Options', 'option' or simply 'o' in the entry field to see the full FAQ again.\n")

            #Same for the case where the input is '2' or '2.'.
            elif user_input == "2" or user_input == "2.":

                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "Sadness, joy, love, anger, fear and surprise.\n")
                self.picture_placeholder.insert(tk.END, "Type 'Options', 'option' or simply 'o' in the entry field to see the full FAQ again.\n")

            #Same for the case where the input is '3' or '3.'.
            elif user_input == "3" or user_input == "3.":

                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "You need an active internet connection. Otherwise the analysis won't work because the needed libraries can not be downloaded. Also you need the trained model.\n")
                self.picture_placeholder.insert(tk.END, "Type 'Options', 'option' or simply 'o' in the entry field to see the full FAQ again.\n")

            #Same for the case where the input is '4' or '4.'.
            elif user_input == "4" or user_input == "4.":

                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "You don't have to download the libraries manually. The program will do this for you\n")
                self.picture_placeholder.insert(tk.END, "Type 'Options', 'option' or simply 'o' in the entry field to see the full FAQ again.\n")

            #Same for the case where the input is '5' or '5.'.
            elif user_input == "5" or user_input == "5.":

                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "Here: https://huggingface.co/cathetus/emotion-detection-model/tree/main - you need to download every file there.\n")
                self.picture_placeholder.insert(tk.END, "Type 'Options', 'option' or simply 'o' in the entry field to see the full FAQ again.\n")


            #Same for the case where the input is '6' or '6.'.
            elif user_input == "6" or user_input == "6.":

                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "YES! You have to create the folder 'Emotion_Detection_Model_Directory' in the directory where your program is and put all downloaded files of the trained model there.\n")
                self.picture_placeholder.insert(tk.END, "Type 'Options', 'option' or simply 'o' in the entry field to see the full FAQ again.\n")

            #Same for the case where the input is '7' or '7.'.
            elif user_input == "7" or user_input == "7.":

                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "Check of the documentation. You can find it here: LINK.\n")
                self.picture_placeholder.insert(tk.END, "Type 'Options', 'option' or simply 'o' in the entry field to see the full FAQ again.\n")

            #When it is options the whole FAQ menu will be shown again so the user can select other options after they have been deleted from the text field.
            elif user_input == "Options" or user_input == "options" or user_input == "o":

                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "1. What is this software for?\n")
                self.picture_placeholder.insert(tk.END, "2. What emotions can be recognized?\n")
                self.picture_placeholder.insert(tk.END, "3. What do I need for the program to work?\n")
                self.picture_placeholder.insert(tk.END, "4. Where can I download the libraries?\n")
                self.picture_placeholder.insert(tk.END, "5. And where do I get the trained model from?\n")
                self.picture_placeholder.insert(tk.END, "6. Is there anything else I have to take into account?\n")
                self.picture_placeholder.insert(tk.END, "7. Where can I get more information?\n")

            #Inputted besides all the options above lead to the FAQ menu being shown again. 
            else:
                self.picture_placeholder.delete("1.0", tk.END)
                self.picture_placeholder.insert(tk.END, "Invalid Option. Please choose one of the available down below: \n")
                self.picture_placeholder.insert(tk.END, "1. What is this software for?\n")
                self.picture_placeholder.insert(tk.END, "2. What emotions can be recognized?\n")
                self.picture_placeholder.insert(tk.END, "3. What do I need for the program to work?\n")
                self.picture_placeholder.insert(tk.END, "4. Where can I download the libraries?\n")
                self.picture_placeholder.insert(tk.END, "5. And where do I get the trained model from?\n")
                self.picture_placeholder.insert(tk.END, "6. Is there anything else I have to take into account?\n")
                self.picture_placeholder.insert(tk.END, "7. Where can I get more information?\n")

                                  
