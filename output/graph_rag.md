ĐẠI HỌC QUỐC GIA TP.HCM TRƯỜNG ĐẠI HỌC BÁCH KHOA KHOA KHOA HỌC VÀ KỸTHUẬT MÁY TÍNH 

## LUẬN VĂN THẠC SĨ 

# **Ứng dụng Graph RAG vào hệthống Q&A trong lĩnh vực giáo dục** 


![](output/graph_rag/graph_rag.pdf-0001-03.png)


GVHD: PGS. TS. Quản Thành Thơ HVCH: Lê Nguyên Khang - 2370618 

Thành phốHồChí Minh, 05 2025 

Ngày: 

PGS. TS. Quản Thành Thơ (GV hướng dẫn) 

Khoa Khoa học và Kỹthuật Máy tính 

ii 

## **Lời cam đoan** 

Tôi xin cam đoan rằng, bài báo cáo Luận văn Thạc sĩ ‘Ứng dụng Graph RAG vào hệ thống Q&A trong lĩnh vực giáo dục’ là sản phẩm nghiên cứu của tôi dưới sựhướng dẫn của thầy PGS. TS. Quản Thành Thơ, chú trọng vào việc giải quyết thách thức thực tiễn trong truy vấn dữliệu cho Chatbot hỏi đáp closed-domain. 

Ngoại trừnhững thông tin tham khảo rõ ràng từcác công trình nghiên cứu khác, các nội dung trong luận văn là kết quảcủa quá trình nghiên cứu chủthểcủa tôi và chưa từng được công bốtrước đây dưới mọi hình thức. 

Tôi chấp nhận hoàn toàn trách nhiệm vềnội dung và chất lượng của luận văn. Mọi sáng tạo và kết quảđều xuất phát từcông lao và sựcốgắng không ngừng của chính tôi. Trong trường hợp có bất kỳsựđạo văn hay vi phạm bản quyền nào, tôi xác nhận sẽchịu trách nhiệm và đảm bảo sửa chữa ngay lập tức. 

Tôi cam kết tuân thủnguyên tắc đạo đức nghiên cứu và tuân thủcác quy định của Trường Đại học Bách khoa - Đại học Quốc gia TP.HCM. Bản cam kết này không làm ảnh hưởng đến uy tín của trường và không tạo ra bất kỳvấn đềpháp lý nào liên quan đến việc sửdụng thông tin hay kết quảnghiên cứu của tôi. 

TP HồChí Minh, Tháng 05/2025 

Tác giả 


![](output/graph_rag/graph_rag.pdf-0003-07.png)


Lê Nguyên Khang 

iii 

## **Lời cảm ơn** 

Tôi xin gửi lời cảm ơn chân thành và tri ân nhất đến thầy PGS.TS Quản Thành Thơ, người đã dành thời gian và tâm huyết hướng dẫn tôi trong quá trình thực hiện đềtài. Sự đồng hành và sựtận tâm chỉdẫn của thầy không chỉgiúp tôi có một cái nhìn toàn diện hơn vềđềtài mà còn nâng cao chất lượng của công trình nghiên cứu. 

Tôi muốn bày tỏlòng biết ơn sâu sắc đến tất cảcác thầy, cô và giảng viên Khoa Khoa học và Kỹthuật Máy tính cũng như Trường Đại học Bách Khoa - Đại học Quốc gia Thành phốHồChí Minh. Kiến thức quý báu mà tôi đã được học từcác thầy, cô đã đóng góp quan trọng vào việc hoàn thành đềtài và phát triển năng lực chuyên môn. 

Mặc dù đã cốgắng hết sức đểhoàn thiện đềtài, tôi nhận thức rằng vẫn còn những hạn chếvà thiếu sót. Tôi mong muốn nhận được những lời nhận xét, góp ý từthầy cô và bạn bè đểbài báo cáo này có thểngày càng được hoàn thiện và phát triển. 

iv 

## **Tóm tắt** 

Hiện nay, với sựtiến bộcủa các kỹthuật Trí tuệnhân tạo (Artificial Intelligence), sự phát triển của các hệthống Chatbot thông minh ngày càng thu hút sựchú ý, đặc biệt là với tính hiệu quảcủa chúng trong việc thay thếcon người ởnhiều lĩnh vực. Trong bối cảnh xu hướng hiện nay, người dùng có xu hướng ưa chuộng sựsửdụng ngôn ngữtự nhiên bởi tính thân thiện và tính dễsửdụng của nó. Tuy nhiên, xửlý dữliệu đểtạo câu trảlời là một bài toán cần giải quyết trong các hệthống Chatbot. 

Retrieval-Augmented Generation (RAG) được sinh ra với mục đích kết hợp hai khả năng mạnh mẽtrong xửlý ngôn ngữtựnhiên: truy vấn thông tin và tạo sinh câu trảlời. Mục tiêu chính của RAG là cải thiện chất lượng và độchính xác của câu trảlời trong các hệthống Q&A hoặc các tác vụtương tự, đặc biệt khi phải làm việc với dữliệu lớn và phức tạp. 

Đềtài này tập trung vào công việc tìm giải pháp đểgiải quyết một sốvấn đềphát sinh khi áp dụng RAG như truy vấn thông tin từnhiều nguồn, xửlý mối quan hệgiữa các đoạn văn bản hay các từkhóa không liên quan đến các đoạn văn bản cần tìm. Việc tăng tốc độxửlý, truy vấn cũng là một trong những thách thức quan trọng cần phải được quan tâm. 

v 

## **Mục lục** 

|**Lời cam đoan**|**Lời cam đoan**|**Lời cam đoan**||**iii**|
|---|---|---|---|---|
|**Lời cảm ơn**||||**iv**|
|**Tóm tắt**||||**v**|
|**1**|**Giới **|**thiệu**||**1**|
||1.1|Đặt vấn đề. . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|1|
||1.2|Phạm vi nghiên cứu<br>. . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|2|
||1.3|Tổng quan vềbáo cáo<br>. . . .|. . . . . . . . . . . . . . . . . . . . . . . .|2|
|**2**|**Kiến thức nền tảng**|||**4**|
||2.1|Large Language Model - LLM|. . . . . . . . . . . . . . . . . . . . . . . .|4|
||2.2|Retrieval-Augmented Generation - RAG<br>. . . . . . . . . . . . . . . . . .||6|
||2.3|Thuật toán Leiden<br>. . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|7|
||2.4|Cơ sởdữliệu Neo4j . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|10|
||2.5|Ngôn ngữtruy vấn Cypher . .|. . . . . . . . . . . . . . . . . . . . . . . .|12|
|**3**|**Công trình liên quan**|||**14**|
||3.1|Phân đoạn văn bản dựa trên sựthay đổi chủđề. . . . . . . . . . . . . .||14|
||3.2|BERT . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|16|
||3.3|Medical Graph RAG . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|17|
|||3.3.1<br>Cấu trúc đồthịba tầng|. . . . . . . . . . . . . . . . . . . . . . .|17|
|||3.3.2<br>Xây dựng ĐồthịY tế|. . . . . . . . . . . . . . . . . . . . . . . .|18|
|||3.3.3<br>Gộp đồthị(Tags Generation and Merge) . . . . . . . . . . . . . .||19|
|||3.3.4<br>Truy xuất từđồthị(Retrieve from the Graph) . . . . . . . . . . .||19|
|||3.3.5<br>Đánh giá phương pháp|. . . . . . . . . . . . . . . . . . . . . . . .|19|
||3.4|Underthesea Toolkit<br>. . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|20|
||3.5|Graphdatascience . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|20|
||3.6|Langchain . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .|21|



vi 

|**4**|**Phương pháp đềxuất**|**Phương pháp đềxuất**|||**22**|
|---|---|---|---|---|---|
||4.1|Tổng quan vềkiến trúc . . . . .|. . . . . . . . .|. . . . . . . . . . . . . .|22|
||4.2|Graph RAG Approach & Pipeline . . . . . . . .||. . . . . . . . . . . . . .|23|
|||4.2.1<br>Phân đoạn văn bản (Document chunking)||. . . . . . . . . . . . .|23|
|||4.2.2<br>Trích xuất thực thể(Entity Extraction) .||. . . . . . . . . . . . . .|23|
|||4.2.3<br>Liên kết thực thể(Relationship linking)||. . . . . . . . . . . . . .|24|
|||4.2.4<br>Lưu trữdữliệu quan hệ|. . . . . . . . .|. . . . . . . . . . . . . .|26|
|||4.2.5<br>Xây dựng đồthịcộng đồng (Graph Communities) . . . . . . . . .|||28|
|||4.2.6<br>Tóm tắt cộng đồng (Communities Summaries) . . . . . . . . . . .|||29|
|||4.2.7<br>Truy vấn dữliệu<br>. . . .|. . . . . . . . .|. . . . . . . . . . . . . .|29|
||4.3|Kết quảhiện thực . . . . . . . .|. . . . . . . . .|. . . . . . . . . . . . . .|31|
|||4.3.1<br>Dữliệu thực nghiệm<br>. .|. . . . . . . . .|. . . . . . . . . . . . . .|31|
|||4.3.2<br>Phương pháp đánh giá .|. . . . . . . . .|. . . . . . . . . . . . . .|31|
|||4.3.3<br>Kết quả. . . . . . . . .|. . . . . . . . .|. . . . . . . . . . . . . .|32|
|**5**|**Kết luận**||||**34**|
||5.1|Nhận xét . . . . . . . . . . . . .|. . . . . . . . .|. . . . . . . . . . . . . .|34|
||5.2|Hướng phát triển trong tương lai|. . . . . . . .|. . . . . . . . . . . . . .|35|
|**Danh sách tham khảo**|||||**36**|



vii 

## **Danh sách hình vẽ** 

|2.1|Minh họa thuật toán Leiden . . . . . . . . . . . . . . . . . . . . . . . . .|8|
|---|---|---|
|2.2|Minh họa quá trình tối ưu hóa cục bộtrong thuật toán Leiden . . . . . .|9|
|3.1|Chiến lược theo dõi sựthay đổi chủđềvăn bản<br>. . . . . . . . . . . . . .|14|
|3.2|Giải thuật phân tách đoạn theo chủđề. . . . . . . . . . . . . . . . . . .|15|
|3.3|Graph RAG pipeline . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|17|
|4.1|hgRAG pipeline . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|23|
|4.2|De-duplication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|26|
|4.3|Cơ sởdữliệu đồthị. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|27|
|4.4|Minh họa một cộng đồng được xây dựng dựa trên thuật toán Leiden . . .|28|
|4.5|Minh họa luồng truy vấn toàn cục . . . . . . . . . . . . . . . . . . . . . .|30|
|4.6|Luồng truy vấn cục bộ. . . . . . . . . . . . . . . . . . . . . . . . . . . .|30|



viii 

## **Danh sách bảng** 

4.1 Bảng kết quảđánh giá BERTscore . . . . . . . . . . . . . . . . . . . . . 32 

ix 

## **Chương 1** 

