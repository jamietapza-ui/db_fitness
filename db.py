# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#  มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# ============================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


def _todo(name):
    raise NotImplementedError(f"TODO: ยังไม่ได้เขียนฟังก์ชัน {name} ใน db.py")


# ---------- สมาชิก (member) ----------
def search_members(filters):
    """ค้นหา สมาชิก ตามเงื่อนไข (name, gender, package_type)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM member WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    # _todo("search_members")
    sql = """SELECT m.member_id,
                    m.name    as Name,
                    m.gender  as Gender,
                    m.age     as Age,
                    m.phone   as Phone,
                    DATE_FORMAT(m.join_date, '%d/%m/%Y') AS join_date,
                    p.pack_name,
                    p.type
                    FROM member m
                    JOIN package p on p.package_id = m.package_id 
                    WHERE 1=1"""
    params = []
    if filters.get("name"):
        sql += " AND m.name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("gender"):
        sql += " AND m.gender = %s"
        params.append(filters["gender"])
    if filters.get("type"):
        sql += " AND p.type = %s"
        params.append(filters["type"])
    if filters.get("pack_name"):
        sql += " AND p.pack_name = %s"
        params.append(filters["pack_name"])
    sql += " ORDER BY m.member_id"
    return run_query(sql, tuple(params))


def member_options():
    """รายชื่อสมาชิกสำหรับ dropdown (value = id, label = ชื่อ)"""
    rows = run_query("SELECT member_id, name FROM member ORDER BY name")
    return [{"value": r["member_id"], "label": r["name"]} for r in rows]


def get_member(member_id):
    sql = """SELECT m.member_id, m.name, m.gender, m.age, m.phone,
                    CAST(m.join_date AS CHAR) AS join_date,
                    p.type, p.pack_name
             FROM member m
             JOIN package p ON p.package_id = m.package_id
             WHERE m.member_id = %s"""
    rows = run_query(sql, (member_id,))
    return rows[0] if rows else None


def create_member(data):
    sql = """INSERT INTO member (name, gender, age, phone, join_date, package_id)
             VALUES (%s, %s, %s, %s, %s,
            (SELECT package_id FROM package WHERE type = %s AND pack_name = %s))"""
    return run_command(sql, (data["name"], data["gender"], data["age"],
                             data["phone"], data["join_date"],
                             data["type"], data["pack_name"]))


def update_member(member_id, data):
    sql = """UPDATE member
            SET name=%s, gender=%s, age=%s, phone=%s, join_date=%s,
            package_id=(SELECT package_id FROM package WHERE type = %s AND pack_name = %s)
            WHERE member_id=%s"""
    return run_command(sql, (data["name"], data["gender"], data["age"],
                             data["phone"], data["join_date"],
                             data["type"], data["pack_name"], member_id))


def delete_member(member_id): 
    sql = "DELETE FROM member WHERE member_id = %s"
    return run_command(sql, (member_id,))

# ---------- คลาสเรียน (gym_class) ----------

def search_classes(filters):
    sql = """SELECT c.class_id,
                    c.name,
                    c.room,
                    t.name AS trainer_name,
                    c.capacity - (SELECT COUNT(*) FROM booking b
                                  WHERE b.class_id = c.class_id
                                    AND LOWER(b.status) = 'booked') AS available_slots,
                    DATE_FORMAT(c.start_date, '%d/%m/%Y %H:%i') AS start_date,
                    DATE_FORMAT(c.end_date, '%d/%m/%Y %H:%i') AS end_date
             FROM gym_class c
             LEFT JOIN trainer t ON c.trainer_id = t.trainer_id
             WHERE 1=1"""
    params = []
    if filters.get("name"): 
        sql += " AND c.name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("room"):
        sql += " AND c.room LIKE %s"
        params.append(f"%{filters['room']}%")
    if filters.get("trainer_id"):
        sql += " AND c.trainer_id = %s"
        params.append(filters["trainer_id"])
    sql += " ORDER BY c.class_id"
    return run_query(sql, tuple(params))


def class_options():
    """รายชื่อคลาสสำหรับ dropdown (value = id, label = ชื่อคลาส)"""
    rows = run_query("SELECT class_id, name FROM gym_class ORDER BY name")
    return [{"value": r["class_id"], "label": r["name"]} for r in rows]


def get_class(class_id):
    sql = """SELECT c.*, 
                    t.name AS trainer_name,
                    CAST(c.start_date AS CHAR) AS start_date,
                    CAST(c.end_date AS CHAR) AS end_date
             FROM gym_class c
             LEFT JOIN trainer t ON c.trainer_id = t.trainer_id
             WHERE c.class_id = %s"""
    rows = run_query(sql, (class_id,))
    return rows[0] if rows else None

def check_can_book(member_id, class_id, booking_id=None):
    safe_id = booking_id if booking_id is not None else 0

    sql = """SELECT c.name,
                    c.capacity - (SELECT COUNT(*) FROM booking b
                                  WHERE b.class_id = c.class_id
                                    AND LOWER(b.status) = 'booked'
                                    AND b.booking_id <> %s) AS seats_left
             FROM gym_class c
             WHERE c.class_id = %s"""
    rows = run_query(sql, (safe_id, class_id))

    if not rows:
        raise ValueError(f"ไม่พบคลาสรหัส {class_id}")
    if rows[0]["seats_left"] <= 0:
        raise ValueError(f"คลาส '{rows[0]['name']}' เต็มแล้ว (ว่าง 0 ที่นั่ง)")

    dup = run_query("""SELECT COUNT(*) AS cnt FROM booking
                       WHERE member_id = %s AND class_id = %s
                         AND LOWER(status) = 'booked' AND booking_id <> %s""",
                    (member_id, class_id, safe_id))
    if dup[0]["cnt"] > 0:
        raise ValueError("สมาชิกนี้จองคลาสนี้อยู่แล้ว")


def create_class(data):
    sql = """INSERT INTO gym_class (name, trainer_id, room, capacity, start_date, end_date)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    return run_command(sql, (data["name"], data["trainer_id"], data["room"],
                             data["capacity"], data["start_date"], data["end_date"]))


