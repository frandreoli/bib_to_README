####################### CONVERSION TEST ######################################

test_entries = [
                "Bettles2016EnhancedArray",
                "Shahmoon2017CooperativeArrays",
                "Rui2020ALayer",
                "Manzoni2018OptimizationArrays"
                ]

biblio_name = "example.bib"
 
 

####################### FUNCTION DEFINITIONS #################################

def entry_data_dictionary(entry_name, biblio, max_length=10**4):
    try:
        entry_pos = biblio.index(entry_name)
    except:
        return "FAILURE"
    #
    entry_pos += len(entry_name)
    max_index = min(len(biblio),entry_pos+max_length)
    #
    count_graph = 1
    last_pos = entry_pos-1
    while count_graph != 0:
        last_pos+=1
        if last_pos>max_index:
            raise Exception("Entry scan ended without closing enough graphs parentheses.")
        new_char = biblio[last_pos]
        if new_char == "{":
            count_graph+=1
        if new_char == "}":
            count_graph-=1
    #
    biblio_catch = biblio[entry_pos:last_pos]
    biblio_catch = ' '.join(biblio_catch.split())
    biblio_catch = biblio_catch[biblio_catch.index(",")+1 :]
    #   
    biblio_catch = biblio_catch.replace("\n","")
    biblio_catch = biblio_catch.replace("{","")
    biblio_catch = biblio_catch.replace("} ,","},")    
    imported_dict = dict((a.strip(),  b.strip() ) for a, b in (element.split("=") for element in biblio_catch.split("},"))) 
    return imported_dict

def construct_md(entry_dictionary):
    pass


def bib_to_md_convert(entry_names, biblio_name, max_length=10**4):
    #
    try:
        biblio_file = open(biblio_name,"r")
    except:
        raise ImportError("I cannot read the file.")
    #
    biblio_full = biblio_file.read()
    #
    converted_string = ""
    #
    for entry_name in entry_names:
        entry_dictionary = entry_data_dictionary(entry_name, biblio_full,max_length)
        entry_string = construct_md(entry_dictionary)
        converted_string = converted_string.join(entry_string)
        #
    return converted_string


