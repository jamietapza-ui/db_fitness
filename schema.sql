-- Active: 1790434080501@@127.0.0.1@3306@project69
-- ============================================================
--  schema.sql — ระบบฟิตเนส (นิสิตออกแบบและเขียนเอง)
--  กติกา: การจอง = M:N (member × gym_class), อุปกรณ์ต่อคลาส = M:N (gym_class × equipment),
--         แต่ละคลาสมีเทรนเนอร์ (1:M จาก trainer)
-- ============================================================
CREATE TABLE package(
    package_id INT AUTO_INCREMENT PRIMARY KEY,
    pack_name  VARCHAR(100) NOT NULL,
    type       VARCHAR(50)  NOT NULL,
    price      INT NOT NULL
);

CREATE TABLE member (
    member_id     INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    gender        CHAR(1) NOT NULL,
    phone         VARCHAR(15) NOT NULL,
    age           INT NOT NULL,
    join_date     DATE NOT NULL,
    package_id    INT NOT NULL,
    FOREIGN KEY (package_id) REFERENCES package(package_id)
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
    start_date    DATETIME NOT NULL,
    end_date      DATETIME NOT NULL,
    CHECK (end_date > start_date),
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
    quantity INT NOT NULL
);

CREATE TABLE class_equipment (    -- M:N: gym_class × equipment
    class_id INT NOT NULL, 
    equip_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    CONSTRAINT pk_class_equip PRIMARY KEY (class_id, equip_id),
    FOREIGN KEY (class_id) REFERENCES gym_class(class_id),
    FOREIGN KEY (equip_id) REFERENCES equipment(equip_id)
);

CREATE TABLE reviews(
    review_id    INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT NOT NULL,
    trainer_id INT NOT NULL,
    member_id INT NOT NULL,
    TEXT_reviews VARCHAR(200) NOT NULL,
    Foreign Key (class_id) REFERENCES gym_class(class_id),
    FOREIGN KEY (member_id) REFERENCES member(member_id)
);

INSERT INTO package (pack_name, type, price) VALUES
('รายวัน',   'basic',   50),
('รายวัน',   'premium', 80),
('รายวัน',   'vip',     120),
('รายเดือน', 'basic',   790),
('รายเดือน', 'premium', 1290),
('รายเดือน', 'vip',     1990),
('รายปี',    'basic',   7900),
('รายปี',    'premium', 12900),
('รายปี',    'vip',     19900);

INSERT INTO member (name, gender, phone, age, join_date, package_id) VALUES
('Somchai Jaidee',       'M', '0811111111', '16', '2025-01-10', 4),
('Somying Raksuk',       'F', '0822222222', '32', '2025-02-05', 5),
('Thanakorn Mankhong',   'M', '0833333333', '14', '2025-03-01', 9),
('Pimchanok Srisuk',     'F', '0844444444', '22', '2025-03-12', 1),
('Weerapong Saengthong', 'M', '0855555555', '15', '2025-04-02', 6),
('Kanokwan Sukjai',      'F', '0866666666', '41', '2025-04-20', 8),
('Nattapon Kengkaj',     'M', '0877777777', '19', '2025-05-05', 2),
('Paweena Jaingam',      'F', '0888888888', '23', '2025-05-15', 7),
('Anucha Boonmee',       'M', '0899990001', '25', '2025-05-20', 5),
('Siriporn Wongsa',      'F', '0899990002', '25', '2025-05-25', 4),
('Kittisak Thongdee',    'M', '0899990003', '21', '2025-06-01', 6),
('Napatsorn Chaiyo',     'F', '0899990004', '18', '2025-06-05', 2),
('Preecha Suksan',       'M', '0899990005', '19', '2025-06-10', 9),
('Jirapat Meesuk',       'F', '0899990006', '35', '2025-06-15', 7);
 
INSERT INTO trainer (name, specialty, phone) VALUES
('Coach Alex',   'Yoga',            '0901111111'),
('Coach Ben',    'Weight Training', '0902222222'),
('Coach Chris',  'Cardio',          '0903333333'),
('Coach David',  'Boxing',          '0904444444'),
('Coach Emma',   'Pilates',         '0905555555'),
('Coach Frank',  'Zumba',           '0906666666'),
('Coach Grace',  'CrossFit',        '0907777777'),
('Coach Henry',  'Spinning',        '0908888888'),
('Coach Ivy',    'Dance Fitness',   '0909999999'),
('Coach Jack',   'Muay Thai',       '0901010101'),
('Coach Kate',   'Stretching',      '0901212121');
 
INSERT INTO equipment (name, zone, quantity) VALUES
('Yoga Mat',        'Studio',      40),
('Dumbbell Set',    'Weight Zone', 20),
('Barbell',         'Weight Zone', 10),
('Treadmill',       'Cardio Zone', 12),
('Boxing Gloves',   'Boxing Zone', 15),
('Punching Bag',    'Boxing Zone', 6),
('Pilates Ball',    'Studio',      20),
('Spinning Bike',   'Cardio Zone', 15),
('Kettlebell',      'Weight Zone', 16),
('Jump Rope',       'Cardio Zone', 25),
('Resistance Band', 'Studio',      30),
('Foam Roller',     'Studio',      20);
 
