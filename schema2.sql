  CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_name TEXT NOT NULL,
  event_date TEXT NOT NULL,
  event_time TEXT NOT NULL,
  graphic TEXT NOT NULL
  );

INSERT INTO events (event_name, event_date, event_time, graphic) VALUES ('Event 1', '20/11/2025', '16:30', 'images/pexels-photo-596134.webp'), ('Event 2', '1/9/2025', '18:00', 'images/pexels-photo-596134.webp');

DROP TABLE IF EXISTS test;
  CREATE TABLE test (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  data TEXT NOT NULL,
  newtest TEXT NOT NULL
  );

  INSERT INTO test (name, data, newtest) VALUES ('name', 'data', 'data2');

