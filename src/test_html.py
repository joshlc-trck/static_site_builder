import unittest
from _html_node import HTMLNode, LeafNode, ParentNode # text_node_to_html_node
from _text_node import TextNode, TextType

class Test_HTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('p',"Some stuff")
        node2 = HTMLNode('p',"Some stuff") 
        self.assertEqual(node.tag,'p')
        self.assertEqual(node2.value,"Some stuff")
        self.assertEqual(node.__repr__(),node2.__repr__())

    def test_eq_a(self):
        node = HTMLNode('a',"Thisisalink",props={"href":"www.google.com"})
        node2 = HTMLNode('a',"Thisisalink",props={"href":"www.google.com"})
        self.assertEqual(node.__repr__(),node2.__repr__())

    def test_eq_diff(self):
        node = HTMLNode('a',"This is a link",props={"search": "results", "href":"www.google.com"})
        self.assertEqual(node.props_to_html(),' search="results" href="www.google.com"')
        node2 = HTMLNode('p',"R^2 tells us how much variance can we explain") 
        self.assertNotEqual(node,node2) 

class Test_LeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a","What is it ?",{"href":"www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">What is it ?</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b","p-values don't tell you much about your model!")
        self.assertEqual(node.to_html(),"<b>p-values don't tell you much about your model!</b>")


class Test_ParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",) 

    def test_to_html_with_multiplechildren(self):
        first_child_node = LeafNode("i","first child")
        second_child_node = LeafNode("b","second child")
        third_child_node = LeafNode("a","What is it ?",{"href":"www.google.com"})
        parent_node = ParentNode("p",[first_child_node,second_child_node,third_child_node])
        self.assertEqual(parent_node.to_html(),'<p><i>first child</i><b>second child</b><a href="www.google.com">What is it ?</a></p>')
        #print(parent_node.to_html()) 


    def test_to_html_with_no_childres(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("p",[])
            parent_node.to_html()    

'''
class test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_notag(self):
        node = TextNode("This ia a text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,None)
'''    

if __name__ == "__main__":
    unittest.main()
