#print("hello, world")

from _text_node import TextNode, TextType
from _html_node import HTMLNode
from _generate_page import generate_page_rec
import logging
import os
import shutil

#logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Added %(name)s
    handlers=[
        logging.FileHandler("my_application.log"),
        logging.StreamHandler()
    ]
)

# Get a logger for the main module
logger = logging.getLogger(__name__) # This will create a logger named 'main'



# Get the specific logger for '_text_node'
#text_node_logger = logging.getLogger('_text_node')
#text_node_logger.propagate = False # Messages from this logger will not go to parent handlers

# Note: If text_node_logger also has its own handlers, those will still work.
# If it has no handlers of its own and propagate is False, then no messages
# from _text_node.py will be processed at all.




def main():
    '''
    #text_type = TextType()
    Test_text_node = TextNode('some anchor text', TextType.LINK, 'http://www.ggogle.com')
    print(Test_text_node)

    Test_html_node = HTMLNode('<p>','p-values tell you how much confidnce you can have in random noise/chance doing as well as your model') 
    print(Test_html_node)
    #output = repr(Test_text_node)
    #print(output)
    '''
    def directory_cleaner(directory):
        if os.path.isdir(directory):
            ls_l = os.listdir(directory)
            for name in ls_l:
                path = os.path.join(directory,name)
                if os.path.isfile(path):
                    logging.info(f"Removing file: {path}")
                    os.remove(path)
                elif os.path.isdir(path):
                    directory_cleaner(path)
                    logging.info(f"Removing directory: {path}")
                    os.rmdir(path)


    def directory_copier(src,dest):
        #if (not os.path.isdir(src)) or (not os.path.isdir(dest)):
        #    print(f"{src} is a directory :{os.path.isdir(src)}")
        #    print(f"{dest} is a directory :{os.path.isdir(dest)}")
        #    raise Exception("unsuitable path passed")
        if not os.path.isdir(dest):
            logging.warning(f"Making new directors along the path: {dest}")
            os.makedirs(dest,exist_ok = True)  #Makes any intermediate directories that don't already exist
        if os.listdir(dest):
            directory_cleaner(dest)
        ls_source = os.listdir(src)
        logging.info(f"list of files, directoris in {src} directory is : \n {ls_source} \n")
        for name in ls_source:
            path = os.path.join(src,name)
            if os.path.isfile(path):
                logging.debug(f"copying file: {path}")
                shutil.copy(path,dest)
                logging.info(f"copied file: {path} to directory :{dest}")
            elif os.path.isdir(path):
                logging.info(f"copying directory: {path} ")
                os.mkdir(os.path.join(dest,name))
                source = path
                destination = os.path.join(dest,name)
                directory_copier(source,destination)
                logging.info(f"Copied directory {source} to {destination}")
            
    cwd = os.getcwd()
    logging.info(f"cwd : {cwd}")
    source = os.path.join(cwd,'src/static')
    logging.info(f"source : {source}")
    destination = os.path.join(cwd,'public')
    logging.info(f"destination: {destination}")
    directory_copier(source,destination)
    

    temp_path = os.path.join(cwd,'template.html')
    from_path = os.path.join(cwd,'content')
    dest_path = os.path.join(cwd,'public')
    logging.info(f"from_path :{from_path} ; dest_path :{dest_path} ; temp_path :{temp_path}")
    generate_page_rec(from_path,temp_path,dest_path)
    
        
        
if __name__ =="__main__" :
    main() 