INSERT INTO gym_class (trainer_id, name, room, capacity, start_date, end_date) VALUES
(1,  'Morning Yoga',        'Room A', 20, '2025-06-01 07:00:00', '2025-06-01 08:00:00'),
(2,  'Strength Basics',     'Room B', 15, '2025-06-01 18:00:00', '2025-06-01 19:00:00'),
(3,  'HIIT Cardio',         'Room C', 25, '2025-06-02 17:30:00', '2025-06-02 18:30:00'),
(4,  'Boxing Fitness',      'Room D', 12, '2025-06-03 19:00:00', '2025-06-03 20:00:00'),
(5,  'Core Pilates',        'Room A', 18, '2025-06-04 09:00:00', '2025-06-04 10:00:00'),
(1,  'Evening Yoga',        'Room A', 20, '2025-06-05 18:30:00', '2025-06-05 19:30:00'),
(6,  'Zumba Party',         'Room E', 30, '2025-06-06 18:00:00', '2025-06-06 19:00:00'),
(7,  'CrossFit Challenge',  'Room B', 15, '2025-06-07 08:00:00', '2025-06-07 09:00:00'),
(8,  'Spinning Ride',       'Room F', 20, '2025-06-08 17:00:00', '2025-06-08 18:00:00'),
(9,  'Dance Fitness',       'Room E', 25, '2025-06-09 19:00:00', '2025-06-09 20:00:00'),
(10, 'Muay Thai Basics',    'Room D', 12, '2025-06-10 18:30:00', '2025-06-10 19:30:00'),
(11, 'Stretch & Relax',     'Room A', 20, '2025-06-11 07:30:00', '2025-06-11 08:30:00');
 
INSERT INTO booking (member_id, class_id, book_date, status) VALUES
(1,  1,  '2025-05-28', 'confirmed'),
(2,  1,  '2025-05-28', 'confirmed'),
(3,  2,  '2025-05-29', 'confirmed'),
(4,  3,  '2025-05-30', 'cancelled'),
(5,  4,  '2025-05-30', 'confirmed'),
(6,  5,  '2025-05-31', 'confirmed'),
(7,  3,  '2025-05-31', 'pending'),
(8,  6,  '2025-06-01', 'confirmed'),
(1,  2,  '2025-06-01', 'confirmed'),
(9,  7,  '2025-06-02', 'confirmed'),
(10, 7,  '2025-06-02', 'confirmed'),
(11, 8,  '2025-06-03', 'confirmed'),
(12, 9,  '2025-06-04', 'pending'),
(13, 10, '2025-06-05', 'confirmed'),
(14, 11, '2025-06-06', 'cancelled'),
(2,  12, '2025-06-07', 'confirmed'),
(3,  9,  '2025-06-07', 'confirmed');
 
INSERT INTO class_equipment (class_id, equip_id, quantity) VALUES
(1,  1,  20),
(2,  2,  15),
(2,  3,  5),
(3,  4,  10),
(4,  5,  12),
(4,  6,  4),
(5,  1,  18),
(5,  7,  18),
(6,  1,  20),
(7,  11, 15),
(8,  9,  10),
(8,  10, 15),
(9,  8,  15),
(10, 11, 20),
(11, 5,  10),
(11, 6,  4),
(12, 12, 20);
 
INSERT INTO reviews (class_id, trainer_id, member_id, TEXT_reviews) VALUES
(1,  1,  1,  'คลาสโยคะผ่อนคลายมาก ครูสอนดี'),
(1,  1,  2,  'บรรยากาศดี เหมาะสำหรับมือใหม่'),
(2,  2,  3,  'ได้เทคนิคยกน้ำหนักที่ถูกต้อง'),
(4,  4,  5,  'สนุก เหนื่อยแต่คุ้ม'),
(5,  5,  6,  'ช่วยให้แกนกลางลำตัวแข็งแรงขึ้น'),
(6,  1,  8,  'ชอบคลาสเย็น ผ่อนคลายหลังเลิกงาน'),
(7,  6,  9,  'Zumba สนุกมาก เผาผลาญได้เยอะ'),
(8,  7,  11, 'หนักแต่ท้าทาย โค้ชดูแลดี'),
(9,  8,  3,  'จักรยานสนุก เพลงมันส์'),
(10, 9,  13, 'ท่าเต้นไม่ยาก เหมาะกับมือใหม่'),
(12, 11, 2,  'ยืดเหยียดแล้วสบายตัวมาก'),
(2,  2,  1,  'โค้ชอธิบายท่าชัดเจน ได้ประโยชน์');
DROP TABLE if exists package

drop table if exists member

drop table if exists trainer

drop table if exists gym_class

drop table if exists booking

drop table if exists equipment

drop table if exists class_equipment

drop Table if EXISTS reviews