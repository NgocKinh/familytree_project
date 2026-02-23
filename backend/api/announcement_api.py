"""
API: Announcement (v4.1-CLEAN-NAME-ORDER)
-----------------------------------------
- Tự động nhận diện giỗ âm/dương
- Ưu tiên anniversary_death (dd/mm âm lịch)
- Nếu rỗng → dùng death_date (dương lịch)
- Thông báo hôm nay + 7 ngày tới
- Format đẹp (Style B)
- Ultra Safe: try/except + safe_close
"""

from flask import Blueprint, jsonify
from db import get_connection
from lunarcalendar import Converter, Lunar
from datetime import date, timedelta

announcement_bp = Blueprint("announcement_bp", __name__)


# ------------------------------------------------------------
# Safe close
# ------------------------------------------------------------
def safe_close(conn, cursor):
    try:
        if cursor:
            cursor.close()
    except Exception as e:
        print("⚠️ Cursor close error:", e)

    try:
        if conn:
            conn.close()
    except Exception as e:
        print("⚠️ Connection close error:", e)


# ------------------------------------------------------------
# Convert dd/mm âm lịch → ngày dương lịch năm nay
# ------------------------------------------------------------
def lunar_to_solar_this_year(lunar_ddmm: str):
    try:
        d, m = lunar_ddmm.split("/")
        year_now = date.today().year
        lunar_obj = Lunar(year_now, int(m), int(d), False)
        solar = Converter.Lunar2Solar(lunar_obj)
        return date(solar.year, solar.month, solar.day)
    except Exception as e:
        print("⚠️ Lỗi âm→dương:", e)
        return None


# ------------------------------------------------------------
# Build message Style B
# ------------------------------------------------------------
def build_message(name, lunar_str, solar_date):
    solar_str = solar_date.strftime("%d/%m/%Y")
    return (
        f"🕯️ Hôm nay là đám giỗ của {name}\n"
        f"→ Âm lịch: {lunar_str}\n"
        f"→ Dương lịch năm nay: {solar_str}"
    )


# ------------------------------------------------------------
# Hôm nay
# ------------------------------------------------------------
@announcement_bp.route("/api/announcement/today", methods=["GET"])
def announcement_today():

    conn = None
    cursor = None

    try:
        today = date.today()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ⭐ FIX THỨ TỰ TÊN – CHUẨN CẤU TRÚC PROJECT
        cursor.execute("""
            SELECT 
                person_id,
                sur_name,
                last_name,
                middle_name,
                first_name,
                anniversary_death,
                death_date
            FROM person
            WHERE delete_status = 0
        """)

        rows = cursor.fetchall()
        result = []

        for row in rows:

            full_name = f"{row['sur_name']} {row['last_name']} {row['middle_name']} {row['first_name']}".strip()

            ann = row["anniversary_death"]

            # ---------------------------
            # Trường hợp có ngày giỗ âm
            # ---------------------------
            if ann:
                solar = lunar_to_solar_this_year(ann)
                if solar and solar == today:
                    result.append({
                        "type": "death_anniversary",
                        "name": full_name,
                        "lunar_date": ann,
                        "solar_date": solar.isoformat(),
                        "calendar_type": "lunar",
                        "message": build_message(full_name, ann, solar)
                    })

            # ---------------------------
            # Không có ngày giỗ âm → lấy ngày mất dương lịch
            # ---------------------------
            else:
                dd = row["death_date"]
                if dd:
                    solar_this_year = date(today.year, dd.month, dd.day)
                    if solar_this_year == today:
                        lunar_today = Converter.Solar2Lunar(
                            date(today.year, dd.month, dd.day)
                        )
                        lunar_str = f"{str(lunar_today.day).zfill(2)}/{str(lunar_today.month).zfill(2)}"

                        result.append({
                            "type": "death_anniversary",
                            "name": full_name,
                            "lunar_date": lunar_str,
                            "solar_date": solar_this_year.isoformat(),
                            "calendar_type": "solar",
                            "message": build_message(full_name, lunar_str, solar_this_year)
                        })

        return jsonify(result), 200

    except Exception as e:
        print("❌ ERROR TODAY:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        safe_close(conn, cursor)


# ------------------------------------------------------------
# Sắp tới 7 ngày
# ------------------------------------------------------------
@announcement_bp.route("/api/announcement/upcoming", methods=["GET"])
def announcement_upcoming():

    conn = None
    cursor = None

    try:
        today = date.today()
        next_7 = today + timedelta(days=7)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ⭐ FIX THỨ TỰ TÊN – CHUẨN CẤU TRÚC PROJECT
        cursor.execute("""
            SELECT 
                person_id,
                sur_name,
                last_name,
                middle_name,
                first_name,
                anniversary_death,
                death_date
            FROM person
            WHERE delete_status = 0
        """)

        rows = cursor.fetchall()
        result = []

        for row in rows:

            full_name = f"{row['sur_name']} {row['last_name']} {row['middle_name']} {row['first_name']}".strip()
            ann = row["anniversary_death"]

            # ---------------------------
            # GIỖ ÂM
            # ---------------------------
            if ann:
                solar = lunar_to_solar_this_year(ann)
                if solar and today < solar <= next_7:
                    result.append({
                        "type": "death_anniversary",
                        "name": full_name,
                        "lunar_date": ann,
                        "solar_date": solar.isoformat(),
                        "calendar_type": "lunar",
                        "message": build_message(full_name, ann, solar)
                    })

            # ---------------------------
            # GIỖ DƯƠNG
            # ---------------------------
            else:
                dd = row["death_date"]
                if dd:
                    solar_this_year = date(today.year, dd.month, dd.day)
                    if today < solar_this_year <= next_7:

                        lunar_today = Converter.Solar2Lunar(solar_this_year)
                        lunar_str = f"{str(lunar_today.day).zfill(2)}/{str(lunar_today.month).zfill(2)}"

                        result.append({
                            "type": "death_anniversary",
                            "name": full_name,
                            "lunar_date": lunar_str,
                            "solar_date": solar_this_year.isoformat(),
                            "calendar_type": "solar",
                            "message": build_message(full_name, lunar_str, solar_this_year)
                        })

        return jsonify(result), 200

    except Exception as e:
        print("❌ ERROR UPCOMING:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        safe_close(conn, cursor)