## **Giới thiệu** 

Trong chương này, tác giảsẽgiới thiệu tổng quan vềnội dung của đềtài cùng với mục tiêu đềra trong quá trình thực hiện đềtài. 

## **1.1 Đặt vấn đề** 

QA là một lĩnh vực nghiên cứu sôi động và nhiều hướng nghiên cứu. Nó là sựgiao thoa kết hợp của Xửlý ngôn ngữtựnhiên (NLP), Truy xuất thông tin (Information Retrieval - IR), Suy luận logic (Logical Reasoning), Biểu diễn tri thức (Knowledge Representation), Học máy máy (Machine Learning), Tìm kiếm Ngữnghĩa (Semantic search). 

CQAS là một hướng nghiên cứu quan trọng trong Xửlý ngôn ngữtựnhiên (Natural Language Processing - NLP) và là hướng mởrộng hơn của bài toán QAS. Do đặc trưng linh hoạt của ngôn ngữtựnhiên mà các câu hỏi rất không có cấu trúc đồng thời do sự mơ hồtrong chính câu hỏi có thểdẫn đến các câu trảlời sai, CQAS có thểgiảm bớt sự nhập nhằng bằng cách đặt thêm một sốcâu hỏi phụcho người hỏi đểlàm rõ hơn vềngữ cảnh. Cụthểhơn, nhiệm vụCQAS là xây dựng một phần mềm có thểtựtrảlời một loạt câu hỏi bằng ngôn ngữtựnhiên có tính liên kết với nhau xuất hiện trong một cuộc hội thoại. Nó cũng có thểduy trì một cuộc đối thoại mạch lạc và phù hợp với người dùng, thay vì chỉcung cấp các câu trảlời đứt đoạn. 

Một trong những công việc cần thiết cho các công tác nghiên cứu QA và CQAS là tăng cường khảnăng xửlý các câu hỏi phức tạp và cải tải thiện chất lượng câu trảlời. Từđó, kỹthuật RAG được áp dụng nhằm kết hợp khảnăng truy vấn thông tin từcác nguồn bên ngoài với khảnăng sinh văn bản của các mô hình ngôn ngữ, tạo ra các câu trảlời chính xác và có tính ứng dụng cao hơn, đặc biệt trong các bài toán có dữliệu lớn và phức tạp, giúp cải thiện hiệu quảvà độchính xác của các hệthống Q&A hoặc các tác vụxửlý ngôn ngữtựnhiên khác. 

Tuy nhiên khi sửdụng RAG, sẽcó một sốkhó khăn như sau: 

- Các từkhóa trong câu hỏi chỉliên quan tới một sốđoạn văn bản nhất định. Và 

1 

_CHƯƠNG 1. GIỚI THIỆU_ 

2 

trong mỗi đoạn văn bản, thì lại đềcập tới các đoạn văn bản khác nhau. Do đó, cần truy vấn được hết các tài liệu này mới có thểtạo thành câu trảlời. 

- Từkhóa trong câu hỏi là là từngữthông dụng, có thểkhông khớp với các đoạn văn bản. 

- Vấn đềhiểu toàn diện dữliệu. 

Nhận thấy vấn đềtrên, tôi quyết định thực hiện đềtài này nhằm tạo ra một giải pháp có khảnăng tăng cường khảnăng tổng hợp thông tin đểtạo thành câu trảlời đầy đủvà chính xác hơn. 

## **1.2 Phạm vi nghiên cứu** 

Trong bài nghiên cứu này, tôi sẽthiết kếvà xây dựng một giải pháp hướng tới giải quyết vấn đềnhư sau: 

- Tôi đã thu thập và sửdụng dữliệu cho đềtài từcác nguồn thông tin, các văn bản chính thống từcác trang web, hệthống lưu trữthuộc Trường Đại học Bách Khoa - Đại học Quốc gia Thành phốHồChí Minh. Các dữliệu dùng đểthửnghiệm trong bài báo cáo này thuộc các thểloại như thủtục hành chính, các bài viết giới thiệu, các quy chế, quy định, các văn bản học thuật,... 

- Giải pháp cung cấp khảnăng cần truy vấn các đoạn văn bản từnhiều tài liệu khác nhau đểtìm ra các câu trảlời phù hợp. Các đoạn văn bản này có thểlà từcác nguồn khác nhau như văn bản luật, tài liệu hướng dẫn. 

- Các từkhóa trong câu hỏi không nhất thiết phải khớp trực tiếp với các đoạn văn bản, và một đoạn văn bản (ví dụ: A) có thểliên quan đến những đoạn khác (ví dụ: B, C). Hệthống cần khảnăng tìm kiếm các mối quan hệnày đểtổng hợp thông tin từcác nguồn khác nhau. 

- Các từkhóa trong câu hỏi đôi khi có thểlà những từngữthông dụng, không trực tiếp khớp với các đoạn văn bản có chứa thông tin cần thiết. Điều này làm cho việc truy vấn trởnên khó khăn hơn, đặc biệt trong các lĩnh vực chuyên môn như giáo dục, quy chế, quy định,... 

## **1.3 vềbáo cáo Tổng quan** 

Có tất cả5 chương được trình bày trong bài cáo báo đồán này: 

- Chương 1: Giới thiệu tổng quan vềnội dung đềtài, mục tiêu và các giai đoạn đặt ra của đềtài. 

_CHƯƠNG 1. GIỚI THIỆU_ 

3 

- Chương 2: Trình bày các kiến thức nền tảng được nghiên cứu và sẽsửdụng trong đềtài. 

- Chương 3: Giới thiệu một sốcông trình liên quan đến đềtài. 

- Chương 4: Trình bày vềgiải pháp mà tôi đã nghiên cứu và thực hiện đềtài này và các kết quảthực nghiệm 

- Chương 5: Tổng kết, đánh giá giải pháp và đềra hướng phát triển cho các giai đoạn tiếp theo trong tương lai. 

## **Chương 2** 

## **Kiến thức nền tảng** 

Trong chương này, tác giảsẽtrình bày các kiến thức nền tảng cần thiết đểhướng đến xây dựng Graph RAG. 

## **2.1 Large Language Model LLM** 

_"Large language model là một loại mô hình ngôn ngữđược đào tạo bằng cách sửdụng các kỹthuật học sâu trên tập dữliệu văn bản khổng lồ. Các mô hình này có khảnăng tạo văn bản tương tựnhư con người và thực hiện các tác vụxửlý ngôn ngữtựnhiên khác nhau."_ 

Một mô hình ngôn ngữcó thểcó độphức tạp khác nhau, từcác mô hình n-gram đơn giản đến các mô hình mạng mô phỏng hệthần kinh của con người vô cùng phức tạp. Tuy nhiên, thuật ngữLarge language model” thường dùng đểchỉcác mô hình sửdụng kỹthuật học sâu và có sốlượng tham sốlớn, có thểtừhàng tỷđến hàng nghìn tỷ. Những mô hình này có thểphát hiện các quy luật phức tạp trong ngôn ngữvà tạo ra các văn bản y hệt con người. 

Kiến trúc của LLM chủyếu bao gồm nhiều lớp mạng neural, như recurrent layers, feedforward layers, embedding layers, attention layers. Các lớp này hoạt động cùng nhau đểxửlý văn bản đầu vào và tạo dựđoán đầu ra. 

- Embedding layer là thành phần quan trọng trong các mạng học sâu, đặc biệt trong xửlý ngôn ngữtựnhiên (NLP). 

_"An embedding layer maps discrete tokens (e.g., words or characters) to continuous vectors in a fixed-dimensional space, enabling the model to learn meaningful semantic representations of the input data during training"[1, 2]._ 

Các vector ánh xạnày có thểhọc được mối quan hệngữnghĩa giữa các từvà được huấn luyện cùng với các trọng sốcủa mô hình. 

Embedding layer chuyển đổi từng từtrong văn bản đầu vào thành biểu diễn vector nhiều chiều (high-dimensional). Những vector này nắm bắt thông tin ngữnghĩa và 

4 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

5 

cú pháp của từng đơn vịcấu tạo nên câu (từhoặc token) và giúp mô hình hiểu được ngữcảnh của văn bản. 

- Feedforward layer là một thành phần cơ bản trong các mạng học sâu. 

_"Feedforward layers are the basic building blocks of deep neural networks, where information flows in a unidirectional manner through successive layers of linear transformations followed by nonlinear activation functions"[3, 4]._ 

Feedforward layers gồm nhiều lớp được kết nối đầy đủáp dụng các phép biến đổi phi tuyến tính cho các embedding vector đầu vào. Các lớp này giúp mô hình học các thông tin trừu tượng hơn từvăn bản đầu vào. 

- Recurrent layers là thành phần thiết yếu trong mạng học sâu, đặc biệt trong xửlý dữliệu chuỗi. 

_"Recurrent layers are specialized neural network components designed for sequence modeling tasks, enabling the model to retain temporal dependencies by incorporating feedback connections that link the outputs of previous steps to the current computation"[5, 6]._ 

Recurrent layers của LLM được thiết kếđểdiễn giải thông tin từvăn bản đầu vào theo trình tự. Các lớp này duy trì trạng thái ẩn được cập nhật ởmỗi bước thời gian, cho phép mô hình nắm bắt được sựphụthuộc giữa các từtrong câu. 

- Attention layers là thành phần quan trọng trong các mạng học sâu, đặc biệt trong các tác vụxửlý chuỗi dữliệu như dịch máy và tóm tắt văn bản. 

   - _"Attention layers are designed to allow the model to focus on different parts of the input sequence with varying attention weights, thus enabling it to capture complex dependencies within the data. This mechanism has proven highly effective in tasks like machine translation and text summarization."[7, 8, 9]._ 

Attention layers là một phần quan trọng khác của LLM, cho phép mô hình tập trung có chọn lọc vào các phần khác nhau của văn bản đầu vào. Cơ chếnày giúp mô hình chú ý đến các phần có liên quan nhất của văn bản đầu vào và tạo ra các dựđoán chính xác hơn. 

LLM học hỏi từkhối lượng dữliệu khổng lồ, thường được xây dựng dựa trên những bộdữliệu đủlớn đểbao gồm gần như mọi thứđã được xuất bản trên internet trong một khoảng thời gian dài. LLM được học từmột khối lượng rất lớn văn bản trước khi có thể ghi nhớcác quy luật và cấu trúc ngôn ngữ. Đây là nguyên nhân mấu chốt đểLLM có thểhiểu và phản hồi theo ngữcảnh một cách logic và mạch lạc. 

Dưới đây là một sốví dụvềLLM trong thực tế: 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

6 

- GPT-3 (Generative Pre-training Transformer 3) – Đây là một trong những Mô hình Ngôn ngữLớn lớn nhất được phát triển bởi OpenAI. Nó có 175 tỷtham sốvà có thểthực hiện nhiều tác vụ, bao gồm tạo văn bản, dịch thuật và tóm tắt. 

