#Loading libraries.
import os
import pandas as pd
import time
import re
from ftfy import fix_text

#Class for any work related to the initial data.
class Data:

    def __init__(self, dataframes_to_preprocess = None):
        self.dataframes_to_preprocess = dataframes_to_preprocess

    #Function with which the user can load the data of 'csv' files only which are in the same folder as the program.
    #
    #!!! Entweder andere Option wählen, oder mindestens im FAQ darauf ansprechen, dass die csv im selben Ordner wie das Programm sein müssen !!!
    #
    def load_data(self):
        
        loaded_dataframes = {}

        #'While' based loop so the user isn't returned to the 'Main Menu' after selecting an option.
        while True:

            #Simple printout to give the user some information.
            print("Please check the print out down below to see which files you can select to load data from. Please note that only '.csv'-files are shown.\n")

            #Assignment of the files that are in the folder to the variable 'folder_csv'.
            folder_csv = os.listdir()

            #Loop using 'for' to iterate through 'folder_csv'. The variable 'number' is for numbering the different '.csv' files.
            number = 1
            for csv in folder_csv:

                #Print out the name of the file if '.csv' is in it together with the variable 'number' and increase 'number' by one.
                if ".csv" in csv:
                    print(str(number) + ". " + csv)
                    number += 1
            
            #Using the method 'input' so the user can select a '.csv'
            load_data_input = input("\nFrom which '.csv' to you want to load data? Type 'cancel' if you don't want to load any data. Otherwise you can select a file by typing in the number next to it.\n")

            #Typing in 'cancel' will return the user to the 'Main Menu'. 'Time.sleep' to pause the process for one second and therefore making sure the user understands what is happening.
            #With 'return' the user will be send back to the 'Main Menu' while keeping any loaded data.
            if load_data_input == "cancel":
                print("Returning you to the 'Main Menu'.")
                time.sleep(1)
                return loaded_dataframes

            #First option with which the user can load the data of the 'test.csv'. 
            elif load_data_input == "1" or load_data_input == "1." or load_data_input == "test.csv":

                #Load data from the 'test.csv'-file and taking the first row as headline ('header = 0').
                dataframe_test = pd.read_csv("test.csv", header = 0)

                #Create a list of names for the columns of the dataframe.
                column_names = ["Text", "Label"]
                
                #Rename the columns.
                dataframe_test.columns = column_names

                #Usage of the function 'insert' to add a new column named 'Mapping' at postion 2 of the dataframe without values.
                dataframe_test.insert(loc = 2, column = "Mapping", value = "")

                #Using 'iterrows' to iterate over the dataframe, meaning the data of the rows and their index.
                for index, row in dataframe_test.iterrows():

                    #Using 'loc' to assign the lables of each row their specific emotion to improve the readability of the dataframe.
                    if row["Label"] == 0:
                        dataframe_test.loc[index, "Mapping"] = "Sadness"

                    elif row["Label"] == 1:
                        dataframe_test.loc[index, "Mapping"] = "Joy"

                    elif row["Label"] == 2:
                        dataframe_test.loc[index, "Mapping"] = "Love"

                    elif row["Label"] == 3:
                        dataframe_test.loc[index, "Mapping"] = "Anger"

                    elif row["Label"] == 4:
                        dataframe_test.loc[index, "Mapping"] = "Fear"

                    elif row["Label"] == 5:
                        dataframe_test.loc[index, "Mapping"] = "Surprise"

                    else:
                        pass

                #Printing the dataframe out - simply for the coding phase.
                print(dataframe_test)

                #Using the method 'input' to ask the user if he wants to continue and maybre create other dataframes or simply wants to return to the 'Main Menu'.
                continue_or_break = input("Your dataframe of the 'test.csv' has been created. Do you want to continue your work here or want to return to the 'Main Menu'?"
                                          " Type 'yes' for continuing or 'no' to return to the 'Main Menu'\n")

                #Typing in 'yes' or 'Yes' will keep the user here where he can load other data into a dataframe.
                if continue_or_break == 'yes' or continue_or_break == 'Yes':
                    
                    #loaded_dataframes.append(dataframe_test)
                    loaded_dataframes["test"] = dataframe_test

                #Typing in 'no' or 'No' will return the user to the 'Main Menu'. 'Time.sleep' to pause the process for one second and therefore making sure the user understands what is happening.
                #With 'return' the user will be send back to the 'Main Menu' while keeping any loaded data.
                elif continue_or_break == 'no' or continue_or_break == 'No':
                    
                    print("Returning you to the 'Main Menu'.")
                    time.sleep(1)
                    loaded_dataframes["test"] = dataframe_test
                    return loaded_dataframes
                
                #Any invalid input will keep the user here.
                else:
                    loaded_dataframes["test"] = dataframe_test
                    print("Invalid input. Keeping you here for now.")

            #Second option for the user to load the data from the 'training.csv'-file.
            elif load_data_input == "2" or load_data_input == "2." or load_data_input == "training.csv":

                #Load data from the 'test.csv'-file and taking the first row as headline ('header = 0').
                dataframe_training = pd.read_csv("training.csv", header = 0)

                #Create a list of names for the columns of the dataframe.
                column_names = ["Text", "Label"]
                
                #Rename the columns.
                dataframe_training.columns = column_names

                #Usage of the function 'insert' to add a new column named 'Mapping' at postion 2 of the dataframe without values.
                dataframe_training.insert(loc = 2, column = "Mapping", value = "")

                #Using 'iterrows' to iterate over the dataframe, meaning the data of the rows and their index.
                for index, row in dataframe_training.iterrows():

                    #Using 'loc' to assign the lables of each row their specific emotion to improve the readability of the dataframe.
                    if row["Label"] == 0:
                        dataframe_training.loc[index, "Mapping"] = "Sadness"

                    elif row["Label"] == 1:
                        dataframe_training.loc[index, "Mapping"] = "Joy"

                    elif row["Label"] == 2:
                        dataframe_training.loc[index, "Mapping"] = "Love"

                    elif row["Label"] == 3:
                        dataframe_training.loc[index, "Mapping"] = "Anger"

                    elif row["Label"] == 4:
                        dataframe_training.loc[index, "Mapping"] = "Fear"

                    elif row["Label"] == 5:
                        dataframe_training.loc[index, "Mapping"] = "Surprise"

                    else:
                        pass

                #Printing the dataframe out - simply for the coding phase.
                print(dataframe_training)

                #Using the method 'input' to ask the user if he wants to continue and maybre create other dataframes or simply wants to return to the 'Main Menu'.
                continue_or_break = input("Your dataframe of the 'test.csv' has been created. Do you want to continue your work here or want to return to the 'Main Menu'?"
                                          " Type 'yes' for continuing or 'no' to return to the 'Main Menu'\n")

                #Typing in 'yes' or 'Yes' will keep the user here where he can load other data into a dataframe.
                if continue_or_break == 'yes' or continue_or_break == 'Yes':
                    
                    #loaded_dataframes.append(dataframe_training)
                    loaded_dataframes["training"] = dataframe_training

                #Typing in 'no' or 'No' will return the user to the 'Main Menu'. 'Time.sleep' to pause the process for one second and therefore making sure the user understands what is happening.
                #With 'return' the user will be send back to the 'Main Menu' while keeping any loaded data.
                elif continue_or_break == 'no' or continue_or_break == 'No':
                    
                    print("Returning you to the 'Main Menu'.")
                    time.sleep(1)
                    loaded_dataframes["training"] = dataframe_training
                    return loaded_dataframes

                #Any invalid input will keep the user here.
                else:
                    loaded_dataframes["training"] = dataframe_training
                    print("Invalid input. Keeping you here for now.")

            #Third option to load the data from the 'validation.csv'-file.
            elif load_data_input == "3" or load_data_input == "3." or load_data_input == "validation.csv":

                #Load data from the 'test.csv'-file and taking the first row as headline ('header = 0').
                dataframe_validation = pd.read_csv("validation.csv", header = 0)

                #Create a list of names for the columns of the dataframe.
                column_names = ["Text", "Label"]
                
                #Rename the columns.
                dataframe_validation.columns = column_names

                #Usage of the function 'insert' to add a new column named 'Mapping' at postion 2 of the dataframe without values.
                dataframe_validation.insert(loc = 2, column = "Mapping", value = "")

                #Using 'iterrows' to iterate over the dataframe, meaning the data of the rows and their index.
                for index, row in dataframe_validation.iterrows():

                    #Using 'loc' to assign the lables of each row their specific emotion to improve the readability of the dataframe.
                    if row["Label"] == 0:
                        dataframe_validation.loc[index, "Mapping"] = "Sadness"

                    elif row["Label"] == 1:
                        dataframe_validation.loc[index, "Mapping"] = "Joy"

                    elif row["Label"] == 2:
                        dataframe_validation.loc[index, "Mapping"] = "Love"

                    elif row["Label"] == 3:
                        dataframe_validation.loc[index, "Mapping"] = "Anger"

                    elif row["Label"] == 4:
                        dataframe_validation.loc[index, "Mapping"] = "Fear"

                    elif row["Label"] == 5:
                        dataframe_validation.loc[index, "Mapping"] = "Surprise"

                    else:
                        pass

                #Printing the dataframe out - simply for the coding phase.
                print(dataframe_validation)

                #Using the method 'input' to ask the user if he wants to continue and maybre create other dataframes or simply wants to return to the 'Main Menu'.
                continue_or_break = input("Your dataframe of the 'test.csv' has been created. Do you want to continue your work here or want to return to the 'Main Menu'?"
                                          " Type 'yes' for continuing or 'no' to return to the 'Main Menu'\n")

                #Typing in 'yes' or 'Yes' will keep the user here where he can load other data into a dataframe.
                if continue_or_break == 'yes' or continue_or_break == 'Yes':
                    
                    loaded_dataframes["validation"] = dataframe_validation
                    #loaded_dataframes.append(dataframe_validation)

                #Typing in 'no' or 'No' will return the user to the 'Main Menu'. 'Time.sleep' to pause the process for one second and therefore making sure the user understands what is happening.
                elif continue_or_break == 'no' or continue_or_break == 'No':
                    
                    print("Returning you to the 'Main Menu'.")
                    time.sleep(1)
                    loaded_dataframes["validation"] = dataframe_validation
                    #loaded_dataframes.append(dataframe_validation)
                    return loaded_dataframes
                    #break

                else:
                    loaded_dataframes["validation"] = dataframe_validation
                    print("Invalid input. Keeping you here for now.")
                    
                

            #Rejection of non valid input which shall protect the program as well as the user from unintentiinal mistakes. 
            else:
                print("Your input was not valid. Please retype.")

    #Function to preprocess the data and therefore cleaning it for the tokenization and training. 
    def preprocessing(self, dataframes = None):

        #Printout where the user can start the preprocessing process manually. 
        preprocess_data_input = input("Let's start with the preprocessing, shall we? Type 'yes' to start or 'no' to cancel\n")

        #In case the user types in 'yes' or 'Yes' the process will stark. 
        if preprocess_data_input == "yes" or preprocess_data_input == "Yes":

            #Simple printout to inform the user that the process has started.
            #'count_iteration' is used to check if the process has reached the finale dataframe, which is important to know so that the correct state can be described.
            print("Let's start with the process. This is completley automatic.\n")
            count_iteration = 0
            
            #Iterate with a 'for'-loop over the keys and values of the dataframe. 
            for name, dataframe in self.dataframes_to_preprocess.items():

                #Printout to inform the user of the process that is starting and printing out the length of the dataframe so the user can compare it with the length after the preprocessing.
                print("Name of the dataframe that is currently preprocessed: " + name)
                print("\n")
                len_before = len(dataframe)
                print("The dataframe " + name + " has currently " + str(len_before) + " rows.")
                count_iteration += 1

                #Empty rows are being removed.
                print("Checking for empty rows...", end="")
                time.sleep(1)
                dataframe = dataframe.dropna()
                print("Done.")

                #Broken signs like 'Ã¶Ã' are being removed - this function is currently not needed. Broken signs are getting fixed when loaded. Legacy code.
                """
                print("Removing brokens signs...", end="")
                time.sleep(1)
                self.dataframes_to_preprocess = self.dataframes_to_preprocess["Text"].apply(fix_text)
                print("Done.")
                """

                #Remove any HTML-Code.
                print("Removing HTML-Code...", end="")
                time.sleep(1)
                print("Done.")
                #Iterating over the dataframe to get the content of each row, looking for HTML-Code and replacing any of it before writing the changed string back to the dataframe.
                for index, row in dataframe.iterrows():
                    text = str(row["Text"])
                    text = re.sub(r"<.*?>", "", text)

                    dataframe.at[index, "Text"] = text

                #Remove duplicates with the method 'drop_duplicates()'.
                print("Removing duplicates...", end="")
                time.sleep(1)
                dataframe = dataframe.drop_duplicates()
                print("Done.")

                #Normalize whitespaces.
                #The code creates strings, erases spaces and especially spaces at the beginning or end and writing the changed text back.
                print("Normalizing whitespaces...", end="")
                time.sleep(1)
                dataframe["Text"] = (dataframe["Text"].astype(str).str.replace(r" +", " ", regex = True).str.strip())
                print("Done.\n")

                #Printout of the length of the dataframe after preprocessing. 
                len_afterwards = len(dataframe)
                print("The dataframe " + name + " has " + str(len_afterwards) + " rows after the preprocessing.")

                #The processed dataframe is assigned to the object. 
                self.dataframes_to_preprocess[name] = dataframe

                #Printout where the user is taking back to the 'Main Menu' when the end of the currently processed dataframe is reached. Otherwise it continues with the next dataframe and informs you whether changes
                #have been made or not.
                if count_iteration == len(self.dataframes_to_preprocess):
                    print("Preprocessing completed. Taking you back to the 'Main Menu'.")
                    time.sleep(2)
                    return self.dataframes_to_preprocess
                elif len_before == len_afterwards:
                    print("Preprocessing successful, but no parts needed to be removed. Let's continue with the next one\n.")
                    self.dataframes_to_preprocess[name] = dataframe
                    time.sleep(2)
                else:
                    print("Preprocessing successful, not needed parts have been removed. Let's continue with the next one\n.")
                    self.dataframes_to_preprocess[name] = dataframe
                    time.sleep(2)
                    
        #Option for the user to return to the 'Main Menu' when he types in 'no' or 'No'.
        elif preprocess_data_input == "no" or preprocess_data_input == "No":
            print("Returning you to the 'Main Menu'.")
            time.sleep(1)
            return self.dataframes_to_preprocess

        #Rejection of invalid input.
        else:
            print("Invalid input. Keeping you here for now.")

    #Function called 'tokenizer' to download the needed libraries and models from 'huggingface' as well as tokenization of the dataframes. 
    def tokenizer(self, dataframes = None):

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

        #To load the transformer and assign it to the variable 'tokenizer'.
        tokenizer = AutoTokenizer.from_pretrained("transformer")

        #Creation of an empty dictionary.
        tokenizer_dictionary = {}

        #Iteration over the keys and values of the dataframes. 
        for name, dataframe in self.dataframes_to_preprocess.items():

            #Preprocessing part where every row missing 'Text' or 'Label' is being deleted. 
            dataframe_in_progress = dataframe.dropna(subset = ["Text", "Label"])

            #Texts are being converted to strings and assigns them to a list.
            texts = dataframe_in_progress["Text"].astype(str).tolist()

            #Labels are being converted to strings and assigns them to a list.
            labels = dataframe_in_progress["Label"].astype(int).tolist()

            #Pushing every text to the tokenizer with needed settings for the tokenization process.
            #Settings have been taken from 'huggingface'.
            convert_strings_to_numbers = tokenizer(

            #Passing the texts. 
            texts,
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

            #'labels' are added to the tokenized data.
            convert_strings_to_numbers["labels"] = labels

            #Transformation of the tokenized data into a dataset that can be used by the 'huggingface' platform later.
            tokenized_dataset = Dataset.from_dict(convert_strings_to_numbers)

            #Assings the tokenized data to the dictionary 'tokenizer_dictionary'.
            tokenizer_dictionary[name] = tokenized_dataset

        #Debug code to iterate over the dictionary.
        for name, tokens in tokenizer_dictionary.items():

            print(name)
            print(tokens["input_ids"][0][:10])
            print(tokens["attention_mask"][0][:10])

        #Returning the dictionary with all the tokenized data. 
        return tokenizer_dictionary




























        
