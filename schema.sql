-- Active: 1790433592999@@127.0.0.1@3306@project69
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