- BERT (Bidirectional Encoder Representations from Transformers) – Được phát triển bởi Google, BERT là một LLM phổbiến khác đã được đào tạo trên một kho dữliệu văn bản khổng lồ. Nó có thểhiểu ngữcảnh của một câu và tạo ra các câu trảlời có ý nghĩa cho các câu hỏi. 

- XLNet – LLM này được phát triển bởi Đại học Carnegie Mellon và Google sửdụng một cách tiếp cận mới đểlập mô hình ngôn ngữđược gọi là “permutation language modeling”. Nó đạt được hiệu suất cao nhất trong các tác vụngôn ngữ, bao gồm tạo ngôn ngữvà trảlời câu hỏi. 

- T5 (Text-to-Text Transfer Transformer) – T5, do Google phát triển, được đào tạo vềnhiều tác vụngôn ngữvà có thểthực hiện chuyển đổi văn bản, như dịch văn bản sang ngôn ngữkhác, tạo bản tóm tắt và trảlời câu hỏi. 

- RoBERTa (Robustly Optimized BERT Pretraining Approach) – Được phát triển bởi Facebook AI Research, RoBERTa là phiên bản BERT cải tiến, hoạt động tốt hơn trên một sốtác vụngôn ngữ. 

## **2.2 Retrieval-Augmented Generation RAG** 

Retrieval-Augmented Generation - RAG [10] là một phương pháp kết hợp giữa truy vấn thông tin (retrieval) và tạo sinh (generation) trong các mô hình ngôn ngữ. Thay vì chỉ dựa vào các thông tin có sẵn trong mô hình, RAG tích hợp quá trình truy vấn từmột cơ sởdữliệu bên ngoài (như một bộdữliệu văn bản) và sửdụng thông tin đó đểhỗtrợ quá trình sinh câu trảlời, giúp cải thiện khảnăng tổng hợp và phản hồi chính xác hơn. 

Retriever (Truy xuất) trong RAG chịu trách nhiệm tìm kiếm và truy xuất các tài liệu có liên quan từmột kho dữliệu lớn (thường là tập hợp các văn bản, tài liệu, hoặc câu hỏi và câu trảlời) dựa trên câu hỏi hoặc bối cảnh đầu vào. Mục tiêu là chọn ra một tập hợp con các tài liệu mà có thểgiúp mô hình trảlời câu hỏi hoặc tạo nội dung chính xác và có liên quan. 

Các kỹthuật phổbiến cho **retriever** bao gồm: 

- **TF-IDF** (Term Frequency-Inverse Document Frequency). 

- **BM25** . 

- **Embedding-based methods** : Sửdụng mạng nơ-ron đểmã hóa tài liệu và câu hỏi thành các vector, sau đó sửdụng khoảng cách giữa các vector đểđánh giá độliên quan. 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

7 

Generator (Tạo ra văn bản) Sau khi tài liệu có liên quan được truy xuất, phần generator sẽsửdụng chúng đểtạo ra văn bản đáp ứng yêu cầu, ví dụnhư câu trả lời cho câu hỏi hoặc một đoạn văn bản mô tả. Các mô hình generator phổbiến hiện nay thường là các mô hình transformer như GPT, BART, hoặc T5. Chúng có khảnăng sinh văn bản tựnhiên và mạch lạc từnhững thông tin có sẵn. 

- Mô hình generator sẽsửdụng thông tin từphần retriever đểbổsung hoặc làm phong 

- phú thêm các câu trảlời, đồng thời đảm bảo rằng văn bản đầu ra là hợp lý và mạch lạc. Lợi ích của RAG: 

   - Cải thiện độchính xác và tính đầy đủcủa câu trảlời: Việc kết hợp thông tin từcơ sởdữliệu ngoài giúp RAG không chỉdựa vào các thông tin được huấn luyện trong mô hình mà còn có thểsửdụng thông tin cập nhật từmôi trường bên ngoài, giúp tăng độchính xác của kết quảsinh ra. 

   - Giảm thiểu khảnăng lan man: Với việc truy vấn các tài liệu liên quan, mô hình RAG có thểgiảm thiểu rủi ro sinh ra thông tin không liên quan hoặc sai lệch. 

   - Ứng dụng trong các nhiệm vụyêu cầu tri thức ngoài mô hình (knowledge-intensive tasks): RAG rất hiệu quảcho các nhiệm vụnhư trảlời câu hỏi, tóm tắt tài liệu, và tìm kiếm thông tin trong các lĩnh vực như y tế, luật, hoặc khoa học. 

## **2.3 Thuật toán Leiden** 

Thuật toán Leiden[11] là một thuật toán được sửdụng đểphát hiện cộng đồng (community detection) trong mạng (graph). Nó cải tiến thuật toán Louvain nổi tiếng bằng cách đảm bảo các cộng đồng kết quảthỏa mãn các thuộc tính mạnh hơn như tính kết nối. 

   - Các bước cơ bản của thuật toán Leiden: 

   - **Bước 1: Tối ưu hóa cục bộtrong thuật toán Leiden** 

- Bước đầu tiên của thuật toán Leiden là tối ưu hóa cục bộcác cộng đồng trong mạng 

- đểtăng giá trịhàm mục tiêu (thường là _modularity_ ). Cụthể, quá trình này tìm cách di chuyển các node giữa các cộng đồng sao cho tổng modularity của mạng được cải thiện. Chi tiết quá trình 

   1. **Khởi tạo** : Mỗi node trong mạng được gán vào một cộng đồng ngẫu nhiên hoặc theo một cách nào đó (ví dụ: theo các đặc trưng sẵn có). 

   2. **Tối ưu hóa modularity** : Mục tiêu là tối ưu hóa modularity (Q), chỉsốthểhiện chất lượng của phân chia cộng đồng. Modulariy đo lường sựphân chia của đồthị thành các cộng đồng so với phân chia ngẫu nhiên. Cộng đồng có modularity cao thì các node trong cùng cộng đồng có nhiều kết nối với nhau hơn là với các node 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

8 


![](output/graph_rag/graph_rag.pdf-0017-02.png)


**Hình 2.1:** Minh họa thuật toán Leiden 

trong cộng đồng khác. 


![](output/graph_rag/graph_rag.pdf-0017-05.png)


Trong đó: 

- _Aij_ : Trọng sốcạnh giữa node _i_ và _j_ , 

- _ki_ : Tổng trọng sốcạnh liên quan đến node _i_ , 

- _m_ : Tổng trọng sốcạnh trong đồthị, 

- _δ_ ( _ci, cj_ ): Bằng 1 nếu _i_ và _j_ thuộc cùng một cộng đồng. 

Mỗi node có thểđược di chuyển giữa các cộng đồng lân cận của nó. Nếu việc di chuyển đó làm tăng giá trịcủa _Q_ , node sẽdi chuyển vào cộng đồng đó. 

3. **Di chuyển các node** : Quá trình này được lặp đi lặp lại cho đến khi không còn node nào có thểdi chuyển mà không làm giảm _Q_ . 

4. **Lặp lại quá trình** : Sau khi hoàn tất quá trình tối ưu hóa cục bộcho tất cảcác node, thuật toán sẽtiếp tục với các bước tiếp theo (phân chia tốt hơn, tạo mạng 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

9 

rút gọn, v.v.), nhưng bước 1 này là trọng tâm trong việc xây dựng cộng đồng ban đầu. 


![](output/graph_rag/graph_rag.pdf-0018-03.png)


**Hình 2.2:** Minh họa quá trình tối ưu hóa cục bộtrong thuật toán Leiden 

## **Bước 2: Phân chia tốt hơn trong thuật toán Leiden** 

Sau khi hoàn tất bước tối ưu hóa cục bộ, thuật toán Leiden thực hiện bước "Phân chia tốt hơn"nhằm đảm bảo rằng các cộng đồng có tính kết nối mạnh mẽhơn. Quá trình này giúp chia nhỏcác cộng đồng không kết nối hoặc không hoàn chỉnh, từđó tạo ra các cộng đồng "tốt hơn"vềmặt cấu trúc và liên kết. 

Chi tiết quá trình 

1. **Kiểm tra tính kết nối của cộng đồng** : Mỗi cộng đồng đã được xác định ởbước 1. Tuy nhiên, các cộng đồng có thểkhông được kết nối hoàn toàn, tức là một cộng đồng có thểchứa nhiều thành phần liên thông rời rạc (tức là các nhóm node trong cộng đồng đó không có đủkết nối với nhau). 

2. **Chia cộng đồng** : Nếu phát hiện một cộng đồng không có tính kết nối mạnh, thuật toán sẽchia nó thành các nhóm con sao cho mỗi nhóm này là một thành phần liên thông. Quá trình chia này không làm giảm chất lượng phân chia cộng đồng, mà giúp các nhóm con có sựliên kết chặt chẽhơn. 

3. **Quá trình tái cấu trúc** : Sau khi phân chia các cộng đồng, thuật toán tiếp tục quá trình tối ưu hóa cục bộ(như đã mô tảởbước 1) trên các cộng đồng mới này, nhằm đảm bảo rằng các cộng đồng nhỏhơn được tối ưu hóa modularity trước khi tiến hành các bước tiếp theo. 

4. **Lặp lại** : Quá trình này có thểđược lặp lại cho đến khi tất cảcác cộng đồng trong mạng đều đạt được tính kết nối tối ưu, và không có cộng đồng nào có thểbịchia nhỏthêm. 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

10 

## **Bước 3: Tạo mạng rút gọn trong thuật toán Leiden** 

Sau khi tối ưu hóa và phân chia cộng đồng, bước tiếp theo trong thuật toán Leiden là **tạo mạng rút gọn** (coarsening the graph). Mạng rút gọn giúp giảm kích thước của đồthịgốc và làm cho quá trình phân tích cộng đồng trởnên hiệu quảhơn. 

- Chi tiết quá trình 

1. **Đại diện cộng đồng là các node** : Mỗi cộng đồng đã được xác định trong các bước trước (tối ưu hóa cục bộvà phân chia tốt hơn) sẽtrởthành một node trong mạng mới. Các node trong cộng đồng được thay thếbằng một điểm duy nhất (node), giúp giảm kích thước của đồthị. 

2. **Kết nối giữa cộng đồng** : Các cộng đồng đã được thay thếbằng các node mới sẽđược kết nối với nhau. Trọng sốcủa các cạnh giữa các cộng đồng sẽđược tính bằng tổng trọng sốcủa tất cảcác cạnh giữa các node trong cộng đồng đó. Công thức tính trọng sốcạnh giữa hai cộng đồng _C_ 1 và _C_ 2 là: 


![](output/graph_rag/graph_rag.pdf-0019-07.png)


Trong đó, _Aij_ là trọng sốcủa cạnh giữa node _i_ và _j_ trong đồthịban đầu. 

3. **Tạo mạng rút gọn** : Sau khi xác định các cộng đồng mới và các kết nối giữa chúng, thuật toán sẽtạo ra một mạng con, trong đó mỗi cộng đồng là một node và các kết nối giữa các cộng đồng là các cạnh. Mạng này có kích thước nhỏhơn và đơn giản hơn so với mạng gốc, giúp giảm độphức tạp tính toán trong các bước tiếp theo. 

