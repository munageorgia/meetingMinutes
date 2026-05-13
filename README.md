# 📋 Minutes Mailer

A professional one-page Streamlit app to distribute meeting minutes to your entire organisation via Gmail — driven by an Excel member list.

## Features
- **Dynamic recipient list** — upload any `.xlsx` with a `Name` and `Email` column; all other columns are ignored
- **Personalised emails** — each recipient receives a `Dear [Name]` message in both plain-text and styled HTML
- **Progress bar** — live per-recipient delivery tracking
- **Secure credentials** — sender email and App Password stored in Streamlit Secrets, never hard-coded

---

## Repository structure
```
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── members_sample.xlsx      # Template Excel file (replace with your real list)
└── .streamlit/
    └── secrets.toml         # Local dev secrets (DO NOT commit real passwords)
```

---

## Deployment to Streamlit Community Cloud

1. **Fork / push** this repo to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → point to `app.py`.
3. After the app is created, open **Settings → Secrets** and paste:

```toml
SENDER_EMAIL = "your-office@gmail.com"
APP_PASSWORD  = "xxxx xxxx xxxx xxxx"
```

> ⚠️ **Never commit real credentials.** The `secrets.toml` file is listed in `.gitignore` and is only used for local development.

4. Click **Deploy**. Done.

---

## Gmail App Password setup

1. Sign in to [myaccount.google.com](https://myaccount.google.com).
2. **Security → 2-Step Verification** — make sure it's enabled.
3. **Security → App Passwords** → choose app = *Mail*, device = *Other* → name it "Minutes Mailer".
4. Copy the 16-character password into Streamlit Secrets.

---

## Excel format

| Name | Email | Department | Role | … |
|------|-------|------------|------|---|
| Alice Johnson | alice@company.com | Engineering | Manager | … |

Only **Name** and **Email** are required. Column names are case-insensitive.

---

## Local development

```bash
pip install -r requirements.txt
streamlit run app.py
```
