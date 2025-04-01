# Work tracker automation

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Playwright](https://img.shields.io/badge/playwright-1.30%2B-green)
![Telegram Bot](https://img.shields.io/badge/telegram%20bot-api-blue)

Automation tool for managing work schedules with browser automation and Telegram notifications.

## 📌 Features

- Automated status changes (Ready/Break/Lunch)
- Configurable break times and durations
- Telegram notifications with screenshots
- Visual GUI for easy configuration
- Total work time calculation
- Scheduled execution

## 🚀 Usage

### 1. Configure Settings
Update these values in the code:
```python
# Telegram Configuration
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"    # From @BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"        # Channel/Group ID

# Work Portal URLs
WEBRTC_URL = "https://your-webrtc-portal.com"
WORK_PORTAL_URL = "https://your-work-portal.com"
```

### 2. Run the Application
Execute the script:
```bash
python for_git_no_personal_info.py
```

### 3. GUI Configuration
Use the interface to:
- ⏰ **Set Schedule Time**  
  *Example: 09:00 AM - 05:00 PM*
- ⏸️ **Configure Breaks**  
  *Defaults: 15m breaks, 30m lunch*
- 🚀 **Start Automation**  
  *Click "Start" to begin* 

## 🕒 Default Schedule

| Action               | Default Time  | Duration      |
|----------------------|---------------|---------------|
| First Break          | After 2 hours | 15 minutes    |
| Lunch                | After 1.25h   | 30 minutes    |
| Second Break         | After 2.5h    | 15 minutes    |
| End of Workday       | After 8 hours | -             |
## 📸 Notification Examples

- ✅ **Login successful** - Notification when successfully logged in
- 🔄 **Status changes** - Alerts for status changes (Ready/Break/Lunch)
- 🚨 **Error alerts** - Error notifications with screenshots
- ⏱️ **Scheduled start confirmation** - Scheduled launch confirmation

## 🤖 Telegram Commands

- 🤖 **Automatic status updates** - Automatic notifications for changes
- 📷 **Screenshot attachments** - Sending screenshots with events
- 🔘 **Manual status check via button** - Manual check via Telegram button