4. **Lặp lại quá trình** : Thuật toán tiếp tục tối ưu hóa cộng đồng trên mạng rút gọn này bằng cách áp dụng lại bước tối ưu hóa cục bộ(như trong Bước 1) và phân chia cộng đồng (như trong Bước 2). Quá trình này có thểđược lặp lại nhiều lần cho đến khi không còn cải thiện rõ rệt. 

## **Bước 4. Lặp lại** 

Bước tối ưu hóa và tạo mạng rút gọn được lặp lại cho đến khi không còn sựthay đổi đáng kểtrong cấu trúc cộng đồng. 

## **2.4 Cơ sởdữliệu Neo4j** 

Neo4j[12] là một cơ sởdữliệu đồthịdựa trên lý thuyết đồthị, trong đó dữliệu được lưu trữbằng các đỉnh (nodes) và các cạnh (edges) [13]. Các nút đại diện cho các thực thể(ví dụ: người, sản phẩm, địa điểm), trong khi các cạnh biểu diễn các mối quan hệgiữa các thực thểđó. 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

11 

Neo4j cho phép lưu trữvà truy vấn các mối quan hệphức tạp một cách tựnhiên, khác với các hệthống cơ sởdữliệu quan hệ, vốn gặp khó khăn trong việc biểu diễn các quan hệbậc cao. Điều này làm cho Neo4j đặc biệt phù hợp với các ứng dụng như: hệ thống đềxuất, mạng xã hội, công cụtìm kiếm, và các hệthống phân tích mạng. 

Neo4j lưu trữvà trình bày dữliệu dưới dạng biểu đồ, thay vì dạng bảng hoặc JSON như các hệquản trịcơ sởdữliệu truyền thống. Trong Neo4j, toàn bộdữliệu được biểu diễn bằng các **nút** và các **quan hệ** giữa các nút. Điều này làm cho Neo4j trởnên độc đáo so với các hệthống quản lý cơ sởdữliệu khác [13]. 

**Cơ sởdữliệu đồthị** : 

- Các hệquản trịcơ sởdữliệu quan hệnhư MS Access, SQL Server sửdụng bảng (gồm hàng và cột) đểlưu trữdữliệu. 

- Trong khi đó, Neo4j không sửdụng bảng, hàng hoặc cột mà sửdụng mô hình đồ thị. 

## **Thành phần của cơ sởdữliệu đồthị** : 

- **Nút (Node)** : Đại diện cho các thực thểnhư con người, doanh nghiệp hoặc đối tượng dữliệu. 

- **Cạnh (Edge hoặc Relationship)** : Kết nối giữa các nút, thểhiện các mối quan hệgiữa các thực thể. 

- **Thuộc tính (Property)** : Cung cấp thông tin bổsung vềcác nút và mối quan hệ. 

Cấu trúc này giúp Neo4j mô hình hóa các tình huống thực tếmột cách tựnhiên và trực quan hơn so với cơ sởdữliệu quan hệtruyền thống. 

## **Tính năng nổi bật của Neo4j** : 

- **Hiệu suất cao và khảnăng mởrộng** : Neo4j xửlý tốt khối lượng dữliệu lớn và các truy vấn phức tạp. Công cụlưu trữvà xửlý đồthịgốc đảm bảo hiệu suất cao ngay cảvới hàng tỷnút và mối quan hệ. 

- **Ngôn ngữtruy vấn Cypher** : Cypher là ngôn ngữtruy vấn mạnh mẽvà dễsử dụng, giúp người dùng tạo, đọc, cập nhật và xóa dữliệu dễdàng với cú pháp ngắn gọn, dễhiểu. 

- **Tuân thủACID** : Neo4j đảm bảo tính toàn vẹn và độtin cậy của dữliệu thông qua việc tuân thủcác nguyên tắc ACID (Tính nguyên tử, Tính nhất quán, Tính cô lập và Tính bền vững). 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

12 

- **Sơ đồlinh hoạt** : Cho phép thêm hoặc thay đổi mô hình dữliệu mà không làm gián đoạn hoạt động của hệthống, lý tưởng cho các môi trường kinh doanh thay đổi nhanh chóng. 

**Ưu điểm của Neo4j** : 

- Dễdàng biểu diễn dữliệu kết nối. 

- Truy xuất, duyệt và điều hướng dữliệu kết nối rất nhanh chóng. 

- Sửdụng mô hình dữliệu đơn giản nhưng mạnh mẽ. 

- Hỗtrợbiểu diễn dữliệu bán cấu trúc một cách tựnhiên. 

**Nhược điểm của Neo4j** : 

- Hỗtrợcho OLAP (Online Analytical Processing) chưa được tối ưu tốt. 

- Lĩnh vực cơ sởdữliệu đồthịvẫn đang trong quá trình nghiên cứu và phát triển, nhiều công nghệliên quan còn chưa hoàn thiện. 

## **2.5 Ngôn ngữtruy vấn Cypher** 

Cypher [14] là một ngôn ngữtruy vấn cơ sởdữliệu đồthị, với ngôn ngữnày chúng ta có thểtương tác như là truy vấn, cập nhật hay quản trịmột cách hiệu quảvới cơ sởdữ liệu đồthị[15]. Ngôn ngữnày được thiết kếgiúp cho developer cũng như các chuyên gia có thểthuận tiện khi làm việc với Neo4j. Cypher vốn được thiết kếđơn giản, tuy nhiên nó rất mạnh mẽ. 

Cypher được lấy cảm hứng từrất nhiều các cách tiếp cận khác nhau. Một sốcác từ khóa như `WHERE` , `ORDER BY` được lấy cảm hứng từngôn ngữSQL, trong khi đó pattern matching thì lại được mượn từSPARQL. Ngoài ra, một vài ngữnghĩa được mượn từcác ngôn ngữkhác như Haskell và Python. Cấu trúc của Cypher được xây dựng dựa trên ngôn ngữtiếng Anh với ngữnghĩa thuận tiện cho người thao tác với ngôn ngữ, điều này giúp cho việc viết và đọc các câu truy vấn cũng dễdàng hơn. 

Cypher có cấu trúc tương tựnhư SQL. Các câu truy vấn được xây dựng từnhiều mệnh đềkhác nhau. Các mệnh đềlà chuỗi liên kết với nhau. Dưới đây là một vài ví dụ sửdụng mệnh đềđểđọc dữliệu từcơ sởdữliệu đồthị: 

- **MATCH** : so khớp với các pattern phù hợp. Đây là cách thông dụng nhất đểlấy dữliệu từgraph. 

- **WHERE** : không phải là một mệnh đềchính quy, nhưng nó là một phần của `MATCH` , `OPTIONAL MATCH` và `WITH` . `WHERE` sẽthêm các ràng buộc vào pattern, hoặc sẽlọc các kết quảcó được thông qua `WITH` . 

_CHƯƠNG 2. KIẾN THỨC NỀN TẢNG_ 

13 

- **RETURN** : trảvềkết quả. 

Ví dụ: 

MATCH (p : Person ) − [:FRIEND]−>( friend ) WHERE p . name = ' Alice ' 

RETURN f riend . name 

## **Giải thích:** 

- `MATCH (p:Person)-[:FRIEND]->(friend)` : Tìm tất cảcác nút `friend` có mối quan hệ `FRIEND` đi ra từmột nút `p` mang nhãn `Person` . 

- `WHERE p.name = ’Alice’` : Giới hạn chỉchọn những nút `Person` có thuộc tính `name` bằng `Alice` . 

- `RETURN friend.name` : Trảvềtên của các nút bạn bè ( `friend` ) của `Alice` . 

## **Chương 3** 

## **trình liên Công quan** 

Sau khi tiến hành tìm hiểu và nghiên cứu, tác giảđã tìm được một vài ứng dụng và kỹ thuật có tính ứng dụng và cách hoạt động có thểgiúp ích cho hướng giải quyết vấn đề ban đầu. 

## **3.1 Phân đoạn văn bản dựa trên sựthay đổi chủđề** 

Đểgiải quyết tác vụchia các bài viết dài thành các đoạn ngắn nhưng vẫn phải đảm bảo đầy đủngữnghĩa, đồng thời xác định đoạn văn này có trùng trong cơ sởdữliệu đã có hay không đểđảm bảo việc lưu trữmột bản duy nhất sẽgiúp việc tìm kiếm và trảlời thông tin được hiệu quả, một cách tiếp cận được biểu diễn ởhình bên dưới.[16] 


![](output/graph_rag/graph_rag.pdf-0023-05.png)


**Hình 3.1:** Chiến lược theo dõi sựthay đổi chủđềvăn bản 

Đầu tiên, với một đoạn văn bản dài, phương pháp phân tách đoạn dựa trên sựthay đổi của chủđềđược sửdụng đểchia văn bản thành các phần, các đoạn ngắn (chunk). Sau đó với mỗi đoạn văn thu được, tác giảtiến hành gán nhãn và embed đoạn văn thành vector. Cuối cùng, tác giảthực hiện công tác so sánh các vector vừa thu được với các vector có trong cơ sởdữliệu dựa trên các nhãn tương ứng, và thực hiện lưu văn bản vào cơ sởdữliệu nếu đoạn văn chưa tồn tại (vềmặt ngữnghĩa, nội dung). 

14 

_CHƯƠNG 3. CÔNG TRÌNH LIÊN QUAN_ 

15 

Đểtiến hành phân tách văn bản thành các đoạn văn ngắn dựa trên sựthay đổi chủ để, tác giảsửdụng một cửa sổtrượt (slide window) đểlần lượt trượt qua toàn bộvăn bản. Kích thước của cửa sổtrượt có thểlà 2, 3, 4 ,... câu nhưng thường sẽkhông có kích thước quá lớn. Thông thường, một đoạn văn tốt sẽcó kích thước từ3 đến 10 câu[1] . 

Với mỗi phần văn bản được trượt qua, tác giảsẽtiến hành đánh giá sựkhác nhau giữa chủđềgiữa phần hiện tại và phần trước đó (hoặc các phần trước đó). Nếu chủđề giữa hai phần có sựkhác nhau (vượt ngưỡng chỉđịnh) thì tiến hành tách đoạn tại điểm hiện tại của cửa sổtrượt. Ngược lại, nếu chủđềgiữa hai phần không có sựkhác biệt tương đối, phần văn bản hiện tại ởcửa sổtrượt sẽđược kết hợp với đoạn trước đó đểso sánh với đoạn tiếp theo. 

Giải thuật phân tách đoạn theo chủđềđược thểhiện ởhình bên dưới. 


![](output/graph_rag/graph_rag.pdf-0024-05.png)


**Hình 3.2:** Giải thuật phân tách đoạn theo chủđề 

> 1Paragraphs - Writing Guide `https://www.usu.edu/markdamen/writingguide/15paragr.htm` 

_CHƯƠNG 3. CÔNG TRÌNH LIÊN QUAN_ 

