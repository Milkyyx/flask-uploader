from flask import Flask, request
import os, time, smtplib
from email.message import EmailMessage

app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# QQ 邮箱 SMTP 设置（建议改成环境变量）
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

def send_email(image_path, result_text):
    msg = EmailMessage()
    msg["Subject"] = "📸 BeagleY-AI 识别通知"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(f"检测结果：{result_text}")

    with open(image_path, "rb") as img:
        img_data = img.read()
        msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

    with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("[✓] 邮件发送成功")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        image = request.files.get('image')
        result = request.form.get('result', 'no result')
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        fname = f"{timestamp}.jpg"

        if image is None:
            return "❌ Missing image file", 400

        image_path = os.path.join(UPLOAD_DIR, fname)
        image.save(image_path)

        with open(os.path.join(UPLOAD_DIR, "log.txt"), "a") as f:
            f.write(f"{timestamp}: {result}\n")

        send_email(image_path, result)
        return "✅ Upload and email sent"
    
    except Exception as e:
        print("❌ 错误:", e)
        return f"❌ Server Error: {str(e)}", 500

