DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS application_data;
DROP TABLE IF EXISTS signatories_table;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL
);

CREATE TABLE application_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT,
  subject TEXT,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE signatories_table (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
  application_id INTEGER,
	sig_name TEXT NOT NULL,
  email_id TEXT NOT NULL,
	designation TEXT NOT NULL,
	institute_name TEXT NOT NULL,
	gender TEXT NOT NULL,
  status CHAR,
	FOREIGN Key (application_id) REFERENCES application_data(id)
);