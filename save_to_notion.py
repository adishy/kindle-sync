from notion.client import NotionClient
from notion.block import PageBlock
from parse_highlights import parse_highlights
from os import environ as env

def save_to_notion():
    file = open("original/input/atomic_habits_highlights.html")
    highlights = parse_highlights(file.read())
    client = NotionClient(token_v2 = env['TOKEN_V2'])
    page = client.get_block(env["PAGE"])
    page.title = "Kindle from script"
    newchild = page.children.add_new(PageBlock, title=f"{highlights['title']} - {highlights['authors']}")
    print(page.title)


if __name__ == "__main__":
    save_to_notion()