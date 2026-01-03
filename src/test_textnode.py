import unittest
from _text_node import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnode


class TestTextNode(unittest.TestCase):
    def test_eq_b(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD) 
        self.assertEqual(node, node2)

    def test_eq_i(self):
        node = TextNode("This is another text node", TextType.ITALIC)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertEqual(node, node2) 

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node,node2)

    def test_eq_l(self):
        node = TextNode("This is a link",TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is an image", TextType.IMAGE, "https://stock.adobe.com/search?k=christmas&asset_id=303504904")
        self.assertNotEqual(node,node2) 

    def test_eq_nlb(self):
        node = TextNode("This is a link", TextType.LINK, "https://ww.google.com")
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node,node2)


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

class test_split_nodes_delimiter(unittest.TestCase):
    def test_code(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("`code block` starts with code",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        output_node_1 = TextNode("This is text with a ",TextType.TEXT) 
        self.assertEqual(new_nodes[0],output_node_1)
        self.assertEqual(new_nodes[3],TextNode('',TextType.TEXT))

    def test_bold(self):
        node_b = TextNode("This is text with a **bold block**",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_b],"**",TextType.BOLD)
        output_node_1 = TextNode("bold block", TextType.BOLD)
        self.assertEqual(new_nodes[1],output_node_1)
        self.assertEqual(new_nodes[2],TextNode('',TextType.TEXT))

    def test_italic(self):
        node_i = TextNode("This has an _italic block_ and `code block` but only one splits", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_i],"_",TextType.ITALIC)
        output_node_2 = TextNode(" and `code block` but only one splits", TextType.TEXT)
        self.assertEqual(new_nodes[2], output_node_2)


class test_split_nodes_image_link(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes)

    def test_split_images(self):
        node = TextNode(
         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        , TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ],
        new_nodes
    )


class text_to_textnode_of_correct_type(unittest.TestCase):
       def test_text_to_textnode_all(self):
           text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
           new_nodes = text_to_textnode(text)
           self.assertListEqual(
           [
           TextNode("This is ", TextType.TEXT),
           TextNode("text", TextType.BOLD),
           TextNode(" with an ", TextType.TEXT),
           TextNode("italic", TextType.ITALIC),
           TextNode(" word and a ", TextType.TEXT),
           TextNode("code block", TextType.CODE),
           TextNode(" and an ", TextType.TEXT),
           TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
           TextNode(" and a ", TextType.TEXT),
           TextNode("link", TextType.LINK, "https://boot.dev"), 
           ], new_nodes)

       def test_text_to_textnode_delims(self):
           text = "This is **bold** with some _italic stuff_ and some `code print()` but no links"
           new_nodes = text_to_textnode(text)
           self.assertListEqual(
           [
           TextNode("This is ",TextType.TEXT), 
           TextNode("bold",TextType.BOLD), 
           TextNode(" with some ",TextType.TEXT),
           TextNode("italic stuff",TextType.ITALIC),
           TextNode(" and some ",TextType.TEXT),
           TextNode("code print()", TextType.CODE),
           TextNode(" but no links",TextType.TEXT),
           ], new_nodes)

if __name__ == "__main__":
    unittest.main()
