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
