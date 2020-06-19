BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "logins" (
	"username"	text,
	"password"	text NOT NULL,
	"role"	text NOT NULL,
	PRIMARY KEY("username")
);
CREATE TABLE IF NOT EXISTS "customer" (
	"cust_id"	integer,
	"ssnid"	integer NOT NULL,
	"name"	text NOT NULL,
	"age"	integer NOT NULL,
	"address"	text,
	"state"	text,
	"city"	text,
	"status"	text,
	"last_updated"	text,
	"message"	text,
	PRIMARY KEY("cust_id")
);
CREATE TABLE IF NOT EXISTS "accounts" (
	"acc_id"	integer,
	"cust_id"	integer NOT NULL,
	"acc_type"	text NOT NULL,
	"balance"	integer NOT NULL,
	"message"	text,
	"last_updated"	text,
	"status"	text,
	FOREIGN KEY("cust_id") REFERENCES "customer"("cust_id"),
	PRIMARY KEY("acc_id")
);
CREATE TABLE IF NOT EXISTS "transactions" (
	"acc_id"	integer NOT NULL,
	"transaction_id"	integer,
	"description"	text NOT NULL,
	"date"	text NOT NULL,
	"amount"	integer NOT NULL,
	FOREIGN KEY("acc_id") REFERENCES "accounts"("acc_id"),
	PRIMARY KEY("transaction_id")
);
CREATE TABLE IF NOT EXISTS "login_timestamp" (
	"username"	text NOT NULL,
	"timestamp"	text NOT NULL,
	FOREIGN KEY("username") REFERENCES "login"("username")
);
INSERT INTO "logins" VALUES ('sainath123','S@inath123','cust_executive');
INSERT INTO "logins" VALUES ('sainath1234','S@inath123','cashier');
INSERT INTO "logins" VALUES ('admin123','Admin@1234','cust_executive');
INSERT INTO "logins" VALUES ('admin1234','Admin@1234','cashier');
INSERT INTO "customer" VALUES (100000002,789456123,'Arun Kudarihal',22,'Sainikpuri','Goa',' Madgaon ','Active','2020/06/17, 18:39:50','Customer update initiated successfully');
INSERT INTO "customer" VALUES (100000003,784656813,'Vasavi',22,'ECIL','Goa',' Mapuca ','Active','2020/06/18, 11:59:56','Customer creation initiated successfully');
INSERT INTO "accounts" VALUES (300000003,100000002,'savings',48400,'Amount received successfully','2020/06/18, 20:56:26','active');
INSERT INTO "transactions" VALUES (300000001,500000001,'Deposit','2020-06-17',20000);
INSERT INTO "transactions" VALUES (300000002,500000002,'Deposit','2020-06-17',2000);
INSERT INTO "transactions" VALUES (300000002,500000003,'Deposit','2020-06-17',2000);
INSERT INTO "transactions" VALUES (300000002,500000004,'Withdraw','2020-06-17',2000);
INSERT INTO "transactions" VALUES (300000002,500000005,'Deposit','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000006,'Deposit','2020-06-18',20000);
INSERT INTO "transactions" VALUES (300000002,500000007,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000002,500000008,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000002,500000009,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000010,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000002,500000011,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000002,500000012,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000002,500000013,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000002,500000014,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000002,500000015,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000002,500000016,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000002,500000017,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000018,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000002,500000019,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000002,500000020,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000002,500000021,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000022,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000002,500000023,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000002,500000024,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000002,500000025,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000026,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000027,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000028,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000029,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000030,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000031,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000032,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000033,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000034,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000035,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000036,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000037,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000038,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000004,500000039,'Deposit','2020-06-18',10000);
INSERT INTO "transactions" VALUES (300000005,500000040,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000041,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000042,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000043,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000044,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000004,500000045,'Deposit','2020-06-18',10000);
INSERT INTO "transactions" VALUES (300000005,500000046,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000047,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000048,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000049,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000050,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000004,500000051,'Deposit','2020-06-18',10000);
INSERT INTO "transactions" VALUES (300000005,500000052,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000053,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000054,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000055,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000056,'Recieved','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000004,500000057,'Deposit','2020-06-18',10000);
INSERT INTO "transactions" VALUES (300000005,500000058,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000059,'Deposit','2020-06-18',5000);
INSERT INTO "transactions" VALUES (300000003,500000060,'Withdraw','2020-06-18',1000);
INSERT INTO "transactions" VALUES (300000003,500000061,'Transfer','2020-06-18',100);
INSERT INTO "transactions" VALUES (300000003,500000062,'Recieved','2020-06-18',100);
INSERT INTO "login_timestamp" VALUES ('admin123','2020/06/18, 22:16:41');
COMMIT;
