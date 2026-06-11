# proposal-walkthrough template

> Template by Loc Tu.

Template chuẩn để trình bày một **proposal / đề xuất / minh họa** cho 1 dự án, feature, sản phẩm hoặc
luồng mới: đi từ general tới detail, mỗi phần có framing trực quan riêng, gắn sẵn framework (Epic /
Feature / User story, RAID, DoD / AC, provenance tier).

## Files

| File | Vai trò |
|---|---|
| `PROPOSAL-TEMPLATE.html` | Skeleton fork được (10 section + CSS distilled). Thay mọi `[ ... ]` bằng nội dung của bạn. |
| `PROPOSAL-TEMPLATE.md` | Spec cấu trúc + 9 quy tắc trình bày + checklist trước khi ship + framework reference. |
| `README.md` | File này. |

## Cách fork

1. Copy `PROPOSAL-TEMPLATE.html` vào output của dự án (vd `projects/<name>/output/walkthrough.html`).
2. Đọc `PROPOSAL-TEMPLATE.md` mục 1 (thứ tự section) + mục 2 (quy tắc). Thay mọi `[ ... ]`; xoá section
   không áp dụng (vd không có provenance thì bỏ tag; không có nhánh maintain thì bỏ nhánh thứ 2 của flow).
3. Giữ đúng các framing: overview = flow connector, per-step = card AC/DoD, simulation = `.uflow`,
   demo = `.demoframe`. KHÔNG để các loại blend vào nhau.
4. Chạy checklist `PROPOSAL-TEMPLATE.md` mục 3 trước khi gửi. Đặc biệt gate AI-tell: 0 em-dash / unicode
   arrow / interpunct (mũi tên đã vẽ bằng CSS), tiếng Việt đủ dấu, table để full id.

## Nguyên tắc cốt lõi (chi tiết ở SPEC mục 2)

- General -> detail; mỗi section một framing trực quan riêng.
- Node/box ghi OUTPUT (kết quả trả về), không chỉ cơ chế.
- Mỗi bước có Acceptance Criteria + Definition of Done; có RAID; có Epic/Feature/User story.
- Tag nguồn mọi field (REASONING cần người duyệt); demo framed rõ là demo; nêu giới hạn thật.

## Ví dụ đã fill đầy đủ

`projects/looker-config-extractor/output/walkthrough.html` (bản gốc chắt lọc ra template này). Design-system
token canonical: `shared/templates/_contract/`.
