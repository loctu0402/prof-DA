# Proposal / PoC walkthrough template - spec cấu trúc + checklist

> Template by Loc Tu.

> Template chuẩn để trình bày một **proposal / đề xuất / minh họa** cho 1 dự án, feature, sản phẩm,
> hoặc 1 luồng mới. Chắt lọc từ pattern walkthrough đã validate (looker-config-extractor). Fork
> `PROPOSAL-TEMPLATE.html`, thay mọi `[ ... ]` bằng nội dung của bạn, xoá section không áp dụng.
> Mục tiêu: người đọc đi từ GENERAL tới DETAIL, mỗi phần có framing trực quan riêng, có đủ framework.

## 1. Thứ tự section (general -> detail)

| # | Section | Chứa gì | Framework |
|---|---|---|---|
| 0 | **Header** | Tiêu đề rõ mục tiêu (technical, không phèn) + tagline giá trị 1 dòng + meta (đối tượng/scope/ngày) | - |
| 1 | **Phạm vi** | Epic (1 câu) + bảng Feature: grain / user story rút gọn / output chính | **Epic / Feature / User story** |
| 2 | **Legend / quy ước** | Tầng nguồn provenance (nếu áp dụng), màu, ký hiệu | **Provenance tier** |
| 3 | **Bức tranh toàn cảnh** | Flow nối connector, mỗi node ghi **OUTPUT** trả về (gắn feature); info panels (số liệu / legend / nguyên tắc) | overview |
| 4 | **Cơ chế chi tiết** | Mỗi bước 1 card: Action / Output / **AC / DoD** + tag nguồn + "reason to believe" (bằng chứng) | **DoD / AC** |
| 5 | **RAID** | Risks / Assumptions / Issues / Dependencies | **RAID** |
| 6 | **Mô phỏng luồng** | 1 ví dụ thật chạy qua các bước, framing RIÊNG (container màu) | proof |
| 7 | **Output + demo** | Mẫu vài dòng output + **demo frame** (snapshot deliverable cuối, người nhận sẽ thấy thế này) | detail |
| 7b | **Output hạ tầng + convention** | KHÔNG chỉ UI: show cả lớp hệ thống bên dưới (cấu trúc folder scaffold idempotent + cache máy đọc + log + evidence), kèm bộ quy tắc/convention ràng buộc cấu trúc đó | **scaffold + convention** |
| 8 | **Giới hạn** | Bảng: Giới hạn / Vì sao / Ảnh hưởng / Cách xử lý | honest |
| 9 | **Provenance footer + roadmap** | Source-tier + freshness + owner + hướng long-term optional | - |

## 2. Quy tắc trình bày (lesson-learn đóng vào template)

1. **General -> detail**: overview (flow) trước, cơ chế/chi tiết sau. Đừng đưa bằng chứng chi tiết lên đầu.
2. **Mỗi loại section có framing trực quan RIÊNG, không blend**:
   - overview = flow connector (`.bpflow`); per-step = card AC/DoD (`.card`); simulation = container màu riêng
     (`.uflow`); demo = frame kiểu cửa sổ file (`.demoframe`). Người đọc nhìn là biết đang ở loại nội dung nào.
3. **Node/box ghi OUTPUT** (kết quả bước đó trả về, gắn với feature/mục tiêu), KHÔNG chỉ mô tả cơ chế.
4. **Tag nguồn mọi field** nếu có provenance (SYSTEM / DERIVED / REASONING); REASONING bắt buộc người duyệt.
5. **Full-id, không viết tắt mơ hồ** (vd table = `project.dataset.table`, không phải tên rút gọn).
6. **0 AI-tell symbol**: mũi tên vẽ bằng CSS (không dùng ký tự unicode `->` mũi tên, em-dash, interpunct);
   tiếng Việt đủ dấu, giọng practitioner (đọc thành tiếng nghe như người thật nói, không dịch cứng).
