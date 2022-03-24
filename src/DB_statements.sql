CREATE SEQUENCE item_id_seq START WITH 1;

create table items (
Item_ID NUMBER PRIMARY KEY,
Item_Type VARCHAR2(100),
Item_UOM VARCHAR2(20),
Price   NUMBER(2), 
Effective_From  DATE,
Effective_To DATE,
CREATED_DATE DATE,
CREATED_BY  VARCHAR2(20),
LAST_UPDATED_DATE DATE,
LAST_UPDATED_BY VARCHAR2(100)
);

COMMIT;

INSERT INTO 
ITEMS (Item_ID,Item_Type,Item_UOM,Price) 
VALUES (item_id_seq.NEXTVAL,'COW MILK','Lt',58);

/

POSTGRES DB

create table items (
Item_ID integer PRIMARY KEY,
Item_Type VARCHAR(100),
-- Item_UOM VARCHAR(20),
Price   integer, 
Effective_From  DATE,
Effective_To DATE,
CREATED_DATE DATE,
CREATED_BY  VARCHAR(20),
LAST_UPDATED_DATE DATE,
LAST_UPDATED_BY VARCHAR(100)
);

select * from items;
CREATE SEQUENCE item_id_seq START WITH 1;

INSERT INTO 
ITEMS (Item_ID,Item_Type,Price) 
VALUES (nextval('item_id_seq'),'COW MILK',58);

COMMIT;

SELECT * FROM ITEMS;

CREATE SEQUENCE item_id_seq START WITH 1;
ALTER SEQUENCE item_id_seq RESTART WITH 2;  --to restart the seq

INSERT INTO 
ITEMS (Item_ID,Item_Type,Price, created_date, last_updated_date) 
VALUES (nextval('item_id_seq'),'ALMOND MILK',100, current_date, current_date); --for SYSDATE

COMMIT;

SELECT * FROM ITEMS;

CREATE SEQUENCE User_ID START WITH 1000;

create table users (
User_ID integer PRIMARY KEY,
Social_Media_Name VARCHAR(100),
Social_Media_Username VARCHAR(100),
Social_Media_Type  VARCHAR(100),
Is_Admin Boolean
);

SELECT * FROM USERS

CREATE SEQUENCE Change_ID START WITH 1000;

create table Change_Details (
Change_ID INTEGER PRIMARY KEY,
Change_DATE DATE,
Item_ID INTEGER,
QTY FLOAT,
User_ID INTEGER
);

SELECT * FROM Change_Details

CREATE SEQUENCE Default_ID START WITH 1000;

create table Default_Details (
Default_ID INTEGER PRIMARY KEY,
Item_ID INTEGER,
Qty  FLOAT,
User_ID INTEGER,
Created_Date DATE,
Last_Updated_Date DATE
);

SELECT * FROM Default_Details

ALTER TABLE Change_Details
ALTER COLUMN QTY TYPE FLOAT;