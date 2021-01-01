from bs4 import BeautifulSoup
import pprint
import sys

def parse_notebook(notebook_data):
    notebook_details = \
    {
        "title": "",
        "authors": "",
        "sections": [ ]
    }

    current_section = None
    current_highlight = None
    highlight_count = 0
    section_count = 0

    soup = BeautifulSoup(notebook_data, "html.parser")

    for div in soup.find_all("div"):
        classname = div.get("class")[0]
        #print(classname)
        data = div.text.strip()
        if classname == "bookTitle":
            print("Book title")
            notebook_details["title"] = data
        elif classname == "authors":
            print("authors")
            notebook_details["authors"] = data
        elif classname == "sectionHeading":
            notebook_details["sections"].append(
                {
                    "section_title": data,
                    "highlights": [ ]
                }
            )
            current_section = notebook_details["sections"][-1]
            section_count += 1
        elif classname == "noteHeading":
            current_section["highlights"].append(
                {
                    "heading": data,
                    "text": ""
                }
            )
            current_highlight = current_section["highlights"][-1]
            highlight_count += 1
        elif classname == "noteText":
            current_highlight["text"] = data

    notebook_details["section_count"] = section_count
    notebook_details["highlight_count"] = highlight_count
    return notebook_details

if __name__ == "__main__":
    notebook_file = open(sys.argv[1], "r")
    details = parse_notebook(notebook_file.read())
    for section in details["sections"]:
        print(section["section_title"])


