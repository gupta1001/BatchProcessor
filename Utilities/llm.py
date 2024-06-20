import time
import os
from functools import wraps
from datetime import datetime
import logging
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from clean_data import clean_output, clean_output_openai
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

openai_api_key = os.getenv('OPENAI_API_KEY')

# Rate limiting decorator
def rate_limited(max_per_minute):
    min_interval = 60.0 / float(max_per_minute)
    def decorator(func):
        last_called = [datetime.min]

        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            elapsed = (datetime.now() - last_called[0]).total_seconds()
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_called[0] = datetime.now()
            return func(*args, **kwargs)
        
        return rate_limited_function
    return decorator

@rate_limited(10)  # Apply the rate limiting decorator
def generate_response(prompt):
    breakpoint()
    try:
        models = genai.list_models()
        for m in models:
            print(f"Model Name: {m.name}")
        print(key_param.LANGUAGE_MODEL_API_KEY)
        llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=key_param.LANGUAGE_MODEL_API_KEY)
        template = prompt
        prompt_template = PromptTemplate(input_variables=[], template=template)
        chain = prompt_template | llm
        output = chain.invoke({})
        print(output)
        cleaned_list = clean_output(output)
        if cleaned_list is not None:
            print(len(cleaned_list))
        print(cleaned_list)
        return cleaned_list
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return None
    
@rate_limited(100)  # Apply the rate limiting decorator
def generate_response_openAI(prompt):
    # breakpoint()
    try:
        
        llm = llm = ChatOpenAI(model="gpt-3.5-turbo")
        template = prompt
        output = llm.invoke(template)
        print(output.content)
        # breakpoint()
        cleaned_list = clean_output_openai(output.content)
        if cleaned_list is not None:
            print(len(cleaned_list))
        print(cleaned_list)
        # breakpoint()
        return cleaned_list
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return None
