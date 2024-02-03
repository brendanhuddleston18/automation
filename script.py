from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path

import os 
import re
import shutil

console = Console()

def create_folder(path):
  folder_name = Prompt.ask("Enter desired name of directory")
  os.makedirs(f"{path}/{folder_name}", exist_ok=True)


def delete_user(user):
  try:
    os.makedirs(f"./temp_delete_{user}")
    shutil.move(f"lab/assets/{user}", f"temp_delete_{user}")
  except FileNotFoundError:
    console.print("[bold red]User Not found[/bold red]")
  

def sort_docs(directory, type=None):
  files = os.listdir(directory)
  matched_type_files = [file for file in files if re.search(type, file)]
  console.print(directory, type)
  if not os.path.exists(f"{directory}/{type}"):
    os.makedirs(f"{directory}/{type}")
  for matched_type in matched_type_files:
    if "mail" in matched_type:
      shutil.move(f"{directory}/{matched_type}", f"{directory}/mail")
    elif "log" in matched_type:
      shutil.move(f"{directory}/{matched_type}", f"{directory}/log")
      console.print("matched type log?", matched_type)
      if os.path.exists(f"{directory}/log"):
        log_files = os.listdir(f"{directory}/log")
        console.print(log_files)
        for log_file in log_files:
          parse_errors(directory, log_file)
      else:
        parse_errors(directory, matched_type)

def parse_errors(directory, file):
  with open(f"{directory}/log/{file}", 'r') as read_file:
    unpacked_file = read_file.read()

  warnings = ""
  errors = ""

  split_file_list = unpacked_file.split('\n')
  for line in split_file_list:
    if "WARNING" in line:
      warnings += f"{line}\n"
    elif "ERROR" in line:
      errors += f"{line}\n"
  
  if warnings:
    if os.path.exists(f"{directory}/log/warnings.txt"):
      with open(f"{directory}/log/warnings.txt", 'w') as warning_writes:
        warning_writes.write(f"{warnings}\n")
    else:
      Path(f"{directory}/log/warnings.txt").touch()
      with open(f"{directory}/log/warnings.txt", 'w') as warning_writes:
        warning_writes.write(f"{warnings}\n")
  
  if errors:
    if os.path.exists(f"{directory}/log/errors.txt"):
      with open(f"{directory}/log/errors.txt", 'w') as error_writes:
        error_writes.write(f"{errors}\n")
    else:
      Path(f"{directory}/log/error.txt").touch()
      with open(f"{directory}/log/error.txt", 'w') as error_writes:
        error_writes.write(f"{errors}\n")

def copy_directory(path):
  shutil.copytree(path, f"{path}.copy")
    

def menu():
  while True:
    console.print("\n 1. Create Folder \n 2. Delete User \n 3. Sort Docs \n 4. Make a Copy \n 5. Quit" )
    choice = Prompt.ask("Choose a task (Enter the number)", choices=['1', '2', '3', '4', '5'], default = '5')
    
    if choice == "1":
      path = None
      while path is None:
        path = Prompt.ask("Where do you want the new folder?")
      
      create_folder(path)
    elif choice == "2":
      user_to_delete = Prompt.ask("Provide username to delete")
      delete_user(user_to_delete)
    elif choice == "3":
      directory = Prompt.ask("Which directory do you want to sort?")
      files_to_sort = Prompt.ask("What type of files do you want to sort? enter: mail or log")
      sort_docs(directory, files_to_sort)
    elif choice == '4':
      directory = Prompt.ask("Which directory do you want to copy?")
      copy_directory(directory)
    else:
      break




if __name__ == "__main__":
  menu()