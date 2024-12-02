import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GENAI_API_KEY')

genai.configure(api_key=api_key)

# Define the completion function


def get_completion(code_snippet):
    python_code_examples = f"""
    ---------------------
    Example 1: Code Snippet
    x = 10
    def foo():
        global x
        x = 5
    foo()
    print(x)
    Correct output: 5
    Code Explanation: Inside the foo function, the global keyword is used to modify the global variable x to be 5.
    So, print(x) outside the function prints the modified value, which is 5.
    ---------------------
    Example 2: Code Snippet
    def modify_list(input_list):
        input_list.append(4)
        input_list = [1, 2, 3]
    my_list = [0]
    modify_list(my_list)
    print(my_list)
    Correct output: [0, 4]
    Code Explanation: Inside the modify_list function, an element 4 is appended to input_list.
    Then, input_list is reassigned to a new list [1, 2, 3], but this change doesn't affect the original list.
    So, print(my_list) outputs [0, 4].
    ---------------------
    """

    prompt = f"""
    Your task is to act as a Python Code Explainer.
    I'll give you a Code Snippet.
    Your job is to explain the Code Snippet step-by-step.
    Break down the code into as many steps as possible.
    Share intermediate checkpoints & steps along with results.
    Few good examples of Python code output between #### separator:
    ####
    {python_code_examples}
    ####
    Code Snippet is shared below, delimited with triple backticks:
    ```
    {code_snippet}
    ```
    """

    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    response = model.generate_content(prompt, generation_config={'max_output_tokens': 1000, 'temperature': 0})
    return response.text

# Streamlit interface


st.title("Code Explainer")

code_snippet = st.text_area("Enter your code snippet here:", height=200)

if st.button("Explain Code"):
    if code_snippet:
        explanation = get_completion(code_snippet)
        st.write("### Explanation:")
        st.write(explanation)
    else:
        st.write("Please enter a code snippet.")
