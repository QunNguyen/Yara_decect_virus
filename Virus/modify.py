target_file = 'victim.conf'
import re

new_username = "new_username"
new_password = "new_password"

# Mở file và đọc tất cả các dòng vào list
with open(target_file, "r") as f:
    lines = f.readlines()

# Dùng regex để tìm và sửa giá trị username
pattern1 = r"(username\s*=\s*)(\S+)"
pattern2 = r"(password\s*=\s*)(\S+)"
for i, line in enumerate(lines):
    match1 = re.search(pattern1, line)
    match2 = re.search(pattern2, line)
    if match1:
        old_value = match1.group(2)
        new_line = re.sub(pattern1, fr"\g<1>{new_username}", line)
        lines[i] = new_line
        print(f"Đã sửa giá trị {old_value} thành {new_username}")
    if match2:
        old_value = match2.group(2)
        new_line = re.sub(pattern2, fr"\g<1>{new_password}", line)
        lines[i] = new_line
        print(f"Đã sửa giá trị {old_value} thành {new_password}")

# Ghi các dòng đã sửa vào file
with open(target_file, "w") as f:
    f.writelines(lines)