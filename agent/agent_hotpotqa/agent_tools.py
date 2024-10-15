from langchain.agents import tool, Tool
import requests
from bs4 import BeautifulSoup

# Tools for HotpotQA benchmarking created using @tool decorators
@tool
def wiki_search(entity: str) -> list:
    """
    Returns the Wikipedia entry of the entity that is requested, if it exists, or else it returns a list of the Top-5 similar entities from Wikipedia

    Parameters:
        entity (str): The string whose Wikipedia page needs to be searched

    Returns:
        list: List of searchable entities that which have existing Wikipedia pages. Note that the first element of the list will always be a string giving information about the search status.
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
        return ["Found exact match.", entity] 

@tool
def wiki_text(entity: str) -> list: 
    """
    Returns the full text in the Wikipedia page of entity

    Parameters:
        entity (str): The string whose Wikipedia page needs to be searched

    Returns:
        list: A collection of all paragraphs in the Wikipedia page.
    """
    entity_ = entity.replace(" ", "+")
    search_url = f"https://en.wikipedia.org/w/index.php?search={entity_}"
    response_text = requests.get(search_url).text
    soup = BeautifulSoup(response_text, features="html.parser")
    page = [p.get_text().strip() for p in soup.find_all("p")]
    if any("may refer to:" in p for p in page):
        wiki_search("[" + entity + "]") #check this
    else:
        return page

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
