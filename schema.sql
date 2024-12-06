DROP TABLE IF EXISTS users;
  CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
  );

