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
    """ค้นหา คลาสเรียน ตามเงื่อนไข (name, room)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM gym_class WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    # _todo("search_classes")
    sql = "SELECT * FROM gym_class WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("room"):
        sql += " AND room = %s"
        params.append(filters["room"])
    return run_query(sql, tuple(params))


def get_class(class_id):
    """ดึง คลาสเรียน 1 รายการตาม class_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    # TODO: SELECT * FROM gym_class WHERE class_id = %s แล้วคืนแถวเดียว
    # _todo("get_class")
    sql = "SELECT * FROM gym_class WHERE class_id = %s"
    return run_query(sql, (class_id,))[0] if run_query(sql, (class_id,)) else None


def create_class(data):
    """เพิ่ม คลาสเรียน ใหม่ — data มีคีย์: name, trainer_id, room, capacity, schedule_time"""
    # TODO: INSERT INTO gym_class (...) VALUES (%s, ...)
    # _todo("create_class")
    sql = "INSERT INTO gym_class (name, trainer_id, room, capacity, schedule_time) VALUES (%s, %s, %s, %s, %s)"
    return run_command(sql, (data["name"], data["trainer_id"], data["room"], data["capacity"], data["schedule_time"]))


def update_class(class_id, data):
    """แก้ไข คลาสเรียน ตาม class_id"""
    # TODO: UPDATE gym_class SET ... WHERE class_id=%s
    # _todo("update_class")
    sql = "UPDATE gym_class SET name=%s, trainer_id=%s, room=%s, capacity=%s, schedule_time=%s WHERE class_id=%s"
    return run_command(sql, (data["name"], data["trainer_id"], data["room"], data["capacity"], data["schedule_time"], class_id))


def delete_class(class_id):
    """ลบ คลาสเรียน ตาม class_id"""
    # TODO: DELETE FROM gym_class WHERE class_id=%s
    # _todo("delete_class")
    sql = "DELETE FROM gym_class WHERE class_id = %s"
    return run_command(sql, (class_id,))

# ---------- การจอง (booking) ----------
def search_bookings(filters):
    """ค้นหา การจอง ตามเงื่อนไข (member_id, class_id, status)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM booking WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    # _todo("search_bookings")
    sql = "SELECT * FROM booking WHERE 1=1"
    params = []
    if filters.get("member_id"):
        sql += " AND member_id = %s"
        params.append(filters["member_id"])
    if filters.get("class_id"):
        sql += " AND class_id = %s"
        params.append(filters["class_id"])
    if filters.get("status"):
        sql += " AND status = %s"
        params.append(filters["status"])
    return run_query(sql, tuple(params))


def get_booking(booking_id):
    """ดึง การจอง 1 รายการตาม booking_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    # TODO: SELECT * FROM booking WHERE booking_id = %s แล้วคืนแถวเดียว
    # _todo("get_booking")
    sql = "SELECT * FROM booking WHERE booking_id = %s"
    return run_query(sql, (booking_id,))[0] if run_query(sql, (booking_id,)) else None


def create_booking(data):
    """เพิ่ม การจอง ใหม่ — data มีคีย์: member_id, class_id, book_date, status"""
    # TODO: INSERT INTO booking (...) VALUES (%s, ...)
    # _todo("create_booking")
    sql = "INSERT INTO booking (member_id, class_id, book_date, status) VALUES (%s, %s, %s, %s)"
    return run_command(sql, (data["member_id"], data["class_id"], data["book_date"], data["status"]))


def update_booking(booking_id, data):
    """แก้ไข การจอง ตาม booking_id"""
    # TODO: UPDATE booking SET ... WHERE booking_id=%s
    # _todo("update_booking")
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
