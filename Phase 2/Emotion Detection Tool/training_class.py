

#Declaration of the class 'Training'.
class Training():

    #Initializes the '__init__' method of the class.
    def __init__(self, dataframes_for_training = None):
        
        self.dataframes_for_training = dataframes_for_training

    #Placeholder function for retraining a model that is legacy code because the 'train_model' function is used for retraining. 
    def retrain_model(self):

        pass

    #Declaration of the function 'train_model'. 
    def train_model(self):

        
        # https://huggingface.co/docs/transformers/tasks/sequence_classification?utm_source=chatgpt.com


        #Map of the numbers/ids and their labels. This makes it later easier to understand a classification.
        #Both are needed to make a translation between number and label and vice versa possible.
        number_to_label = {0: "Sadness", 1: "Joy", 2: "Love", 3: "Anger", 4: "Fear", 5: "Surprise"}
        label_to_number = {"Sadness": 0, "Joy": 1, "Love": 2, "Anger": 3, "Fear": 4, "Surprise": 5}

        #Load the model and the classes required for training.
        from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer, AutoTokenizer, DataCollatorWithPadding

        #Loading of the 'Distilbert' model. The dictionaries 'number_to_label' and 'label_to_number' are assigned to it.  
        model = AutoModelForSequenceClassification.from_pretrained(
            "distilbert/distilbert-base-uncased",
            num_labels = 6,
            id2label = number_to_label,
            label2id = label_to_number
        )

        #Loads the tokenizer that is used for the data. 
        tokenizer = AutoTokenizer.from_pretrained("transformer")

        #Collator or in other words supervisor which adds padding to the test data.
        data_collator = DataCollatorWithPadding(tokenizer = tokenizer)

        #Defining the parameters for the training process.
        #All values chosen are default values for "DistilBert" that "HuggingFace" recommands. 
        training_arguments = TrainingArguments(

            #Directory where training outputs and checkpoints are stored.
            output_dir = "Emotion_Detection_Model_Directory",

            #Controls how strongly the model weights are changed during training. 
            learning_rate = 2e-5,

            #How many examples are processed each batch (group of examples).
            per_device_train_batch_size = 16,

            #How many examples are processed during validation. The validation of the model is part of the training.
            per_device_eval_batch_size = 16,

            #How many times is the dataset used for a training circle. 
            #One 'epoch' means one complete training circle. In this case 3 complete trainings happen.
            #Multiple epochs allow the model to learn repeateadly from the training data.
            num_train_epochs = 3,

            #Weights are being reduced to prevent overfitting. 
            weight_decay = 0.01,

            #Start a validation after every epoch.
            eval_strategy = "epoch",

            #Saving the newly trained model after each epoch, meaning each training cycle.
            save_strategy = "epoch",

            #The best model is chosen and loaded at the end of all training cycles.
            #With this the program does not provide the model of the last epoch, which could be a worse one.
            load_best_model_at_end = True,

            #Decide which metric is chosen to select the best model. In this case 'accuracy'.
            metric_for_best_model = "accuracy",

            #When is model better than another one? A model is better the higher its 'accuracy'.
            greater_is_better = True,

            #Disables the progress bar during training which makes the training much faster. 
            disable_tqdm = True
            )

        #Creates the Trainer object that controls the training and validation process.
        trainer = Trainer(

            #The model that is being used for the training.
            model = model,

            #Passes the arguments of 'training_arguments'.
            args = training_arguments,

            #Passes the function that computes the evaluation metrics used to compare checkpoints.
            train_dataset = self.dataframes_for_training["training"],

            #Passes the tokenized dataframe for validation.
            eval_dataset = self.validate_model(),

            #Passes a function that computes the evaluation metrics. This is important to later chose the best one.
            compute_metrics = self.compute_metrics,

            #Passes the data collator that handles the padding of the data. 
            data_collator = data_collator
            )

            
        #Starts the training process. 
        trainer.train()

        #Saves the trained model in the specified directory. 
        trainer.save_model("Emotion_Detection_Model_Directory")
        
    #Declaration of the function 'validate_model'. It provides the validation dataframe for the validation during the training process. 
    def validate_model(self):

        return self.dataframes_for_training["validation"]

    #Declaration of the function 'compute_metrics'. It serves to evaluate the performance of the model that is being trained.
    #The function is called with a tuple containing predictions and the label ids.
    def compute_metrics(self, evaluate_predictions):

        #Necessary libraries to compute the accuracy.
        import numpy as np
        from sklearn.metrics import accuracy_score


        #Seperating the predictions and labels into two different variables called 'predictions' and 'labels'.
        predictions, labels = evaluate_predictions

        #Using the 'np.argmax' method to find the biggest value of a prediction. 
        predictions = np.argmax(predictions, axis = 1)

        accuracy = accuracy_score(labels, predictions)

        #Returning of the 'accuracy' after comparing the values.
        return {"accuracy": accuracy}
        
