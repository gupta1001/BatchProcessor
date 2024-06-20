import re
import ast
import logging


def clean_output(llm_output):
    try:
        llm_output = llm_output.strip()
        match = re.search(r'```(?:python)?\n?(.*?)```', llm_output, re.DOTALL)
        if match:
            content = match.group(1).strip()
        else:
            content = llm_output.strip()
        cleaned_list = ast.literal_eval(content)
        if isinstance(cleaned_list, list) and all(isinstance(item, str) for item in cleaned_list):
            return cleaned_list
        else:
            raise ValueError("Output is not a list of strings")
    except (SyntaxError, ValueError) as e:
        logging.error(f"Error in clean_output: {e}")
        return None
    
def clean_output_openai(llm_output):
    try:

        output_list = ast.literal_eval(llm_output)
        
        if isinstance(output_list, list):
            return output_list
        else:
            raise ValueError("The evaluated output is not a list.")

    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")
        output_list = []
