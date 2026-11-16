#Import of all the needed libraries. 
import os
import tkinter as tk
from datetime import datetime

#Declaration of the class 'DataProcessing' which purpose it is to analyze comments and classify them. 
class DataProcessing:

    #Declaration of the '__init__' method to assign the needed variables. 
    def __init__(self, single_comment_to_analyze = None, multiple_comments_to_analyze = None, comments_to_compare_1 = None, comments_to_compare_2 = None, picture_placeholder = None):

        self.single_comment_to_analyze = single_comment_to_analyze
        self.multiple_comments_to_analyze = multiple_comments_to_analyze
        self.comments_to_compare_1 = comments_to_compare_1
        self.comments_to_compare_2 = comments_to_compare_2
        self.picture_placeholder = picture_placeholder

    #Declaration of the 'tokenizer' function which serves to tokenize single comments and multiple comments. 
    def tokenizer(self, single_comment_to_analyze = None, multiple_comments_to_analyze = None, comments_to_compare_1 = None, comments_to_compare_2 = None):

        #'if-else'-structure to first check if the needed elements for the tokenization are already installed.
        #Creating the path and downloading everything if not or checking further to make sure the necessary elements are really there. Otherwise it will download them as well. 
        if not os.path.exists("transformer"):

            #Creates a directory.
            os.makedirs("transformer")
            print("Creating a new directory for the transformer...", end="")
            time.sleep(2)
            print("Done.")

            #Printout to inform the user that the transformer will be downloaded.
            print("Downloading the transformer now. This will take some time...", end="")
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            tokenizer.save_pretrained("transformer")

            from transformers import AutoModelForSequenceClassification
            model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
            model.save_pretrained("transformer")

            #Prinout when everythin is done.
            print("Done.")

        #'elif' for when the directory where the transformer is located exists.
        elif os.path.exists("transformer"):

            #Checks the directory for files.
            required_files = os.listdir("transformer")

            #Downloading everything if any of the needed elements/files are missing.
            if "config.json" not in required_files or "model.safetensors" not in required_files or "tokenizer.json" not in required_files or "tokenizer_config.json" not in required_files:

                print("Downloading the transformer now. This will take some time...", end="")
                from transformers import AutoTokenizer
                tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
                tokenizer.save_pretrained("transformer")

                from transformers import AutoModelForSequenceClassification
                model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
                model.save_pretrained("transformer")

                #Prinout when everythin is done.
                print("Done.")

            #Skipping the downloading part when not only the directory but also the files are there.
            else:
                print("Transformer is already installed.")

        #Legacy 'else' that is never trigged because of the 'elif' above. 
        else:
            print("Transformer and directory are both here. Let's continue with the ML process.")


        #Failsafe that the 'AutoTokenizer' is downloaded in any case.
        from transformers import AutoTokenizer
        #Library to later create a dataset that is suitable for 'huggingface'. 
        from datasets import Dataset

        #'if-else' structure which differentiates between variables that represent single comments, multiple comments and comments to compare.
        #This first 'if' is executed when the variable 'single_comment_to_analyze' is not 'None'. 
        if single_comment_to_analyze != None:

            #To load the transformer and assign it to the variable 'tokenizer'.
            tokenizer = AutoTokenizer.from_pretrained("transformer")

            #Pushing every text to the tokenizer with needed settings for the tokenization process.
            #Settings have been taken from 'huggingface'.
            tokenized_single_comment = tokenizer(

                #Passing the texts. 
                single_comment_to_analyze,
                #Not addings any tokens at the moment.
                padding = False,
                #Texts are made shorter if the are bigger than allowed.
                truncation = True,
                #Text are allowed to be 512 tokens at max.
                max_length = 512,
                #return_tensors = "pt", Entfernt, damit Trainer Umwandlung in PyTorch selber übernimmt
                #'distilbert' needs special tokens - it is allowed to add them.
                add_special_tokens = True,
                #Creating an attention mask that is needed for the training later. 
                return_attention_mask = True

                )

            #Calls the function 'analyze_single_comment' with the tokenized data. Assigns the result to the variable 'analyze'.
            analyze = self.analyze_single_comment(tokenized_single_comment)

            #Dictionary with which a translation of the numeric label to the related emotion is possible. 
            label_to_emotion = {
                0: "Sadness",
                1: "Joy",
                2: "Love",
                3: "Anger",
                4: "Fear",
                5: "Surprise"
                }

            #Assigning the emotion to the variable 'emotion' that has been translated with 'label_to_emotion'.
            emotion = label_to_emotion[analyze]

            #Deletes the current content of 'picture_placeholder' from top to bottom.
            self.picture_placeholder.delete("1.0", tk.END)

            #The currently analyzed comment is put into 'picture_placeholder'.
            self.picture_placeholder.insert(tk.END, single_comment_to_analyze + "\n")

            #The detected emotion below the comment is put into 'picture_placeholder'.
            self.picture_placeholder.insert(tk.END, "Emotion: " + emotion + "\n\n")

        #'elif' that is executed when 'multiple_comments_to_analyze' is not empty or 'None'.
        elif multiple_comments_to_analyze != None:

            #To load the transformer and assign it to the variable 'tokenizer'.
            tokenizer = AutoTokenizer.from_pretrained("transformer")

            #Iterating over every comment in the list of comments. 
            for single_comment in multiple_comments_to_analyze:

                #Pushing every text to the tokenizer with needed settings for the tokenization process.
                #Settings have been taken from 'huggingface'.
                tokenized_single_comment = tokenizer(

                    #Passing the texts. 
                    single_comment,
                    #Not addings any tokens at the moment.
                    padding = False,
                    #Texts are made shorter if the are bigger than allowed.
                    truncation = True,
                    #Text are allowed to be 512 tokens at max.
                    max_length = 512,
                    #return_tensors = "pt", Entfernt, damit Trainer Umwandlung in PyTorch selber übernimmt
                    #'distilbert' needs special tokens - it is allowed to add them.
                    add_special_tokens = True,
                    #Creating an attention mask that is needed for the training later. 
                    return_attention_mask = True

                    )

                #Assigns the input ids and the attention mask to the current comment. 
                multiple_comments_to_analyze[single_comment]["input_ids"] = tokenized_single_comment["input_ids"]
                multiple_comments_to_analyze[single_comment]["attention_mask"] = tokenized_single_comment["attention_mask"]

                #Calls the function 'analyze_single_comment' with the tokenized data. Assigns the result to the variable 'analyze'.
                analyze = self.analyze_single_comment(tokenized_single_comment)

                #The numeric value, meaning the emotion, is assigned to the current comment at the key 'label'.
                multiple_comments_to_analyze[single_comment]["label"] = analyze

                #Dictionary with which a translation of the numeric label to the related emotion is possible. 
                label_to_emotion = {
                    0: "Sadness",
                    1: "Joy",
                    2: "Love",
                    3: "Anger",
                    4: "Fear",
                    5: "Surprise"
                    }

                #Assigning the emotion to the key 'emotion' that has been translated with 'label_to_emotion'.
                multiple_comments_to_analyze[single_comment]["emotion"] = label_to_emotion[analyze]

            #Assigning the album name of the current comment to the variable 'get_album'.
            get_album = multiple_comments_to_analyze[single_comment]["album"]

            #Deletes the current content of 'picture_placeholder' from top to bottom.
            self.picture_placeholder.delete("1.0", tk.END)

            #The name of the album is put into 'picture_placeholder' and displayed in the GUI. 
            self.picture_placeholder.insert(tk.END, "Album: " + get_album + "\n\n")

            #Every comment is displayed in the GUI together with the detected emotion. 
            for comment in multiple_comments_to_analyze:

                self.picture_placeholder.insert(tk.END, comment.strip() + "\n")

                self.picture_placeholder.insert(tk.END, "Emotion: " + multiple_comments_to_analyze[comment]["emotion"] + "\n\n")

        #'elif' that is executed when 'comments_to_compare_1' and 'comments_to_compare_2' are not empty or not 'None'. 
        elif comments_to_compare_1 != None and comments_to_compare_2 != None:

            #To load the transformer and assign it to the variable 'tokenizer'.
            tokenizer = AutoTokenizer.from_pretrained("transformer")

            #Iterating over every comment in the dictionary 'comments_to_compare_1'. 
            for single_comment in comments_to_compare_1:

                #Pushing every text to the tokenizer with needed settings for the tokenization process.
                #Settings have been taken from 'huggingface'.
                tokenized_single_comment = tokenizer(

                    #Passing the texts. 
                    single_comment,
                    #Not addings any tokens at the moment.
                    padding = False,
                    #Texts are made shorter if the are bigger than allowed.
                    truncation = True,
                    #Text are allowed to be 512 tokens at max.
                    max_length = 512,
                    #return_tensors = "pt", Entfernt, damit Trainer Umwandlung in PyTorch selber übernimmt
                    #'distilbert' needs special tokens - it is allowed to add them.
                    add_special_tokens = True,
                    #Creating an attention mask that is needed for the training later. 
                    return_attention_mask = True

                    )

                #Assigns the input ids and the attention mask to the current comment of the dictionary 'comments_to_compare_1'. 
                comments_to_compare_1[single_comment]["input_ids"] = tokenized_single_comment["input_ids"]
                comments_to_compare_1[single_comment]["attention_mask"] = tokenized_single_comment["attention_mask"]

                #Calls the function 'analyze_single_comment' with the tokenized data. Assigns the result to the variable 'analyze'.
                analyze = self.analyze_single_comment(tokenized_single_comment)

                #The numeric value, meaning the emotion, is assigned to the current comment at the key 'label'.
                comments_to_compare_1[single_comment]["label"] = analyze

                #Dictionary with which a translation of the numeric label to the related emotion is possible.
                label_to_emotion = {
                    0: "Sadness",
                    1: "Joy",
                    2: "Love",
                    3: "Anger",
                    4: "Fear",
                    5: "Surprise"
                    }

                #Assigning the emotion to the key 'emotion' that has been translated with 'label_to_emotion'.
                comments_to_compare_1[single_comment]["emotion"] = label_to_emotion[analyze]

            #Assigning the album name of the current comment to the variable 'get_album'.
            get_album = comments_to_compare_1[single_comment]["album"]

            #Deletes the current content of 'picture_placeholder' from top to bottom.
            self.picture_placeholder.delete("1.0", tk.END)

            #The name of the album is put into 'picture_placeholder' and displayed in the GUI. 
            self.picture_placeholder.insert(tk.END, "Album: " + get_album + "\n\n")

            #Every comment is displayed in the GUI together with the detected emotion. 
            for comment in comments_to_compare_1:

                self.picture_placeholder.insert(tk.END, comment.strip() + "\n")

                self.picture_placeholder.insert(tk.END, "Emotion: " + comments_to_compare_1[comment]["emotion"] + "\n\n")

            #Iterating over every comment in the dictionary 'comments_to_compare_2'.
            for single_comment in comments_to_compare_2:

                #Pushing every text to the tokenizer with needed settings for the tokenization process.
                #Settings have been taken from 'huggingface'.
                tokenized_single_comment = tokenizer(

                    #Passing the texts. 
                    single_comment,
                    #Not addings any tokens at the moment.
                    padding = False,
                    #Texts are made shorter if the are bigger than allowed.
                    truncation = True,
                    #Text are allowed to be 512 tokens at max.
                    max_length = 512,
                    #return_tensors = "pt", Entfernt, damit Trainer Umwandlung in PyTorch selber übernimmt
                    #'distilbert' needs special tokens - it is allowed to add them.
                    add_special_tokens = True,
                    #Creating an attention mask that is needed for the training later. 
                    return_attention_mask = True

                    )

                #Assigns the input ids and the attention mask to the current comment of the dictionary 'comments_to_compare_1'. 
                comments_to_compare_2[single_comment]["input_ids"] = tokenized_single_comment["input_ids"]
                comments_to_compare_2[single_comment]["attention_mask"] = tokenized_single_comment["attention_mask"]

                #Calls the function 'analyze_single_comment' with the tokenized data. Assigns the result to the variable 'analyze'.
                analyze = self.analyze_single_comment(tokenized_single_comment)

                #The numeric value, meaning the emotion, is assigned to the current comment at the key 'label'.
                comments_to_compare_2[single_comment]["label"] = analyze

                #comments_to_compare_2[single_comment]["label"] = analyze

                #Dictionary with which a translation of the numeric label to the related emotion is possible.
                label_to_emotion = {
                    0: "Sadness",
                    1: "Joy",
                    2: "Love",
                    3: "Anger",
                    4: "Fear",
                    5: "Surprise"
                    }

                #Assigning the emotion to the key 'emotion' that has been translated with 'label_to_emotion'.
                comments_to_compare_2[single_comment]["emotion"] = label_to_emotion[analyze]

            #Assigning the album name of the current comment to the variable 'get_album'.
            get_album = comments_to_compare_2[single_comment]["album"]

            #The name of the album is put into 'picture_placeholder' and displayed in the GUI. 
            self.picture_placeholder.insert(tk.END, "Album: " + get_album + "\n\n")

            #Every comment is displayed in the GUI together with the detected emotion.
            for comment in comments_to_compare_2:

                self.picture_placeholder.insert(tk.END, comment.strip() + "\n")

                self.picture_placeholder.insert(tk.END, "Emotion: " + comments_to_compare_2[comment]["emotion"] + "\n\n")

        #'else' that is executed if nothing above is triggered. Here an error message is printed out. 
        else:
            print("Something might have gone wrong! There is nothing to print out.")

    #Declaration if the function 'analyze_single_comment' with takes the tokenized data as argument. 
    #https://huggingface.co/docs/transformers/main/tasks/sequence_classification
    def analyze_single_comment(self, tokenized_single_comment):

        #Import of the needed model/library. 
        from transformers import AutoModelForSequenceClassification
        import torch

        #The trained model is loaded from its directory. 
        call_model = AutoModelForSequenceClassification.from_pretrained("Emotion_Detection_Model_Directory")

        #The model is set to evaluation mode so it can be used for prediction. 
        call_model.eval()

        #Assigning the 'input_ids' values as a PyTorch tensor to the variable 'input_ids'.  
        input_ids = torch.tensor([tokenized_single_comment["input_ids"]])

        #Assigning the 'attention_mask' values as a PyTorch tensor to the variable 'attention_mask'. 
        attention_mask = torch.tensor([tokenized_single_comment["attention_mask"]])

        #No training is needed so the 'gradient calculation' is disabled. 
        torch.set_grad_enabled(False)

        #The model is called with the assigned input ids and the attention mask.
        outputs = call_model(input_ids = input_ids, attention_mask = attention_mask)

        #The label with the highest output value is found and assigned to 'prediction_single_comment'. The result is a integer. 
        prediction_single_comment = outputs.logits.argmax(dim = 1).item()

        #Returning the result. 
        return prediction_single_comment

    #Declaration of the function 'create_value' which takes the dictionary 'multiple_comments_to_visualize' as argument. 
    def create_visual(self, multiple_comments_to_visualize):

        #Deletes the current content of 'picture_placeholder' from top to bottom.
        self.picture_placeholder.delete("1.0", tk.END)

        #Import of 'matplotlib' to create the diagram. 
        import matplotlib.pyplot as plt

        #Dictionary which is used to count the occurrence of each emotion. 
        emotion_counter = {

            "Sadness": 0,
            "Joy": 0,
            "Love": 0,
            "Anger": 0,
            "Fear": 0,
            "Surprise": 0

            }

        #Assigning 'None' to 'album_name'. 
        album_name = None

        #Iteration through every comment, gets the detected emotion and increases the counter for this detected emotion. 
        for comment in multiple_comments_to_visualize:

            emotion = multiple_comments_to_visualize[comment]["emotion"]

            emotion_counter[emotion] += 1

            #Gets the name of the album if 'album_name' is still 'None'. 
            if album_name == None:

                album_name = multiple_comments_to_visualize[comment]["album"]

        #Creation of a bar chart with the emotions as key and their number of occurrence as value. 
        plt.bar(emotion_counter.keys(), emotion_counter.values())

        #Uses the album name as the title of the diagram. 
        plt.title(album_name)

        #The labels of the x- and y-axis are set. 
        plt.xlabel("Emotion")
        plt.ylabel("Number of Comments")

        #Creating the name for a file with a timestamp to make it unique as a 'png' and assign the name to the variable 'filename'. 
        filename = "visual_" + str(int(datetime.now().timestamp())) + ".png"

        #The 'png' meaning the generated diagram is saved. 
        plt.savefig(filename)

        #Closes the current matplot figure to free up RAM. 
        plt.close()

        #Loads the saved image. 
        self.picture_placeholder.visual_image = tk.PhotoImage(file = filename)

        #Displayed the image and with this the generated diagram in the GUI.
        self.picture_placeholder.image_create("1.0", image = self.picture_placeholder.visual_image)

        
    #Declaration of the function 'create_report' which takes 'comments_to_compare_1' and 'comments_to_compare_2' as arguments.
    def create_report(self, comments_to_compare_1, comments_to_compare_2):

        #Deletes the current content of 'picture_placeholder' from top to bottom.
        self.picture_placeholder.delete("1.0", tk.END)

        #Dictionary which is used to count the occurrence of each emotion for 'comments_to_compare_1'.
        emotion_counter_1 = {

            "Sadness": 0,
            "Joy": 0,
            "Love": 0,
            "Anger": 0,
            "Fear": 0,
            "Surprise": 0

            }

        #Dictionary which is used to count the occurrence of each emotion for 'comments_to_compare_2'.
        emotion_counter_2 = {

            "Sadness": 0,
            "Joy": 0,
            "Love": 0,
            "Anger": 0,
            "Fear": 0,
            "Surprise": 0

            }

        #Assigning 'None' to 'album_name_1' and 'album_name_2'. 
        album_name_1 = None

        album_name_2 = None

        #Iteration through every comment, gets the detected emotion and increases the counter for this detected emotion. 
        for comment in comments_to_compare_1:

            emotion = comments_to_compare_1[comment]["emotion"]

            emotion_counter_1[emotion] += 1

            #Gets the name of the album if 'album_name' is still 'None'. 
            if album_name_1 == None:

                album_name_1 = comments_to_compare_1[comment]["album"]

        #Same functionality for the dictionary 'comments_to_compare_2'.
        for comment in comments_to_compare_2:

            emotion = comments_to_compare_2[comment]["emotion"]

            emotion_counter_2[emotion] += 1

            if album_name_2 == None:

                album_name_2 = comments_to_compare_2[comment]["album"]


        #Title of the report that is displayed in the GUI. 
        self.picture_placeholder.insert(tk.END, "Comparison Report\n\n")

        #The name of the album is put into 'picture_placeholder' and displayed in the GUI. 
        self.picture_placeholder.insert(tk.END, "Album: " + album_name_1 + "\n")

        #Iteration through all emotions and displays them together with their number of occurrence. 
        for emotion in emotion_counter_1:

            self.picture_placeholder.insert(tk.END, emotion + ": " + str(emotion_counter_1[emotion]) + "\n")

        #The name of the album is put into 'picture_placeholder' and displayed in the GUI.
        self.picture_placeholder.insert(tk.END, "\nAlbum: " + album_name_2 + "\n")

        #Iteration through all emotions and displays them together with their number of occurrence. 
        for emotion in emotion_counter_2:

            self.picture_placeholder.insert(tk.END, emotion + ": " + str(emotion_counter_2[emotion]) + "\n")

    #Declaration of 'create_dashboard' which takes 'comments_to_compare_1' and 'comments_to_compare_2' as arguments.
    def create_dashboard(self, comments_to_compare_1, comments_to_compare_2):

        #Creation of visuals by calling the function 'create_visual_for_dashboard'.
        visual_1 = self.create_visual_for_dashboard(comments_to_compare_1)
        visual_2 = self.create_visual_for_dashboard(comments_to_compare_2)

        #Creation of reports by calling the function 'create_report_for_dashboard'.
        report_1, report_2 = self.create_report_for_dashboard(comments_to_compare_1, comments_to_compare_2)

        #Creation of a new 'tk' window.
        dashboard_window = tk.Toplevel()

        #Setting title and size of dashboard. 
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("1200x800")

        #Creation of frames for the visuals.
        frame_visual_1 = tk.Frame(dashboard_window)
        frame_visual_2 = tk.Frame(dashboard_window)

        #Creation of frames for the report. 
        frame_report_1 = tk.Frame(dashboard_window)
        frame_report_2 = tk.Frame(dashboard_window)

        #Determination of the position of the frames for the visuals.
        frame_visual_1.grid(row = 0, column = 0, padx = 10, pady = 10)
        frame_visual_2.grid(row = 0, column = 1, padx = 10, pady = 10)

        #Determination of the position of the frames for the visuals. 
        frame_report_1.grid(row = 1, column = 0, padx = 10, pady = 10)
        frame_report_2.grid(row = 1, column = 1, padx = 10, pady = 10)

        #Loading of the first visual.
        load_first_visual = tk.PhotoImage(file = visual_1)
        label_visual_1 = tk.Label(frame_visual_1, image = load_first_visual)
        label_visual_1.pack()

        
        #Loading of the second visual.
        load_second_visual = tk.PhotoImage(file = visual_2)
        label_visual_2 = tk.Label(frame_visual_2, image = load_second_visual)
        label_visual_2.pack()

        #Showing the first report.
        label_report_1 = tk.Label(frame_report_1, text = report_1, justify = "left")
        label_report_1.pack()

        #Showing the second report.
        label_report_2 = tk.Label(frame_report_2, text = report_2, justify = "left")
        label_report_2.pack()

        #Stores a reference to the visuals so they are not removed from RAM.
        dashboard_window.load_first_visual = load_first_visual
        dashboard_window.load_second_visual = load_second_visual
        
    #Creatation of the class 'create_visual_for_dashboard' which takes 'comments_to_compare' as argument. This function is used to create images that are used for a dashboard. 
    def create_visual_for_dashboard(self, comments_to_compare = None):

        #Import of 'matplotlib' to create the diagram. 
        import matplotlib.pyplot as plt

        #Dictionary which is used to count the occurrence of each emotion.
        emotion_counter = {

            "Sadness": 0,
            "Joy": 0,
            "Love": 0,
            "Anger": 0,
            "Fear": 0,
            "Surprise": 0

            }

        #Assigning 'None' to 'album_name'.
        album_name = None

        #Iteration through every comment, gets the detected emotion and increases the counter for this detected emotion. 
        for comment in comments_to_compare:

            emotion = comments_to_compare[comment]["emotion"]

            emotion_counter[emotion] += 1

            #Gets the name of the album if 'album_name' is still 'None'. 
            if album_name == None:

                album_name = comments_to_compare[comment]["album"]

        #Creation of a bar chart with the emotions as key and their number of occurrence as value. 
        plt.bar(emotion_counter.keys(), emotion_counter.values())

        #Uses the album name as the title of the diagram. 
        plt.title(album_name)

        #The labels of the x- and y-axis are set.
        plt.xlabel("Emotion")
        plt.ylabel("Number of Comments")

        #Creating the name for a file with a timestamp to make it unique as a 'png' and assign the name to the variable 'filename'. 
        filename = "visual_" + str(datetime.now().timestamp()) + ".png"

        #The 'png' meaning the generated diagram is saved.
        plt.savefig(filename)

        #Closes the current matplot figure to free up RAM.
        plt.close()

        #Returns the visual.
        return filename

    #Declaration of the function 'create_report_for_dashboard'. 
    def create_report_for_dashboard(self, comments_to_compare_1, comments_to_compare_2):

        #Dictionary which is used to count the occurrence of each emotion for 'comments_to_compare_1'.
        emotion_counter_1 = {

            "Sadness": 0,
            "Joy": 0,
            "Love": 0,
            "Anger": 0,
            "Fear": 0,
            "Surprise": 0

            }

        #Dictionary which is used to count the occurrence of each emotion for 'comments_to_compare_2'.
        emotion_counter_2 = {

            "Sadness": 0,
            "Joy": 0,
            "Love": 0,
            "Anger": 0,
            "Fear": 0,
            "Surprise": 0

            }

        #Assigning 'None' to 'album_name_1' and 'album_name_2'.
        album_name_1 = None

        album_name_2 = None

        #Iteration through every comment, gets the detected emotion and increases the counter for this detected emotion.
        for comment in comments_to_compare_1:

            emotion = comments_to_compare_1[comment]["emotion"]

            emotion_counter_1[emotion] += 1

            #Gets the name of the album if 'album_name' is still 'None'. 
            if album_name_1 == None:

                album_name_1 = comments_to_compare_1[comment]["album"]

        #Same functionality for the dictionary 'comments_to_compare_2'.
        for comment in comments_to_compare_2:

            emotion = comments_to_compare_2[comment]["emotion"]

            emotion_counter_2[emotion] += 1

            if album_name_2 == None:

                album_name_2 = comments_to_compare_2[comment]["album"]

        #Beginning of the creation of the first report by assigning the word 'Album' plus the name of the album and a new line to it. 
        report_1 = "Album: " + album_name_1 + "\n"

        #Iteration through all emotions in 'emotion_counter_1'. 
        for emotion in emotion_counter_1:

            #Assigns the emotion, its number of occurence and a new line to 'report_1'.
            report_1 += emotion + ": " + str(emotion_counter_1[emotion]) + "\n"

        #Same functionality for 'report_2'.
        report_2 = "Album: " + album_name_2 + "\n"

        for emotion in emotion_counter_2:

            report_2 += emotion + ": " + str(emotion_counter_2[emotion]) + "\n"

        #Returns both reports. 
        return report_1, report_2 






























            


            
