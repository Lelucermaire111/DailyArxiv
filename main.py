import requests
import feedparser
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 配置部分：关键词、类别、结果数量、邮箱账户等
KEYWORD = "xxxxxxxxx"
MAX_RESULTS = 20            # 获取论文数量上限
# 邮件配置（建议用Gmail邮箱，其他邮箱暂未尝试）
GMAIL_USER = "your_gmail_account@gmail.com"       # 发件人Gmail地址
# 在Google账户搜索应用专用密码可设置16位应用专用密码
GMAIL_PASS = "your_gmail_app_password_or_token"   # 发件人Gmail密码（或应用专用密码）
RECIPIENT_EMAIL = "recipient@example.com"         # 收件人邮箱地址

def fetch_latest_papers(keyword: str, max_results: int = 100):
    """从 arXiv API 获取指定关键词和类别的最新论文列表。"""
    base_url = "http://export.arxiv.org/api/query?"
    # 构造搜索查询：关键词 + 类别过滤
    search_query = f'all:"{keyword}"'
    # 使用 requests 请求 arXiv API，获取 Atom feed
    response = requests.get(base_url, params={
        "search_query": search_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results
    })
    # 解析 Atom feed
    feed = feedparser.parse(response.text)
    return feed.entries

def filter_papers_by_date(entries, start_time: datetime, end_time: datetime):
    """过滤给定论文列表，只保留在指定时间区间提交的论文（根据 UTC 时间）。"""
    filtered_entries = []
    for entry in entries:
        if not hasattr(entry, "published"):
            continue  # 没有发布日期则跳过
        published_str = entry.published  # 如 "2025-02-26T13:45:00Z"
        try:
            published_dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            # 若日期格式解析失败，跳过该条目
            continue
        # 如果发表时间在[start_time, end_time)区间内，则保留
        if start_time <= published_dt < end_time:
            filtered_entries.append(entry)
    return filtered_entries

def send_email_via_gmail(subject: str, body: str, to_email: str, from_email: str, gmail_password: str):
    """通过 Gmail SMTP 发送邮件，支持将 arXiv 链接转为可点击的超链接，并显示论文提交日期。"""
    # 构建邮件内容，修改为 HTML 格式
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # 使用 HTML 格式将内容填充到邮件体中
    body_html = """
    <html>
    <body>
        <p>Hi,</p>
        <p>以下是在 arXiv (cs 类别) 中最近五天提交的包含关键词 '{}' 的论文：</p>
        <ul>
    """.format(KEYWORD)
    
    for entry in recent_entries:
        title = entry.title.strip()
        link = entry.id.strip()  # 论文的 arXiv 链接
        published_str = entry.published  # 提交日期（格式：YYYY-MM-DDTHH:MM:SSZ）
        # 解析提交日期并格式化
        published_date = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        
        # 构建带有超链接和提交日期的邮件项
        body_html += f'<li><a href="{link}">{title}</a><br><small>提交日期: {published_date}</small></li>'
    
    body_html += """
        </ul>
        <p>请查收以上最新论文详情。</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body_html, "html"))
    
    # 连接到 Gmail SMTP 服务器并发送邮件
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()  # 开启 TLS 加密
        server.login(from_email, gmail_password)
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
    finally:
        server.quit()


if __name__ == "__main__":
    # 计算时间范围：UTC时间的过去五天到今天
    now_utc = datetime.utcnow()
    yesterday_utc = now_utc - timedelta(days=5)
    # 获取 arXiv 最新论文并筛选过去五天提交的论文
    all_entries = fetch_latest_papers(KEYWORD, max_results=MAX_RESULTS)
    recent_entries = filter_papers_by_date(all_entries, start_time=yesterday_utc, end_time=now_utc)
    if not recent_entries:
        print("No new papers found in the last 5 days.")
    else:
        # 准备邮件内容：列出论文标题和链接
        lines = []
        for entry in recent_entries:
            title = entry.title.strip()
            # 使用论文摘要页面链接（entry.id 通常为 arXiv 摘要页URL）
            link = entry.id.strip() if hasattr(entry, "id") else entry.link
            lines.append(f"- {title}\n  {link}")
        email_body = "Hi,\n\n以下是在 arXiv (cs 类别) 中最近5天提交的包含关键词 '{}' 的论文：\n\n".format(KEYWORD)
        email_body += "\n\n".join(lines)
        email_body += "\n\n请查收以上最新论文详情。"
        # 设置邮件主题
        email_subject = f"Daily arXiv Alert: {KEYWORD}"
        # 发送邮件
        send_email_via_gmail(email_subject, email_body, RECIPIENT_EMAIL, GMAIL_USER, GMAIL_PASS)
