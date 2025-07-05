from flask import Flask, request
import os, time, smtplib
from email.message import EmailMessage

app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# QQ邮箱 SMTP 配置
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

def send_email(image_path, result_text):
    msg = EmailMessage()
    msg["Subject"] = "BeagleY-AI 识别结果通知"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(f"检测结果：{result_text}")

    # 附加图像
    with open(image_path, "rb") as img:
        img_data = img.read()
        msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

    # 使用 QQ 邮箱 SMTP 发送邮件
    with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("[+] 邮件已发送")

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files.get('image')
    result = request.form.get('result', 'no result')
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    fname = f"{timestamp}.jpg"

    if image is None:
        return "Missing image file", 400

    image_path = os.path.join(UPLOAD_DIR, fname)
    image.save(image_path)

    # 写日志文件
    with open(os.path.join(UPLOAD_DIR, "log.txt"), "a") as f:
        f.write(f"{timestamp}: {result}\n")

    # 发送邮件
    try:
        send_email(image_path, result)
    except Exception as e:
        print("❌ 邮件发送失败:", e)
        return "Failed to send email", 500

    return "OK"
