import google.generativeai as genai
import os 
from app.core.config import settings
import re

genai.configure(api_key="AIzaSyBo5L0BBP-8B9r7cBsw008BuJpHZ_vgcLw")

model = genai.GenerativeModel(model_name = settings.GEMINI_MODEL) # We already selected in config.py => gemini-1.5-pro
MAX_INPUT_TOKENS = 32760  # The maximum input token limit
OUTPUT_PAGE_SIZE = 16380  # The maximum tokens per page in the output


#TODO_1: Eliminate the markdowns from the text
# - Removes links formatted as [text](url) and keeps only the text.
# - Removes markdown formatting characters such as *, _, ~, and `.
def clean_markdown(text):
    cleaned_text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)  # Remove markdown links
    cleaned_text = re.sub(r"[*_~`]", "", cleaned_text)  # Remove formatting markers
    cleaned_text = re.sub(r"(^|\n)#+\s*", "", cleaned_text)  # Remove headers
    cleaned_text = re.sub(r"(^|\n)>\s*", "", cleaned_text)  # Remove block quotes
    return cleaned_text
#====================================================================================
#TODO_2: Make sure to have a limit for the token (input)
#- Splits the text into words to estimate the token count.
#- Raises a ValueError if the token count exceeds the specified limit.

def enforce_token_limit(text, max_tokens=32760):
    token_count = len(text.split())  # Estimate token count
    if token_count > max_tokens:
        raise ValueError(f"Input exceeds the maximum token limit of {max_tokens} tokens.")
    return text

#======================================================================================
# TODO_3: Make sure to have a pagination for the output
#- Splits the text into words.
#- Groups the words into pages, each containing up to `page_size` tokens.

def paginate_output(text, page_size=16380):
    words = text.split()
    pages = [" ".join(words[i:i + page_size]) for i in range(0, len(words), page_size)]
    return pages

def gemini_response(text):
    # Step 1: Clean markdown from the input text
    cleaned_text = clean_markdown(text)

    # Step 2: Enforce the token limit on the cleaned text
    validated_text = enforce_token_limit(cleaned_text)

    # Step 3: Generate the Gemini response
    response = model.generate_content(validated_text)

    # Step 4: Paginate the output text
    paginated_output = paginate_output(response.text)

    return paginated_output
