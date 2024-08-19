# Dependency Explaining

This project will create an excel file containing descreptions and info about dependencies in a git project and stats about languages.

This project is depended on the following projects:

- syft (https://github.com/anchore/syft)
- github-linguist, the tool used by github to determain the language usage for every project (https://github.com/github-linguist/linguist)
- openpyxl (python lib)
- openai api (will be changed)

Installation:
--------------

1. install openpyxl:
   ```console
   pip install openpyxl
   
3. install the oenai api (will be changed):
   ```console
   pip install openai
5. install syft:
   follow instructions on the project's github.
6. install github-linguist:
   follow instructions on the project's github.  
   > check you can run in the terminal:
   > ```console
   >  github-linguist
   >  ```
   > if not you may need to add it to the PATH

running the project:
----------------------

1. create an excel file containing the projects url one after the other in column A.
   for example:  
   ![Screenshot 2024-08-19 at 21 48 18](https://github.com/user-attachments/assets/f1d8b2d5-5937-45fa-b5c7-a3db263b25a8)

3. download the python file (main.py) and run it with the following arguments, as shown in this command:  
   ```console
   python3 main.py [path to the input excel you created earlier] [openai api key] [path to excel output file]
