import os
from dotenv import load_dotenv
from langchain_experimental.sql import SQLDatabaseSequentialChain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import psycopg2
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseSequentialChain
from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers.list import CommaSeparatedListOutputParser
from mistralai.client import MistralClient
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from fastapi import HTTPException
from langchain_core.output_parsers import JsonOutputParser

base_dir = os.path.abspath(__file__)

load_dotenv()

schema_name = os.environ.get("DB_SCHEMA_NAME")
db_connection = os.environ.get("db_connection")
password = os.environ.get('DB_PASSWORD')

uft_api_key=os.getenv("FT_MISTRAL_API_KEY")

def model_v2_hf():
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
    # repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1" 
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_length=1024,
        temperature=0.5,
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )

    return llm
llm=model_v2_hf()

def get_db_connection():
    print("get_db_connection-->" )
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    
    connection_string = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    print("db connection successfull!!!...")
    return conn, cursor

connection, cursor = get_db_connection()

def db_connection_close(connection, cursor):
    try:
        connection.commit()
        connection.close()
        cursor.close()
    except Exception as error:
        return {"response": f"{error}"}
    
db_connection_close(connection, cursor)

connection_string = db_connection % quote_plus(password)
connection, cursor =  get_db_connection()

def get_data(question):
    print("In get_data----------->")
    engine = create_engine(connection_string)
    db = SQLDatabase(engine,include_tables=["coverage_benefit"],schema = 'hackathon')
    PROMPT_SUFFIX = """Only use the following tables:
        {table_info} table used - coverage_benefit

        Question: {input}"""
    _DEFAULT_TEMPLATE = f"""You are an expert in writing sql queries.

        your task is to understand the user question and generate the sql query for getting the response from database(postgresql), you have to retreive response from 'coverage_benefit' table.

        The system should interpret user questions and fetch relevant information from the  database based on the provided mappings between user inquiries and table columns.

        below is the coverage_benefit table Database columns and Corresponding User Inquiries:

        if the user question only contains 'Account id': Responses are fetched from the 'account_id' column *case sensitive.

        if the user question contains 'First Name': Data should be retrieved from the 'first_name' column *case sensitive.

        if the user question contains 'Last Name': Information should be retrieved from the 'last_name' column *case sensitive.

        if the user question contains 'email':Responses should be fetched from the 'email' column *case sensitive. 

        if the user question contains 'primary copay/copay balance': Responses should be fetched from the  'primary_copay_usd' column *case sensitive.

        if the user question contains 'secondary copay/copay balance': Data should be retrieved from the 'secondary_copay_usd' column *case sensitive.

        if the user question contains 'date of birth/DOB/birth date':Responses should be fetched from the 'date_of_birth' column *case sensitive in YYYY/MM/DD format.

        Your system should accurately interpret user queries and retrieve the corresponding information from the database. Ensure that the responses provided by the system are relevant and precise, enhancing the overall usability and efficiency of the conversational AI interface.
        
        Here is the question:{question}
        
        note: 
        - Give a single 'SELECT' query  with 'date_of_birth' condition only.

        - Do not give any explanation about the generated query 'SQLQuery', just give query alone in response. 

        - Do not give any other extra informations along with the 'SQLResult' ,just give the Answer alone.

        - SQLResult can either be 'qualified', 'unqualified', 'contacted', 'open'

        note : use schema name 'hackathon' in your query 
        
        your helpful response below:
        """

    PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX,)

    db_chain = SQLDatabaseSequentialChain.from_llm(llm=llm,db=db,query_prompt=PROMPT,verbose=False)
    response = db_chain.run(question)
    return response 

