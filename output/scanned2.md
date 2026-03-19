<!-- Trang 1 -->
DAI HỌC QUỐC GIA TP.HCM  
TRƯỜNG ĐẠI HỌC BÁCH KHOA  
KHOA KHOA HỌC VÀ KỸ THUẬT MÁY TÍNH  

---

LUẬN VĂN THẠC SĨ  

---

**Ứng dụng Graph RAG vào hệ thống Q&A trong lĩnh vực giáo dục**

---

<div style="text-align: center;">
  ![image](image_1.png)
</div>

---

GVHD: PGS. TS. Quản Thành Thơ  
HVCH: Lê Nguyên Khang - 2370618  

---

Thành phố Hồ Chí Minh, 05 2025

---

<!-- Trang 2 -->
PGS. TS. Quản Thành Thơ (GV hướng dẫn) Ngày: ___________

Khoa Khoa học và Kỹ thuật Máy tính

ii

---

<!-- Trang 3 -->
# Lời cam đoan

Tôi xin cam đoan rằng, bài báo cáo Luân văn Thạc sĩ ‘Ứng dụng Graph RAG vào hệ thống Q&A trong lĩnh vực giáo dục’ là sản phẩm nghiên cứu của tôi dưới sự hướng dẫn của thầy PGS. TS. Quản Thành Thơ, chú trọng vào việc giải quyết thách thức thực tiễn trong truy vấn dữ liệu cho Chatbot hồi đáp closed-domain.

Ngoại trừ những thông tin tham khảo rõ ràng từ các công trình nghiên cứu khác, các nội dung trong luận văn là kết quả của quá trình nghiên cứu chủ thể của tôi và chưa từng được công bố trước đây dưới mọi hình thức.

Tôi chấp nhận hoàn toàn trách nhiệm về nội dung và chất lượng của luận văn. Mọi sáng tạo và kết quả đều xuất phát từ công lao và sự cố găng không ngừng của chính tôi. Trong trường hợp có bất kỳ sự đạo văn hay vi phạm bản quyền nào, tôi xác nhận sẽ chịu trách nhiệm và đảm bảo sửa chữa ngay lập tức.

Tôi cam kết tuân thủ nguyên tắc đạo đức nghiên cứu và tuân thủ các quy định của Trường Đại học Bách khoa - Đại học Quốc gia TP.HCM. Bản cam kết này không làm ảnh hưởng đến uy tín của trường và không tạo ra bất kỳ vấn đề pháp lý nào liên quan đến việc sử dụng thông tin hay kết quả nghiên cứu của tôi.

TP Hồ Chí Minh, Tháng 05/2025

Tác giả

Lê Nguyễn Khang

iii

---

<!-- Trang 4 -->
# Lời cảm ơn

Tôi xin gửi lời cảm ơn chân thành và tri ân nhất đến thầy PGS.TS Quản Thành Thọ, người đã dành thời gian và tâm huyết hưởng dân tôi trong quá trình thực hiện đề tài. Sự đồng hành và sự tận tâm chỉ dẫn của thầy không chỉ giúp tôi có một cái nhìn toàn diện hơn về đề tài mà còn nâng cao chất lượng của công trình nghiên cứu.

Tôi muốn bày tỏ lòng biết ơn sâu sắc đến tất cả các thầy, cô và giảng viên Khoa Khoa học và Kỹ thuật Máy tính cũng như Trường Đại học Bách Khoa - Đại học Quốc gia Thành phố Hồ Chí Minh. Kiến thức quý báu mà tôi đã được học từ các thầy, cô đã đóng góp quan trọng vào việc hoàn thành đề tài và phát triển năng lực chuyên môn.

Mặc dù đã có đáng hết sức để hoàn thiện đề tài, tôi nhận thức rằng vẫn còn những hạn chế và thiếu sót. Tôi mong muốn nhân được những lời nhân xét, góp ý từ thầy cô và bạn bè để bài báo cáo này có thể ngày càng được hoàn thiện và phát triển.

iv

---

<!-- Trang 5 -->
# Tóm tắt

Hiện nay, với sự tiến bộ của các kỹ thuật Trí tuệ nhân tạo (Artificial Intelligence), sự phát triển của các hệ thống Chatbot thông minh ngày càng thu hút sự chú ý, đặc biệt là với tính hiệu quả của chúng trong việc thay thế con người ở nhiều lĩnh vực. Trong bối cảnh xu hướng hiện nay, người dùng có xu hướng ưa chương sự sử dụng ngôn ngữ tự nhiên bởi tính thân thiện và tính dễ sử dụng của nó. Tuy nhiên, xỉ lý dữ liệu để tạo câu trả lời là một bài toán cần giải quyết trong các hệ thống Chatbot.

Retrieval-Augmented Generation (RAG) được sinh ra với mục đích kết hợp hai khả năng mạnh mẽ trong xỉ lý ngôn ngữ tự nhiên: truy vấn thông tin và tạo sinh câu trả lời. Mục tiêu chính của RAG là cải thiện chất lượng và độ chính xác của câu trả lời trong các hệ thống Q&A hoặc các tác vụ tương tự, đặc biệt khi phải làm việc với dữ liệu lớn và phức tạp.

Dễ tài này tập trung vào công việc tìm giải pháp để giải quyết một số vấn đề phát sinh khi áp dụng RAG như truy vấn thông tin từ nhiều nguồn, xỉ lý mối quan hệ giữa các đoạn văn bản hay các từ khóa không liên quan đến các đoạn văn bản cần tìm. Việc tăng tốc độ xỉ lý, truy vấn cũng là một trong những thách thức quan trọng cần phải được quan tâm.

v