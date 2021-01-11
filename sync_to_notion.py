from notion.client import NotionClient
from notion.block import PageBlock, TextBlock, SubheaderBlock, ToggleBlock
from os import environ as env
import threading

class SyncToNotion:
    def __init__(self, highlights):
        self.highlights = highlights
        self.sync()
        return
        thread = threading.Thread(target=self.sync, args=())
        thread.daemon = True
        thread.start()

    def sync(self):
        highlights = self.highlights
        print("Starting highlights sync")
        client = NotionClient(token_v2 = env['TOKEN_V2'])
        page = client.get_block(env["PAGE"])
        new_page_title = f"{highlights['title']} - {highlights['authors']}"
        try:
            for child in page.children:
                if child.title == new_page_title:
                    child.remove()
            new_notebook_page = page.children.add_new(PageBlock, title=new_page_title)
            saved_section_count = 0
            saved_highlight_count = 0
            for section in highlights["sections"]:
                new_notebook_page.children.add_new(SubheaderBlock, title = section["section_title"])
                for highlight in section["highlights"]:
                    new_highlight_block = new_notebook_page.children.add_new(ToggleBlock, title=highlight["text"])
                    new_highlight_block.children.add_new(TextBlock, title=highlight["heading"])
                    saved_highlight_count += 1
                    print(f"Saved highlight {saved_highlight_count} of {highlights['highlight_count']}")
                saved_section_count += 1
                print(f"Saved section {saved_section_count} of {highlights['section_count']}")
            print("Synced highlights")
        except Exception as e:
            print(e)
            print("An error occured while syncing!")