def get_data_pa_status(question):
    print("In get_data_pa_status----------->")
    engine = create_engine(connection_string)
    db = SQLDatabase(engine,include_tables=["care_prior_authorization"],schema = 'hackathon')
    PROMPT_SUFFIX = """Only use the following tables:
        {table_info} table used - care_prior_authorization

        Question: {input}"""
    _DEFAULT_TEMPLATE = f"""You are an expert in writing sql queries.

        your task is to understand the user question and generate the sql query for getting the response from database(postgresql), you have to retreive response from 'care_prior_authorization' table.

        The system should interpret user questions and fetch relevant information from the  database based on the provided mappings between user inquiries and table columns.

        below is the care_prior_authorization table Database columns and Corresponding User Inquiries:

        if the user question only contains 'Account id': Responses are fetched from the 'account_id' column *case sensitive.

        if the user question contains 'First Name': Data should be retrieved from the 'first_name' column *case sensitive.

        if the user question contains 'Last Name': Information should be retrieved from the 'last_name' column *case sensitive.

        if the user question contains 'email':Responses should be fetched from the 'email' column *case sensitive.

        if the user question contains 'date of birth/DOB/birth date':Responses should be fetched from the 'date_of_birth' column *case sensitive in YYYY/MM/DD format. 

        if the user question contains 'pa status': Responses should be fetched from the  'status' column *case sensitive.    
        
        
        Your system should accurately interpret user queries and retrieve the corresponding information from the database. Ensure that the responses provided by the system are relevant and precise, enhancing the overall usability and efficiency of the conversational AI interface.
        
        Here is the question:{question}

        note: 
        - Give a single 'SELECT' query  with 'date_of_birth' condition only.

        - Do not give any explanation about the generated query 'SQLQuery', just give query alone in response. 

        - Do not give any other extra informations along with the 'SQLResult' ,just give the Answer alone.

        - SQLResult can either be 'qualified', 'unqualified', 'contacted', 'open'

        note : use schema name 'hackathon' in your query 
        
        your helpful response below:
        """
    PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX,)
    db_chain = SQLDatabaseSequentialChain.from_llm(llm=llm,db=db,query_prompt=PROMPT,verbose=False)
    response = db_chain.run(question)
    return response 

def get_data_insurance(question):
    print("In get_data_insurance----------->")
    engine = create_engine(connection_string)
    db = SQLDatabase(engine,include_tables=["insurance"],schema = 'hackathon')
    PROMPT_SUFFIX = """Only use the following tables:
        {table_info} table used - insurance

        Question: {input}"""
    _DEFAULT_TEMPLATE = f"""You are an expert in writing sql queries.

        your task is to understand the user question and generate the sql query for getting the response from database(postgresql), you have to retreive response from 'insurance' table.

        The system should interpret user questions and fetch relevant information from the  database based on the provided mappings between user inquiries and table columns.

        below is the insurance table Database columns and Corresponding User Inquiries:

        if the user question only contains 'Account id': Responses are fetched from the 'account_id' column *case sensitive.

        if the user question contains 'First Name': Data should be retrieved from the 'first_name' column *case sensitive.

        if the user question contains 'Last Name': Information should be retrieved from the 'last_name' column *case sensitive.

        if the user question contains 'email':Responses should be fetched from the 'email' column *case sensitive. 

        if the user question contains 'payer name': Responses should be fetched from the  'payer_name' column *case sensitive.

        if the user question contains 'policy id/policy number': Responses should be fetched from the  'policy_id' column *case sensitive.

        if the user question contains 'insurance id/insurance number': Responses should be fetched from the  'insurance_id' column *case sensitive.

        if the user question contains 'date of birth/DOB/birth date':Responses should be fetched from the 'date_of_birth' column *case sensitive in YYYY/MM/DD format.

        if the user question contains 'coverage details/insurance coverage':Responses should be fetched from the 'insurance_coverage' column *case sensitive.

        
        Your system should accurately interpret user queries and retrieve the corresponding information from the database. Ensure that the responses provided by the system are relevant and precise, enhancing the overall usability and efficiency of the conversational AI interface.
        
        Here is the question:{question}

        note: 
        - Give a single 'SELECT' query  with 'date_of_birth' condition only.

        - Do not give any explanation about the generated query 'SQLQuery', just give query alone in response. 

        - Do not give any other extra informations along with the 'SQLResult' ,just give the Answer alone.

        - SQLResult can either be 'qualified', 'unqualified', 'contacted', 'open'

        note : use schema name 'hackathon' in your query 
        
        your helpful response below:
        """
    
    PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX,)
    db_chain = SQLDatabaseSequentialChain.from_llm(llm=llm,db=db,query_prompt=PROMPT,verbose=False)
    response = db_chain.run(question)
    return response 

