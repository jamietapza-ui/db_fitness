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
    phone         VARCHAR(15) NOT NULL,
    birth_date    DATE NOT NULL,
    join_date     DATE NOT NULL,
    package_type  VARCHAR(10) NOT NULL
);

CREATE TABLE trainer (
    trainer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    specialty    VARCHAR(100) NOT NULL,
    phone        VARCHAR(15) NOT NULL,
    status       VARCHAR(20) NOT NULL
);

CREATE TABLE gym_class (          -- 1:M จาก trainer
    class_id      INT AUTO_INCREMENT PRIMARY KEY,
    trainer_id    INT NOT NULL,
    name          VARCHAR(100) NOT NULL,
    room          VARCHAR(50) NOT NULL,
    capacity      INT NOT NULL,
    start_date    DATETIME NOT NULL,
    end_date    DATETIME NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id)
);

CREATE TABLE booking (
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


INSERT INTO member (name, gender, phone, birth_date, join_date, package_type) VALUES
('Somchai Jaidee',     'M', '0812345601', '1995-03-14', '2026-01-05', 'basic'),
('Suda Rakdee',        'F', '0823456702', '1998-07-22', '2026-01-12', 'VIP'),
('Anan Wongsawat',     'M', '0834567803', '1990-11-02', '2026-02-01', 'VIP'),
('Napat Srisuk',       'F', '0845678904', '2001-05-30', '2026-02-15', 'basic'),
('Kittisak Phromma',   'M', '0856789005', '1987-09-18', '2026-03-03', 'premium'),
('Pimchanok Thongdee', 'F', '0867890106', '1999-12-09', '2026-03-20', 'premium'),
('Thanawat Boonmee',   'M', '0878901207', '1993-01-27', '2026-04-08', 'premium'),
('Warunee Saetang',    'F', '0889012308', '1996-06-11', '2026-05-14', 'basic'),
('Chaiwat Prasert',    'M', '0890123409', '1985-08-05', '2026-06-01', 'VIP'),
('Orawan Chaiyo',      'F', '0801234510', '2002-02-19', '2026-07-10', 'basic');

INSERT INTO trainer (name, specialty, phone, status) VALUES
('Kru Mali Sukjai',  'Yoga & Pilates',    '0911111101', 'Active'),
('Kru Tong Kaewkla', 'HIIT & Cardio',     '0922222202', 'Active'),
('Kru Ploy Meechai', 'Spinning',          '0933333303', 'Active'),
('Kru Beer Nakorn',  'Boxing',            '0944444404', 'On leave'),
('Kru Aom Vichai',   'Strength Training', '0955555505', 'Active');

INSERT INTO gym_class (trainer_id, name, room, capacity, start_date, end_date) VALUES
(1, 'Morning Yoga',      'Studio A',    20, '2026-10-12 07:00:00', '2026-10-12 08:00:00'),
(2, 'HIIT Burn',         'Studio B',    15, '2026-10-12 18:00:00', '2026-10-12 19:00:00'),
(3, 'Spinning',          'Cycle Room',  12, '2026-10-13 06:30:00', '2026-10-13 07:30:00'),
(4, 'Boxing Basics',     'Studio B',    12, '2026-10-13 19:00:00', '2026-10-13 20:00:00'),
(1, 'Pilates',           'Studio A',    15, '2026-10-14 09:00:00', '2026-10-14 10:00:00'),
(5, 'Strength Training', 'Weight Zone', 10, '2026-10-14 17:30:00', '2026-10-14 18:30:00'),
(2, 'Zumba Dance',       'Studio A',    25, '2026-10-15 18:30:00', '2026-10-15 19:30:00'),
(5, 'Core & Stretch',    'Studio B',    18, '2026-10-16 08:00:00', '2026-10-16 09:00:00');

INSERT INTO booking (member_id, class_id, book_date, status) VALUES
(1, 1, '2026-10-05', 'Confirmed'),
(2, 1, '2026-10-05', 'Confirmed'),
(3, 2, '2026-10-06', 'Confirmed'),
(4, 1, '2026-10-06', 'Cancelled'),
(5, 3, '2026-10-06', 'Confirmed'),
(6, 5, '2026-10-07', 'Confirmed'),
(7, 6, '2026-10-07', 'Confirmed'),
(8, 7, '2026-10-07', 'Confirmed'),
(9, 6, '2026-10-07', 'Confirmed'),
(10, 7, '2026-10-08', 'Confirmed'),
(1, 2, '2026-10-08', 'Confirmed'),
(2, 5, '2026-10-08', 'Confirmed'),
(3, 3, '2026-10-08', 'Cancelled'),
(4, 8, '2026-10-08', 'Confirmed'),
(5, 6, '2026-10-08', 'Confirmed'),
(6, 1, '2026-10-08', 'Confirmed'),
(7, 3, '2026-10-08', 'Confirmed'),
(8, 8, '2026-10-08', 'Confirmed'),
(9, 2, '2026-10-08', 'Confirmed'),
(10, 4, '2026-10-08', 'Confirmed');

INSERT INTO equipment (name, zone, status) VALUES
('Yoga Mat',        'Studio A',    'Available'),
('Dumbbell Set',    'Weight Zone', 'Available'),
('Spinning Bike',   'Cycle Room',  'Available'),
('Boxing Gloves',   'Studio B',    'Available'),
('Kettlebell',      'Weight Zone', 'Available'),
('Treadmill',       'Cardio Zone', 'Maintenance'),
('Barbell',         'Weight Zone', 'Available'),
('Resistance Band', 'Studio B',    'Available');

INSERT INTO class_equipment (class_id, equip_id, quantity) VALUES
(1, 1, 20),
(2, 5, 10),
(2, 8, 15),
(3, 3, 12),
(4, 4, 12),
(5, 1, 15),
(5, 8, 15),
(6, 2, 10),
(6, 5, 6),
(6, 7, 4),
(8, 1, 18),
(8, 8, 18);

drop table member

drop table trainer

drop table gym_class

drop table booking

drop table equipment

drop table class_equipment