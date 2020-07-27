# Selly Oak Clinic
Database engineering
## General info
Starting work on the project we analyzed the described business model of the clinic. We divided the work on the project into stages to better systematize our work. We started by designing the ER diagram and then we transformed it into a relational model. The next stage of our work was to implement all previously planned entities together with tables linking each of them with the n:m to Sqlite3 relation. Making sure that all the entities are well implemented, including the limitations in filling in individual records, we moved on to filling in our database with test data. The test data we implemented were selected in such a way as to show errors in relations between individual tables. There was enough data to check the operation of the database queries to such an extent that it was clearly visible which of the entered records corresponded to specific queries that should not appear in the selected queries and which were limit data checking the accuracy of the entered queries. After making sure that the database is working satisfactorily, we moved on to the implementation of our database to Python 3 along with building a graphic design to make it easier to use, we used Tkinter for this purpose. The individual stages of our work and the assumptions for our database are described in more detail below.

## Technologies 
Project is created with:
Python, sqlite3, tkinter
