import unittest
from _markdown_extractor import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title  

'''
class test_extractor(unittest.TestCase):
    def test_md_to_blocks_extralineseparation(self):
        md = """
This is simple.



 Lets see if this works.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
                blocks,
                [
                 "This is simple.",
                 "Lets see if this works.",
                ])
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
      



    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        print(matches)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_links(self):
        matches = extract_markdown_links("This is a text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")],matches)
    


class test_block_to_block_type(unittest.TestCase):
    def test_block_type_heading(self):
        block1 = "# This is a heading."
        block2 = "##2# This is not a heading"
        self.assertEqual(block_to_block_type(block1),BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(block2),BlockType.HEADING)

    def test_block_type_ordered_list(self):
        block1 = """1. This is element one.
2. This should be okay."""
        block2 = """2. This is weird.
5. Clearly not numbered properly."""
        self.assertEqual(block_to_block_type(block1),BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(block2),BlockType.ORDERED_LIST)
    
    def test_block_type_unordered_list(self):
        block1 = """- This is element one.
- This should be okay."""
        block2 = """- This is weird.
-Clearly not spaced properly."""
        self.assertEqual(block_to_block_type(block1),BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(block2),BlockType.UNORDERED_LIST)

    def test_block_quote(self):
        block = """> What ?
>%?@ who said that ?"""
        self.assertEqual(block_to_block_type(block),BlockType.QUOTE)

    def test_block_type_code(self):
        block1 = "``` This will be code () %, but what kind ```"
        block2 = """```More than one line.
Doesn't matter.```"""
        self.assertEqual(block_to_block_type(block1),BlockType.CODE)
        self.assertEqual(block_to_block_type(block2),BlockType.CODE)
    
    def test_block_type_paragraph(self):
        block1 = "This should be a paragraph."
        block2 = """This could be a paragraph.
#Oh i think it is.
>But it has other shit in it"""
        self.assertEqual(block_to_block_type(block1),BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block2),BlockType.PARAGRAPH)
'''


class test_mark_down_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",)

    def test_quoteblock(self):
        md = """
>This is a long quote.
>Important things said he.
>Cause wise he was.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html) 
        self.assertEqual(
        html,
        "<div><blockquote>This is a long quote.\nImportant things said he.\nCause wise he was.</blockquote></div>")
    
    def test_headingblock(self):
        md = """
# This is the title.

## This is some chapter heading.
Very long one.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(html,
        "<div><h1>This is the title.</h1><h2>This is some chapter heading.\nVery long one.</h2></div>")

    def test_ordered_listblock(self):
        md = """
1. This is the first item.
2. This is the second.
But it is a long one.
3.  Just to finish.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(html,
        "<div><ol><li>This is the first item.</li><li>This is the second.\nBut it is a long one.</li><li>Just to finish.</li></ol></div>")
        
    def test_unordered_listblock(self):
        md = """
- This is item 1.
- This is the second one.
-  This is whatever.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(html,
        "<div><ul><li>This is item 1.</li><li>This is the second one.</li><li>This is whatever.</li></ul></div>")

    def test_extract_title(self):
        md = """
## This could be the title.
# #This is the title.
"""  
        title = extract_title(md)
        self.assertEqual("#This is the title.",title)


    def test_extract_file_notitle(self):
        md = """
## This is not a title.
### This is not a title.
This is not a title.
"""
        #title = extract_title(md)
        self.assertRaises(Exception, extract_title, md)
if __name__ =="__main__":
    unittest.main()
