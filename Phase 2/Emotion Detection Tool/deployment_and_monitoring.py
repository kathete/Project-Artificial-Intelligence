#Import of needed libraries. 
import os
import time
import shutil
import datetime

#Declaration of the class 'Deployment_and_Monitoring'
class Deployment_and_Monitoring:

    #Initializes the '__init__' method of the class.
    def __init__(self, dataframes_for_monitoring = None):

        self.dataframes_for_monitoring = dataframes_for_monitoring

    #Declaration of the function 'deploy_model'. 
    def deploy_model(self):

        #Printout to inform the user that the trained model is about to be deployed. 
        print("Deploying the model...", end="")

        #Tries to create a directory for the model and to copy the model to that newly created directory. 
        try:
            os.mkdir("marketing_department")
            shutil.copytree('./Emotion_Detection_Model_Directory', './marketing_department', dirs_exist_ok = True)
            time.sleep(1)
            print("Done.")
            print("The model has been deployed to the directory 'marketing_department'. "
                  "You can find the directory 'marketing_department' at the same place of this program.")
            time.sleep(3)
        #Executed if the directory already exists. The model is then copied to it. 
        except FileExistsError:
            time.sleep(1)
            shutil.copytree('./Emotion_Detection_Model_Directory', './marketing_department', dirs_exist_ok = True)
            print("Done.")
            print("The model has been deployed to the already existing directory 'marketing_department'.")
            time.sleep(2)

    #Declaration of the function 'monitor_model'. 
    def monitor_model(self):

        #'if' to check whether the trained model exists. 
        if os.path.exists("Emotion_Detection_Model_Directory"):
            print("exists")

            #Checking if a tokenized dataset exists. 
            try:
                (self.dataframes_for_monitoring["test"])
                print("Tokenized dataset exists. We can continue and will start with the monitoring...")
                time.sleep(3)
                print("Starting the monitoring process...")

            #'except' that is executed when there is not tokenized dataset. Returns to the previous menu. 
            except KeyError:
                print("There is a trained model but no tokenized data. Please reload the data, preprocess and tokenize it "
                      "before you can monitor the model.")
                time.sleep(3)
                return

            #Import of the components that are needed to evaluate a model. These are from 'huggingface'. 
            from transformers import AutoModelForSequenceClassification, Trainer, AutoTokenizer, DataCollatorWithPadding, TrainingArguments

            #Loading of the trained model.
            loading_trained_model = AutoModelForSequenceClassification.from_pretrained("Emotion_Detection_Model_Directory")

            #Loading of the tokenized dataset. 
            loading_tokenizer = AutoTokenizer.from_pretrained("Emotion_Detection_Model_Directory")

            #Collator or in other words supervisor which adds padding to the test data. 
            data_collator_for_padding = DataCollatorWithPadding(tokenizer = loading_tokenizer)

            #Defines the needed arguments, deactivates the progress bar of the testing with 'disable_tqdm = True'. 
            testing_arguments = TrainingArguments(output_dir = "Emotion_Detection_Model_Directory", disable_tqdm = True)

            #Creates an Hugging-Face object that is used to test the model.
            create_trainer = Trainer(model = loading_trained_model,
                                     data_collator = data_collator_for_padding, args = testing_arguments)

            #Uses the test dataset to make predictions. 
            results_of_testing = create_trainer.predict(self.dataframes_for_monitoring["test"])

            #Import of the libraries needed to evaluate the performance and predictions of the model. 
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            import numpy as np

            #Getting the predicted result with the highest score. 
            predicted_labels_from_test = np.argmax(results_of_testing.predictions, axis = 1)

            #Getting the labels of the test dataset. 
            actual_labs_from_test = results_of_testing.label_ids

            #Calculation of accuracy, prediction, recall and the f1-score of the model. 
            accuracy = accuracy_score(actual_labs_from_test, predicted_labels_from_test)
            precision = precision_score(actual_labs_from_test, predicted_labels_from_test, average = "weighted", zero_division = 0)
            recall = recall_score(actual_labs_from_test, predicted_labels_from_test, average = "weighted", zero_division = 0)
            f1 = f1_score(actual_labs_from_test, predicted_labels_from_test, average = "weighted", zero_division = 0)

            #Printout for the results.
            print(f"Accuracy: {accuracy: .4f}")
            print(f"Precision: {precision: .4f}")
            print(f"Recall: {recall: .4f}")
            print(f"F1-Score: {f1: .4f}")

            #Opens/Creates a text-file to append the results of this test to the file. With this text-file the user can see if the values change over time which could show that the prediction quality of the model decreases.
            #In this case a decrease in quality should never happen because the model is not constantly fed with user data. This is only to complete the ml-process. 
            with open("performance.txt", "a") as file:
                file.write(
                    f"{datetime.datetime.now()}\n"
                    f"Accuracy: {accuracy: .4f}\n"
                    f"Precision: {precision: .4f}\n"
                    f"Recall: {recall: .4f}\n"
                    f"F1-Score: {f1: .4f}\n\n")
                           
        #Executed when there is no trained model. The user is send back to the 'Main Menu'. 
        else:
            print("No trained model exists at the moment. Loading the Main Menu...")
            time.sleep(3)
