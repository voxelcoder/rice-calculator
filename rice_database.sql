-- Creates the liquid_types table.
CREATE TABLE IF NOT EXISTS liquid_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

-- Creates the rice_types table.
CREATE TABLE IF NOT EXISTS rice_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    info_text TEXT,
    liquid_type_id INTEGER NOT NULL,
    liquid_ratio REAL NOT NULL DEFAULT 1.5,
    FOREIGN KEY (liquid_type_id)
      REFERENCES liquid_types (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);

-- Creates the device_types table.
CREATE TABLE IF NOT EXISTS device_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

/*
 * Creates the rice_type_to_device_type table,
 * which links each rice type to a device and
 * their cooking time, respectively.
 */
CREATE TABLE IF NOT EXISTS rice_type_to_device_type (
    rice_type_id INTEGER,
    device_type_id INTEGER,
    cooking_time INTEGER NOT NULL,
    PRIMARY KEY (rice_type_id, device_type_id),
    FOREIGN KEY (rice_type_id)
      REFERENCES rice_types (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION,
    FOREIGN KEY (device_type_id)
       REFERENCES device_types (id)
          ON DELETE CASCADE
          ON UPDATE NO ACTION
);

-- Inserts liquids into the liquid_types table.
INSERT INTO liquid_types
    (id, type)
    VALUES
    (0, "Water"),
    (1, "Broth"),
    (2, "Milk");

/*
 * Inserts the rice ID, the rice's name, the liquid ID,
 * and, if necessary, a little info text on a specific
 * sort of rice into the rice_types table.
 */
INSERT INTO rice_types
    (id, type, liquid_type_id, liquid_ratio, info_text)
    VALUES
    (0, "Basmati", 0, 1.5, NULL),
    (1, "Whole Grain Basmati", 0, 2.5, NULL),
    (2, "Sushi", 0, 1.5, NULL),
    (3, "Risotto", 1, 3.0, NULL),
    (4, "Sadri", 0, 1.5, NULL),
    (5, "Jasmine", 0, 1.5, NULL),
    (6, "Whole Grain Jasmine", 0, 2.5, NULL),
    (7, "Rice Pudding", 2, 5.0, NULL),
    (8, "Brown", 0, 2.0, NULL),
    (9, "Paella", 1, 3.0, NULL),
    (10, "Red", 0, 2.5, NULL),
    (11, "Sticky", 0, 1.5, "Blanche the rice at least 2 hours in water before you wan't to use it!"),
    (12, "Black", 0, 2.5, NULL),
    (13, "Purple", 0, 2.5, NULL),
    (14, "Quinoa", 0, 2.0, NULL);

-- Inserts devices into the device_types table.
INSERT INTO device_types
    (id, type)
    VALUES
    (0, "Pot"),
    (1, "Rice cooker"),
    (2, "Microwave"),
    (3, "Steamer");

/*
 * Inserts rice ID's, device ID's and the cooking times
 * into the rice_type_to_device_type table.
 */
INSERT INTO rice_type_to_device_type
    (rice_type_id, device_type_id, cooking_time)
    VALUES
    (0, 0, 20), -- Basmati
    (0, 1, 15),
    (0, 2, 15),
    (0, 3, 40),
    (1, 0, 40), -- Whole Grain Basmati
    (1, 1, 30),
    (2, 0, 20), -- Sushi
    (2, 1, 15),
    (2, 2, 15),
    (2, 3, 40),
    (3, 0, 30), -- Risotto
    (4, 0, 20), -- Sadri
    (4, 1, 15),
    (4, 2, 15),
    (4, 3, 40),
    (5, 0, 20), -- Jasmine
    (5, 1, 15),
    (5, 2, 15),
    (5, 3, 40),
    (6, 0, 40), -- Whole Grain Jasmine
    (6, 1, 30),
    (7, 0, 30), -- Rice Pudding
    (8, 0, 30), -- Brown
    (8, 1, 25),
    (9, 0, 30), -- Paella
    (10, 0, 40), -- Red
    (10, 1, 30),
    (11, 0, 20), -- Sticky (Blanche 2h before use!! (still have to do an entry for that!)
    (11, 1, 15),
    (11, 2, 15),
    (11, 3, 40),
    (12, 0, 40), -- Black
    (12, 1, 30),
    (13, 0, 40), -- Purple
    (13, 1, 30),
    (14, 0, 20), -- Quinoa
    (14, 1, 15);
