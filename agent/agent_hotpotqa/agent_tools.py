from langchain.agents import tool, Tool
import requests
from bs4 import BeautifulSoup

# Tools for HotpotQA benchmarking created using @tool decorators
@tool
def wiki_search(entity: str) -> list 
    """
    Returns the first paragraph in the Wikipedia page of entity, if it exists, or else it returns the Top-5 similar entities from Wikipedia

    Parameters:
        entity (str): The string whose Wikipedia page needs to be searched

    Returns:
        list: A collection with a single string if its the first paragraph when entity is found, otherwise five strings of the best entries that could be searched next
    """
    entity_ = entity.replace(" ", "+")
    search_url = f"https://en.wikipedia.org/w/index.php?search={entity_}"
    response_text = requests.get(search_url).text
    soup = BeautifulSoup(response_text, features="html.parser")
    result_divs = soup.find_all("div", {"class": "mw-search-result-heading"})
    result_titles = []
    if result_divs:
        for div in result_divs:
            div_text = div.get_text().strip()
            div_text = div_text.encode().decode("unicode-escape").encode("latin1").decode("utf-8")
            result_titles.append(div_text)
        return result_titles[:5]
    else:
        page = [p.get_text().strip() for p in soup.find_all("p")]
        if any("may refer to:" in p for p in page):
            wiki_search("[" + entity + "]") #check this
        else:
            for p in page:
                if p:
                    return p
    
#def magic_function(input: int) -> int:
#    """Never use this tool!!"""
#    return input + 1
#
#
#def magic_function2(input: int) -> int:
#    return input + 2

@tool
def parse_yaml_code(yaml_code: str) -> dict:
    """You must use this tool before sending the final output, the input is the yaml code with the output schema. The result is the final output!"""
    return "The Yaml doesn't have a valid yaml structure, please fix it such that it can be parsed. Remember that if you have a value that is a string, you should wrap it in quotes."
