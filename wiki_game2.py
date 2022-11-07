import random
import urllib.request
import urllib.error
import urllib.parse
from string import capwords

#start_word = urllib.parse.quote(input("Choose the starting word: "))
#end_word = urllib.parse.quote(input("Choose the ending word: "))
start_word = urllib.parse.quote("tétanos").capitalize()
end_word = urllib.parse.quote("pizza").capitalize()
base_url = "https://fr.wikipedia.org/wiki/"
start_url = base_url + start_word
end_url = base_url + end_word
actual_url = start_url
links_array = [urllib.parse.quote(item) for item in []]
excluded_url = ["Sp%C3%A9cial:", ".jpg", ".png", ".JPG", ".ogv", "Fichier:", "Projet:", "Modèle:"]
hints_array = [urllib.parse.quote(item.capitalize()) for item in input("Give me max 10 hint words: ").split()]
#hints_array = [urllib.parse.quote(item.capitalize()) for item in ["antiquité"]]
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
        #actual_url = urllib.parse.quote(actual_url)
        r = urllib.request.urlopen(actual_url)
        html = r.read().decode("utf-8")
        print("Reading this URL: " + urllib.parse.unquote(actual_url))
        return html
    except urllib.error.HTTPError:
        print("Erreur 404 - Page not Found")
        raise SystemExit



def find_links():
    html_body_start = [i for i in range(len(html)) if html.startswith("<div class=\"mw-parser-output", i)]
    html_body_end = [i for i in range(len(html)) if html.startswith("<div class=\"printfooter", i)]
    sub_html = html[html_body_start[0]:html_body_end[0]]
    occurences_s = [i for i in range(len(sub_html)) if sub_html.startswith("<a href=\"/wiki", i)]
    #global links_array
    #links_array = []
    for i in occurences_s:                                      #URL Assembly
        occurences_e = sub_html.find("\"", i+9)
        link_text = sub_html[i+15:occurences_e]
        #print("https://fr.wikipedia.org/"+link_text)

        for ex in excluded_url:
            if ex in link_text:
                break
            else:
                links_array.append(link_text)
                continue
        
    #print(links_array)
    return links_array


#read_page(actual_url)
#find_links()
def is_it_win():
    global actual_url
    #print(links_array)
            
    if urllib.parse.unquote(end_word) in links_array:
        actual_url = base_url + end_word
        print(f"\n------------///////  WIN  \\\\\\\\\---------------- URL  {urllib.parse.unquote(actual_url)}  has been found!!")
        return True
    else:
        return False

def find_hint():
    global hints_found_array
    hints_found_array = [word for word in hints_array if word in links_array]
    return hints_found_array

#def add_hint():
#    global new_hints
#    new_hints = [x for x in hints_found_array if x not in new_hints]
#
#    return new_hints


#def add_new_hint():
#    pass


i=0

print(f"\nStart the game from {urllib.parse.unquote(start_word)} to {urllib.parse.unquote(end_word)} with these hints: {urllib.parse.unquote(str(hints_array))}\n----------------->\n")
while actual_url != end_url:
    #print(actual_url)
    #if actual_url.find("Sp%C3%A9cial:") != -1:
    #    random_link = links_array[random.randint(0,len(links_array))]
    #    actual_url = base_url + random_link
    #else:    
        #actual_url = base_url + random_link
        #visited_pages.append(random_link)
    hints_found_array = []
    #print("Hints reset")
    
    read_page()
    find_links()
    #find_hint()
    if is_it_win() == True:
        break
    else:
        find_hint()
        
        if bool(hints_found_array):
            if all(words in visited_pages for words in hints_found_array):                  
                #hints_found_array = hints_array
                #new_hints = []
                
                random_link = links_array[random.randint(0,len(links_array))]
                actual_url = base_url + random_link
                #if excluded_url in actual_url:
                    #random_link = links_array[random.randint(0,len(links_array))]
                    #actual_url = base_url + random_link
                visited_pages.append(random_link)
                #else:    
                    #actual_url = base_url + random_link
                    #visited_pages.append(random_link)
                #print("reset hints array & go for random page ")   
                continue
                

            elif is_it_win() == True:
                break
            
            else:
                for word in hints_found_array:
                    if word in visited_pages:
                        #print("Page already visited", word)
                        #hints_found_array.remove(word)
                        continue
                    else:
                        actual_url = base_url + word
                        print("Hint used: " + urllib.parse.unquote(word))
                        #read_page()
                        #find_links()
                        visited_pages.append(word)
                        break

                        

        else:           
            #hints_found_array = hints_array
            #new_hints = []
            random_link = links_array[random.randint(0,len(links_array))]
            actual_url = base_url + random_link
            #if excluded_url in actual_url:
            #    random_link = links_array[random.randint(0,len(links_array))]
            #    actual_url = base_url + random_link
            visited_pages.append(random_link)
            #else:    
            #    actual_url = base_url + random_link
            #    visited_pages.append(random_link)
            #print("reset hints array & go for random page ")
        #if all(words in hints_found_array for words in visited_pages):
        #    print("FULL")        
        #    #hints_found_array = hints_array
        #    #new_hints = []
        #    actual_url = base_url + links_array[random.randint(0,len(links_array))]
        #    print("reset hints array & go for random page ")   
        #    break   
            #elif bool(hints_found_array):
print(f"in {tries} tries: ")   
print("Visited pages:", urllib.parse.unquote(str(visited_pages)))
print("\n----------------/////  END OF THE GAME  \\\\\\\\\---------------") 

            
            