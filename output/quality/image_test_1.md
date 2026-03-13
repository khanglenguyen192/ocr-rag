spaces / 📄 MCLT 12 / 📄 12 400 / 📄 12 400

# [FEAT-DEV] Image analysis

+ ⚙️

## Key details

**Labels**  
None

**Description**

**Hiện tại:**

- Khi upload ảnh, hệ thống gửi trực tiếp ảnh sang AI.
- AI sẽ:
  - tự extract content
  - tự chunk nội dung
  - trả về text cho hệ thống.

**Vấn đề:**

- Platform đang phụ thuộc hoàn toàn vào AI để xử lý nội dung từ ảnh.

**Hướng cài thiện:**

- Platform sẽ tự convert image thành text trước.
- Sau đó mới gửi dữ liệu sang AI.

**Flow dự kiến:**

→ Platform convert image → text  
→ gửi image + extracted text sang AI.

**Lưu ý:** Ảnh có nhiều format file khác nhau. Cán research và xác định những format mà platform sẽ support.

**Điểm khác so với hiện tại:** Phần content extraction sẽ được xử lý từ phía platform trước khi gửi AI.