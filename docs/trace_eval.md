# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Châu Tùng Dương  
> **Mã Sinh Viên / Mã Học viên:** 2A202602822  
> **Chủ đề Lựa chọn:** Trợ lý Thông minh Theo dõi, Tổng hợp Thông báo Đa kênh (Discord, Email, Zalo, GitHub) kết hợp Lên lịch Google Calendar

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm (Định lượng số lượng) |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Chuỗi 4 bước suy luận liên tiếp: Phân tích truy vấn -> Quét thông báo đa kênh -> Trích xuất thời gian/tiêu đề họp -> Ra quyết định đặt lịch. |
| **2. Tool Interaction** | 4 / 5 | Tích hợp dữ liệu từ 4 nền tảng (Discord, Email, Zalo, GitHub) và 2 công cụ thao tác qua MCP Server (search_notifications, create_calendar_event). |
| **3. Dynamic Decision** | 4 / 5 | Tối thiểu 3 điểm rẽ nhánh động phụ thuộc Observation: Nếu không có tin nhắn -> dừng; nếu có tin nhưng không có deadline -> chỉ tóm tắt; nếu có deadline -> tạo lịch. |
| **4. Long Horizon Goal** | 4 / 5 | Duy trì mục tiêu dài hạn qua chu trình ReAct 4-5 bước lặp (Thought -> Action -> Observation) để hoàn thành trọn vẹn yêu cầu người dùng. |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | *Tổng điểm 16/20 (> 12/20): Bài toán hoàn toàn phù hợp và tối ưu khi triển khai Agentic ReAct System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Kiểm tra xem có thông báo mới nào liên quan đến 'pull request' hoặc 'release' trên kênh GitHub không?",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_notifications",
    "arguments": {
      "platform": "github",
      "query": "release"
    },
    "observation": {
      "status": "SUCCESS",
      "count": 1,
      "platform_filter": "github",
      "query": "release",
      "data": [
        {
          "id": "NOTIF-GH-01",
          "platform": "github",
          "sender": "GitHub Actions",
          "title": "Release v2.5.0 Deployment Succeeded",
          "content": "Pull Request #42 đã được merge vào nhánh main. Phiên bản release v2.5.0 đã deploy thành công lúc 08:30.",
          "timestamp": "08:30 13/09/2026"
        }
      ],
      "message": "Tìm thấy 1 thông báo khớp với từ khóa 'release'."
    },
    "latency_ms": 5838.08
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
