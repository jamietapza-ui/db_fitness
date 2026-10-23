# ============================================================
#  app.py — เว็บแอป Flask (ทำให้เสร็จแล้ว ★ ไม่ต้องแก้)
#  รัน:  python app.py  แล้วเปิด http://127.0.0.1:5000
# ============================================================
from flask import Flask, request, jsonify, render_template
import db

app = Flask(__name__)
app.json.sort_keys = False

def safe(fn, *args, **kwargs):  
    try:
        return jsonify({"ok": True, "data": fn(*args, **kwargs)})
    except NotImplementedError as e:
        return jsonify({"ok": False, "todo": True, "error": str(e)}), 501
    except Exception as e:
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500


@app.route("/")
def page_home():
    return render_template("index.html")

@app.route("/report")
def page_report():
    return render_template("report.html")


# ---- สมาชิก ----
@app.route("/api/members", methods=["GET"])
def members_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_members, filters)

@app.route("/api/members/options", methods=["GET"])
def members_options():
    return safe(db.member_options)

@app.route("/api/members/<int:_id>", methods=["GET"])
def member_get(_id):
    return safe(db.get_member, _id)

@app.route("/api/members", methods=["POST"])
def member_create():
    return safe(db.create_member, request.json)

@app.route("/api/members/<int:_id>", methods=["PUT"])
def member_update(_id):
    return safe(db.update_member, _id, request.json)

@app.route("/api/members/<int:_id>", methods=["DELETE"])
def member_delete(_id):
    return safe(db.delete_member, _id)

# ---- คลาสเรียน ----
@app.route("/api/classes", methods=["GET"])
def classes_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_classes, filters)

@app.route("/api/classes/options", methods=["GET"])
def classes_options():
    return safe(db.class_options)

@app.route("/api/classes/<int:_id>", methods=["GET"])
def class_get(_id):
    return safe(db.get_class, _id)

@app.route("/api/classes", methods=["POST"])
def class_create():
    return safe(db.create_class, request.json)

@app.route("/api/classes/<int:_id>", methods=["PUT"])
def class_update(_id):
    return safe(db.update_class, _id, request.json)

@app.route("/api/classes/<int:_id>", methods=["DELETE"])
def class_delete(_id):
    return safe(db.delete_class, _id)

# ---- การจอง ----
@app.route("/api/bookings", methods=["GET"])
def bookings_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_bookings, filters)

@app.route("/api/bookings/<int:_id>", methods=["GET"])
def booking_get(_id):
    return safe(db.get_booking, _id)

@app.route("/api/bookings", methods=["POST"])
def booking_create():
    return safe(db.create_booking, request.json)

@app.route("/api/bookings/<int:_id>", methods=["PUT"])
def booking_update(_id):
    return safe(db.update_booking, _id, request.json)

@app.route("/api/bookings/<int:_id>", methods=["DELETE"])
def booking_delete(_id):
    return safe(db.delete_booking, _id)

# ---- เทรนเนอร์ ----
@app.route("/api/trainers", methods=["GET"])
def trainers_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_trainers, filters)

@app.route("/api/trainers/options", methods=["GET"])
def trainers_options():
    return safe(db.trainer_options)

@app.route("/api/trainers/<int:_id>", methods=["GET"])
def trainer_get(_id):
    return safe(db.get_trainer, _id)

@app.route("/api/trainers", methods=["POST"])
def trainer_create():
    return safe(db.create_trainer, request.json)

@app.route("/api/trainers/<int:_id>", methods=["PUT"])
def trainer_update(_id):
    return safe(db.update_trainer, _id, request.json)

@app.route("/api/trainers/<int:_id>", methods=["DELETE"])
def trainer_delete(_id):
    return safe(db.delete_trainer, _id)

# ---- อุปกรณ์ ----
@app.route("/api/equipment", methods=["GET"])
def equipment_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_equipment, filters)

@app.route("/api/equipment/options", methods=["GET"])
def equipment_options():
    return safe(db.equipment_options)

@app.route("/api/equipment/<int:_id>", methods=["GET"])
def equipment_get(_id):
    return safe(db.get_equipment, _id)

@app.route("/api/equipment", methods=["POST"])
def equipment_create():
    return safe(db.create_equipment, request.json)

@app.route("/api/equipment/<int:_id>", methods=["PUT"])
def equipment_update(_id):
    return safe(db.update_equipment, _id, request.json)

@app.route("/api/equipment/<int:_id>", methods=["DELETE"])
def equipment_delete(_id):
    return safe(db.delete_equipment, _id)

@app.route("/api/reports/summary")
def report_summary():
    return safe(db.report_summary)

@app.route("/api/reports/popular-classes")
def route_report_popular_classes():
    return safe(db.report_popular_classes)

@app.route("/api/reports/top-trainers")
def route_report_trainers_above_avg():
    return safe(db.report_trainers_above_avg)

@app.route("/api/reports/class-equipment")
def route_report_class_equipment():
    return safe(db.report_class_equipment)

#---- แพ็กเกจ ----
@app.route("/api/packages", methods=["GET"])
def packages_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_packages, filters)

@app.route("/api/packages/<int:_id>", methods=["GET"])
def package_get(_id):
    return safe(db.get_package, _id)

@app.route("/api/packages", methods=["POST"])
def package_create():
    return safe(db.create_package, request.json)

@app.route("/api/packages/<int:_id>", methods=["PUT"])
def package_update(_id):
    return safe(db.update_package, _id, request.json)

@app.route("/api/packages/<int:_id>", methods=["DELETE"])
def package_delete(_id):
    return safe(db.delete_package, _id)

#---- รีวิว ----
@app.route("/api/reviews", methods=["GET"])
def reviews_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_reviews, filters)

@app.route("/api/reviews/<int:_id>", methods=["GET"])
def review_get(_id):
    return safe(db.get_review, _id)

@app.route("/api/reviews", methods=["POST"])
def review_create():
    return safe(db.create_review, request.json)

@app.route("/api/reviews/<int:_id>", methods=["PUT"])
def review_update(_id):
    return safe(db.update_review, _id, request.json)

@app.route("/api/reviews/<int:_id>", methods=["DELETE"])
def review_delete(_id):
    return safe(db.delete_review, _id)

#---- อุปกรณ์ต่อคลาส ----
@app.route("/api/class_equipment", methods=["GET"])
def class_equipment_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_class_equipment, filters)

@app.route("/api/class_equipment", methods=["POST"])
def class_equipment_create():
    return safe(db.create_class_equipment, request.json)

@app.route("/api/class_equipment/<int:class_id>/<int:equip_id>", methods=["GET"])
def class_equipment_get(class_id, equip_id):
    return safe(db.get_class_equipment, class_id, equip_id)

@app.route("/api/class_equipment/<int:class_id>/<int:equip_id>", methods=["PUT"])
def class_equipment_update(class_id, equip_id):
    return safe(db.update_class_equipment, class_id, equip_id, request.json)

@app.route("/api/class_equipment/<int:class_id>/<int:equip_id>", methods=["DELETE"])
def class_equipment_delete(class_id, equip_id):
    return safe(db.delete_class_equipment, class_id, equip_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)