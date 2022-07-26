-- items table
CREATE SEQUENCE item_id_seq START WITH 1;
CREATE SEQUENCE item_type_id_seq START WITH 1;
create table items (
    item_id INTEGER PRIMARY KEY,
    Item_Type VARCHAR(100),
    Item_Type_ID INTEGER,
    Price   INTEGER, 
    Effective_From  DATE,
    Effective_To DATE,
    CREATED_DATE DATE,
    CREATED_BY  VARCHAR(20),
    LAST_UPDATED_DATE DATE,
    LAST_UPDATED_BY VARCHAR(100)
);

-- location table (need to add)
CREATE SEQUENCE location_id START WITH 1;
CREATE TABLE Locations(
    location_id INTEGER PRIMARY KEY,
    area VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    Created_Date DATE,
    Last_Updated_Date DATE
);  

INSERT INTO Locations VALUES 
(NEXTVAL('location_id'),
 'WADGAON','PUNE','MH','IN',CURRENT_DATE,CURRENT_DATE);
 INSERT INTO Locations VALUES 
(NEXTVAL('location_id'),
 'BANER','PUNE','MH','IN',CURRENT_DATE,CURRENT_DATE);
 INSERT INTO Locations VALUES 
(NEXTVAL('location_id'),
 'BANDRA','MUMBAI','MH','IN',CURRENT_DATE,CURRENT_DATE);
 INSERT INTO Locations VALUES 
(NEXTVAL('location_id'),
 'JUHU','MUMBAI','MH','IN',CURRENT_DATE,CURRENT_DATE);
 INSERT INTO Locations VALUES 
(NEXTVAL('location_id'),
 'DHAYARI','PUNE','MH','IN',CURRENT_DATE,CURRENT_DATE);
 /
 INSERT INTO Locations VALUES 
(NEXTVAL('location_id'),
 'WAKAD','PUNE','MH','IN',CURRENT_DATE,CURRENT_DATE);
 INSERT INTO Locations VALUES 
(NEXTVAL('location_id'),
 'INDIRA NAGAR','HYDERABAD','TS','IN',CURRENT_DATE,CURRENT_DATE);

-- milkman table
CREATE SEQUENCE milkman_id START WITH 1;
CREATE TABLE MILKMAN(
    milkman_id INTEGER PRIMARY KEY,
    milkman_shop VARCHAR(100),
    Created_Date DATE,
    Last_Updated_Date DATE
);
ALTER TABLE MILKMAN
    ADD COLUMN location_id INTEGER REFERENCES locations(location_id);
ALTER TABLE MILKMAN
    ADD COLUMN signed_in BOOLEAN;
ALTER TABLE MILKMAN
    ADD COLUMN password text;

-- users table
CREATE SEQUENCE User_ID START WITH 1;
create table users (
User_ID INTEGER PRIMARY KEY,
Social_Media_Name VARCHAR(100),
Social_Media_Email VARCHAR(100),
Social_Media_Type  VARCHAR(100),
Is_Admin Boolean,
signed_in Boolean,
Password text,
user_rating FLOAT,
address VARCHAR(1000)
);

ALTER TABLE users
    ADD COLUMN milkman_id INTEGER REFERENCES milkman(milkman_id);

-- change_details table
CREATE SEQUENCE Change_ID START WITH 1;
create table Change_Details (
Change_ID INTEGER PRIMARY KEY,
Item_ID INTEGER,
QTY FLOAT,
User_ID INTEGER,
Effective_From DATE,
Effective_To DATE
);

-- default_details table
CREATE SEQUENCE Default_ID START WITH 1000;
create table Default_Details (
Default_ID INTEGER PRIMARY KEY,
Item_ID INTEGER,
Qty  FLOAT,
User_ID INTEGER,
Created_Date DATE,
Last_Updated_Date DATE,
Effective_From DATE,
Effective_To DATE
);

-- milkman_rating table
CREATE SEQUENCE RATING_ID START WITH 1;
create table milkman_rating(
    RATING_ID INTEGER PRIMARY KEY,
	MILKMAN_ID INTEGER,
	OVERALL_RATING FLOAT,
	NO_OF_USERS INTEGER
)
-- ALTER SEQUENCE RATING_ID RESTART WITH 1;
