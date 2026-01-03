from enum import Enum
from _html_node import LeafNode
import re
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url =None):
        self.text = text
        #Type_of_text = TextType()
        self.text_type = text_type 
        self.url = url
    def __eq__(self, node):
        return ((self.text == node.text) and (self.text_type == node.text_type) and (self.url == node.url))
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.name},{self.url})"

##### Following code turns a TextNode to an HTMLNode with no children i.e. LeafNode

def text_node_to_html_node(textnode):
    if not isinstance(textnode.text_type,TextType):
        raise Exception("Invalid text type")
    match textnode.text_type.value:
        case 'text': return LeafNode(None,textnode.text)
        case 'bold': return LeafNode('b',textnode.text)
        case 'italic': return LeafNode('i',textnode.text)
        case 'code': return LeafNode('code',textnode.text)
        case 'link': return LeafNode('a',textnode.text, {"href":f"{textnode.url}"})
        case 'image': return LeafNode('img','',{"alt":f"{textnode.text}","src":f"{textnode.url}"})

######### Following function splits TextNodes based on the delimiter passed to it

def node_type_decider(text, delimiter):
    match delimiter:
        case '': return TextNode(text,TextType.TEXT)
        case '**': return TextNode(text,TextType.BOLD)
        case '_': return TextNode(text,TextType.ITALIC)
        case "`": return TextNode(text,TextType.CODE)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        #print(f"{node} , text_type:{node.text_type.value}")

        if node.text_type.value != "text":
            new_nodes.append(node)
        if node.text_type.value == "text":
            if node.text:
                text_list =node.text.split(delimiter).copy()
                for i in range(0,len(text_list)):
                    if i%2 == 0:
                        node_t = node_type_decider(text_list[i],'')
                        new_nodes.append(node_t)
                    else:
                        node_d = node_type_decider(text_list[i],delimiter)
                        new_nodes.append(node_d)
            #else:
             #   node_ = TextNode('',TextType.TEXT)
              #  new_nodes.append(node_)
    return new_nodes
####### Following code takes TextNodes of TextType text and splits them into their image/link part and their text part.
def split_nodes_image(old_nodes):
    new_nodes = []
    #print(old_nodes)    
    for node in old_nodes:
        if node.text:
           pattern = r"(!\[[^\[\]]*\]\([^\(\)]*\))"
           text_list = re.split(pattern,node.text)
           if len(text_list) > 1 and (len(text_list)%2 ==1) :
               for i in range(len(text_list)):
                    if text_list[i] != '' and (i%2==0):
                        node_tl = TextNode(text_list[i], TextType.TEXT)  
                        new_nodes.append(node_tl)
                    elif i%2 == 1:
                         pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
                         matches= re.findall(pattern,text_list[i])
                         for match in matches:
                             #node_t = TextNode(match[0],TextType.TEXT)
                             node_img = TextNode(match[0],TextType.IMAGE,match[1])
                             new_nodes.append(node_img)
           else:
               new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    #print(old_nodes)
    for node in old_nodes:
        if node.text:
            pattern = r"(\[[^\[\]]*\]\([^\(\)]*\))"
            text_list = re.split(pattern,node.text)
            if len(text_list) > 1 and (len(text_list)%2 ==1) :
               for i in range(len(text_list)):
                   if text_list[i] != '' and i%2==0:
                       node_tl = TextNode(text_list[i], TextType.TEXT)  
                       new_nodes.append(node_tl)
                   elif i%2 ==1:   
                       pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
                       matches= re.findall(pattern,text_list[i])
                       if matches:
                           for match in matches:
                               #node_t = TextNode(match[0],TextType.TEXT)
                               node_link = TextNode(match[0],TextType.LINK,match[1])
                               new_nodes.append(node_link)
            else:
                new_nodes.append(node)
    return new_nodes

 ####### Following function turns text into a TextNode and splits it into multiple TextNodes of different TextType based on the delimiters in the text

def text_to_textnode(text):
    node = TextNode(text,TextType.TEXT)
    new_nodes = []
    oldnodes = [node]
    delimiters = ['**','_','`']
    for delimiter in delimiters:
        new_nodes = split_nodes_delimiter(oldnodes,delimiter,TextType.TEXT)
        oldnodes = new_nodes
    new_nodes = split_nodes_image(oldnodes)
    oldnodes = new_nodes.copy()
    new_nodes = split_nodes_link(oldnodes)

    #print(new_nodes)
    return new_nodes