16 

Trong đó: 

- p(n) là phần văn bản thứn được theo dõi bởi cửa sổtrượt. 

- d(i) là phân phối chủđềcủa văn bản thứi. 

Vì đơn vịcủa cửa sổtrượt là câu nên tác giảđã kết hợp với một sốcông cụhỗtrợđể phân tách văn bản thành cách câu trong quá trình xửlý. Một sốcông cụhỗtrợđã được sửdụng như Underthesea Toolkit... 

## **3.2 BERT** 

BERT (Bidirectional Encoder Representations from Transformers)[17] là một mô hình học sâu được phát triển bởi Google và được công bốvào năm 2018. BERT là một phần của họmô hình Transformers, và nó đã tạo ra bước tiến lớn trong lĩnh vực xửlý ngôn ngữtựnhiên (NLP). Đặc điểm chính của BERT: 

- **Bidirectional** : Không giống như các mô hình trước đó chỉxửlý văn bản từtrái sang phải hoặc từphải sang trái, BERT xửlý văn bản theo cảhai chiều. Điều này cho phép BERT nắm bắt được ngữcảnh đầy đủcủa một từdựa trên cảvăn bản trước và sau từđó. 

- **Pre-training và Fine-tuning** : BERT được huấn luyện trước (pre-trained) trên một lượng lớn dữliệu văn bản từWikipedia và BooksCorpus, sau đó có thểđược tinh chỉnh (fine-tuned) cho các nhiệm vụcụthểnhư phân loại văn bản, trảlời câu hỏi, và nhiều nhiệm vụkhác. 

- **Transformers** : BERT dựa trên kiến trúc Transformer, một kiến trúc mạng neural mạnh mẽcho phép mô hình xửlý mối quan hệgiữa các từtrong một câu mà không cần đến sựphụthuộc tuần tựnhư các mô hình Recurrent Neural Network (RNN). 

PhoBERT [18] là một mô hình ngôn ngữdựa trên BERT được phát triển đặc biệt cho tiếng Việt. Giống như BERT, PhoBERT cũng sửdụng kiến trúc Transformer và kỹ thuật học sâu đểnắm bắt ngữcảnh của từtrong câu, nhưng nó được huấn luyện trên một lượng lớn dữliệu tiếng Việt. 

Đặc điểm chính của PhoBERT: 

- **Ngôn ngữđặc thù** : PhoBERT được phát triển riêng cho tiếng Việt, tận dụng các đặc trưng ngữpháp và từvựng của tiếng Việt đểcải thiện hiệu suất cho các tác vụ NLP liên quan đến tiếng Việt. 

_CHƯƠNG 3. CÔNG TRÌNH LIÊN QUAN_ 

17 

- **Corpus huấn luyện** : PhoBERT được huấn luyện trên một lượng lớn dữliệu văn bản tiếng Việt từnhiều nguồn khác nhau như báo chí, sách, và các trang web. Điều này giúp mô hình hiểu rõ hơn vềngữcảnh và ý nghĩa của từtrong tiếng Việt. 

- **Kiến trúc** : PhoBERT sửdụng kiến trúc BERT cơ bản, bao gồm các tầng encoder của Transformer, giúp mô hình học được mối quan hệgiữa các từtrong câu theo cảhai chiều (trái sang phải và phải sang trái). 

## **3.3 Medical Graph RAG** 

Phương pháp dựa trên đồthịtrong mô hình Retrieval-Augmented Generation (RAG) cho lĩnh vực y tế, gọi là **MedGraphRAG** [19]. 

## **3.3.1 Cấu trúc đồthịba tầng** 


![](output/graph_rag/graph_rag.pdf-0026-07.png)


**Hình 3.3:** Graph RAG pipeline 

MedGraphRAG sửdụng một đồthịphân cấp gồm ba tầng đểliên kết các thực thểy tếvới kiến thức cơ bản: 

- **Cấp 1:** Tài liệu người dùng cung cấp (ví dụ: báo cáo y tế). 

- **Cấp 2:** Kiến thức y học nền tảng từsách và bài báo khoa học. 

_CHƯƠNG 3. CÔNG TRÌNH LIÊN QUAN_ 

18 

- **Cấp 3:** Thuật ngữvà quan hệy học chuẩn hóa từhệthống UMLS (Unified Medical Language System). 

**Chiến lược U-retrieve** kết hợp việc truy xuất thông tin theo cách từtrên xuống dưới và tạo câu trảlời từdưới lên trên. Mô hình bắt đầu từtruy vấn của người dùng, phân loại theo các nhãn y tếvà duyệt qua các đồthịđểtìm ra câu trảlời phù hợp. Thông — tin được lấy từcác _meta-graph_ những nút đồthịvà mối quan hệgần nhất với truy — vấn sau đó được tổng hợp thành một câu trảlời chi tiết. 

## **3.3.2 Xây dựng ĐồthịY tế** 

**Phân đoạn tài liệu ngữnghĩa** : Các tài liệu y tếlớn thường chứa nhiều chủđềkhác nhau, cần phân chia tài liệu thành các đoạn nhỏmà vẫn duy trì được ngữcảnh. 

- Kết hợp phương pháp phân đoạn ký tự(tách đoạn theo dấu ngắt dòng) với phân đoạn ngữnghĩa (dựa trên chủđề). 

- Sửdụng kỹthuật _proposition transfer_ đểtrích xuất các phát biểu độc lập và quyết định cách nhóm chúng. 

- Dùng cửa sổtrượt ( _sliding window_ ) đểxửlý 5 đoạn văn một lần, điều chỉnh cho phù hợp với giới hạn ngữcảnh của LLM. 

## **Trích xuất các phần tử(entities): Trích xuất thực thểtừvăn bản đã phân đoạn, gồm tên, loại và mô tả.** 

- Sửdụng LLM đểnhận diện thực thểy tếtrong mỗi đoạn. 

- Gán mỗi thực thểvới một ID duy nhất đểtruy xuất nguồn gốc. 

- Quá trình trích xuất lặp nhiều lần đểđảm bảo đầy đủ. 

## **Liên kết phân cấp (Hierarchy Linking): Duy trì tính chính xác và thuật ngữy học chuẩn hóa.** 

- Xây dựng cấu trúc đồthịba tầng: tài liệu người dùng _→_ kiến thức nền _→_ thuật ngữUMLS. 

- So sánh thực thểvới thuật ngữbằng độtương đồng ngữnghĩa đểliên kết chính xác. 

## **Liên kết quan hệ(Relationship Linking): Xác định các mối quan hệgiữa thực thểtrong đồthị.** 

- Dùng LLM đểxác định quan hệdựa trên tên, mô tả, định nghĩa và kiến thức nền. 

- Biểu diễn quan hệdưới dạng đồthịcó hướng có trọng số( _weighted directed graph_ ), gọi là _meta-graph_ . 

_CHƯƠNG 3. CÔNG TRÌNH LIÊN QUAN_ 

19 

## **3.3.3 Gộp đồthị(Tags Generation and Merge)** 

- Xây dựng _meta-graph_ cho từng phần dữliệu. 

- Dùng LLM tóm tắt các _meta-graph_ theo danh mục y tế(triệu chứng, thuốc men, v.v.). 

- Hợp nhất các _meta-graph_ dựa trên độtương đồng đểtạo thực thểlớn hơn. 

- Quá trình lặp lại tối đa 24 lần đểtránh mất chi tiết. 

## **3.3.4 Truy xuất từđồthị(Retrieve from the Graph)** 

## **Chiến lược U-retrieve:** 

- Sửdụng thẻmô tảtóm tắt đểxác định đồthịphù hợp. 

- Truy xuất thông tin từcác _meta-graph_ liên quan. 

- Tạo phản hồi trung gian dựa trên thực thểliên quan và kiến thức nền. 

- Tổng hợp thêm từcấp cao hơn trong đồthịđểtạo phản hồi cuối cùng, đảm bảo bao quát và chính xác. 

## **3.3.5 Đánh giá phương pháp** 

Các kết quảđánh giá phương pháp MedGraphRAG được trình bày rất chi tiết và bao gồm nhiều khía cạnh khác nhau. 

## **Các chỉsốđánh giá (Metrics)** 

MedGraphRAG được đánh giá bằng các thước đo chính sau: 

- **Faithfulness (Tính trung thực):** Kiểm tra mức độmà câu trảlời của mô hình LLM khớp với thông tin từtài liệu y khoa thực tế. Các công cụđánh giá được sử dụng bao gồm: FactScore, BLEU, ROUGE-L, BERTScore, v.v. 

- **Correctness (Tính đúng đắn):** Được đánh giá bởi chuyên gia y tếhoặc thông qua các tập dữliệu gán nhãn (ví dụ: câu trảlời đúng/sai). 

- **Completeness (Tính đầy đủ):** Đo lường mức độmà câu trảlời bao phủđầy đủ các yếu tốquan trọng trong tài liệu tham khảo. 

_CHƯƠNG 3. CÔNG TRÌNH LIÊN QUAN_ 

20 

## **Bộdữliệu đánh giá** 

Phương pháp được đánh giá trên các tập dữliệu đa dạng, bao gồm: 

- **9 bộQA y tế:** như _PubMedQA_ , _MedMCQA_ , _MedicationQA_ , _HealthSearchQA_ , v.v. 

- **2 bộdữliệu kiểm chứng sựthật:** như _HealthVer_ và _SCI-Fact_ . 

- **1 tập dữliệu tạo văn bản dài:** dùng đểđánh giá khảnăng phản hồi toàn diện của mô hình với các truy vấn y tếphức tạp. 

## **Kết quảnổi bật** 

MedGraphRAG vượt trội hơn GPT-4 + RAG truyền thống ởtất cảcác thước đo. 

Đặc biệt tốt trong các truy vấn dài, phức tạp, nơi cần tổng hợp kiến thức từnhiều phần tài liệu khác nhau. 

Khảnăng truy vết nguồn tài liệu (source-grounding) cao, giúp tăng độtin cậy trong các ứng dụng y tếnhạy cảm. 

## **3.4 Underthesea Toolkit** 

Underthesea[2] là bộdữliệu module Python nguồn mởvà các hướng dẫn hỗtrợnghiên cứu và phát triển vềXửlý ngôn ngữtựnhiên tiếng Việt. Nó cung cấp API cực kỳdễdàng đểnhanh chóng áp dụng các mô hình NLP đã được huấn luyện trước cho văn bản tiếng Việt, chẳng hạn như phân đoạn từ, gắn thẻmột phần giọng nói (PoS), nhận dạng thực thểđược đặt tên (NER), phân loại văn bản và phân tích cú pháp phụthuộc. 

Underthesea được hỗtrợbởi một trong những thư viên học sâu phổbiến nhất, Pytorch, giúp nó dễdàng train các mô hình học sâu và thửnghiệp các phương pháp tiếp cận mới bằng cách sửdụng các Module và Class của Underthesea. 

