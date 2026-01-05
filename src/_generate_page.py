from _markdown_extractor import markdown_to_html_node, extract_title
from _html_node import ParentNode
import os
import re
import logging

logger = logging.getLogger(__name__)

def generate_page_rec(dir_path_content,temp_path,dest_path, base_path):
    logging.info(f"source :{dir_path_content} ; destination:{dest_path} ; temp: {temp_path}")
    if not os.path.isdir(dir_path_content):
        raise ValueError("Invalid content path")
    os.makedirs(dest_path,exist_ok = True)
    ls_content = os.listdir(dir_path_content)
    logging.info(ls_content)
    if ls_content:
        for element in ls_content:
            path = os.path.join(dir_path_content, element)
            if os.path.isfile(path):   #when element is a file
                if element.endswith('.md'):
                    new_dest_path = os.path.join(dest_path,element[:len(element)-3]+'.html')
                    generate_page(path,temp_path,new_dest_path,base_path)
            else:  #when element is a directory
                new_dest_path = os.path.join(dest_path,element)
                generate_page_rec(path, temp_path,new_dest_path,base_path)
    else:
        raise ValueError("The content directory is empty")






def generate_page(from_path, temp_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {temp_path}.")
    with open(from_path,'r') as f:
         md = f.read() 
    with open(temp_path, 'r') as t:
         template = t.read()
    html_string = markdown_to_html_node(md).to_html()
    Title = extract_title(md)
    temp_list = re.split(r"{{[\w ]+}}",template)
    template = temp_list[0] + Title + temp_list[1] + html_string + temp_list[2]
    #print(f"The template is : {template}") 
    template.replace('href="/',f'href="{base_path}')
    template.replace('href="/',f'href="{base_path}')
    
    os.makedirs(os.path.dirname(dest_path),exist_ok = True)
    with open(dest_path,'w') as html_dest:
         html_dest.write(template)
    with open(dest_path, 'r') as check:
         output = check.read()
         #print(f"At the destination {dest_path} the html looks like : {output}")

