#from textnode import TextNode, TextType
class HTMLNode:
      def __init__(self, tag=None, value=None, children=None, props=None):
          self.tag = tag
          self.value = value
          self.children = children
          self.props = props

      def to_html(self):
          raise NotimplementedError("to_html is not implemented")

      def props_to_html(self):
          if self.props is None:
              return ''
          if not self.props:
              return ''
          output = ''
          for key in self.props:
              output+= f' {key}="{self.props[key]}"' #extra space before every key=value output
              #print(output)
          return output
      def __repr__(self):
          return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

         
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        
        super().__init__(tag, value, None, props)

    def to_html(self):
        print(self)
        if self.value is None:
            raise ValueError("Leaf nodes must have value")
        if not self.tag:
            return f"{self.value}"
        ''' match self.tag:
            case "p": 
                return f"<p>{self.value}</p>"
            case "b": 
                return f"<b>{self.value}</b>"
            case "i" : 
                return f"<i>{self.value}</i>"
            case "a": 
                for key in self.props:
                    return f"<a {key}={self.props[key]}>{self.value}</a>" 
            case _ : 
                return "Tag not recognized" '''
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
    def to_html(self):
        print(self)
        if not self.tag:
            raise ValueError("There's no tag- Not a node.")
        if not self.children:
            raise ValueError("The node has no children- Not a parent")
        output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            output += f"{child.to_html()}"
        output = output + f"</{self.tag}>"
        return output
'''
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

'''
