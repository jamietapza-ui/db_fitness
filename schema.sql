-- Active: 1790433592999@@127.0.0.1@3306@project69
-- ============================================================
--  schema.sql — ระบบฟิตเนส (นิสิตออกแบบและเขียนเอง)
--  กติกา: การจอง = M:N (member × gym_class), อุปกรณ์ต่อคลาส = M:N (gym_class × equipment),
--         แต่ละคลาสมีเทรนเนอร์ (1:M จาก trainer)
-- ============================================================
CREATE TABLE member (
    member_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: name, gender, join_date, package_type
);
CREATE TABLE trainer (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: name, specialty, phone
);
CREATE TABLE gym_class (          -- 1:M จาก trainer
    class_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: trainer_id (FK), name, room, capacity, schedule_time
);
CREATE TABLE booking (            -- M:N: member × gym_class
    booking_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: member_id (FK), class_id (FK), book_date, status
);
CREATE TABLE equipment (
    equip_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: name, zone, status
);
CREATE TABLE class_equipment (    -- M:N: gym_class × equipment
    -- TODO: class_id (FK), equip_id (FK), quantity ; PRIMARY KEY (class_id, equip_id)
    class_id INT, equip_id INT
);
-- TODO: INSERT ข้อมูลตัวอย่างทุกตาราง
