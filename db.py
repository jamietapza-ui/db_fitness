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
    sql = """SELECT member_id,
                    name    as Name,
                    gender  as Gender,
                    timestampdiff(year, birth_date, curdate()) as Age,
                    birth_date,
                    phone   as Phone,
                    join_date,
                    package_type
                    FROM member WHERE 1=1"""
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("gender"):
        sql += " AND gender = %s"
        params.append(filters["gender"])
    if filters.get("package_type"):
        sql += " AND package_type = %s"
        params.append(filters["package_type"])
    return run_query(sql, tuple(params))


def get_member(member_id):
    sql = "SELECT * FROM member WHERE member_id = %s"
    return run_query(sql, (member_id,))[0] if run_query(sql, (member_id,)) else None


def create_member(data):
    sql = "INSERT INTO member (name, gender, birth_date, phone, join_date, package_type) VALUES (%s, %s, %s, %s, %s, %s)"
    return run_command(sql, (data["name"], data["gender"], data["birth_date"], data["phone"] ,data["join_date"], data["package_type"]))


def update_member(member_id, data):
    sql = "UPDATE member SET name=%s, gender=%s, join_date=%s, package_type=%s WHERE member_id=%s"
    return run_command(sql, (data["name"], data["gender"], data["join_date"], data["package_type"], member_id))


def delete_member(member_id): 
    sql = "DELETE FROM member WHERE member_id = %s"
    return run_command(sql, (member_id,))

# ---------- คลาสเรียน (gym_class) ----------
def search_classes(filters):
    sql = """SELECT c.class_id,
                    c.name,
                    c.room,
                    t.name AS trainer_name,
                    c.capacity,
                    c.start_date,
                    c.end_date
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
    if filters.get("trainer_name"):
        sql += " AND t.name LIKE %s"
        params.append(f"%{filters['trainer_name']}%")
    sql += " ORDER BY c.class_id"
    return run_query(sql, tuple(params))


def get_class(class_id):
    sql = """SELECT c.*, t.name AS trainer_name
             FROM gym_class c
             LEFT JOIN trainer t ON c.trainer_id = t.trainer_id
             WHERE c.class_id = %s"""
    rows = run_query(sql, (class_id,))
    return rows[0] if rows else None


def create_class(data):
    sql = """INSERT INTO gym_class (name, trainer_id, room, capacity, start_date)
             VALUES (%s, %s, %s, %s, %s)"""
    return run_command(sql, (data["name"], trainer_id, data["room"],
                             data["capacity"], data["start_date"]))


def update_class(class_id, data):
    sql = """UPDATE gym_class
             SET name=%s, trainer_id=%s, room=%s, capacity=%s, start_date=%s
             WHERE class_id=%s"""
    return run_command(sql, (data["name"], trainer_id, data["room"],
                             data["capacity"], data["start_date"], class_id))


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
                    b.book_date, 
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
    sql = """SELECT b.*, 
                    m.name AS member_name, 
                    c.name AS class_name 
                    FROM booking b 
                    LEFT JOIN member m ON b.member_id = m.member_id 
                    LEFT JOIN gym_class c ON b.class_id = c.class_id 
                    WHERE b.booking_id = %s"""
    return run_query(sql, (booking_id,))[0] if run_query(sql, (booking_id,)) else None


def create_booking(data):
    """เพิ่ม การจอง ใหม่ — data มีคีย์: member_id, class_id, book_date, status"""
    # TODO: INSERT INTO booking (...) VALUES (%s, ...)
    # _todo("create_booking")
    sql = "INSERT INTO booking (member_id, class_id, book_date, status) VALUES (%s, %s, %s, %s)"
    return run_command(sql, (member_id, class_id, data["book_date"], data["status"]))


def update_booking(booking_id, data):
    """แก้ไข การจอง ตาม booking_id"""
    # TODO: UPDATE booking SET ... WHERE booking_id=%s
    # _todo("update_booking")
    sql = "UPDATE booking SET member_id=%s, class_id=%s, book_date=%s, status=%s WHERE booking_id=%s"
    return run_command(sql, (member_id, class_id, data["book_date"], data["status"], booking_id))


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
                    phone,
                    status
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
    sql = "SELECT * FROM equipment WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    return run_query(sql, tuple(params))

def get_equipment(equipment_id):
    sql = "SELECT * FROM equipment WHERE equipment_id = %s"
    return run_query(sql, (equipment_id,))[0] if run_query(sql, (equipment_id,)) else None

def create_equipment(data):
    sql = "INSERT INTO equipment (name, zone, status) VALUES (%s, %s, %s)"
    return run_command(sql, (data["name"], data["zone"], data["status"]))

def update_equipment(equipment_id, data):
    sql = "UPDATE equipment SET name=%s, zone=%s, status=%s WHERE equipment_id=%s"
    return run_command(sql, (data["name"], data["zone"], data["status"], equipment_id))

def delete_equipment(equipment_id):
    sql = "DELETE FROM equipment WHERE equipment_id = %s"
    return run_command(sql, (equipment_id,))

# ============================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
# ============================================================
def report_summary():
    """ตัวเลขสรุปบนการ์ด dashboard — คืน dict เช่น {"members": 10, ...}
    คำใบ้: ใช้ COUNT(*) หลายครั้ง"""
    # TODO: นับจำนวนรวมต่าง ๆ เพื่อแสดงบนการ์ด
    _todo("report_summary")

def report_popular_classes():
    """📈 คลาสยอดนิยม (Most Booked)
    คำใบ้: JOIN booking→gym_class, GROUP BY class, COUNT, ORDER BY DESC, LIMIT 5"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    _todo("report_popular_classes")

def report_trainers_above_avg():
    """🏅 เทรนเนอร์ที่มีผู้จองมากกว่าค่าเฉลี่ย (Above Average)
    คำใบ้: JOIN booking→gym_class→trainer, GROUP BY trainer, HAVING COUNT(*) > (subquery AVG)"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    _todo("report_trainers_above_avg")

def report_class_equipment():
    """🧰 อุปกรณ์ที่ใช้ในแต่ละคลาส (Join 3 Tables)
    คำใบ้: JOIN class_equipment→gym_class, class_equipment→equipment"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    _todo("report_class_equipment")
