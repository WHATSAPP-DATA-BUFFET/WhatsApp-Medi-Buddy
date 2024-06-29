import json
import os
import functools
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_mistralai import ChatMistralAI
from mistralai.client import MistralClient
from dotenv import load_dotenv
from mistralai.models.chat_completion import ChatMessage
from fastapi import HTTPException
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate 
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from db_utils import get_data, get_data_pa_status, get_data_insurance, get_data_case, get_data_lead

base_dir = os.path.abspath(__file__)

load_dotenv()

# Read model_id and api_key from environment variables
fine_tuned_model_id = os.environ.get('MODEL_ID')
api_key = os.environ.get('FT_MISTRAL_API_KEY')

uft_model = ChatMistralAI(api_key=api_key, model_name='mistral-medium-latest')

client = MistralClient(api_key=api_key)

class eval_json_mcq(BaseModel):
    response: str = Field(description="Yes/No")
    description: str = Field(description="reason for your response")

def get_prompt(user_query_val_prompt=None):
        if user_query_val_prompt:
            user_query_val_prompt="""You are a expert in categorizing user query
            if the query is related to any details about copay, PA status, case status, insurance coverage and lead status, your response should be 'Yes'.
            if it is not related to the details of the above mentioned functions, your response should be 'No' and suggest user to ask about related questions in description. 
            query:{query}
            
            \n{format_instructions}\n

            your helpful question below

            """
            return user_query_val_prompt
        
def filter_user_query(question):
        print("--filter_user_query--")

        parser = JsonOutputParser(pydantic_object=eval_json_mcq)

        prompt_initialize_question = PromptTemplate(
        template=get_prompt(user_query_val_prompt=True),
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        validation_chain = prompt_initialize_question | uft_model | parser
        try:
            val_response = validation_chain.invoke({"query": question})

            print("validation chain response : ",val_response)

        except Exception as error:
            raise HTTPException(
                status_code=500, detail=f"Error :{error} | {base_dir}"
            )
        
        if val_response['response'].lower()=="yes":
            return {"status":200,"response":question}
        else:
             return {"status":500,"response":val_response['description']}

def common_func(question):
    print("In common_func")
    data_ = ""

    def retrieve_copay_status(date_of_birth):
        nonlocal data_
        print("--retrieve_copay_status--")
        print(question)
        print("Calling the retrieve_copay_status----->")
        data = get_data(question)
        print("data----->", data)
        data_ = data  # Assign the new data to data_ instead of appending

    def retrieve_pa_status(date_of_birth):
        nonlocal data_
        print("--retrieve_pa_status--")
        print(question)
        print("Calling the retrieve_pa_status----->")
        data = get_data_pa_status(question)
        print("data----->", data)
        data_ = data  # Assign the new data to data_ instead of appending

    def retrieve_insurance_update(date_of_birth):
        nonlocal data_
        print(question)
        print("Calling the retrieve_insurance_update----->")
        data = get_data_insurance(question)
        print("data----->", data)
        data_ = data  # Assign the new data to data_ instead of appending

    def retrieve_case_report(date_of_birth):
        nonlocal data_
        print(question)
        print("Calling the retrieve_case_report----->")
        data = get_data_case(question)
        print("data----->", data)
        data_ = data  # Assign the new data to data_ instead of appending

    def retrieve_lead_details(date_of_birth):
        nonlocal data_
        print(question)
        print("Calling the retrieve_case_report----->")
        data = get_data_lead(question)
        print("data----->", data)
        data_ = data  # Assign the new data to data_ instead of appending

    tools = [
        {
            "type": "function",
            "function": {
                "name": "retrieve_copay_status",
                "description": "Get copay status of a account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date_of_birth": {
                            "type": "string",
                            "description": "date of birth of the user",
                        }
                    },
                    "required": ["date_of_birth"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "retrieve_pa_status",
                "description": "Get pa status of a account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date_of_birth": {
                            "type": "string",
                            "description": "date of birth of the user",
                        }
                    },
                    "required": ["date_of_birth"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "retrieve_insurance_update",
                "description": "Get the insurance details of a account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date_of_birth": {
                            "type": "string",
                            "description": "date of birth of the user",
                        }
                    },
                    "required": ["date_of_birth"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "retrieve_case_report",
                "description": "Get the case details of a account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date_of_birth": {
                            "type": "string",
                            "description": "date of birth of the user",
                        }
                    },
                    "required": ["date_of_birth"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "retrieve_lead_details",
                "description": "Get the lead details of a account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date_of_birth": {
                            "type": "string",
                            "description": "date of birth of the user",
                        }
                    },
                    "required": ["date_of_birth"],
                },
            },
        }
    ]

    names_to_functions = {
        'retrieve_copay_status': functools.partial(retrieve_copay_status, date_of_birth=question),
        'retrieve_pa_status': functools.partial(retrieve_pa_status, date_of_birth=question),
        'retrieve_insurance_update': functools.partial(retrieve_insurance_update, date_of_birth=question),
        'retrieve_case_report': functools.partial(retrieve_case_report, date_of_birth=question),
        'retrieve_lead_details': functools.partial(retrieve_lead_details, date_of_birth=question)
    }

    messages = [ChatMessage(role="user", content=question)]

    response = client.chat(
        model=fine_tuned_model_id,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    print("response---->", response)

    messages.append(response.choices[0].message)

    print("messages----->", messages)

    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_params = json.loads(tool_call.function.arguments)
    print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)

    # Clear the data_ variable before calling the function
    data_ = ""
    names_to_functions[function_name](**function_params)

    messages.append(ChatMessage(role="tool", name=function_name, content=data_, tool_call_id=tool_call.id,prompt =""))

    print("messages------>", messages)
    
    response = client.chat(
        model=fine_tuned_model_id,
        messages=messages
    )

    print("Final Response---->", response.choices[0].message.content)
    
    res = response.choices[0].message.content
    return res