def get_data_case(question):
    print("In get_data_case----------->")
    engine = create_engine(connection_string)
    db = SQLDatabase(engine,include_tables=["report_case"],schema = 'hackathon')

    PROMPT_SUFFIX = """Only use the following tables:
        {table_info} table used - report_case

        Question: {input}"""
    _DEFAULT_TEMPLATE = f"""You are an expert in writing sql queries.

        your task is to understand the user question and generate the sql query for getting the response from database(postgresql), you have to retreive response from 'report_case' table.

        The system should interpret user questions and fetch relevant information from the  database based on the provided mappings between user inquiries and table columns.

        below is the report_case table Database columns and Corresponding User Inquiries:

        if the user question only contains 'Account id': Responses are fetched from the 'account_id' column *case sensitive.

        if the user question contains 'description/details': Data should be retrieved from the 'description' column *case sensitive.

        if the user question contains 'case id/case number': Information should be retrieved from the 'case_id' column *case sensitive.

        if the user question contains 'date of birth/DOB/birth date':Responses should be fetched from the 'date_of_birth' column *case sensitive in YYYY/MM/DD format.

        if the user question contains 'phone number':Responses should be fetched from the 'phone_number' column *case sensitive. 
        
        if the user question contains 'case details/case description':Responses should be fetched from the 'description' column *case sensitive.

        if the user question contains 'case status/status':Responses should be fetched from the 'case_status' column *case sensitive.

        Your system should accurately interpret user queries and retrieve the corresponding information from the database. Ensure that the responses provided by the system are relevant and precise, enhancing the overall usability and efficiency of the conversational AI interface.
        

        Here is the question:{question}


        note: 
        - Give a single 'SELECT' query  with 'date_of_birth' condition only.

        - Do not give any explanation about the generated query 'SQLQuery', just give query alone in response. 

        - Do not give any other extra informations along with the 'SQLResult' ,just give the Answer alone.

        - SQLResult can either be 'qualified', 'unqualified', 'contacted', 'open'

        note : use schema name 'hackathon' in your query 
        
        your helpful response below:
        """

    PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX,)
    db_chain = SQLDatabaseSequentialChain.from_llm(llm=llm,db=db,query_prompt=PROMPT,verbose=False)
    response = db_chain.run(question)
    return response 

def get_data_lead(question):
    print("In get_data_lead----------->")
    engine = create_engine(connection_string)
    print("engine--->",engine)
    db = SQLDatabase(engine,include_tables=["lead_creation"],schema = 'hackathon')

    PROMPT_SUFFIX = """Only use the following tables:
        {table_info} table used - lead_creation

        Question: {input}"""
    _DEFAULT_TEMPLATE = f"""You are an expert in writing sql queries.

        your task is to understand the user question and generate the sql query for getting the response from database(postgresql), you have to retreive response from 'lead_creation' table.

        The system should interpret user questions and fetch relevant information from the  database based on the provided mappings between user inquiries and table columns.

        below is the lead_creation table Database columns and Corresponding User Inquiries:

        if the user question only contains 'lead id': Responses are fetched from the 'lead_id' column *case sensitive.

        if the user question contains 'first name': Data should be retrieved from the 'first_name' column *case sensitive.

        if the user question contains 'last name': Information should be retrieved from the 'last_name' column *case sensitive.

        if the user question contains 'email':Responses should be fetched from the 'email' column *case sensitive. 

        if the user question contains 'date of birth/DOB/birth date':Responses should be fetched from the 'date_of_birth' column *case sensitive in YYYY/MM/DD format.

        if the user question contains 'phone number':Responses should be fetched from the 'phone_number' column *case sensitive. 

        if the user question contains 'street':Responses should be fetched from the 'street' column *case sensitive. 

        if the user question contains 'city':Responses should be fetched from the 'city' column *case sensitive. 

        if the user question contains 'state':Responses should be fetched from the 'state' column *case sensitive. 

        if the user question contains 'country':Responses should be fetched from the 'country' column *case sensitive. 

        if the user question contains 'pincode':Responses should be fetched from the 'pincode' column *case sensitive. 

        if the user question contains 'lead status':Responses should be fetched from the 'lead_status' column *case sensitive.

        Your system should accurately interpret user queries and retrieve the corresponding information from the database. Ensure that the responses provided by the system are relevant and precise, enhancing the overall usability and efficiency of the conversational AI interface.
        

        Here is the question:{question}

        note: 
        - Give a single 'SELECT' query  with 'date_of_birth' condition only.

        - Do not give any explanation about the generated query 'SQLQuery', just give query alone in response. 

        - Do not give any other extra informations along with the 'SQLResult' ,just give the Answer alone.

        - SQLResult can either be 'qualified', 'unqualified', 'contacted', 'open'

        note : use schema name 'hackathon' in your query 
        
        your helpful response below:
        """
    
    PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX,)
    db_chain = SQLDatabaseSequentialChain.from_llm(llm=llm,db=db,query_prompt=PROMPT,verbose=False)
    response = db_chain.run(question)
    return response 

# question="what is the lead status for this date of birth '2023-01-15'?"
# question="What is the primary copay for account id 'A9300010839761'?"
