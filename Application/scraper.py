from bs4 import BeautifulSoup
import requests
import os
from time import sleep
from re import sub




def read_link() -> str:
    """_summary_
        read the link from the Env File
    Returns:
        str: Return the Manga Website link for scrapper to function
    """
    with open("/home/eternity/Personal_Project/MangaApplication/.venv/.links") as f:
        link = f.read() 
        return link


def get_page(link:str) -> list[bool, BeautifulSoup]: 
    """Get the page HTML

    Args:
        link (str): The link to the page

    Returns:
        list[bool, BeautifulSoup]: A Bool to indicate if succeeded and the content
    """
    response: requests.Response = requests.get(link)
    if response.status_code != 200: 
        return [False, 0]
    
    soup = BeautifulSoup(response.content, "html.parser")
    return [True, soup]


def get_manga(soup: BeautifulSoup, con) -> None: 
    filter = ""
    for manga in soup.find_all("div", {"class": "flex border-b border-b-base-200 pb-3"}):
        title, thumnpnail = get_title_thumpnail(str(manga.find_all('img')))
        genre = get_genre(str(manga.find_all("div", {"class": "flex flex-wrap text-xs opacity-70"})))
        main_page = get_main_page(str(manga.find_all("a", {"class": "link-hover link-pri"})))        
        chapters = get_main_page_info(main_page)
        break
        
        # print(f"Title: {title}, Genre: {genre}\nThumpnail: {thumnpnail}\nMain Page: {main_page} \n" )

def get_title_thumpnail(soup: str) -> tuple:
    thumpnail = soup.split('src="')[-1].split('"')[0]
    title = soup.split('title="')[1].split('"')[0]
    return title, thumpnail

def get_main_page(soup: str) -> str:
    
    main_page = soup.split('href="')[1].split('"')[0]
    return main_page    


def get_genre(soup: str) -> tuple: 

    genres = soup.split("<span")
    
    manga_genre = []
    for genre in genres:
        if genre.__contains__("whitespace-nowrap"):
            genre = genre.split("->")[1].split("<!")[0]
            manga_genre.append(genre)

    return manga_genre
    
def get_main_page_info(link: str):
    full_link = f"{read_link()[0:-8]}{link}"
    soup = get_page(full_link)
    
    if soup[0] == False:
        return False, 0
    
    chapters = get_all_available_chapter(soup[1])

    return True, chapters
    

def get_all_available_chapter(soup):

    chapters = {}
    for chapter in soup.find_all("div", {"class": "px-2 py-2 flex flex-wrap justify-between hover:bg-accent/5 border-b border-base-300/50 group-[.flex-col]:last:border-b-0 group-[.flex-col-reverse]:first:border-b-0"}):
        chapter = chapter.find_all("a", {"class": "link-hover link-primary visited:text-accent"})
        chapter_number = (str(chapter)).split('">')[-1].split("<")[0]
        chapter_link = (str(chapter)).split('href="')[1].split('" ')[0]
        chapters[chapter_number] = chapter_link
    
    return chapter_link

def get_chapter(link: str):
    
    soup = get_page(link)  
    if soup[0]:
       return find_src(str(soup[1]))


def find_src(soup: str):
    links = []
    split = soup.split("https://", 1)
    while len(split) == 2:
        source = split[1].split('"')[0]
        if source.__contains__(".jpeg"):
            links.append(f"https://{source}")
        split = split[1].split("https://", 1)
    return links
    