def update_class(class_id, data):
    sql = """UPDATE gym_class
             SET name=%s, room=%s, capacity=%s, start_date=%s, end_date=%s, trainer_id=%s
             WHERE class_id=%s"""
    return run_command(sql, (data["name"], data["room"], data["capacity"],
                             data["start_date"], data["end_date"], data["trainer_id"], class_id))


def delete_class(class_id):
    return run_command("DELETE FROM gym_class WHERE class_id = %s", (class_id,))

# ---------- การจอง (booking) ----------

def search_bookings(filters):
    """ค้นหา การจอง ตามเงื่อนไข (member_id, class_id, status)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM booking WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    # _todo("search_bookings")
    sql = """SELECT b.booking_id, 
                    m.name AS member_name, 
                    c.name AS class_name, 
                    DATE_FORMAT(b.book_date, '%d/%m/%Y') AS book_date, 
                    b.status 
                    FROM booking b 
                    LEFT JOIN member m ON b.member_id = m.member_id 
                    LEFT JOIN gym_class c ON b.class_id = c.class_id 
                    WHERE 1=1"""
    params = []
    if filters.get("member_name"):
        sql += " AND m.name LIKE %s"
        params.append(f"%{filters['member_name']}%")
    if filters.get("class_name"):
        sql += " AND c.name LIKE %s"
        params.append(f"%{filters['class_name']}%")
    if filters.get("status"):
        sql += " AND b.status = %s"
        params.append(filters["status"])
    sql += " order by b.booking_id"
    return run_query(sql, tuple(params))


def get_booking(booking_id):
    """ดึง การจอง 1 รายการตาม booking_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    # TODO: SELECT * FROM booking WHERE booking_id = %s แล้วคืนแถวเดียว
    # _todo("get_booking")
    sql = """SELECT b.member_id, b.class_id,
                    m.name AS member_name, 
                    c.name AS class_name ,
                    CAST(b.book_date AS CHAR) AS book_date,
                    b.status
                    FROM booking b 
                    LEFT JOIN member m ON b.member_id = m.member_id 
                    LEFT JOIN gym_class c ON b.class_id = c.class_id 
                    WHERE b.booking_id = %s"""
    return run_query(sql, (booking_id,))[0] if run_query(sql, (booking_id,)) else None

