"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Đề tài: Trợ lý Tổng hợp Thông báo Đa kênh (Discord, Email, Zalo, GitHub) & Google Calendar.
"""

import json
from typing import Dict, Any, List

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # --------------------------------------------------------------------------
    # TOOL 1: Tra cứu & Lọc thông báo đa kênh (Discord, Email, Zalo, GitHub)
    # --------------------------------------------------------------------------
    {
        "name": "search_notifications",
        "description": "Tìm kiếm và lọc các thông báo, tin nhắn từ các kênh liên lạc (Discord, Email, Zalo, GitHub) theo từ khóa hoặc nền tảng.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Từ khóa tìm kiếm trong nội dung thông báo (ví dụ: 'release', 'thuyết trình', 'deadline', 'họp')."
                },
                "platform": {
                    "type": "string",
                    "description": "Kênh thông báo cần lọc: 'discord', 'email', 'zalo', 'github' hoặc 'all'.",
                    "enum": ["discord", "email", "zalo", "github", "all"]
                }
            },
            "required": ["query"]
        }
    },

    # --------------------------------------------------------------------------
    # TOOL 2: Tạo sự kiện trên Google Calendar
    # --------------------------------------------------------------------------
    {
        "name": "create_calendar_event",
        "description": "Tạo một sự kiện hoặc lịch hẹn mới trên Google Calendar từ thông báo thu thập được hoặc theo yêu cầu người dùng.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Tiêu đề cuộc họp hoặc sự kiện cần lên lịch (ví dụ: 'Họp Review Sprint K4', 'Lịch thuyết trình đồ án')."
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian diễn ra sự kiện (ví dụ: '09:00 20/09/2026' hoặc '08:30 25/09/2026')."
                },
                "location_or_link": {
                    "type": "string",
                    "description": "Địa điểm họp hoặc đường dẫn trực tuyến (ví dụ: 'Google Meet', 'Phòng Lab 1', 'Zoom')."
                },
                "description": {
                    "type": "string",
                    "description": "Ghi chú tóm tắt nội dung cuộc họp hoặc nguồn trích xuất thông báo."
                }
            },
            "required": ["title", "datetime_str"]
        }
    },

    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # Đảm bảo 100% tương thích với bài kiểm tra tự động của hệ thống
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn tư vấn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn học tập phụ trách (ví dụ: 'PGS.TS Nguyễn Văn A')"
                }
            },
            "required": ["student_id", "datetime_str", "advisor_name"]
        }
    },

    # Tool tra cứu học vụ ban đầu (giữ tương thích)
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

# Kho thông báo đa kênh mô phỏng
MOCK_NOTIFICATIONS_DB = [
    {
        "id": "NOTIF-GH-01",
        "platform": "github",
        "sender": "GitHub Actions",
        "title": "Release v2.5.0 Deployment Succeeded",
        "content": "Pull Request #42 đã được merge vào nhánh main. Phiên bản release v2.5.0 đã deploy thành công lúc 08:30.",
        "timestamp": "08:30 13/09/2026"
    },
    {
        "id": "NOTIF-DC-02",
        "platform": "discord",
        "sender": "Mentor AI Lab (Channel #announcements)",
        "title": "Lịch thuyết trình đồ án Khóa K4",
        "content": "Nhắc nhở toàn bộ học viên: Lịch thuyết trình đồ án diễn ra vào lúc 08:30 ngày 25/09/2026 trên Google Meet phòng Lab 1.",
        "timestamp": "10:15 13/09/2026"
    },
    {
        "id": "NOTIF-ZL-03",
        "platform": "zalo",
        "sender": "Trưởng nhóm Đồ án",
        "title": "Họp thống nhất slide đồ án",
        "content": "Tối nay 20:00 ngày 15/09/2026 nhóm mình họp online qua Google Meet để chốt slide nhé.",
        "timestamp": "11:00 13/09/2026"
    },
    {
        "id": "NOTIF-EM-04",
        "platform": "email",
        "sender": "VinUni Academic Affairs <academic@vinuni.edu.vn>",
        "title": "Thông báo mở cổng đăng ký môn học học kỳ mới",
        "content": "Cổng đăng ký môn học sẽ chính thức mở từ 09:00 ngày 01/10/2026.",
        "timestamp": "09:00 12/09/2026"
    }
]

# Cơ sở dữ liệu học vụ ban đầu
MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}


def execute_search_notifications(query: str, platform: str = "all") -> str:
    """Thực thi tìm kiếm và lọc thông báo đa kênh"""
    q = query.strip().lower()
    p = platform.strip().lower() if platform else "all"

    matched = []
    for notif in MOCK_NOTIFICATIONS_DB:
        # Lọc platform nếu có chỉ định cụ thể
        if p != "all" and notif["platform"].lower() != p:
            continue
        
        # Tìm kiếm từ khóa trong title, content, sender
        searchable_text = f"{notif['title']} {notif['content']} {notif['sender']}".lower()
        if q in searchable_text:
            matched.append(notif)

    if matched:
        return json.dumps({
            "status": "SUCCESS",
            "count": len(matched),
            "platform_filter": p,
            "query": query,
            "data": matched,
            "message": f"Tìm thấy {len(matched)} thông báo khớp với từ khóa '{query}'."
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "count": 0,
            "platform_filter": p,
            "query": query,
            "message": f"Không tìm thấy thông báo nào liên quan đến từ khóa '{query}' trên kênh '{platform}'."
        }, ensure_ascii=False)


def execute_create_calendar_event(title: str, datetime_str: str, location_or_link: str = "Google Meet", description: str = "") -> str:
    """Thực thi tạo sự kiện trên Google Calendar"""
    event_id = f"GCAL-EVT-{abs(hash(title + datetime_str)) % 10000:04d}"
    return json.dumps({
        "status": "SUCCESS",
        "event_id": event_id,
        "title": title,
        "datetime": datetime_str,
        "location": location_or_link,
        "description": description,
        "message": f"Đã tạo thành công sự kiện '{title}' trên Google Calendar vào lúc {datetime_str} (Địa điểm: {location_or_link})."
    }, ensure_ascii=False)


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "search_notifications": execute_search_notifications,
    "create_calendar_event": execute_create_calendar_event,
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
