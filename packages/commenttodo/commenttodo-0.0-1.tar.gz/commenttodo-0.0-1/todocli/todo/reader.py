import re
import os
from .utils.comment import Comment
from .utils.file import File
from .config import lang_list

#   this is the module to read the files and find the comments in them

def read_line_in_file(file_name:str, regex_to_find):
    comments = []
    linenum = 0
    try:
        with open(file_name, 'r') as file:
            for line in file:
                linenum += 1
                for regex in regex_to_find:
                    match = re.search(regex, line)
                    if match:
                        comments.append(Comment(linenum, match.group(1)))
    except FileNotFoundError:
        raise
    return comments

def create_file_object(file_name:str, comments:list):
    if len(comments) > 0:
        return File(file_name, comments)
    else:
        return None

def read_comments_in_files(file_names:list):
    found_comments = []
    for fname in file_names:
        file_extension = os.path.splitext(fname)[1].lower()
        try:
            regex_list = lang_list[file_extension].get_compiled_regexes()
        except KeyError as error:
            error.args = [r"No such extension is supported: '" + f'{file_extension}' + r"'"]
            raise
        comment_in_file = read_line_in_file(fname, regex_list)
        found_comments.append(create_file_object(fname, comment_in_file))
    found_comments =  list(filter(None, found_comments))
    return found_comments

def attach_working_dir(commandsObj):
    # if no file or folder is specified, use current working directory
    if commandsObj.names is None or not commandsObj.names :
        commandsObj.names = [os.getcwd()]
        commandsObj.is_folder = True
    return commandsObj

def get_all_dir_files(folders:list, debug:bool, extensions:list):
    files = []
    if (debug):
        print(folders)
        print("Files found:")
    for folder in folders:
        #   will look through the specified folder and all its sub/child folders
        #   find all the files in the foldeR and sub folders
        #   join the path of the file to the root path
        #   add the file path to the array
        try:
            fnames = [os.path.join(root_dir,file) for root_dir,sub_dir,found_files in os.walk(folder) for file in found_files]
        except OSError:
            raise
        # Only add known source code extensions to the list
        for fname in fnames:
            if (debug):
                print(fname)
            if (fname.lower().endswith(tuple(extensions))):
                files.append(fname)

    if (debug):
        print(files)
    
    #comments = read_comments_in_files(files_to_read.names)
    return files
