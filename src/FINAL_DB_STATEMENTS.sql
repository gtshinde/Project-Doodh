CREATE SEQUENCE item_id_seq START WITH 1;
CREATE SEQUENCE item_type_id_seq START WITH 1;
create table items (
Item_ID integer PRIMARY KEY,
Item_Type VARCHAR(100),
Item_Type_ID INTEGER,
Price   integer, 
Effective_From  DATE,
Effective_To DATE,
CREATED_DATE DATE,
CREATED_BY  VARCHAR(20),
LAST_UPDATED_DATE DATE,
LAST_UPDATED_BY VARCHAR(100)
);


SELECT * FROM ITEMS;
CREATE SEQUENCE User_ID START WITH 1;

create table users (
User_ID integer PRIMARY KEY,
Social_Media_Name VARCHAR(100),
Social_Media_Email VARCHAR(100),
Social_Media_Type  VARCHAR(100),
Is_Admin Boolean,
signed_in VARCHAR(1),
Password text
);
CREATE SEQUENCE Change_ID START WITH 1;
CREATE TABLE MILKMAN(
    milkman_id INTEGER PRIMARY KEY,
    milkman_shop VARCHAR(100),
    area VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    Created_Date DATE,
    Last_Updated_Date DATE
);

ALTER TABLE users
    ADD COLUMN milkman_id INTEGER REFERENCES milkman(milkman_id);

create table Change_Details (
Change_ID INTEGER PRIMARY KEY,
Item_ID INTEGER,
QTY FLOAT,
User_ID INTEGER,
Effective_From DATE,
Effective_To DATE
);
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