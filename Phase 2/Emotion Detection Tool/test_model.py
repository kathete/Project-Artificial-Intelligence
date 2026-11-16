# Links

# https://huggingface.co/docs/transformers/main/tasks/sequence_classification?utm_source=chatgpt.com
# https://huggingface.co/docs/transformers/main_classes/trainer?utm_source=chatgpt.com
# https://huggingface.co/docs/evaluate/en/base_evaluator?utm_source=chatgpt.com
# https://huggingface.co/docs/transformers/main_classes/trainer?utm_source=chatgpt.com
# welche Metriken für was relevant
    # https://huggingface.co/docs/evaluate/considerations?utm_source=chatgpt.com
    # https://huggingface.co/tasks/text-classification?utm_source=chatgpt.com - rechts an der seite
# trainer
    # https://huggingface.co/docs/transformers/main_classes/trainer?utm_source=chatgpt.com
    # https://huggingface.co/docs/evaluate/transformers_integrations?utm_source=chatgpt.com


#Import of needed libraries. 
import os
import time

#Declaration of the class 'Testing'.
class Testing:

    #Initializes the '__init__' method of the class.
    def __init__(self, dataframe_for_testing):

        self.dataframe_for_testing = dataframe_for_testing

    #Declaration of the function 'test_model'.
    def test_model(self):

        #'if' to check whether the trained model exists.
        if os.path.exists("Emotion_Detection_Model_Directory"):
            print("exists")

            #Checking if a tokenized dataset exists. 
            try:
                (self.dataframe_for_testing["test"])
                print("Tokenized dataset exists. We can continue and will start with the testing...")
                time.sleep(3)
                print("Starting the testing process...")

            #'except' that is executed when there is not tokenized dataset. Returns to the previous menu. 
            except KeyError:
                print("There is a trained model but no tokenized data. Please reload the data, preprocess and tokenize it "
                      "before you can test the model.")
                time.sleep(3)
                return

            #Import of the components that are needed to evaluate a model. These are from 'huggingface'. 
            from transformers import AutoModelForSequenceClassification, Trainer, AutoTokenizer, DataCollatorWithPadding, TrainingArguments

            #Loading of the tokenized dataset.
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
            results_of_testing = create_trainer.predict(self.dataframe_for_testing["test"])

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

        #Executed when there is no trained model. The user is send back to the 'Main Menu'.
        else:
            print("No trained model exists at the moment. Loading the Main Menu...")
            time.sleep(3)
