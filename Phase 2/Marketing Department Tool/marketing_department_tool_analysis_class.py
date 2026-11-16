#Import of 'tkinter' library to create the GUI.
import tkinter as tk
#Import of sublibraries to work with files.
from tkinter.filedialog import askopenfilename, asksaveasfilename
#Import of the class 'DataProcessing' to analyze comments.
from marketing_department_comment_processing import DataProcessing
#Import of 'os' to work with file paths.
import os

#Class to create the frames and buttons of the 'analysis_menu'.
class Analysis:

    #'__ini__' method to initialize the frames, buttons and dictionaries. 
    def __init__(self, frame_buttons_analysis_class, frame_buttons_analysis_menu, picture_placeholder):

        self.frame_buttons_analysis_class = frame_buttons_analysis_class
        self.frame_buttons_analysis_menu = frame_buttons_analysis_menu
        self.picture_placeholder = picture_placeholder
        self.dictionary_for_comments = {}
        self.dictionary_for_comparison_1 = {}
        self.dictionary_for_comparison_2 = {}

    #Declaration of the function 'check_entry' with which the program checks whether an input has been made by the user.
    def check_entry(self, entry_comment):

        #'get' method to get the input and 'strip' to remove potential whitespaces.
        if self.entry_comment.get().strip():

             #The button 'button_analyse_single_comment' is activated when an input has been made.
            self.button_analyse_single_comment.config(state = "normal")

        #'else' for when no input has been made.
        else:
            #Disables the button then.
            self.button_analyse_single_comment.config(state = "disabled")

    #Declaration of the 'open_file' function which opens one or more files depending on the variable 'value'.
    def open_file(self, value = None):

        #'if' to check if 'value' is 'None'. 
        if value == None:

            #This part makes it possible to open files that end with '.txt' as well as other types and assign them to the variable 'filepath'.
            filepath = askopenfilename(
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
                )

            #Returns when the user does not select a file.
            if not filepath:
                
                return

            #If the user selects a file, it is opened in reading mode. 
            with open(filepath, mode="r", encoding="utf-8") as input_file:

                #The name of the file is extracted and everything behind the word 'album' is removed. With this the album name is assigned to the variable 'filename'.
                filename = os.path.basename(filepath).split(" album")[0]
                #Rading every line and assigning them to 'all_comments_from_file'.
                all_comments_from_file = input_file.readlines()

                #Iterating through every comment.
                for single_comment in all_comments_from_file:

                    #Nothing happens when the comment is just a line break. 
                    if single_comment == "\n":

                        pass

                    #Otherwise a dictionary with the comment, needed values for the tokenization and the analysis is created. 
                    else:

                        comment = {single_comment: {"input_ids": None,
                                                    "attention_mask": None,
                                                    "token_type_ids": None,
                                                    "label": None,
                                                    "emotion": None,
                                                    "album": filename}}

                        #The dictionary 'comment' is added to the dictionary 'dictionary_for_comments' to create a nested dictionary. 
                        self.dictionary_for_comments.update(comment)
                        
                #The 'picture_placeholder' variable and the just created nested dictionary are passed to the class 'DataProcessing' to further work with both.
                call_data_processing = DataProcessing(picture_placeholder = self.picture_placeholder)
                call_data_processing.tokenizer(multiple_comments_to_analyze = self.dictionary_for_comments)

        #'else' that is executed when the variable 'value' is not 'None'.
        else:

            #For the time the 'value' variable is bigger than 0...
            while value > 0:

                #...files can be opened. 
                filepath = askopenfilename(
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
                )

                #The process is stopped with this 'return' when the selection is cancelled.
                if not filepath:
                    
                    return

                #If the user selects a file, it is opened in reading mode. 
                with open(filepath, mode="r", encoding="utf-8") as input_file:

                    #The name of the file is extracted and everything behind the word 'album' is removed. With this the album name is assigned to the variable 'filename'.
                    filename = os.path.basename(filepath).split(" album")[0]
                    #Rading every line and assigning them to 'all_comments_from_file'.
                    all_comments_from_file = input_file.readlines()

                    #Iterating through every comment.
                    for single_comment in all_comments_from_file:

                        #Nothing happens when the comment is just a line break. 
                        if single_comment == "\n":

                            pass

                        #Otherwise a dictionary with the comment, needed values for the tokenization and the analysis is created. 
                        else:

                            #Different from the process above the dictionary these values get assigns to depend on the number 'value' represents. 
                            if value == 2:

                                comment = {single_comment: {"input_ids": None,
                                                        "attention_mask": None,
                                                        "token_type_ids": None,
                                                        "label": None,
                                                        "emotion": None,
                                                        "album": filename}}
                                
                                #The dictionary 'comment' is added to the dictionary 'dictionary_for_comparison_1' to create a nested dictionary. 
                                self.dictionary_for_comparison_1.update(comment)

                            #When the number of 'value' is one then the other dictionary is used to assign the value to. 
                            elif value == 1:

                                comment = {single_comment: {"input_ids": None,
                                                        "attention_mask": None,
                                                        "token_type_ids": None,
                                                        "label": None,
                                                        "emotion": None,
                                                        "album": filename}}

                                #The dictionary 'comment' is added to the dictionary 'dictionary_for_comparison_2' to create a nested dictionary. 
                                self.dictionary_for_comparison_2.update(comment)

                            
                #'value' is being reduced by one to avoid a infinite loop.
                value -= 1

            #The 'picture_placeholder' variable and the just created nested dictionaries are passed to the class 'DataProcessing' to further work with both.
            call_data_processing = DataProcessing(picture_placeholder = self.picture_placeholder)
            call_data_processing.tokenizer(comments_to_compare_1 = self.dictionary_for_comparison_1, comments_to_compare_2 = self.dictionary_for_comparison_2)
            

    #Declaration of the 'compare_albums' function. 
    def compare_albums(self):

        #Iterating over every widget in the current frame and removes it. This way the program avoids that buttons that are not needed remain and only the neccessary ones are loaded. 
        for empty_buttons in  self.frame_buttons_analysis_class.winfo_children():
            empty_buttons.destroy()

        #Creation of the button to compare albums together with the determination of its position. With 'command' the 'open_file' function is called to select files. 
        self.button_compare_albums = tk.Button(self.frame_buttons_analysis_class, text = "Compare albums", command = lambda: self.open_file(value = 2))
        self.button_compare_albums.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to create a visual for the results of the compared albums together with the determination of its position. The button is 'disabled'. 
        self.button_create_visual = tk.Button(self.frame_buttons_analysis_class, text = "Create Visual", state = "disabled")
        self.button_create_visual.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to create a report together with the determination of its position. With 'command' the 'DataProcessing' class is called for further processing. 
        self.button_create_report = tk.Button(self.frame_buttons_analysis_class, text = "Create Report", command = lambda: DataProcessing(picture_placeholder = self.picture_placeholder
                                                                                                                                          ).create_report(self.dictionary_for_comparison_1, self.dictionary_for_comparison_2))
        self.button_create_report.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to create a dashboard together with the determination of its position. With 'command' the 'DataProcessing' class is called for further processing.
        self.button_create_dashboard = tk.Button(self.frame_buttons_analysis_class, text = "Create Dashboard", command = lambda: DataProcessing().create_dashboard(self.dictionary_for_comparison_1, self.dictionary_for_comparison_2))
        self.button_create_dashboard.grid(row = 3, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to return to the analysis menu together with the determination of its position. With 'command' the current frame is removed and the one from the analysis menu is being loaded.
        self.button_return_to_analysis_menu = tk.Button(self.frame_buttons_analysis_class, text = "Go back", command = lambda:
                                       (self.frame_buttons_analysis_class.grid_forget(), self.frame_buttons_analysis_menu.grid(row = 0, column = 0, sticky = "ns")))
        self.button_return_to_analysis_menu.grid(row = 4, column = 0, sticky = "ew", padx = 5, pady = 5)

        #The frame of the analysis menu is removed and the frame of the analysis class is shown. 
        self.frame_buttons_analysis_menu.grid_forget()
        self.frame_buttons_analysis_class.grid(row = 0, column = 0, sticky = "ns")

    #Declaration of the 'analyse_comments' function.     
    def analyse_comments(self):

        #Iterating over every widget in the current frame and removes it. This way the program avoids that buttons that are not needed remain and only the neccessary ones are loaded. 
        for empty_buttons in  self.frame_buttons_analysis_class.winfo_children():
            empty_buttons.destroy()

        #Creation of the button to analyze comments together with the determination of its position. With 'command' the 'open_file' function is called to select a file.
        self.button_analyse_comments = tk.Button(self.frame_buttons_analysis_class, text = "Analyse Comments", command = self.open_file)
        self.button_analyse_comments.grid(row = 0, column = 0, sticky = "ew", padx =5, pady = 5)

        #Creation of the button to create a visual for the results of the compared albums together with the determination of its position. The button is 'disabled'. 
        self.button_create_visual = tk.Button(self.frame_buttons_analysis_class, text = "Create Visual", command = lambda: DataProcessing(picture_placeholder = self.picture_placeholder
                                                                                                                                          ).create_visual(self.dictionary_for_comments))
        self.button_create_visual.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to create a report together with the determination of its position. The button is disabled because this functionality is not needed. Every information is displayed with a visual. 
        self.button_create_report = tk.Button(self.frame_buttons_analysis_class, text = "Create Report", state = "disabled")
        self.button_create_report.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to create a dashboard together with the determination of its position. The button is disabled because this functionality is not needed. Every information is displayed with a visual.
        self.button_create_dashboard = tk.Button(self.frame_buttons_analysis_class, text = "Create Dashboard", state = "disabled")
        self.button_create_dashboard.grid(row = 3, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to return to the analysis menu together with the determination of its position. With 'command' the current frame is removed and the one from the analysis menu is being loaded.
        self.button_return_to_analysis_menu = tk.Button(self.frame_buttons_analysis_class, text = "Go back", command = lambda:
                                       (self.frame_buttons_analysis_class.grid_forget(), self.frame_buttons_analysis_menu.grid(row = 0, column = 0, sticky = "ns")))
        self.button_return_to_analysis_menu.grid(row = 4, column = 0, sticky = "ew", padx = 5, pady = 5)

        #The frame of the analysis menu is removed and the frame of the analysis class is shown. 
        self.frame_buttons_analysis_menu.grid_forget()
        self.frame_buttons_analysis_class.grid(row = 0, column = 0, sticky = "ns")

    #Declaration of the 'analyse_a_single_comment' function. 
    def analyse_a_single_comment(self):

        #Iterating over every widget in the current frame and removes it. This way the program avoids that buttons that are not needed remain and only the neccessary ones are loaded. 
        for empty_buttons in  self.frame_buttons_analysis_class.winfo_children():
            empty_buttons.destroy()

        #Creation of the button to analyze a single comment together with the determination of its position. With 'command' the 'DataProcessing' class is called for further processing.
        #The button is disabled as long as the user hasn't entered a comment and pressed enter. 
        self.button_analyse_single_comment = tk.Button(self.frame_buttons_analysis_class, text = "Analyse a single Comment",
                                                       command = lambda: DataProcessing(picture_placeholder = self.picture_placeholder).tokenizer(single_comment_to_analyze = self.entry_comment.get().strip()), state = "disabled")
        self.button_analyse_single_comment.grid(row = 0, column = 0, sticky = "ew", padx =5, pady = 5)

        #Creation of the button to create a visual for the results of the compared albums together with the determination of its position. The button is 'disabled'. 
        self.button_create_visual = tk.Button(self.frame_buttons_analysis_class, text = "Create Visual", state = "disabled")
        self.button_create_visual.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to create a report together with the determination of its position. The button is 'disabled'.
        self.button_create_report = tk.Button(self.frame_buttons_analysis_class, text = "Create Report", state = "disabled")
        self.button_create_report.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to create a dashboard together with the determination of its position. The button is 'disabled'.
        self.button_create_dashboard = tk.Button(self.frame_buttons_analysis_class, text = "Create Dashboard", state = "disabled")
        self.button_create_dashboard.grid(row = 3, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of the button to return to the analysis menu together with the determination of its position. With 'command' the current frame is removed and the one from the analysis menu is being loaded.
        self.button_return_to_analysis_menu = tk.Button(self.frame_buttons_analysis_class, text = "Go back", command = lambda:
                                       (self.frame_buttons_analysis_class.grid_forget(), self.frame_buttons_analysis_menu.grid(row = 0, column = 0, sticky = "ns")))
        self.button_return_to_analysis_menu.grid(row = 8, column = 0, sticky = "ew", padx = 5, pady = 5)

        #Creation of a label that is explaining where the user should enter his comment.
        tk.Label(self.frame_buttons_analysis_class, text = "Enter the comment here and press 'Enter'.").grid(row = 4)

        #Creation of a entry field where the user can input a comment together with the determination of its position. 
        self.entry_comment = tk.Entry(self.frame_buttons_analysis_class)
        self.entry_comment.grid(row = 5, column = 0)

        #Pressing the enter key is connected with the function 'check_entry' which enables the button 'Analyse a single Comment'. 
        self.entry_comment.bind("<Return>", self.check_entry)

        #The frame of the analysis menu is removed and the frame of the analysis class is shown. 
        self.frame_buttons_analysis_menu.grid_forget()
        self.frame_buttons_analysis_class.grid(row = 0, column = 0, sticky = "ns")

        
