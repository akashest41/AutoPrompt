from langchain.agents import tool, Tool
import requests
from bs4 import BeautifulSoup

# Tools for HotpotQA benchmarking created using @tool decorators
@tool
def wiki_search(entity: str) -> list: 
    """
    Returns the first paragraph in the Wikipedia page of entity, if it exists, or else it returns the Top-5 similar entities from Wikipedia

    Parameters:
        entity (str): The string whose Wikipedia page needs to be searched

    Returns:
        list: A collection with a single string if its the first paragraph when entity is found, otherwise five strings of the best entries that could be searched next. Note that the first element of the list will always be a string giving information about the search status.
    """
    entity_ = entity.replace(" ", "+")
    search_url = f"https://en.wikipedia.org/w/index.php?search={entity_}"
    response_text = requests.get(search_url).text
    soup = BeautifulSoup(response_text, features="html.parser")
    result_divs = soup.find_all("div", {"class": "mw-search-result-heading"})
    result_titles = []
    if result_divs:
        result_titles.append("No exact matches found. Here are the top 5 most similar entries in its place.")
        for div in result_divs:
            div_text = div.get_text().strip()
            div_text = div_text.encode().decode("unicode-escape").encode("latin1").decode("utf-8")
            result_titles.append(div_text)
        return result_titles[:6]
    else:
        page = [p.get_text().strip() for p in soup.find_all("p")]
        if any("may refer to:" in p for p in page):
            wiki_search("[" + entity + "]") #check this
        else:
            for p in page:
                if p:
                    return ["Found exact match. Here is the first paragraph from its Wikipedia page.", p]

@tool
def find_on_page(keyword: str, page: str) -> list:
    """
    Returns all sentences from the Wikipedia page that contains the searched keyword. This is meant to replicate the Ctrl+F/Cmd+F functionality on the Wikipedia page's content. Note here that the Wikipedia content is assumed to be only formed from the first paragraph of the Wikipedia page.

    Parameters:
        phrase (str): The keyword to be searched.
        page (str): First paragraph of the Wikipedia page where this keyword needs to be searched

    Returns:
        list: All sentences in the first paragraph of the Wikipedia page where the keyword was found
    """    
    sentences = page.split('. ')
    sentences = [s.strip() + '.' for s in sentences if s.strip()]
    return [p for p in sentences if keyword.lower() in p.lower()]

@tool
def parse_yaml_code(yaml_code: str) -> dict:
    """You must use this tool before sending the final output, the input is the yaml code with the output schema. The result is the final output!"""
    return "The Yaml doesn't have a valid yaml structure, please fix it such that it can be parsed. Remember that if you have a value that is a string, you should wrap it in quotes."