7. **Mỗi bước có Acceptance Criteria + Definition of Done**; có **RAID**; có **Epic/Feature/User story**.
8. **Demo / minh họa phải framed rõ** là demo (tag "DEMO", frame file), đừng để lẫn như nội dung thật.
9. **Honest**: nêu giới hạn thật + cách xử lý, không giấu.
10. **User story theo block có cấu trúc** (Connextra: Là role / Muốn capability / Để value + Output),
    KHÔNG viết 1 đoạn văn dài (thiếu chuyên nghiệp, không follow framework chuẩn).
11. **Output gồm CẢ hạ tầng/hệ thống bên dưới, không chỉ UI người dùng thấy**: proposal kèm output thật
    phải show lớp chạy bên dưới (cấu trúc folder scaffold **idempotent**, cache máy đọc, log, evidence),
    không chỉ snapshot UI. Luôn đi kèm bộ quy tắc + template chuẩn + minh họa cụ thể + convention. Lớp hạ
    tầng này LÀ bằng chứng đề xuất chuẩn chỉnh, quy trình thật và lặp lại được. Nếu output là knowledge base
    extract từ resource dùng chung (vd 1 table phục vụ nhiều report), tách **layer SoT xuyên-scope** (tích lũy,
    không khóa vào 1 lần extract) khỏi layer scoped; naming/tổ chức do owner chọn, agent đề xuất option từ
    discovery (không hardcode một convention cứng).
12. **Highlight khóa liên kết khi trình bày quy trình nhiều bước / nhiều tool**: nếu proposal/walkthrough mô tả
    một process mà output bước này nối với bước kia (ID, key, value đối chiếu qua lại giữa các tool), gán **mỗi
    loại khóa một màu cố định** (vd report_id đỏ, datasource_id xanh, field/alias teal, value tím, title amber),
    kèm legend + chuỗi nối (vẽ bằng CSS arrow, không unicode). Người đọc luôn hỏi "làm sao các thông tin nối với
    nhau giữa các bước"; hệ màu trả lời trực quan: cùng màu nghĩa là cùng một mẩu thông tin được dùng lại ở bước
    khác. Bắt buộc khi build HTML walkthrough / report proposal có nhiều phase scan-collect-map.

## 3. Checklist trước khi ship

```
[ ] Header: tiêu đề cover đủ mục tiêu, technical, không phèn; tagline 1 dòng
[ ] Phạm vi: Epic + mọi Feature có grain / user story / output
[ ] Overview: flow nối connector; mỗi node ghi OUTPUT; có info panel
[ ] Per-step: mỗi bước có Action / Output / AC / DoD + tag + reason-to-believe
[ ] RAID đủ 4 mục
[ ] Simulation: 1 ví dụ thật, framing riêng (khác per-step)
[ ] Output: mẫu vài dòng + demo frame của deliverable cuối
[ ] Giới hạn: bảng có cấu trúc (vì sao / ảnh hưởng / cách xử lý)
[ ] Footer: source-tier + freshness + owner (+ roadmap optional)
[ ] Output hạ tầng: folder scaffold idempotent + cache/log/evidence (không chỉ UI); convention được document ràng buộc
[ ] Linking keys: nếu là process nhiều bước/tool, highlight khóa nối (màu cố định theo loại) + legend + chuỗi nối
[ ] Gate: 0 em-dash / unicode arrow / interpunct; VN đủ dấu; table full-id; demo framed rõ
```

## 4. Framework reference

- **Epic / Feature / User story**: Epic = mục tiêu lớn nhất; Feature = mảng deliverable (có grain + output);
  User story = "là [vai trò], tôi muốn [hành động] để [giá trị]".
- **DoD / AC**: Acceptance Criteria = điều kiện pass binary của bước; Definition of Done = trạng thái coi là xong.
- **RAID**: Risks (rủi ro + giảm thiểu) / Assumptions (giả định) / Issues (vấn đề mở) / Dependencies (phụ thuộc).
- **Provenance tier**: SYSTEM (tool nguyên văn) / DERIVED (code deterministic, verify được) / REASONING
  (suy luận, cần người duyệt). Provenance footer = source-tier + freshness + owner để người đọc biết độ tin.

> Ví dụ đã fill đầy đủ template này: `projects/looker-config-extractor/output/walkthrough.html`.
> Token màu lấy theo <organization> theme; design-system canonical: `shared/templates/_contract/`.
