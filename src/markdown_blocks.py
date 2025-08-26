from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"



def markdown_to_blocks(markdown):
    split_text = markdown.split("\n\n")
    empty_removed = []
    for item in split_text:
        stripped_item = item.strip()
        if stripped_item: # not empty
            empty_removed.append(stripped_item)
    return empty_removed


def block_to_block_type(block):
    block_len = len(block)
    split_lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # commented code below is alternate in case we need checking for the block to not be empty after the " "
    """
    if block.startswith("#"):
        count = 0
        # Iterate through the characters of the block
        for char in block: # count is at the index we are checking each new loop
            # If the character is a '#', increment the count
            if char == "#":
                count += 1
            # If it's not a '#', we've found the end of the leading hashes, so break the loop
            else:
                break
        if 1 <= count <= 6 and block_len >= count + 2 and block[count] == " ":
            return BlockType.HEADING
    """
    if block.startswith("```") and block.endswith("```") and block_len >= 6:
        return BlockType.CODE
    if block.startswith(">"):
        for line in split_lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH 
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in split_lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH 
        return BlockType.ULIST
    if block[0:3] == "1. ":
        num = 1
        for line in split_lines:
            expected = f"{num}. "
            if not line.startswith(expected):
                return BlockType.PARAGRAPH 
            num += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH 