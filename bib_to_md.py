####################### FUNCTION DEFINITIONS #################################


def entry_data_dictionary(entry_name, biblio, max_length=10**4):
    #
    #If the entry doesn't exist returns an empty dictionary
    try:
        entry_pos = biblio.index(entry_name)
    except:
        return {}
    #
    #Setting the entry index in the main text
    entry_pos += len(entry_name)
    max_index = min(len(biblio),entry_pos+max_length)
    #
    #Check what it the index where the entry ends, by controlling that all graph parentheses have been closed
    count_graph = 1
    last_pos = entry_pos-1
    while count_graph != 0:
        last_pos+=1
        if last_pos>max_index:
            raise Exception("Entry scan ended without closing enough graph parentheses.")
        new_char = biblio[last_pos]
        if new_char == "{":
            count_graph+=1
        if new_char == "}":
            count_graph-=1
    #
    #Extract the entry texts, delete consecutive spaces and the first comma
    biblio_catch = biblio[entry_pos:last_pos]
    biblio_catch = " ".join(biblio_catch.split())
    biblio_catch = biblio_catch[biblio_catch.index(",")+1 :]
    #   
    #Delete few unwanted elements
    biblio_catch = biblio_catch.replace("\n","")
    biblio_catch = biblio_catch.replace("{","")
    biblio_catch = biblio_catch.replace("} ,","},")   
    biblio_catch = biblio_catch.replace("},","---")   
    biblio_catch = biblio_catch.replace("}","")
    #
    #Translate the text into a dictionary 
    imported_dict = dict((a.strip(),  b.strip() ) for a, b in (element.split("=") for element in biblio_catch.split("---"))) 
    #
    #Return the dictionary
    return imported_dict


def key_check(entry_dictionary,entry_key):
    #
    #Check if the entry exists and in case delete consecutive spaces
    try:
        result = entry_dictionary[entry_key]
        result = " ".join(result.split())
        result = result.replace("--","-")
    except:
        result = ""
        #
    return result


def key_extract(entry_dictionary,entry_key,string_prepend="",string_append=""):
    #
    string_to_add = key_check(entry_dictionary,entry_key)
    #
    if string_to_add!="":
        string_to_add = string_prepend + string_to_add + string_append
    #
    return string_to_add


def add_period_authors(text_string):
    #
    #Splitting the words in suthor list
    text_string_sliced = text_string.split(" ")
    #
    #Checking if some isolated letters don't have a period afterwards
    for i_slice, text_slice in enumerate(text_string_sliced):
        if len(text_slice)==1:
            text_string_sliced[i_slice] = text_slice + "."
        if (len(text_slice)==2 and text_slice[-1]==","):
            text_string_sliced[i_slice] = text_slice[0] + "." + text_slice[-1]
    #
    #Return the corrected author list
    return " ".join(text_string_sliced)


def construct_md(entry_name,entry_dictionary,entry_index):
    #
    #Check if no data exist for that entry
    if entry_dictionary=={}:
        return "", 0
    #
    #Initial entry definition for Markdown
    final_string = "<a id=\"" + entry_name + "\">[" + str(entry_index) +"]</a>\n"
    #
    #Adding the authors
    string_to_add = key_check(entry_dictionary,"author")
    if string_to_add!="":
        string_to_add = string_to_add.translate({ord(i): None for i in ",/?_*&^%$@#!<>{}[]"})
        string_to_add = string_to_add.replace(" and",",")
        string_to_add = add_period_authors(string_to_add)
        final_string += string_to_add + ",\n" 
    #
    #Creating the hyper-link to the paper
    link_string = key_extract(entry_dictionary,"doi","](https://dx.doi.org/",")")
    if link_string=="":
        link_string = key_extract(entry_dictionary,"url","](",")")
    #    
    #Adding the title
    final_string += key_extract(entry_dictionary,"title","*","*,\n")
    #
    #Adding the journal
    if link_string!="":
        start_braket = "["
    else:
        start_braket = ""
    final_string += key_extract(entry_dictionary,"journal",start_braket," ")
    #
    #Adding the volume, pages, hyper-link
    final_string += key_extract(entry_dictionary,"volume","",", ")
    final_string += key_extract(entry_dictionary,"pages")
    final_string += link_string
    final_string += key_extract(entry_dictionary,"year"," (",")")
    #
    #Returning the converted entry        
    return "\n" + final_string + "\n", 1


def bib_to_md_convert(entry_name_list, biblio_name, start_index = 1, max_length=10**4):
    #
    #Trying to import the bibliography file
    try:
        biblio_file = open(biblio_name,"r")
        biblio_full = biblio_file.read()
    except:
        raise ImportError("I cannot read the file.")    
    #
    #Initializing variables
    converted_string = ""
    entry_index = start_index
    #
    #Translating the entries from bib to md
    for entry_name in entry_name_list:
        entry_dictionary = entry_data_dictionary(entry_name, biblio_full,max_length)
        entry_string, i_to_add = construct_md(entry_name,entry_dictionary,entry_index)
        converted_string += entry_string 
        entry_index += i_to_add
        #
    return converted_string


####################### CONVERSION TEST ######################################

import os

test_entries = [
                "Bettles2016EnhancedArray",
                "Shahmoon2017CooperativeArrays",
                "Rui2020ALayer",
                "Manzoni2018OptimizationArrays"
                #,"WrongEntry",
                #"TestIncompleteEntry"
                ]

biblio_name = "example.bib"

os.chdir(os.path.dirname(__file__))
converted_text = bib_to_md_convert(test_entries, biblio_name, 18)
print(converted_text)

try:
    with open('converted_text.txt', 'w') as f:
        f.write(converted_text)    
except:
    raise Exception("Cannot open and write the converted file.")

