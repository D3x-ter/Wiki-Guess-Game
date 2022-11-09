import random
import urllib.request
import urllib.error
import urllib.parse
from string import capwords

start_word = urllib.parse.quote(input("Choose the starting word: ").capitalize())
end_word = urllib.parse.quote(input("Choose the ending word: ").capitalize())
hints_array = [urllib.parse.quote(item.capitalize()) for item in input("Give me max 10 hint words: ").split()]
#start_word = urllib.parse.quote("WORD".capitalize())
#end_word = urllib.parse.quote("WORD".capitalize())
#hints_array = [urllib.parse.quote(item.capitalize()) for item in ["WORD1", "WORD2", "WORD3"]]
base_url = "https://fr.wikipedia.org/wiki/"
start_url = base_url + start_word
end_url = base_url + end_word
actual_url = start_url
links_array = []
excluded_url = [":", "."]
hints_found_array = []
new_hints = []
tries = 0
path_used = []
visited_pages = []

def read_page():
    
    global tries, html, actual_url
    tries += 1
    print(f"<--------------------------------New try number {tries} ------------------------------->")
    
    try:
        r = urllib.request.urlopen(actual_url)
        html = r.read().decode("utf-8")
        print("Reading this URL: " + urllib.parse.unquote(actual_url))
        return html
    except urllib.error:
        print("Erreur 404 - Page not Found")
        raise SystemExit



def find_links():
    global links_array
    links_array = []
    html_body_start = [i for i in range(len(html)) if html.startswith("<div class=\"mw-parser-output", i)]
    html_body_end = [i for i in range(len(html)) if html.startswith("<div class=\"printfooter", i)]                         #Get hmtl body between 2 classes
    sub_html = html[html_body_start[0]:html_body_end[0]]
    links_occurence = [i for i in range(len(sub_html)) if sub_html.startswith("<a href=\"/wiki", i)]
    y = 0

    for i in links_occurence:                                                                                               #get URL links
        occurences_e = sub_html.find("\"", i+9)
        link_text = sub_html[i+15:occurences_e]
        
        if any(ex in link_text for ex in excluded_url):                                                                     #Exclude some keywords
            continue
        else:
            links_array.append(link_text)

    return links_array


def is_it_win():
    global actual_url

    if end_word in links_array:
        actual_url = base_url + end_word
        print(f"\n------------///////  WIN  \\\\\\\\\---------------- URL  {urllib.parse.unquote(actual_url)}  has been found!!")
        return True
    else:
        return False

def find_hint():                                                                                                                            #Find matching hints in the links
    global hints_found_array
    hints_found_array = [word for word in hints_array if word in links_array]
    return hints_found_array



print(f"\nStart the game from {urllib.parse.unquote(start_word)} to {urllib.parse.unquote(end_word)} with these hints: {urllib.parse.unquote(str(hints_array))}\n----------------->\n")
while actual_url != end_url:

    hints_found_array = []
    read_page()
    find_links()
    find_hint()

    if is_it_win() == True:
        break
    else:
        if all(words in visited_pages for words in hints_found_array):                                                      #Check if unused hints remain -> Follow hint or random URL
            random_link = links_array[random.randint(0,len(links_array)-1)]
            actual_url = base_url + random_link
            visited_pages.append(random_link)
            continue

        for word in hints_found_array:                                         
            if word in visited_pages:
                continue
            else:
                actual_url = base_url + word
                print("Hint used: " + urllib.parse.unquote(word))
                visited_pages.append(word)
                break   


print(f"From {urllib.parse.unquote(start_word)} to {urllib.parse.unquote(end_word)} in {tries} tries: ")   
print("Visited pages:", urllib.parse.unquote(str(visited_pages)))
print("\n----------------/////  END OF THE GAME  \\\\\\\\\---------------") 

            
            
