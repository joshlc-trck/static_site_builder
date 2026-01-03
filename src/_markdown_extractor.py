import re
from enum import Enum
from _text_node import TextNode, text_to_textnode, text_node_to_html_node
from _html_node import ParentNode, LeafNode

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks]
    #print([block.strip() for block in blocks if block.strip()])    
    return [block.strip() for block in blocks if block.strip()]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def check_heading(block):
    pattern = r"^[#]{1,6} "
    if re.findall(pattern,block):
       return True
    return False

def check_code(block):
    pattern = r"^```(?:[\d\D]*?)```$"
    if re.findall(pattern,block):
        return True
    return False

def check_quote(block):
    for line in block.split('\n'):
        if line[0] != ">":
            return False
    return True

def check_unordered(block):
    pattern = r"^- (?:[\d\D]*?)"
    for line in block.split('\n'):
        if not re.findall(pattern,line):
           return False
    return True

def check_ordered(block):
    pattern = r"([\d])+\. " 
    match = re.findall(pattern,block)
    if not match:
        return False
    for i in range(len(match)):    
        if int(match[i])!= (i+1) :
            return False
    return True

def block_to_block_type(block):
    if check_heading(block):
        return BlockType.HEADING
    elif check_code(block):
        return BlockType.CODE
    elif check_quote(block):
        return BlockType.QUOTE
    elif check_unordered(block):
        return BlockType.UNORDERED_LIST
    elif check_ordered(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def convert_text_nodes_to_html_nodes(text_nodes_list):
    html_nodes = []
    for node in text_nodes_list:
        print(node)
        html_node = text_node_to_html_node(node)
        print(html_node)
        html_nodes.append(html_node)
        
    return html_nodes

def block_to_children(block):
     text_nodes_list = text_to_textnode(block)
     html_nodes_list = convert_text_nodes_to_html_nodes(text_nodes_list)
     return html_nodes_list

def markdown_to_html_node(markdown):
    Blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in Blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                block = block.lstrip('`\n ').rstrip('`')
                child = LeafNode('code',block)
                node = ParentNode('pre', [child])
            case BlockType.HEADING:
                 pattern = r"^([#]+).*"
                 match = re.findall(pattern,block)
                 number = len(match[0])
                 block = block.lstrip('# ')
                 print(block)
                 children = block_to_children(block)
                 tag = f"h{number}"
                 node = ParentNode(tag,children)
            case BlockType.QUOTE:
                 quote_lines =[line.strip() for line in block.split('>') if line.strip()]
                 block_quote = '\n'.join(quote_lines)
                 children = block_to_children(block_quote)
                 node = ParentNode('blockquote',children)
            case BlockType.ORDERED_LIST:
                 pattern = r"[\d]+\. "
                 list_items = [line.strip() for line in re.split(pattern,block) if line.strip()]
                 nodes_for_items = []
                 for item in list_items:
                     children = block_to_children(item)
                     nodes_for_items.append(ParentNode('li',children))
                 node = ParentNode('ol',nodes_for_items)
            case BlockType.UNORDERED_LIST:
                 list_items = [item.strip() for item in block.split('-') if item.strip()]
                 nodes_for_items = []
                 for item in list_items:
                     children = block_to_children(item)
                     nodes_for_items.append(ParentNode('li',children)) 
                 node = ParentNode('ul',nodes_for_items) 
            case BlockType.PARAGRAPH:
                 block = block.replace('\n',' ')
                 children = block_to_children(block)
                 node = ParentNode('p',children)
        nodes.append(node)
    return ParentNode('div',nodes)    


def extract_title(markdown):
    md_line_list = markdown.splitlines()
    for line in md_line_list:
        if line.startswith('#') and line[1]!= '#':
            return line[1:].strip()
    raise Exception("No h1 header")

                           
'''

if __name__ == "__main__":
   with open('index_test.md','r') as f:
       md = f.read()
   #blocks_list = markdown_to_blocks(md)
   #print(blocks_list)
   #for block in blocks_list:
   #    print(f"The type of block is: {block_to_block_type(block)}")
   #    print(f"The block is :{block}", end = '\n\n\n')

   html_node = markdown_to_html_node(md)
   output = html_node.to_html()
   print(output)

'''









'''
def extract_markdown_images(text):
    #matched_images = re.findall(r"!\[(\w+)\]\((.*?)\)",text)
    matched_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matched_images

def extract_markdown_links(text):
    print(text)
    #matched_links = re.findall(r"\[(\w+)\]\((.*?)\)",text)
    matched_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matched_links
'''