def create_booking(data):
    """เพิ่ม การจอง ใหม่ — data มีคีย์: member_id, class_id, book_date, status"""
    # TODO: INSERT INTO booking (...) VALUES (%s, ...)
    # _todo("create_booking")
    if data["status"].casefold() == "booked":
        check_can_book(data["member_id"], data["class_id"])
    sql = "INSERT INTO booking (member_id, class_id, book_date, status) VALUES (%s, %s, %s, %s)"
    return run_command(sql, (data["member_id"], data["class_id"], data["book_date"], data["status"]))


def update_booking(booking_id, data):
    """แก้ไข การจอง ตาม booking_id"""
    # TODO: UPDATE booking SET ... WHERE booking_id=%s
    # _todo("update_booking")
    if data["status"].casefold() == "booked":
        check_can_book(data["member_id"], data["class_id"], booking_id)
    sql = "UPDATE booking SET member_id=%s, class_id=%s, book_date=%s, status=%s WHERE booking_id=%s"
    return run_command(sql, (data["member_id"], data["class_id"], data["book_date"], data["status"], booking_id))


def delete_booking(booking_id):
    """ลบ การจอง ตาม booking_id"""
    # TODO: DELETE FROM booking WHERE booking_id=%s
    # _todo("delete_booking")
    sql = "DELETE FROM booking WHERE booking_id = %s"
    return run_command(sql, (booking_id,))


# ---------- เทรนเนอร์ (trainers) ----------
def search_trainers(filters):
    sql = """SELECT trainer_id,
                    name,
                    specialty,
                    phone
                    FROM trainer WHERE 1=1"""
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("specialty"):
        sql += " AND specialty = %s"
        params.append(filters['specialty'])
    if filters.get("phone"):
            sql += " AND phone LIKE %s"
            params.append(f"%{filters['phone']}%")
    return run_query(sql, tuple(params))

def trainer_options():
    """รายชื่อเทรนเนอร์สำหรับ dropdown (value = id, label = ชื่อ)"""
    rows = run_query("SELECT trainer_id, name FROM trainer ORDER BY name")
    return [{"value": r["trainer_id"], "label": r["name"]} for r in rows]

def get_trainer(trainer_id):
    sql = "SELECT * FROM trainer WHERE trainer_id = %s"
    return run_query(sql, (trainer_id,))[0] if run_query(sql, (trainer_id,)) else None

def create_trainer(data):
    sql = "INSERT INTO trainer (name, specialty, phone) VALUES (%s, %s, %s)"
    return run_command(sql, (data["name"], data["specialty"], data["phone"]))

def update_trainer(trainer_id, data):
    sql = "UPDATE trainer SET name=%s, specialty=%s, phone=%s WHERE trainer_id=%s"
    return run_command(sql, (data["name"], data["specialty"], data["phone"], trainer_id))

def delete_trainer(trainer_id):
    sql = "DELETE FROM trainer WHERE trainer_id = %s"
    return run_command(sql, (trainer_id,))

# ---------- อุปกรณ์ (equipment) ----------
def search_equipment(filters):
    sql = "SELECT equip_id, name, zone, quantity FROM equipment WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    return run_query(sql, tuple(params))

def equipment_options():
    """รายชื่ออุปกรณ์สำหรับ dropdown (value = equip_id, label = ชื่อ)"""
    rows = run_query("SELECT equip_id, name FROM equipment ORDER BY name")
    return [{"value": r["equip_id"], "label": r["name"]} for r in rows]

def get_equipment(equip_id):
    sql = "SELECT * FROM equipment WHERE equip_id = %s"
    rows = run_query(sql, (equip_id,))
    return rows[0] if rows else None

def create_equipment(data):
    sql = "INSERT INTO equipment (name, zone, quantity) VALUES (%s, %s, %s)"
    return run_command(sql, (data["name"], data["zone"], data["quantity"]))

def update_equipment(equip_id, data):
    sql = "UPDATE equipment SET name=%s, zone=%s, quantity=%s WHERE equip_id=%s"
    return run_command(sql, (data["name"], data["zone"], data["quantity"], equip_id))

def delete_equipment(equip_id):
    sql = "DELETE FROM equipment WHERE equip_id = %s"
    return run_command(sql, (equip_id,))

