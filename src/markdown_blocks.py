

def markdown_to_blocks(markdown):
    split_text = markdown.split("\n\n")
    empty_removed = []
    for item in split_text:
        stripped_item = item.strip()
        if stripped_item: # not empty
            empty_removed.append(stripped_item)
    return empty_removed