Underthesea được công bốtheo giấy phép GNU General Public License v3.0. Các quyền của giấy phép này có điều kiện là cung cấp mã nguồn hoàn chỉnh của các tác phẩm được cấp phép và sửa đổi, bao gồm các tác phẩm lớn hơn sửdụng tác phẩm được cấp phép, theo cùng một giấy phép. 

## **3.5 Graphdatascience** 

Thư viện graphdatascience[3] là một công cụPython cho phép tương tác với Neo4j Graph Data Science (GDS). Thư viện này hỗtrợthực hiện các thao tác đồthị, chạy các thuật toán và xây dựng pipeline học máy trong GDS. API của thư viện cung cấp các phép toán 

> 2Underthesea `https://github.com/undertheseanlp/underthesea` 

_CHƯƠNG 3. CÔNG TRÌNH LIÊN QUAN_ 

21 

đồthịmạnh mẽvà dễsửdụng, giúp người dùng dễdàng làm việc với dữliệu đồthịphức tạp trong môi trường Neo4j. 

## **3.6 Langchain** 

LangChain[4] là một thư viện mã nguồn mởđược phát triển bằng Python và JavaScript, giúp xây dựng các ứng dụng sửdụng mô hình ngôn ngữlớn (LLM) như GPT-4, GPT-3.5, và các mô hình khác. Thư viện này cung cấp các công cụđểkết nối mô hình ngôn ngữ với dữliệu bên ngoài, cho phép tạo ra các ứng dụng thông minh và có khảnăng xửlý ngữcảnh phức tạp. 

Với LangChain, các nhà phát triển có thểđiều chỉnh linh hoạt mô hình ngôn ngữcho các bối cảnh kinh doanh cụthểbằng cách chỉđịnh các bước cần thiết đểtạo ra kết quả mong muốn. 

Chuỗi là nguyên tắc cơ bản chứa nhiều thành phần AI khác nhau trong LangChain đểđưa ra câu trảlời nhận biết ngữcảnh. Chuỗi là một loạt các hành động tựđộng từ truy vấn của người dùng đến đầu ra của mô hình. Ví dụ: các nhà phát triển có thểsử dụng chuỗi để: 

- Kết nối với các nguồn dữliệu khác nhau. 

- Tạo nội dung độc đáo. 

- Dịch nhiều ngôn ngữ. 

- Trảlời các truy vấn của người dùng. 

Chuỗi được hình thành từcác liên kết. Mỗi hành động được các nhà phát triển xâu chuỗi lại với nhau đểtạo thành chuỗi được kết nối gọi là một liên kết. Với các liên kết, nhà phát triển có thểchia các tác vụphức tạp thành nhiều tác vụnhỏhơn. Ví dụvềcác liên kết bao gồm: 

- Định dạng đầu vào của người dùng. 

- Gửi truy vấn đến LLM. 

- Truy xuất dữliệu từkho lưu trữđám mây. 

- Dịch từngôn ngữnày sang ngôn ngữkhác. 

Trong khung LangChain, một liên kết chấp nhận đầu vào từngười dùng và chuyển đầu vào đó đến các thư viện LangChain đểxửlý. LangChain cũng cho phép sắp xếp lại liên kết đểtạo các quy trình làm việc AI khác nhau. 

> 3graphdatascience `https://pypi.org/project/graphdatascience/` 

> 4Langchain `https://www.langchain.com/` 

## **Chương 4** 

## **đềxuất Phương pháp** 

Trong chương này, tác giảsẽtrình hướng giải quyết bày bài toán ban đầu, đồng thời giới thiệu các thách thức và vấn đềcần giải quyết, cũng như các giải pháp được đềxuất để đạt được mục tiêu đềra. 

## **4.1 vềkiến trúc Tổng quan** 

Các kỹthuật RAG đã cho thấy triển vọng trong việc giúp các LLM lý luận vềcác tập dữliệu riêng tư - dữliệu mà LLM không được đào tạo và chưa bao giờthấy trước đó, chẳng hạn như nghiên cứu độc quyền, tài liệu kinh doanh hoặc giao tiếp của một doanh nghiệp. Baseline RAG được tạo ra đểgiúp giải quyết vấn đềnày, nhưng khi triển khai sẽcó những tình huống mà Baseline RAG hoạt động rất kém. Ví dụBaseline RAG gặp khó khăn khi nối kết các điểm thông tin. Điều này xảy ra khi trảlời một câu hỏi đòi hỏi phải đi qua các mảnh thông tin khác nhau, đôi khi thông tin sẽkhá rắc rối, sau đó được tổng hợp lại. Và đôi khi do sựphức tạp hoặc dư thừa từdữliệu đưa vào mà LLM trảlời sai. 

Đểgiải vấn đềnày, Graph RAG[20] ra đời, thay vì lưu trữcác chunk text và embedding của nó đểtìm kiếm, thì Graph RAG biểu diễn và lưu trữdưới dạng đồthị, cùng các kỹ thuật nâng cao vềgom nhóm, tìm kiếm đểđưa ra câu trảlời tối ưu nhất, khắc phục được nhược điểm nêu trên[21]. Và đểáp dụng Graph RAG vào tập dữliệu giáo dục, tác giảđề xuất một cách tiếp cận được biểu diễn ởhình bên dưới, gọi là **hgRAG** . 

22 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

23 


![](output/graph_rag/graph_rag.pdf-0032-02.png)


**Hình 4.1:** hgRAG pipeline 

Cách hoạt động của hgRAG: 

- Bước 1: Xây dựng biểu đồtri thức từvăn bản (dựa trên các thực thểvà mối quan hệgiữa chúng). 

- Bước 2: Dùng các thuật toán phát hiện cộng đồng đểchia biểu đồnày thành các nhóm nhỏ. 

- Bước 3: Mỗi nhóm sẽđược tóm tắt thành các câu trảlời cục bộ. 

- Bước 4: Các bản tóm tắt cục bộnày sẽđược kết hợp lại thành một câu trảlời tổng quan cho câu hỏi toàn cục. 

## **4.2 Graph RAG Approach & Pipeline** 

## **4.2.1 Phân đoạn văn bản (Document chunking)** 

Bước quan trọng đầu tiên trong quy trình xây dựng đồthịtri thức và trảlời câu hỏi trong phương pháp Graph RAG là tách các tài liệu nguồn (source documents) thành các đoạn văn bản nhỏhơn (text chunks) đểdễdàng xửlý và phân tích trong các bước tiếp theo. 

Phương pháp được sửdụng đểtách các văn bản thành các đoạn ngắn được sửdụng là dựa trên sựthay đổi chủđềđược trình bày ởmục 3.1. 

Các đoạn văn bản sau khi tách được lưu theo từng loại chủđềriêng biệt và hầu như không có sựtrùng lặp đểtăng hiệu suất xửlý ởcác bước tiếp theo. 

## **4.2.2 Trích xuất thực thể(Entity Extraction)** 

Sau khi thực hiện quá trình phân đoạn, tác giảsẽtiến hành xác định và trích xuất các thực thể(entities) và mối quan hệ(relationships) từmỗi đoạn văn bản (text chunk). Quy trình thực hiện: 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

24 

## 1. **Trích xuất thực thể** : 

   - **Thực thể** : Là các đối tượng quan trọng được nhắc đến trong văn bản (ví dụ: người, địa điểm, tổchức, hoặc các khái niệm). 

   - Các thông tin vềthực thểbao gồm: 

      - **Tên thực thể** ( _name_ ): Ví dụ, “Albert Einstein”. 

      - **Loại thực thể** ( _type_ ): Ví dụ, “nhà khoa học” hoặc “địa điểm”. 

      - **Mô tảthực thể** ( _description_ ): Ví dụ, “nhà vật lý lý thuyết nổi tiếng với thuyết tương đối”. 

2. **Trích xuất mối quan hệ** : 

   - Sau khi xác định được các thực thể, tác giảsẽtìm các mối quan hệgiữa chúng, ví dụ: 

      - **Nguồn** ( _source_ ): Thực thểbắt đầu mối quan hệ. 

      - **Đích** ( _target_ ): Thực thểkết thúc mối quan hệ. 

      - **Mô tảmối quan hệ** ( _description_ ): Ví dụ, “là giáo viên của”, “được phát minh bởi”. 

3. **Trích xuất thông tin bổsung (covariates)** : 

   - Ngoài thực thểvà mối quan hệ, có thểtrích xuất thêm các thuộc tính bổsung, bao gồm: 

      - **Chủthể** ( _subject_ ), **đối tượng** ( _object_ ). 

      - **Loại thông tin** ( _type_ ), **mô tả** ( _description_ ). 

      - **Nguồn gốc thông tin** ( _source text span_ ). 

      - **Thời gian bắt đầu và kết thúc** ( _start/end dates_ ). 

      - **Embeddings** . 

## **4.2.3 Liên kết thực thể(Relationship linking)** 

Liên kết thực thểlà quá trình rút trích và xây dựng các mệnh đềquan hệ(relation) từ các thực thể, sựmối quan hệvà các thông tin liên quan từbước đểtạo thành một bộba (triplet). 

Ví dụcho một câu văn như sau: 

- _"Chương trình đào tạo thạc sĩ công nhận chứng chỉbồi dưỡng sau đại học (Chứng chỉ_ 

- _có hiệu lực 3 năm kểtừngày cấp)."_ 

Từcâu trên, tiến hành các bước đã trình bày, ta thu được: 

- Entities: Chương trình đào tạo thạc sĩ, Chứng chỉbồi dưỡng sau đai học. 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

25 

- Relations: Công nhận. 

- Thông tin bổsung: Chứng chỉcó hiệu lực 3 năm kểtừngày cấp. 

Kết quảquá trình này sẽtạo ra một chuỗi json biểu diễn cho triple (Sinh viên, có, GPA dưới 2.0) có dạng như sau: 

```
{
"start":{
"identity":127,
"labels":["__Entity__","Concept"],
"properties":{
"wcc":101,
"description":"Chứngchỉcóthờihạnhiệulực3nămkểtừngày
cấp.",
"id":"ChứngChỉBồiDưỡngSauĐạiHọc",
"embedding":[-0.002568683587014675,...],
"communities":[101,29,34]
},
"elementId":"4:0b05b9d5-53ab-4890-a95a-b1d9099fa44f:127"
},
"relationship":{
"identity":1153045749420785791,
"start":127,
"end":20,
"type":"CÔNG_NHẬN",
"properties":{
"description":"Chứngchỉđượccôngnhậnchomônhọctương
ứngthuộcchươngtrìnhđàotạothạcsĩ."
},
"elementId":"5:0b05b9d5-53ab-4890-a95a-b1d9099fa44f:1153045749420785791",
"startNodeElementId":"4:0b05b9d5-53ab-4890-a95a-b1d9099fa44f:127",
"endNodeElementId":"4:0b05b9d5-53ab-4890-a95a-b1d9099fa44f:20"
},
"end":{
"identity":20,
"labels":["__Entity__","Concept","Program"],
"properties":{
"wcc":0,
"description":"Chươngtrìnhđàotạothạcsĩcókhốilượng60
```

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