#----- แพ็กเกจ -----
def search_packages(filters):
    sql = "SELECT * FROM package WHERE 1=1"
    params = []
    if filters.get("type"):
        sql += " AND type LIKE %s"
        params.append(f"%{filters['type']}%")
    if filters.get("pack_name"):
        sql += " AND pack_name LIKE %s"
        params.append(f"%{filters['pack_name']}%")
    return run_query(sql, tuple(params))

def get_package(package_id):
    sql = "SELECT * FROM package WHERE package_id = %s"
    return run_query(sql, (package_id,))[0] if run_query(sql, (package_id,)) else None

def create_package(data):
    sql = "INSERT INTO package (pack_name, type, price) VALUES (%s, %s, %s)"
    return run_command(sql, (data["pack_name"], data["type"], data["price"]))

def update_package(package_id, data):
    sql = "UPDATE package SET pack_name=%s, type=%s, price=%s WHERE package_id=%s"
    return run_command(sql, (data["pack_name"], data["type"], data["price"], package_id))

def delete_package(package_id):
    sql = "DELETE FROM package WHERE package_id = %s"
    return run_command(sql, (package_id,))

#----- รีวิว -----
def search_reviews(filters):
    sql = """SELECT r.review_id,
                    c.name AS class_name,
                    t.name AS trainer_name,
                    m.name AS member_name,
                    r.TEXT_reviews
             FROM reviews r
             JOIN gym_class c ON r.class_id = c.class_id
             JOIN trainer t ON r.trainer_id = t.trainer_id
             JOIN member m ON r.member_id = m.member_id
             WHERE 1=1"""
    params = []
    if filters.get("class_id"):
        sql += " AND r.class_id = %s"
        params.append(filters["class_id"])
    if filters.get("member_id"):
        sql += " AND r.member_id = %s"
        params.append(filters["member_id"])
    if filters.get("trainer_id"):
        sql += " AND r.trainer_id = %s"
        params.append(filters["trainer_id"])
    sql += " ORDER BY r.review_id"
    return run_query(sql, tuple(params))

def get_review(review_id):
    rows = run_query("SELECT * FROM reviews WHERE review_id = %s", (review_id,))
    return rows[0] if rows else None

def create_review(data):
    # เทรนเนอร์ดึงจากคลาสอัตโนมัติ ไม่ต้องเลือกซ้ำ
    sql = """INSERT INTO reviews (class_id, trainer_id, member_id, TEXT_reviews)
             VALUES (%s, (SELECT trainer_id FROM gym_class WHERE class_id = %s), %s, %s)"""
    return run_command(sql, (data["class_id"], data["class_id"],
                             data["member_id"], data["TEXT_reviews"]))

def update_review(review_id, data):
    sql = """UPDATE reviews
             SET class_id=%s,
                 trainer_id=(SELECT trainer_id FROM gym_class WHERE class_id = %s),
                 member_id=%s, TEXT_reviews=%s
             WHERE review_id=%s"""
    return run_command(sql, (data["class_id"], data["class_id"],
                             data["member_id"], data["TEXT_reviews"], review_id))

def delete_review(review_id):
    return run_command("DELETE FROM reviews WHERE review_id = %s", (review_id,))

#----- อุปกรณ์ต่อคลาส -----
def search_class_equipment(filters):
    sql = """SELECT ce.class_id, 
                    gc.name AS class_name, 
                    e.name AS equipment_name, 
                    ce.quantity
                    FROM class_equipment ce
                    JOIN gym_class gc ON ce.class_id = gc.class_id
                    JOIN equipment e ON ce.equip_id = e.equip_id
                    WHERE 1=1"""
    params = []
    if filters.get("class_id"):
        sql += " AND ce.class_id = %s"
        params.append(filters["class_id"])
    if filters.get("equip_id"):
        sql += " AND ce.equip_id = %s"
        params.append(filters["equip_id"])
    sql += " ORDER BY ce.class_id, ce.equip_id"
    return run_query(sql, tuple(params))

