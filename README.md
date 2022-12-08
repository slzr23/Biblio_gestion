# Biblio_gestion
A software program to to make it easier to manage a book library , made by SLZR for a school project.

# Explanatory notes
This system works with Python and SQL (go to biblio.py to see exactly how it works). You can manage any book library with some different methods. 

# Different functions & methods
You have different functions that you can use: 
    - add a new member: this function send a request to the SQL database in order to add a new member in the member's table. The new member has to fill out a                 registration form.
    - add a new book: this function send a request to the SQL database in order to add a new book in the book's table. The user just has to give the ISBN of the new         book, and the programm will find the information about the book (thanks to the API 'isbnlib'). 
    - make a loan: this function send a request to the SQL database in order to add a new loan in the loan's table. The new memeber has to fill in a form.

# API 'isbnlib'
Thaks to the API 'isbnlib', you can find all the information about a book just by writing its ISBN. I decided to implement this API in my project because of the fact that it can allow me to find every book just by its ISBN number. Here is the documentation of the API: (https://pypi.org/project/isbnlib/)

# SQL Database
Thanks to the SQL language, and with the use of DB Browser software, I built a database directly linked to my python program. It changes automatically when the user performs an action, depending on what he does (new member, new loan, new book,...)

# Displaying
For the software display, I used a famous python library called "Tkinter", here is the documentation that explain who this library works:(https://docs.python.org/fr/3/library/tk.html)

# Contact
If you have any question or want to contact me: slzr.tech@gmail.com


# THANKS FOR READING
