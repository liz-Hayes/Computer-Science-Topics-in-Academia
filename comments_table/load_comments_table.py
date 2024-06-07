import mysql_utils
import sys 

csv_loc = sys.argv[1]

#Create the comments table
stmt = "CREATE TABLE comments (id INT PRIMARY KEY , text VARCHAR(1000) NOT NULL, num_likes INT DEFAULT 0, keyword_id INT NOT NULL, FOREIGN KEY (keyword_id) REFERENCES keyword (id) );"
mysql_utils.exec(stmt)

#Load data from proviced comments.csv into DB
stmt = 'LOAD DATA INFILE \'' + csv_loc+'\' INTO TABLE comments FIELDS TERMINATED BY \',\' IGNORE 1 ROWS;'
mysql_utils.exec(stmt) 