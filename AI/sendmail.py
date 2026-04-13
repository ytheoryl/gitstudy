import smtplib
import argparse
import os
from email.message import EmailMessage

def send_mail(targets, file_path=None, message_text=None, title=None):
    # 配置信息: 使用 Direct Send 终结点
    # 租户特定的 MX 记录: synaxg-com.mail.protection.outlook.com
    # Direct Send 不需要验证，但只能发送到组织内部地址
    smtp_server = "synaxg-com.mail.protection.outlook.com"
    smtp_port = 25
    sender_email = "itsupport@synaxg.com"

    # 创建邮件对象
    msg = EmailMessage()
    msg['Subject'] = title if title else "Automated Email from Linux (Direct Send)"
    msg['From'] = sender_email
    msg['To'] = ", ".join(targets)

    # 设置邮件正文
    body = message_text if message_text else ""
    msg.set_content(body)

    # 处理附件
    if file_path and os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(file_path)
            
            msg.add_attachment(
                file_data,
                maintype='application',
                subtype='octet-stream',
                filename=file_name
            )
        except Exception as e:
            print(f"Error reading file: {e}")
            return

    try:
        # 连接服务器并直接发送 (Direct Send 模式，不需要 login)
        print(f"Connecting to {smtp_server} on port {smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # 这种模式不使用认证
            print(f"Sending via Direct Send to: {', '.join(targets)}")
            server.send_message(msg)
        print(f"Successfully sent email to {len(targets)} recipient(s)")
    except Exception as e:
        print(f"Failed to send email: {e}")
        print("\nPossible issues:")
        print("1. Your sender IP is not in Synaxg's SPF record (or is being throttled).")
        print("2. Recipient is outside synaxg.com (Direct Send only allows internal mail).")
        print("3. Port 25 is blocked by your ISP or firewall.")

def main():
    parser = argparse.ArgumentParser(description="Send an email via Microsoft 365 SMTP.")
    parser.add_argument("--target", required=True, nargs='+', help="Recipient email address(es), space-separated")
    parser.add_argument("--file", help="Path to the file to attach (optional)")
    parser.add_argument("--message", help="Message body (optional)")
    parser.add_argument("--title", help="Email subject (optional)")

    # 如果没有提供参数，则显示帮助信息并退出
    import sys
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nExample Usage:")
        print('  python sendmail.py --target abc@synaxg.com --title "Job Alert" --file /var/log/123.txt --message "okok"')
        print('  python sendmail.py --target user1@synaxg.com user2@synaxg.com --title "Weekly Report" --message "Hello world"')
        print('  python sendmail.py --target abc@synaxg.com')
        sys.exit(0)

    args = parser.parse_args()

    send_mail(args.target, args.file, args.message, args.title)

if __name__ == "__main__":
    main()