26 

```
tínchỉ.",
```

```
"id":"ChươngTrìnhĐàoTạoThạcSĩ",
"embedding":[-0.019571976736187935,...],
"communities":101,29,34]
```

```
},
```

```
"elementId":"4:0b05b9d5-53ab-4890-a95a-b1d9099fa44f:20"
}
```

```
}
```

Trong đó: 

- start: Thực thểbắt đầu với các thông tin như labels (loại thực thể), description (mô tả), elementId (định danh thực thể)... 

- end: Thực thểkết thúc. 

- relationship: Quan hệ. 

## **4.2.4 Lưu trữdữliệu quan hệ** 

Ởbước 4.2.3, tác giảđã thu được các bộba biễu diễn dữliệu mệnh đềquan hệdưới dạng các chuỗi json. Dữliệu từcác mệnh đềquan hệnêu trên là cơ sởđểxây dựng các đồthị tri thức (Knowledge Graph). 

Đểlưu các đồthịtri thức siêu quan hệ(hyper-relational knowledge graphs) vào chuẩn cơ sởdữliệu Neo4j, với mỗi node là một entity, và các cạnh là các quan hệtương ứng. Tuy nhiên, đểquản lý và truy vấn, cần xửlý hiệu quảcác dữliệu trên. 

De-duplication: Đảm bảo rằng mỗi thực thểđược biểu diễn duy nhất và chính xác, ngăn ngừa trùng lặp và hợp nhất các bản ghi tham chiếu đến cùng một thực thểtrong thếgiới thực. Duy trì tính toàn vẹn và nhất quán của dữliệu trong biểu đồ. Nếu không De-duplication, biểu đồtri thức sẽbịphân mảnh và dữliệu không nhất quán, dẫn đến lỗi và thông tin chi tiết không đáng tin cậy. 


![](output/graph_rag/graph_rag.pdf-0035-15.png)


**Hình 4.2:** De-duplication 

Quy trình loại bỏtrùng lặp: 

1. **Embedding Entity** — Bắt đầu với tất cảcác thực thểtrong biểu đồ, thêm thuộc tính embedding chứa thông tin vector của các thực thể. 

- 

- 2. **kNN** Xây dựng đồthịkNN, kết nối các thực thểtương tựdựa trên _embedding_ . 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

27 

- 

- 3. **Thành phần liên thông yếu (Weak Connected Component)** Xác định các thành phần kết nối yếu trong đồthịkNN, nhóm các thực thểcó khảnăng tương tựnhau. Thêm bước lọc khoảng cách sau khi các thành phần này đã được xác định. 

- 

- 4. **Đánh giá bằng LLM** Sửdụng LLM đểđánh giá các thành phần này và quyết định xem các thực thểtrong mỗi thành phần có nên được sáp nhập hay không, từ đó đưa ra quyết định cuối cùng vềviệc giải quyết thực thể. 

Sau khi xây dựng hệthống lưu trữ, việc truy vấn và biểu diễn các đồthịtri thức ( _knowledge graph_ ) sẽđược quan tâm tiếp theo. Ngôn ngữtruy vấn Cypher được sửdụng đểtruy xuất thông tin trên các đồthịnày. 

**Ví dụ:** Truy vấn tất cảcác node có nhãn `Organization` và giới hạn kết quảở25 node đầu tiên: 

```
MATCH(n:Organization)RETURNnLIMIT25
```


![](output/graph_rag/graph_rag.pdf-0036-07.png)


**Hình 4.3:** Cơ sởdữliệu đồthị 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

28 

## **4.2.5 Xây dựng đồthịcộng đồng (Graph Communities)** 

Community detection (phát hiện cộng đồng) là quá trình phân tách hoặc phân cụm các đỉnh trong một mạng hoặc đồthịthành các nhóm hoặc cộng đồng dựa trên mối liên kết mạng giữa chúng. Mục tiêu của community detection là tìm hiểu cấu trúc tổchức và mối quan hệtrong mạng, tìm ra các nhóm tương đồng hoặc có chức năng tương tự. Các cộng đồng trong một mạng có thểđược xác định dựa trên nhiều tiêu chí khác nhau, bao gồm mối quan hệtương đồng, gần gũi, hay tương tác giữa các thành viên trong cộng đồng. 

Tác giảsửdụng thuật toán phát hiện cộng đồng (community detection) đểnhóm các thực thểvà mối quan hệliên quan thành các cộng đồng, dựa trên độkết nối mạnh giữa chúng. 

- Nghiên cứu sẽsửdụng thuật toán Leiden. cùng với Graphdatascience là công cụđược 

- sửdụng đểhỗtrợhiện thực thuật toán. 

- Thuật toán Leiden cho phép phân chia đồthịthành nhiều cấp độcộng đồng, từcấp 

- thấp (chi tiết) đến cấp cao (bao quát). 

Cộng đồng cấp thấp (Leaf-level communities): Đây là các cộng đồng ban đầu, thường chứa các nhóm nút liên kết mạnh với nhau. 

Cộng đồng cấp cao (Higher-level communities): Sau khi các cộng đồng cấp thấp được hợp nhất, thuật toán sẽtạo ra các cộng đồng lớn hơn, với các node tương ứng là các cộng đồng cấp thấp đã được hợp nhất. 


![](output/graph_rag/graph_rag.pdf-0037-09.png)


**Hình 4.4:** Minh họa một cộng đồng được xây dựng dựa trên thuật toán Leiden 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

29 

## **4.2.6 Tóm tắt cộng đồng (Communities Summaries)** 

Mục đích của bước này nhằm tạo các tóm tắt chi tiết cho từng cộng đồng, cung cấp cái nhìn toàn diện vềtừng phần của dữliệu và đảm bảo rằng các tóm tắt này có thểđược sửdụng đểtrảlời câu hỏi hoặc làm cơ sởcho các phân tích toàn cục. Quy trình thực hiện: 

- Cộng đồng cấp thấp nhất (leaf-level communities): Đối với các cộng đồng ởcấp thấp nhất (chi tiết nhất), tất cảcác thực thể, mối quan hệ, và thuộc tính liên quan được đưa vào một cửa sổngữcảnh cho LLM, sau đó tiến hành tạo ra một bản tóm tắt cô đọng dựa trên các thông tin này. 

- Cộng đồng cấp cao hơn (higher-level communities): Đối với các cộng đồng lớn hơn, tóm tắt của các cộng đồng con được sửdụng thay vì thông tin chi tiết từng thực thể, đểđảm bảo không vượt quá giới hạn token. 

Khi tổng hợp thông tin, các thực thểvà mối quan hệcó mức độquan trọng cao (ví dụ: sốlượng liên kết lớn) sẽđược ưu tiên. Thông tin được thêm vào tóm tắt theo thứtự ưu tiên cho đến khi đạt giới hạn token của mô hình. 

## **4.2.7 Truy vấn dữliệu** 

Việc truy vấn dữliệu trong Graph RAG bao gồm 2 phần: truy vấn toàn cục và truy vấn cục bộ. 

## **Truy vấn toàn cục** 

- Sửdụng với các câu hỏi mang tính toàn diện, tổng quan vềdữliệu, những câu hỏi mang tính khái quát chung mà RAG truyền thống có khảnăng thất bại cao. 

- Công việc truy vấn sẽdựa trên các Communities Summaries đã được xây dựng trước đó: 

   - Truy vấn ra các bản tóm tắt (Community Summaries) có liên quan nhất đến câu hỏi ban đầu. 

   - Các Communities Summaries được chia thành các đoạn nhỏhơn (chunks) với kích thước cốđịnh phù hợp với giới hạn ngữcảnh (context window) của mô hình LLM. 

   - Các đoạn được xáo trộn ngẫu nhiên đểphân tán thông tin, tránh việc tất cả thông tin liên quan bịcô lập trong một đoạn mà có thểbịbỏsót khi xửlý. 

   - Dùng LLM đểsinh câu trảlời cho từng chunk và tiến hành đánh giá. 

   - Các câu trảlời được đánh giá tốt sẽđược đưa vào LLM đểsinh ra các phản hồi cho đến khi đạt giới hạn token. 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

30 


![](output/graph_rag/graph_rag.pdf-0039-02.png)


**Hình 4.5:** Minh họa luồng truy vấn toàn cục 

## **Truy vấn cục bộ** 

- Phù hợp với các câu hỏi sâu vềmột chủđềnào đó, phù hợp đểsuy luận sâu hơn vềcác thực thểvà các mối quan hệ. 

   - Xác định một tập các thực thểtừcác knowledge graph có liên quan từtruy vấn ban đầu. Các thực thểnày là các node trong graph, cho phép truy xuất thêm các thông tin liên quan đểtạo thành câu trảlời như các mối quan hệ, các thực thểđược liên kết, các thông tin bổsung. 

   - Ngoài ra, có thểtrích xuất các đoạn văn bản được liên kết với các thực thể (nếu có) đểlàm giàu cho câu trảlời. 

   - Các kết quảtừcác truy vấn này sẽđược sửdụng phù hợp với LLM đểsinh ra câu trảlời cuối cùng. 


![](output/graph_rag/graph_rag.pdf-0039-09.png)


**Hình 4.6:** Luồng truy vấn cục bộ 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

31 

## **4.3 Kết quảhiện thực** 

## **4.3.1 Dữliệu thực nghiệm** 

Nguồn dữliệu đầu vào cho pipeline Graph RAG là các văn bản giáo dục được lấy từkho dữliệu, từcác website chính thống của trường Đại học Bách Khoa Thành phốHồChí Minh. Ởđây, 25 văn bản, với nội dung chủyếu liên quan đến các quy chếvà quy định được sửdụng. 

Một tập dataset gồm 3000 câu hỏi và câu trảlời tương ứng với các văn bản ởtrên cũng được xây dựng nhằm phục vụcông việc đánh giá kết quả. 

## **4.3.2 Phương pháp đánh giá** 

BERTScore [22] là một phương pháp đánh giá độgiống nhau ngữnghĩa giữa hai đoạn văn bản, dựa trên các vector embedding sinh ra bởi các mô hình ngôn ngữnhư BERT, RoBERTa, v.v. 

Khác với các chỉsốtruyền thống như BLEU, ROUGE (so sánh theo từhoặc n-gram), BERTScore so sánh **ý nghĩa** của các từ, thay vì chỉdựa trên hình thức. 

## **Quy trình tính BERTScore:** 

Giảsử: 

- **Candidate** : Câu trảlời từmô hình (Prediction). 

- **Reference** : Đáp án chuẩn (Ground Truth). 

Các bước tính toán: 

1. **Tokenize** : Candidate và Reference được token hóa thành các từ/token nhỏ. Ví dụ: 

   - Candidate tokens: [sinh, viên, cần, 135, tín, chỉ] 

   - Reference tokens: [sinh, viên, phải, hoàn, thành, 135, tín, chỉ] 

