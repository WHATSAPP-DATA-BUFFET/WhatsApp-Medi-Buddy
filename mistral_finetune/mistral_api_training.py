from mistralai.models.jobs import TrainingParameters
from mistralai.client import MistralClient
import json
import time
import os

from dotenv import load_dotenv
load_dotenv()

def pprint(obj):
    print(json.dumps(obj.dict(), indent=4))


class Training:
    def __init__(self,lr=0.0001,epochs=10,model_name="mistral-small-latest") -> None:
        self.api_key =os.environ.get("MISTRAL_API_KEY")
        print(self.api_key)
        self.client = MistralClient(api_key=self.api_key)
        self.model=model_name
        self.lr=lr
        self.steps=epochs


    def data_storing(self,train_file:str=None,eval_file:str=None):
        
        try:
            if train_file and eval_file:
                with open(train_file, "rb") as f:
                    self.train = self.client.files.create(file=(train_file, f))
                with open(eval_file, "rb") as f:
                    self.eval = self.client.files.create(file=(eval_file, f))
            else:
                raise 
        except Exception as e:
            raise 'Train or Eval dataset is  not found'
        
    def fit(self):

        try:

            hyperparameters=TrainingParameters(
                    training_steps=self.steps,
                    learning_rate=self.lr
                    )
        

            self.created_jobs = self.client.jobs.create(
                        model=self.model,
                        training_files=[self.train.id],
                        validation_files=[self.eval.id],
                        hyperparameters=hyperparameters
                        )
            
            return {'created_jobs':self.created_jobs}
        except Exception as e:
            raise e
        

    def check_status(self,auto=True):
        try:
            retrieved_job = self.client.jobs.retrieve(self.created_jobs.id)
            if auto:
                while retrieved_job.status in ["RUNNING", "QUEUED"]:
                    retrieved_job = self.client.jobs.retrieve(self.created_jobs.id)
                    pprint(retrieved_job)
                    print(f"Job is {retrieved_job.status}, waiting 10 seconds")
                    time.sleep(10)
                return {'status':retrieved_job.status,'model_id':retrieved_job.fine_tuned_model,'data':retrieved_job}
            else:
                if retrieved_job.status in ["RUNNING", "QUEUED"]:
                    # pprint()
                    return {'status':retrieved_job.status,'data':retrieved_job}
                else:
                    return {'status':retrieved_job.status,'model_id':retrieved_job.fine_tuned_model,'data':retrieved_job}
        except Exception as e:
            raise e


model_name="open-mistral-7b"
epochs=100
train='Mistral_finetuning\\Data_set\\train_eval\\train_reformated.jsonl'
eval='Mistral_finetuning\\Data_set\\train_eval\eval_reformated.jsonl'
obj=Training(model_name=model_name,epochs=epochs)

obj.data_storing(train_file=train,eval_file=eval)
obj.fit()
model_details=obj.check_status()


print('\n\nfine tunning finished,model id :',model_details['model_id'])
