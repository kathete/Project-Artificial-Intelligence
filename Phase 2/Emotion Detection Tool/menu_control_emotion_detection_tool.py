#Loading libraries.
import sys
import time

#Loading other classes of the program.
from data_class_emotion_detection_tool import Data
from training_class import Training
from test_model import Testing
from deployment_and_monitoring import Deployment_and_Monitoring


#Class to navigate through the start and main menu.
class Menu_Control:

    # Constructor for the implementation of the objects. 
    def __init__(self, dataframes = None):
        
        self.dataframes = []
        self.tokenized_data = {}

    #Function prints out the start menu options the user can choose from.
    def start_menu(self):

        #'While' based loop which leads to a printout of the options whenevery the function is called.
        while True:

            #Menu options
            print("\n1. Enter Main Menu")
            print("2. FAQ")
            print("3. Exit\n")

            #Using the method 'input' so the user can select. He can do so by typing in the number or writing down the name.
            start_menu_input = input("What option would you like to select? Navigate easily by typing in the number of the menu option\n")

            
            if start_menu_input == "1" or start_menu_input == "1." or start_menu_input == "Enter Main Menu" or start_menu_input == "enter main menu":
                self.main_menu()

            elif start_menu_input == "2" or start_menu_input == "2." or start_menu_input == "FAQ" or start_menu_input == "faq":
                print("FAQ\n")

            #Selecting option '3' will end the program.
            elif start_menu_input == "3" or start_menu_input == "3." or start_menu_input == "Exit" or start_menu_input == "exit":

                #The user is informed that the program is being terminated. The program is paused by using 'time.sleep(1)' for one second so the user can follow what is happening. 
                print("Ending the program. Goodbye!")
                time.sleep(1)
                #Method to end the program and every running process correctly.
                sys.exit()

            #Rejection of non valid input which shall protect the program as well as the user from unintentiinal mistakes. 
            else:
                print("Your input was not valid. Please retype.")

    #Function prints out the main menu options the user can choose from.
    def main_menu(self, dataframe_training = None):

        #'While' based loop which leads to a printout of the options whenevery the function is called.
        while True:

            #Menu options
            print("\n1. Load data")
            print("2. Start data preprocessing")
            print("3. Start the tokenization")
            print("4. Run the training")
            print("5. Test the trained model")
            print("6. Deploy model")
            print("7. Monitor model")
            print("8. Return to the Start Menu")
            print("TEST print dataframe for training\n")

            #Using the method 'input' so the user can select. He can do so by typing in the number or writing down the name.
            main_menu_input = input("What option would you like to select? Navigate easily by typing in the number of the menu option.\n")

            #First option to load the data from the files.
            if main_menu_input == "1" or main_menu_input == "1." or main_menu_input == "Other options" or main_menu_input == "other options":

                #Calling the repsonsible class and function.
                call_data_class = Data()
                self.dataframes = call_data_class.load_data()

            #Second option for the preprocessing. 
            elif main_menu_input == "2" or main_menu_input == "2." or main_menu_input == "Start data preprocssing" or main_menu_input == "start data preprocessing":

                #Set of variables that represent the names of the keys of the loaded data.
                required_keys = {"test", "training", "validation"}

                #Call the responsible class and function only when the data from every file was loaded, meaning the names of the keys of the dataframe match the set-values.
                #This 'if-else' is necessary because for the ml-process the 'test', 'training' and 'validation' data ist needed. 
                if required_keys.issubset(self.dataframes):

                    #Calling the repsonsible class and function.
                    call_data_class = Data(self.dataframes)
                    self.dataframes = call_data_class.preprocessing()

                else:

                    print("You need to load every '.csv'-file first, meaning test, training and validation to continue. Please load them first and then return here.\n")
                    time.sleep(3)

            #Third option for the tokenization.
            elif main_menu_input == "3" or main_menu_input == "3." or main_menu_input == "Start the tokenization" or main_menu_input == "start the tokenization":

                #Same process here of checking for the necessary data. 
                required_keys = {"test", "training", "validation"}

                if required_keys.issubset(self.dataframes):

                    #Calling the repsonsible class and function.
                    call_data_class = Data(self.dataframes)
                    self.tokenized_data = call_data_class.tokenizer()

                else:

                    print("You need to load every '.csv'-file first, meaning test, training and validation to continue. Please load them first and then return here.\n")
                    time.sleep(3)

            #Fourth option for the training. 
            elif main_menu_input == "4" or main_menu_input == "4." or main_menu_input == "Run the training" or main_menu_input == "run the training":

                #Same process here of checking for the necessary data. But this time in the 'tokenized_data'. 
                required_keys = {"test", "training", "validation"}

                if required_keys.issubset(self.tokenized_data):

                    #Calling the repsonsible class and function.
                    call_training_class = Training(self.tokenized_data)
                    call_training_class.train_model()

                else:

                    print("You need to load every '.csv'-file first, meaning test, training and validation to continue. Please load them first and then return here.\n")
                    time.sleep(3)
                    
            #Fifth option the test the generated model.
            elif main_menu_input == "5" or main_menu_input == "5." or main_menu_input == "Test the trained model" or main_menu_input == "test the trained model":

                #Calling the repsonsible class and function.
                call_testing = Testing(self.tokenized_data)
                call_testing.test_model()

            #Sixth option for model deployment.
            elif main_menu_input == "6" or main_menu_input == "6." or main_menu_input == "Deploy model" or main_menu_input == "deploy model":

                #Calling the repsonsible class and function.
                call_deployment_and_monitoring = Deployment_and_Monitoring()
                call_deployment_and_monitoring.deploy_model()

            #Seventh option with which the model can be monitored. 
            elif main_menu_input == "7" or main_menu_input == "7." or main_menu_input == "Monitor model" or main_menu_input == "monitor model":

                #Calling the repsonsible class and function.
                call_monitoring = Deployment_and_Monitoring(self.tokenized_data)
                call_monitoring.monitor_model()

            #Eigth option to go back to the 'Start Menu'.
            elif main_menu_input == "8" or main_menu_input == "8." or main_menu_input == "Return to the Start Menu" or main_menu_input == "return to the start menu":
                self.start_menu()

            #Simply debugging option that is only here while programming and will not be part of the finished program. 
            elif main_menu_input == "test":
                print("DATAFRAME")
                print(type(self.dataframes))
                print(len(self.dataframes))
                print(self.dataframes)
                print("TOKEN")
                print(self.tokenized_data)

            #Rejection of non valid input which shall protect the program as well as the user from unintentiinal mistakes. 
            else:
                print("Your input was not valid. Please retype.")

                

































            
