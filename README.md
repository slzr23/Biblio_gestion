# Biblio_gestion
A software program to to make it easier to manage a book library , made by SLZR for a school project.

# Explanatory notes
This system works  with Python and SQL (go to biblio.py to see exactly how it works). You can manage any book library with some different methods. 

# Different functions & methods
You have different functions that you can use: 
    - add a new member: this function send a request to the SQL database in order to add a new member in the member's table. The new member has to fill out a                 registration form.
    - add a new book: this function send a request to the SQL database in order to add a new book in the book's table. The user just has to give the ISBN of the new         book, and the programm will find the information about the book (thanks to the API 'isbnlib'). 
    - make a loan: this function send a request to the SQL database in order to add a new loan in the loan's table. The new memeber has to fill in a form.

# API 'isbnlib'
Thaks to the API 'isbnlib', you can find all the information about a book just by writing its ISBN

# Vigenere
For Vigenere's method, the system is the same: it works also with a key. The key is in the form of a word or a sentence. In order to encrypt our text, for each character we use a letter of the key to perform the substitution. Obviously, the longer and more varied the key, the better the text will be encrypted.
(Vigenere decryption is coming)

# Displaying
For the software display, I used a famous python library called "Tkinter", here is the documentation that explain who this library works:(https://docs.python.org/fr/3/library/tk.html)

# ZIP file
The  software is available in ".exe" format in the zipped file called "Message_Encoder.zip". To make it executable, I used a software called "auto-py-to-exe", you can find and download this software here: 
(https://pypi.org/project/auto-py-to-exe/)

# Contact
If you have any question or want to contact me: slzr.tech@gmail.com


# THANKS FOR READING
