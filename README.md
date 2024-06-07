<h1>Computer Science Keyword Explorer</h1>
<h2>Purpose</h2>
The purpose of this application is to allow students to explore topics in Computer Science.  The users of this dashboard could be potential students who want to compare areas of computer science and find the best universities to apply to based on their interests.  This dashboard will give them a great starting place to inform their decision.


![Computer Science Keyword Explorer App](https://github.com/CS411DSO-SP24/ElizabethHayes/blob/main/images/app.PNG)\

<h2>Demo</h2>
[Computer Science Keyword Explorer Demo Video ](https://mediaspace.illinois.edu/media/t/1_jg8kgvib)


<h2>Installation</h2> 

1. Clone the repository

```
git clone https://github.com/CS411DSO-SP24/ElizabethHayes.git
```

2. Install necessary packages:

```
pip install dash
pip install pandas
pip install dash_bootstrap_components
pip install plotly_express
```

3. Use the 'load_comments_table.py' script to create and populate the comments table in MySQL

```
python load_comments_table.py [PATH_TO_COMMENTS_CSV]
```

**NOTE:** If MySQL server is using the --secure-file-priv option, then the comments.csv file must be uploaded from the directory specified by --secure-file-priv.

4. Start Neo4j Database 
![start neo4j](https://github.com/CS411DSO-SP24/ElizabethHayes/blob/main/images/start_neo4j.PNG)

5. Change directories to the repository. In your terminal, run:

```
  python .\app.py
```

6. Follow link to see dash app
![start app](https://github.com/CS411DSO-SP24/ElizabethHayes/blob/main/images/start_app.PNG)


<h2>Usage</h2> 
Select a CS keyword from the drop down menu at the top of the page, or start typing to search for a keyword you're interested in.  The widgets will update to display information about this keyword.  To see top faculty for the keyword at a specific univeristy, select the 'See Faculty' button for the university you are interested in. To add a comment about the keyword, type your comment and hit the 'Submit' button.  Like a comment by selecting the '♥' button.

<h2>Design</h2>
The dashboard utilizes the MySQL, MongoDB, and Neo4j databases used throughout the semester.  Additionally, the dashboard uses a 'comments' table with the following schema:

![comments table schema](https://github.com/CS411DSO-SP24/ElizabethHayes/blob/main/images/comments_table_schema.PNG)

The top of the page contains a dropdown with all the keywords from the dataset. Selecting a keyword, causes each widget to update.  Upon starting up the app, 'machine learning' is the default selected keyword. The first widget shows top universities for the keyword.  When the keyword is changed, MySQL is queried to display the top 5 univeristies for the keyword.  The universities are displayed, each with a 'See Faculty Button'.  Selecting this button for a university updates the 2nd widget which displays top faculty.  This widget uses Neo4j as its backend database to display top faculty for the selected keyword at the selected university.  If no university has been selected, the widget displays top faculty at the top university.  The third widget displays information about the top 5 most relevant publications to the keyword. This widget uses MongoDB as its backend.  The fourth widget queries SQL and displays the keyword popularity over time in a plotly express line graph.  The final two widgets are encompassed in the comments section.  The first widget adds comments to the MySQL 'comments' table. A user can type a comment into the input box.  When the submit button is pressed, the comment gets inserted into the database. All comments for the keyword are displayed.  The final widget allows users to update the comments by liking them. Selecting the like button on a comment increments the num_likes field in the MySQL database and updates the number of likes displayed on the app.

<h2>Implementation</h2> 
This project uses SQL, MongoDB, and Neo4j as the backend databases. To connect my dash app with each database, I created mysql_utils.py, neo4j_utils.py, and mongodb_utils.py. To connect to each database I used MySQL Connector/Python, Neo4j Python driver, and PyMongo.
For the frontend, I used Dash Plotly. Libraries used include Dash Bootstrap Components, Pandas, and Plotly Express. To create the app layout, I used the components Row, Col, and Stack from Dash Bootstrap Components.  I also used Table to build a table of top publications and Card to build containers for the comments and top universities. Plotly Express was used to build a line graph showing the popularity of the keyword in publications over time. Pandas is also used throughout the code to manage queried data.

<h2>Database Techniques</h2> 

1. Transactions (SQL): In the insert, exec, and delete functions in my_sql_uils implement transactions by using the commit and rollback methods. In each of these functions, we attempt to execute a SQL statement.  If the execute step passes, then we permanently commit the change. If either of those steps fail, the change is reversed and not commited, using the rollback method.

2. [Prepared Statements (SQL)](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorprepared.html):  The insert function in my_sql_utils.py creates a cursor that is able to execute prepared statements.  The statement is then executed using a parameterized input 

3. Constraints (SQL): In the comments table there are contraints on various fields.  For example, the num_likes field has a default value of 0.  Additionally, the id field has the PRIMARY_KEY constraint. 

<h2>Extra-Credit Capabilities</h2>

1. Multi-database querying:  The widgets that display top faculty and top publications use multi-database querying.  The keyword drop down list in generated from querying MySQL.  The result of the dropdown selection is then used to query Neo4j and MongoDB.

2. Data expansion: An additional 'comments' dataset has been provided.  This additional table is useful because it allows users to interact by leaving comments on the page and liking eachother's comments.

<h2>Contributions</h2> 

I completed this project on my own and spent about 40 hrs to complete it.