def get_class_equipment(class_id, equip_id):
    sql = """SELECT ce.class_id, 
                    gc.name AS class_name, 
                    ce.equip_id, 
                    e.name AS equipment_name, 
                    ce.quantity
                    FROM class_equipment ce
                    JOIN gym_class gc ON ce.class_id = gc.class_id
                    JOIN equipment e ON ce.equip_id = e.equip_id
                    WHERE ce.class_id = %s AND ce.equip_id = %s"""
    rows = run_query(sql, (class_id, equip_id))
    return rows[0] if rows else None

def create_class_equipment(data):
    sql = "INSERT INTO class_equipment (class_id, equip_id, quantity) VALUES (%s, %s, %s)"
    return run_command(sql, (data["class_id"], data["equip_id"], data["quantity"]))

def update_class_equipment(class_id, equip_id, data):
    sql = "UPDATE class_equipment SET quantity=%s WHERE class_id=%s AND equip_id=%s"
    return run_command(sql, (data["quantity"], class_id, equip_id))

def delete_class_equipment(class_id, equip_id):
    sql = "DELETE FROM class_equipment WHERE class_id=%s AND equip_id=%s"
    return run_command(sql, (class_id, equip_id))

# ============================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
# ============================================================
def report_summary():
    """ตัวเลขสรุปบนการ์ด dashboard — คืน dict เช่น {"members": 10, ...}
    คำใบ้: ใช้ COUNT(*) หลายครั้ง"""
    # TODO: นับจำนวนรวมต่าง ๆ เพื่อแสดงบนการ์ด
    # _todo("report_summary")
    members = run_query("SELECT COUNT(*) AS count FROM member")[0]["count"]
    classes = run_query("SELECT COUNT(*) AS count FROM gym_class")[0]["count"]
    bookings = run_query("SELECT COUNT(*) AS count FROM booking")[0]["count"]
    trainers = run_query("SELECT COUNT(*) AS count FROM trainer")[0]["count"]
    return {"members": members, "classes": classes, "bookings": bookings, "trainers": trainers}

def report_popular_classes():
    """📈 คลาสยอดนิยม (Most Booked)
    คำใบ้: JOIN booking→gym_class, GROUP BY class, COUNT, ORDER BY DESC, LIMIT 5"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    # _todo("report_popular_classes")
    sql = """
        SELECT gc.class_id, gc.name, COUNT(b.booking_id) as booking_count
        FROM gym_class gc
        LEFT JOIN booking b ON gc.class_id = b.class_id
        GROUP BY gc.class_id, gc.name
        ORDER BY booking_count DESC
        LIMIT 5
    """
    return run_query(sql)

def report_trainers_above_avg():
    """🏅 เทรนเนอร์ที่มีผู้จองมากกว่าค่าเฉลี่ย (Above Average)
    คำใบ้: JOIN booking→gym_class→trainer, GROUP BY trainer, HAVING COUNT(*) > (subquery AVG)"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    # _todo("report_trainers_above_avg")
    sql = """
        SELECT t.trainer_id, t.name, COUNT(b.booking_id) as booking_count
        FROM trainer t
        LEFT JOIN gym_class gc ON t.trainer_id = gc.trainer_id
        LEFT JOIN booking b ON gc.class_id = b.class_id
        GROUP BY t.trainer_id, t.name
        HAVING COUNT(b.booking_id) > (
            SELECT AVG(booking_count)
            FROM (
                SELECT COUNT(b2.booking_id) as booking_count
                FROM trainer t2
                LEFT JOIN gym_class gc2 ON t2.trainer_id = gc2.trainer_id
                LEFT JOIN booking b2 ON gc2.class_id = b2.class_id
                GROUP BY t2.trainer_id
            ) avg_bookings
        )
    """
    return run_query(sql)

def report_class_equipment():
    """🧰 อุปกรณ์ที่ใช้ในแต่ละคลาส (Join 3 Tables)
    คำใบ้: JOIN class_equipment→gym_class, class_equipment→equipment"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    # _todo("report_class_equipment")
    sql = """
        SELECT gc.class_id, gc.name, e.equip_id, e.name as equipment_name
        FROM gym_class gc
        LEFT JOIN class_equipment ce ON gc.class_id = ce.class_id
        LEFT JOIN equipment e ON ce.equip_id = e.equip_id
    """
    return run_query(sql)