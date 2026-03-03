import os
import re
import logging
import requests
from datetime import datetime, timedelta

# Configuring logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SENT_FILE = "sent_ids.txt"

def load_sent_ids():
    """Load successfully sent employment IDs to avoid duplicates."""
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_ids(sent_ids):
    """Save successfully sent employment IDs."""
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        for jid in sent_ids:
            f.write(f"{jid}\n")

def send_telegram_message(text):
    """Send HTML-formatted text message to Telegram channel/user."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning("TELEGRAM_TOKEN or TELEGRAM_CHAT_ID not provided. Message will not be sent.")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        logging.error(f"Telegram API HTTP error {status}: {e.response.text}")
    except Exception as e:
        logging.error(f"Failed to send telegram message: {e}")
    return False

def format_date(iso_str):
    """Convert ISO8601 offset strings to readable YYYY-MM-DD HH:MM."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso_str

def main():
    logging.info("Starting up Jasoseol employment scraper")
    sent_ids = load_sent_ids()
    
    # 1. Fetch upcoming employments
    now = datetime.utcnow()
    start_time = now.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end_time = (now + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    url_calendar = "https://jasoseol.com/employment/calendar_list.json"
    try:
        res = requests.post(url_calendar, json={"start_time": start_time, "end_time": end_time})
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        logging.error(f"Failed to fetch calendar_list: {e}")
        return

    employments = data.get("employment", [])
    
    # 2. Extract targets via 1st Filter
    target_jobs = []
    for job in employments:
        sub_employments = job.get("employments", [])
        is_target = False
        
        for sub in sub_employments:
            div = sub.get("division", -1)
            # condition 1: division is 1 or 3
            if div not in (1, 3):
                continue
                
            duty_groups = sub.get("duty_groups", [])
            for duty in duty_groups:
                g_id = duty.get("group_id", 0)
                # condition 2: duty group in [160, 173]
                if 160 <= g_id <= 173:
                    is_target = True
                    break
            if is_target:
                break
                
        if is_target:
            target_jobs.append(job)

    logging.info(f"Target jobs found after 1st filter: {len(target_jobs)}")

    url_detail = "https://jasoseol.com/employment/get.json"
    url_question = "https://jasoseol.com/employment/employment_question.json"

    new_sent_count = 0

    # 3. Request details per remaining element
    for job in target_jobs:
        job_id = job.get("id")
        if not job_id:
            continue
            
        if str(job_id) in sent_ids:
            continue
            
        try:
            res_detail = requests.post(url_detail, json={"skip_read_log": True, "employment_company_id": job_id})
            res_detail.raise_for_status()
            detail_data = res_detail.json()
        except Exception as e:
            logging.error(f"Failed to fetch details for {job_id}: {e}")
            continue

        company_name = detail_data.get("name", "Unknown Company")
        title = detail_data.get("title", "No Title")
        start_t = format_date(detail_data.get("start_time"))
        end_t = format_date(detail_data.get("end_time"))
        
        # Extract Image URL from HTML content
        content = detail_data.get("content", "")
        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
        img_url = img_match.group(1) if img_match else "No Image Found"

        # 4. Filter with sub employment items again
        sub_employments = detail_data.get("employments", [])
        valid_role_data = []

        for sub in sub_employments:
            div = sub.get("division", -1)
            if div not in (1, 3):
                continue
            
            duty_group_ids = sub.get("duty_group_ids", [])
            is_valid_role = any(160 <= gid <= 173 for gid in duty_group_ids)
            
            if is_valid_role:
                sub_id = sub.get("id")
                field_name = sub.get("field", "Unknown Role")
                
                # Fetch questions
                try:
                    res_q = requests.post(url_question, json={"employment_id": sub_id})
                    res_q.raise_for_status()
                    q_data = res_q.json().get("employment_question", [])
                    # Sort questions by number
                    questions = sorted(q_data, key=lambda x: x.get("number", 0))
                    q_texts = [q.get("question", "") for q in questions]
                    
                    valid_role_data.append({"field": field_name, "questions": q_texts})
                except Exception as e:
                    logging.error(f"Failed to fetch questions for sub_id {sub_id}: {e}")
        
        if valid_role_data:
            # 5. Format to Telegram message and send
            msg = f"🏢 <b>{company_name} - {title}</b>\n"
            msg += f"📅 접수기간: {start_t} ~ {end_t}\n"
            if img_url != "No Image Found":
                msg += f"🔗 공고본문: <a href='{img_url}'>이미지 링크</a>\n\n"
            else:
                msg += "🔗 공고본문 이미지 없음\n\n"
            
            msg += "<b>[모집 직무 및 자소서 문항]</b>\n"
            
            for role in valid_role_data:
                msg += f"\n🎯 <b>{role['field']}</b>\n"
                if not role['questions']:
                    msg += "- 문항 없음 혹은 등록 전\n"
                for i, q in enumerate(role['questions'], 1):
                    msg += f" {i}. {q}\n"
                    
            if send_telegram_message(msg):
                sent_ids.add(str(job_id))
                save_sent_ids(sent_ids)
                new_sent_count += 1
                logging.info(f"Sent listing: {company_name} / {title}")

    logging.info(f"Done. Newly sent items: {new_sent_count}")

if __name__ == "__main__":
    main()