2. **Embedding** : Mỗi token được ánh xạthành một vector embedding bằng mô hình ngôn ngữnhư BERT. Vector thểhiện ý nghĩa ngữcảnh của token. 

3. **Tính toán độtương đồng** : Với mỗi token trong Candidate, tìm token trong Reference có độtương đồng cosine cao nhất. Ngược lại, cũng thực hiện từReference đến Candidate. 

4. **Tính Precision, Recall và F1** : 

_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

32 

- **Precision** : Trung bình độtương đồng cao nhất của mỗi token trong Candidate so với Reference, có giá trịtrong khoảng [0;1]. 

- **Recall** : Trung bình độtương đồng cao nhất của mỗi token trong Reference so với Candidate, có giá trịtrong khoảng [0;1]. 

- **F1** : Trung bình điều hòa giữa Precision và Recall, có giá trịtrong khoảng [0;1]. 

## **Công thức toán học:** 

Gọi: 

- _C_ là tập token trong Candidate, 

- _R_ là tập token trong Reference, 

ta có: 


![](output/graph_rag/graph_rag.pdf-0041-10.png)


## **Ưu điểm của BERTScore:** 

- Hiểu ý nghĩa ngữcảnh: Không yêu cầu phải khớp chính xác từngữ. 

- Ngôn ngữđộc lập: Áp dụng tốt cho nhiều ngôn ngữkhác nhau. 

- Phát hiện tốt lỗi nội dung: Phát hiện lỗi thêm hoặc thiếu ý. 

## **4.3.3 Kết quả** 

Khi chạy thực nghiệm trên tập dữliệu quan đầu, kết quảchỉsốF1 thu được là 0.776. Nếu một mô hình có F1 Score cao, nó có nghĩa là nó đang đưa ra nhiều dựđoán chính xác và có độphủtốt. 

**Bảng 4.1:** Bảng kết quảđánh giá BERTscore 

|**Phương pháp**|**Precision**|**Recall**|**F1**|
|---|---|---|---|
|Graph RAG|0.819|0.739|0.776|
|RAG|0.813|0.702|0.753|
|GPT-4o|0.698|0.570|0.628|



_CHƯƠNG 4. PHƯƠNG PHÁP ĐỀXUẤT_ 

33 

- Với mô hình Gpt-4o, không được train trên tập dữliệu thực nghiệp, các câu trảlời chủyếu được _"bịa"_ ra, do đó chỉsốF1 chỉlà 0.628, độtin cậy thấp. 

- Khi sửdụng RAG và Graph RAG trên tập dữliệu ban đầu, kết quảthu được có độtin cậy cao hơn, và Graph RAG đạt kết quảcao nhất. 

## **Chương 5** 

## **Kết luận** 

Nội dung chương này sẽkhái quát lại những điều đã làm được, nhận xét và định hướng tương lai. 

## **5.1 Nhận xét** 

Bài báo cáo Luận văn Thạc sĩ này đã trình bày vềcác mô hình, các công trình nghiên cứu liên quan đểđềxuất một phương pháp cho phép triển khai pipeline Graph RAG - hgRAG trong lĩnh vực giáo dục đểgiải quyết các khó khăn khi nối kết các điểm thông tin, các tác vụtóm tắt, khái quát hóa và đem lại cái nhìn tổng quan vềdữliệu, đồng thời cũng đã tiến hành triển khai và đánh giá kết quảtheo phương pháp được đềxuất. Các kết quảban đầu thu được mang hướng tích cực, pipeline đềxuất đem lại khảnăng cải thiện chất lượng câu trảlời dựa trên cái knowledge graph, đem lại hiệu quảtốt hơn so với RAG trong nhiều trường hợp. 

Tuy nhiên, trong quá trình nghiên cứu vẫn còn gặp nhiều thách thức cần được giải quyết trong thời gian tới: 

- Tốn nhiều không gian lưu trữhơn so với RAG. 

- Việc triển khai phức tạp. Thay vì chỉcần lưu trữcác chunk text và embedding của chúng như trong RAG truyền thống, hgRAG cần thực hiện nhiều công đoạn, lưu trữdữliệu dưới dạng knowledge graph và embedding. Ngoài ra, liên kết thực thể là một bước vô cùng quan trọng trong pipeline Graph RAG. Tuy nhiên, việc xửlý dữliệu đểthu được các bộba (triples) còn gặp nhiều khó khăn. Các mô hình như Transformer hay phoBERT được sửdụng đểhỗtrợquá trình này, tuy nhiên, các kết quảthu được tính đến thời điểm hiện tại chưa thực sựtốt. Do đó, các công việc trong giai đoạn này thương phải được xửlý nhiều lần. 

- Kết quảtrảlời tùy thuộc vào lượng thông tin trích xuất được từquá trình truy vấn dữliệu. Do đó, trong một sốtrường hợp, database chứa các knowledge graph 

34 

_CHƯƠNG 5. KẾT LUẬN_ 

35 

không mang đủthông tin cần thiết, cần tiến hành bổsung dữliệu vào database để làm giàu cho ngữcảnh của câu trảlời. 

- Phương pháp đã giải quyết các vấn đềliên quan đến tóm tắt thông tin, khái quát vềdữliệu so với baseline RAG, tuy nhiên, tốc độtruy vấn cho các trường hợp này cũng là một vấn đềcần được quan tâm. 

## **5.2 Hướng phát triển trong tương lai** 

Mặc dù đã đạt được những kết quảkhảquan, pipeline Graph RAG vẫn có thểđược cải thiện và phát triền thêm đểnâng cao hiệu suất. Dưới đây là một sốhướng phát triển tiềm năng: 

- Cải thiện khảnăng của module trích xuất thực thể, mối quan hệ. 

- Xây dựng cấu trúc dữliệu liên kết vào tập dữliệu chuẩn cho các từngữchuyên ngành, từngữhọc thuật... 

- Tạo một pipeline Graph RAG cho dữliệu có cấu trúc [23]. 

Bằng cách tập trung vào những hướng phát triển này, nghiên cứu có thểđược mở rộng và hoàn thiện hơn. Nghiên cứu này đã khẳng định tiềm năng to lớn của Graph RAG vào việc truy vấn thông tin từcác nguồn bên ngoài nhằm cải thiện hiệu quả, độchính xác của các hệthống Q&A, hứa hẹn sẽmởra thêm những hướng đi mới cho lĩnh vực xử lý ngôn ngữtựnhiên. 

## **Danh sách tham khảo** 

- [1] Y. Bengio, R. Ducharme, P. Vincent, and C. Jauvin, “A neural probabilistic language model,” _Journal of machine learning research_ , vol. 3, pp. 1137–1155, 2003. 

- [2] T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, and J. Dean, “Distributed representations of words and phrases and their compositionality,” _Advances in neural information processing systems_ , vol. 26, pp. 3111–3119, 2013. 

- [3] I. Goodfellow, Y. Bengio, and A. Courville, _Deep learning_ . MIT press, 2016. 

- [4] Y. LeCun, Y. Bengio, and G. Hinton, “Deep learning,” _Nature_ , vol. 521, no. 7553, pp. 436–444, 2015. 

- [5] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” _Neural computation_ , vol. 9, no. 8, pp. 1735–1780, 1997. 

- [6] K. Cho, B. van Merrienboer, C. Gulcehre, D. Bahdanau, F. Bougares, H. Schwenk, and Y. Bengio, “Learning phrase representations using rnn encoder-decoder for statistical machine translation,” _arXiv preprint arXiv:1406.1078_ , 2014. 

- [7] D. Bahdanau, K. Cho, and Y. Bengio, “Neural machine translation by jointly learning to align and translate,” _arXiv preprint arXiv:1409.0473_ , 2014. 

- [8] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Kaiser, and I. Polosukhin, “Attention is all you need,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [9] Z. Lin, Y. Deng, J. Kuo, R. Zhang, and H. Liu, “Structured attention networks,” _arXiv preprint arXiv:1702.00887_ , 2017. 

- [10] M. Lewis, Y. Liu, N. Goyal, S. Ruder, D. Gromann, S. K. Moosavi, N. Bassil, Y. Jernite, , _et al._ , “Retrieval-augmented generation for knowledge-intensive nlp tasks,” _Proceedings of NeurIPS 2020_ , 2020. 

- [11] V. Traag, L. Waltman, and N. J. van Eck, “From louvain to leiden: Guaranteeing well-connected communities,” _arXiv preprint arXiv:1810.08473_ , 2018. 

36 

_DANH SÁCH THAM KHẢO_ 

37 

- [12] Neo4j, “What’s neo4j?.” `https://neo4j.com/docs/getting-started/ whats-neo4j/` , n.d. Truy cập lần cuối: tháng 4, 2025. 

- [13] GeeksforGeeks, “Neo4j introduction.” `https://www.geeksforgeeks.org/ neo4j-introduction/` , n.d. Truy cập lần cuối: tháng 4, 2025. 

- [14] Neo4j, “Cypher query language manual.” `https://neo4j.com/docs/ cypher-manual/current/introduction/` , n.d. Truy cập lần cuối: tháng 4, 2025. 

- [15] Viblo, “Tìm hiểu vềngôn ngữtruy vấn cypher.” `https://viblo.asia/p/ tim-hieu-ve-ngon-ngu-truy-van-cypher-gDVK2BmAKLj` , n.d. Truy cập lần cuối: tháng 4, 2025. 

- [16] L. N. Khang, “Bài toán xác định nội dung trùng lặp,” June 2024. Accessed: 202412-11. 

- [17] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” _In: Google AI Language_ , p. 1. 

- [18] N. Q. Dat and N. T. Anh, “Phobert: Pre-trained language models for vietnamese,” _In: Findings of the Association for Computational Linguistics: EMNLP 2020_ , p. 1037–1042, 2020. 

- [19] J. Wu, J. Zhu, Y. Qi, J. Chen, M. Xu, F. Menolascina, and V. Grau, “Medical graph rag: Towards safe medical large language model via graph retrieval-augmented generation,” _arXiv preprint arXiv:2408.04187_ , 2024. Version 2, revised on 15 Oct 2024. 

- [20] N. C. J. B. A. C. A. M. S. T. J. L. Darren Edge, Ha Trinh, “From local to global: A graph rag approach to query-focused summarization,” _arXiv preprint arXiv:2404.16130_ , 2023. 

- [21] J. Wu, J. Zhu, and Y. Qi, “Medical graph rag: Towards safe medical large language model via graph retrieval-augmented generation.” `https://arxiv.org/abs/2408. 04187` , 2024. Truy cập lần cuối: tháng 4, 2025. 

- [22] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi, “Bertscore: Evaluating text generation with bert,” _arXiv preprint arXiv:1904.09675_ , 2019. Version 3, revised on 24 Feb 2020. 

- [23] J. Zou, D. Fu, S. Chen, X. He, Z. Li, Y. Zhu, J. Han, and J. He, “Gtr: Graph-table-rag for cross-table question answering,” _arXiv preprint arXiv:2504.01346_ , 2025. Version 2, revised on 3 Apr 2025. 

