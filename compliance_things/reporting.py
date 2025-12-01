# One table at a time    
def format_summary_table(severity_breakdown,category_breakdown):
    title1 = "Severity"
    title2 = "Category"
    title3 = "Counts"
    #severity lengths
    severity_name_lengths = [len(severity) for severity in severity_breakdown.keys()]
    severity_name_lengths.append(len(title1))
    severity_labels_lengths = max(severity_name_lengths)
    #category lengths
    category_name_lengths = [len(category) for category in category_breakdown.keys()]
    category_name_lengths.append(len(title2))
    category_labels_lengths = max(category_name_lengths)
    #counts lengths
    count_lengths_sev = [len(str(count)) for count in severity_breakdown.values()]
    count_lengths_sev.append(len(title3))
    count_sev = max(count_lengths_sev)

    count_lengths_cat = [len(str(count)) for count in category_breakdown.values()]
    count_lengths_cat.append(len(title3))
    count_cat = max(count_lengths_cat)
    
    border_cat_width = "+" + ("-" * category_labels_lengths) + "+" + ("-" * count_cat) + "+"
    border_sev_width = "+" + ("-" * severity_labels_lengths) + "+" + ("-" * count_sev) + "+"

    header1 = f"|{title1.center(severity_labels_lengths," ")}|{title3.center(count_sev," ")}|"
    header2 = f"|{title2.center(category_labels_lengths," ")}|{title3.center(count_cat," ")}|"


    yield border_sev_width
    yield header1
    yield border_sev_width
    sev_items = list(severity_breakdown.items())
    cat_items = list(category_breakdown.items())
    for i in range(len(sev_items)):
        severity, severity_count = sev_items[i]
        sev_row = f"|{severity.center(severity_labels_lengths," ")}|{str(severity_count).center(count_sev," ")}|"
        yield sev_row
    yield border_sev_width    
    yield ""
    yield border_cat_width
    yield header2
    yield border_cat_width
    for i in range(len(cat_items)):
        category, cat_count = cat_items[i]
        cat_row = f"|{category.center(category_labels_lengths, " ")}|{str(cat_count).center(count_cat," ")}|"
        yield cat_row
    yield border_cat_width

def build_word_table(wordList):
    title1 = "Word"
    title2 = "Category"
    title3 = "Severity"
    title4 = "Count"

    #getting lengths of words and titles

    severity_name_lengths = [len(data["severity"]) for word, data in wordList.items()]
    severity_name_lengths.append(len(title3))
    word_lengths = [len(word) for word in wordList]
    word_lengths.append(len(title1))
    category_lengths = [len(data["category"]) for word, data in wordList.items()]
    category_lengths.append(len(title2))
    count_lengths = [len(str(data["count"])) for word, data in wordList.items()]
    count_lengths.append(len(title4))

    sev_count = max(severity_name_lengths)
    cat_count = max(category_lengths)
    word_count = max(word_lengths)
    count_count = max(count_lengths)
    

    header = f"|{title1.center(word_count," ")}|{title2.center(cat_count," ")}|{title3.center(sev_count, " ")}|{title4.center(count_count," ")}|"

    wordList_border = "+" + ("-" * word_count) + "+" + ("-" * cat_count) + "+" + ("-" * sev_count) + "+" + ("-" * count_count) + "+"

    wordList_items = list(wordList.items())
    yield wordList_border
    yield header
    yield wordList_border
    for i in range(len(wordList_items)):
        word, data = wordList_items[i] 
        category = data["category"]
        severity = data["severity"]
        count = data["count"]
        wordList_row = f"|{word.center(word_count," ")}|{category.center(cat_count," ")}|{severity.center(sev_count," ")}|{str(count).center(count_count," ")}|"
        yield wordList_row
    yield wordList_border
    yield ""
    
    #return  cat_count
    
