-- Active: 1790434080501@@127.0.0.1@3306@project69
-- ============================================================
--  schema.sql — ระบบฟิตเนส (นิสิตออกแบบและเขียนเอง)
--  กติกา: การจอง = M:N (member × gym_class), อุปกรณ์ต่อคลาส = M:N (gym_class × equipment),
--         แต่ละคลาสมีเทรนเนอร์ (1:M จาก trainer)
-- ============================================================
CREATE TABLE member (
    member_id     INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    gender        CHAR(1) NOT NULL,
    join_date     DATE NOT NULL,
    package_type  VARCHAR(50) NOT NULL
);
CREATE TABLE trainer (
    trainer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    specialty    VARCHAR(100) NOT NULL,
    phone        VARCHAR(15) NOT NULL

);
CREATE TABLE gym_class (          -- 1:M จาก trainer
    class_id      INT AUTO_INCREMENT PRIMARY KEY,
    trainer_id    INT NOT NULL,
    name          VARCHAR(100) NOT NULL,
    room          VARCHAR(50) NOT NULL,
    capacity      INT NOT NULL,
    schedule_time DATETIME NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id)
);
CREATE TABLE booking (            -- M:N: member × gym_class
    booking_id  INT AUTO_INCREMENT PRIMARY KEY,
    member_id   INT NOT NULL,
    class_id    INT NOT NULL,
    book_date   DATE NOT NULL,
    status      VARCHAR(20) NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (class_id) REFERENCES gym_class(class_id)
);
CREATE TABLE equipment (
    equip_id INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    zone     VARCHAR(50) NOT NULL,
    status   VARCHAR(20) NOT NULL
);
CREATE TABLE class_equipment (    -- M:N: gym_class × equipment
    class_id INT NOT NULL, 
    equip_id INT NOT NULL,
    quantity INT NOT NULL,
    CONSTRAINT pk_class_equip PRIMARY KEY (class_id, equip_id),
    FOREIGN KEY (class_id) REFERENCES gym_class(class_id),
    FOREIGN KEY (equip_id) REFERENCES equipment(equip_id)
);
-- TODO: INSERT ข้อมูลตัวอย่างทุกตาราง
INSERT INTO member (name, gender, join_date, package_type) VALUES
('Film',   'M', '2025-01-10', 'Basic'),
('jame',   'F', '2025-02-15', 'Premium'),
('keng',       'M', '2025-03-01', 'Basic'),
('khaw',     'F', '2025-03-20', 'Premium'),
('fam',    'M', '2025-04-05', 'VIP'),
('sam',     'F', '2025-05-11', 'Basic'),
('gun', 'M', '2025-06-18', 'Premium'),
('korn',    'F', '2025-07-02', 'VIP');

INSERT INTO trainer (name, specialty, phone) VALUES
('Coach Nat',    'Cardio',        '0891234567'),
('Coach Ploy',   'Yoga',          '0899876543'),
('Coach Beam',   'Weight Training','0812345678'),
('Coach Aof',    'Zumba',         '0823456789');

INSERT INTO gym_class (trainer_id, name, room, capacity, schedule_time) VALUES
(1, 'Morning Cardio Blast',  'Room A', 20, '2025-09-01 07:00:00'),
(2, 'Sunrise Yoga',          'Room B', 15, '2025-09-01 08:00:00'),
(3, 'Strength & Power',      'Room C', 12, '2025-09-01 17:00:00'),
(4, 'Zumba Dance Party',     'Room A', 25, '2025-09-01 18:00:00'),
(1, 'HIIT Cardio',           'Room A', 20, '2025-09-02 07:00:00'),
(3, 'Weight Lifting Basics', 'Room C', 10, '2025-09-02 18:00:00');

INSERT INTO booking (member_id, class_id, book_date, status) VALUES
(1, 1, '2025-08-30', 'Confirmed'),
(2, 2, '2025-08-30', 'Confirmed'),
(3, 3, '2025-08-30', 'Cancelled'),
(4, 4, '2025-08-31', 'Confirmed'),
(5, 1, '2025-08-31', 'Confirmed'),
(6, 5, '2025-09-01', 'Pending'),
(7, 6, '2025-09-01', 'Confirmed'),
(8, 2, '2025-09-01', 'Confirmed'),
(1, 5, '2025-09-02', 'Confirmed'),
(2, 6, '2025-09-02', 'Pending');

INSERT INTO equipment (name, zone, status) VALUES
('Treadmill',        'Cardio Zone',  'Available'),
('Stationary Bike',  'Cardio Zone',  'Available'),
('Dumbbell Set',     'Weight Zone',  'Available'),
('Barbell Rack',     'Weight Zone',  'Maintenance'),
('Yoga Mat',         'Studio Zone',  'Available'),
('Resistance Band',  'Studio Zone',  'Available'),
('Kettlebell',       'Weight Zone',  'Available'),
('Speaker System',   'Studio Zone',  'Available');

INSERT INTO class_equipment (class_id, equip_id, quantity) VALUES
(1, 1, 10),  
(1, 2, 10),
(2, 5, 15),   
(2, 6, 15),
(3, 3, 12),   
(3, 4, 4),
(3, 7, 8),
(4, 8, 1),    
(5, 1, 10),
(6, 3, 10);


