from textnode import TextNode, TextType
from copy_static import copy_static

def main():


    node = TextNode(
        "This is a text node",
        TextType.BOLD, 
        "https://www.boot.dev"
        )
    
    print(node) # __repr__ method automatically called, no need to explicitly call it

    copy_static("static", "public")

if __name__ == "__main__": # evaluates to TRUE if this script/file is run directly, so code below executes. If you import it to someting else, this will be FALSE, so code below will not run automatically
    main() # main function gets executed
    
