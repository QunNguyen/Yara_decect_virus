# malware-detection



## Getting started
Đây là dự án của nhóm gồm nhiều thành viên khi tham khảo vui lòng tôn trọng quyền tác giả !!!
Tôi - Nguyễn Văn Quân là người chịu trách nhiệm triển khai yara, phân tích mã, xây dựng rule cho mã độc.

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/anhnp.ptit/malware-detection.git
git branch -M main
git push -uf origin main
```

## Introduction
Yara là một công cụ phân tích mã độc, cho phép tạo ra các quy tắc mô tả các mẫu hoặc mô hình của mã độc dựa trên các đặc điểm như chuỗi ký tự, giá trị hex, biểu thức chính quy, …
Sandbox là một kỹ thuật quan trọng trong lĩnh vực bảo mật có tác dụng cô lập các ứng dụng, ngăn chặn các phần mềm độc hại để chúng không thể làm hỏng hệ thống máy tính, hay cài các mã độc nhằm ăn cắp thông tin cá nhân hoặc tổ chức.
Malware (Malicious Software) là một thuật ngữ dùng để chỉ các phần mềm hoặc chương trình có mục đích gây hại hoặc gây rối đến hệ thống máy tính, mạng hoặc thiết bị điện tử khác. Malware có thể được thiết kế để thực hiện các hoạt động không mong muốn, như đánh cắp thông tin cá nhân, tấn công mạng, kiếm soát từ xa thiết bị, tạo spam, hoặc gây hỏng hóc hệ thống.
## Note
Dự án dùng yara để phân tích, rà quét file hoặc folder bất kì mà người dùng nghi ngờ chứa mã độc.
Dự án dùng python để xây dựng UI và yara để rà quét file. Khi rà quét file có thể phát hiện và không phát hiện do bộ test còn hạn chế và sự phát triển của mã độc liên tục sinh ra mã mới. Do đó chúng tôi tích hợp file sandbox là kĩ thuật cô lập rà quét mã độc một cách độc lập, ảo hóa chạy mẫu mã độc tránh gây hư hại trực tiếp tới hệ thống máy tính.
