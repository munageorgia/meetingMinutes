import streamlit as st
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import date
from pathlib import Path
import unicodedata

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

logo_path = Path("Logo.jpg")

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Minutes Mailer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
#  CUSTOM CSS  – refined navy/gold corporate look
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --navy:   #0d1b2a;
    --navy2:  #162236;
    --gold:   #c9a84c;
    --gold2:  #e8c87a;
    --cream:  #f8f4ee;
    --muted:  #8a96a3;
    --border: #d6cebd;
    --success:#2d6a4f;
    --danger: #9b2335;
    --white:  #ffffff;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream) !important;
    color: var(--navy) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 960px; }

/* ── Top masthead ── */
.masthead {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid var(--gold);
    padding-bottom: 1.2rem;
    margin-bottom: 2rem;
}
.masthead-left { display: flex; flex-direction: column; }
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: 0.02em;
    line-height: 1.1;
}
.masthead-sub {
    font-size: 0.82rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.masthead-badge {
    background: var(--navy);
    color: var(--gold);
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    width: 3.2rem;
    height: 3.2rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--gold);
}

/* ── Section labels ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.5rem;
    margin-top: 1.6rem;
}

/* ── Card wrapper ── */
.card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 2px 8px rgba(13,27,42,0.06);
}

/* ── Recipient pill table ── */
.recipient-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.6rem;
}
.pill {
    background: var(--navy);
    color: var(--gold2);
    font-size: 0.72rem;
    padding: 0.28rem 0.7rem;
    border-radius: 20px;
    font-weight: 500;
    letter-spacing: 0.03em;
}

/* ── Streamlit widgets polish ── */
label { font-weight: 500 !important; font-size: 0.85rem !important; color: var(--navy) !important; }
.stTextInput input, .stTextArea textarea, .stDateInput input {
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    background: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--navy) !important;
    font-size: 0.92rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
}
.stTextArea textarea { min-height: 260px !important; }

/* ── Primary button ── */
.stFormSubmitButton button, .stButton button {
    background: var(--navy) !important;
    color: var(--gold) !important;
    border: 1px solid var(--navy) !important;
    border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.8rem !important;
    transition: all 0.2s ease !important;
}
.stFormSubmitButton button:hover, .stButton button:hover {
    background: var(--navy2) !important;
    border-color: var(--gold) !important;
    box-shadow: 0 4px 12px rgba(13,27,42,0.18) !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 4px !important; font-size: 0.88rem !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.8rem 0 !important; }

/* ── Upload zone ── */
.uploadedFile { font-size: 0.82rem !important; }
[data-testid="stFileUploader"] {
    border: 1.5px dashed var(--gold) !important;
    border-radius: 6px !important;
    background: rgba(201,168,76,0.04) !important;
    padding: 0.8rem !important;
}

/* ── Spinner text ── */
.stSpinner p { color: var(--navy) !important; font-size: 0.85rem !important; }

/* ── Success / error banners ── */
.result-banner {
    padding: 1rem 1.4rem;
    border-radius: 5px;
    font-size: 0.9rem;
    font-weight: 500;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.result-banner.success { background: #e8f5ee; border-left: 4px solid var(--success); color: var(--success); }
.result-banner.error   { background: #fceaea; border-left: 4px solid var(--danger);  color: var(--danger);  }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────
def load_recipients(excel_file) -> pd.DataFrame:
    """
    Read the uploaded Excel. Accepts any sheet that contains
    'Name' and 'Email' columns (case-insensitive).
    Returns a DataFrame with at least 'Name' and 'Email'.
    """
    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()

    # Case-insensitive column match
    col_map = {c.lower(): c for c in df.columns}
    if "name" not in col_map or "email" not in col_map:
        st.error("❌ Excel must contain **Name** and **Email** columns.")
        st.stop()

    df = df.rename(columns={col_map["name"]: "Name", col_map["email"]: "Email"})
    df = df[["Name", "Email"]].dropna(subset=["Email"])
    df["Email"] = df["Email"].str.strip()
    return df


def build_message(
    name: str,
    meeting_date: str,
    subject: str,
    body: str,
    president_name: str,
    secretary_name: str,
) -> MIMEMultipart:
    msg_root = MIMEMultipart("related")
    msg_root["Subject"] = subject

    signature_plain = (
        f"President: {president_name}\n"
        "___________________________\n"
        f"{president_name}\n\n"
        f"Secretary: {secretary_name}\n"
        "___________________________\n"
        f"{secretary_name}\n\n"
        "MUNA GEORGIA"
    )

    plain = (
        f"Dear {name},\n\n"
        f"{body}\n\n"
        "---\n"
        f"{signature_plain}"
    )

    html = f"""\
    <html><body style="font-family:Georgia,serif;color:#0d1b2a;max-width:680px;margin:auto;padding:2rem;">
      <div style="border-top:4px solid #c9a84c;padding-top:1.2rem;margin-bottom:1.5rem;">
        <h2 style="font-size:1.4rem;margin:0;color:#0d1b2a;">MUNA GEORGIA Meeting Minutes</h2>
        <p style="color:#8a96a3;font-size:0.82rem;margin:0.35rem 0 0;">{meeting_date}</p>
      </div>
      <p style="font-size:1rem;line-height:1.8;">Dear <strong>{name}</strong>,</p>
      <div style="white-space:pre-wrap;line-height:1.8;font-size:0.96rem;color:#1f2d3d;">{body}</div>
      <div style="margin-top:2rem;padding:1.2rem 1.4rem;border:1px solid #d6cebd;border-radius:8px;background:#f8f4ee;">
        <p style="margin:0 0 0.6rem;font-size:0.95rem;font-weight:700;color:#0d1b2a;">Approved signatories</p>
        <p style="margin:0.2rem 0;line-height:1.6;font-size:0.95rem;"><strong>President:</strong> {president_name}</p>
        <p style="margin:0.2rem 0;line-height:1.6;font-size:0.95rem;"><strong>Secretary:</strong> {secretary_name}</p>
      </div>
      <div style="margin-top:2rem;border-top:1px solid #d6cebd;padding-top:1rem;display:flex;align-items:center;gap:1rem;">
        <div>
          <p style="margin:0;font-size:1rem;font-weight:700;color:#0d1b2a;">MUNA GEORGIA</p>
          <p style="margin:0;font-size:0.82rem;color:#8a96a3;">Executive Meeting Distribution</p>
        </div>
        <div style="min-width:96px;min-height:96px;">
          <img src="cid:logo" alt="MUNA GEORGIA" style="max-width:96px;max-height:96px;object-fit:contain;" />
        </div>
      </div>
    </body></html>"""

    alternative = MIMEMultipart("alternative")
    alternative.attach(MIMEText(plain, "plain"))
    alternative.attach(MIMEText(html, "html"))
    msg_root.attach(alternative)

    if logo_path.exists():
        try:
            with logo_path.open("rb") as f:
                logo_data = f.read()
            image = MIMEImage(logo_data)
            image.add_header("Content-ID", "<logo>")
            image.add_header("Content-Disposition", "inline", filename=logo_path.name)
            msg_root.attach(image)
        except Exception:
            pass

    return msg_root


def send_bulk_email(
    sender_email: str,
    app_password: str,
    subject: str,
    meeting_date: str,
    body: str,
    president_name: str,
    secretary_name: str,
    recipients_df: pd.DataFrame,
) -> dict:
    results = {"sent": [], "failed": []}
    sender_email = sender_email.strip()
    app_password = app_password.replace(" ", "")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.ehlo()
        server.starttls()
        server.login(sender_email, app_password)
    except Exception as e:
        return {"error": str(e), "sent": [], "failed": []}

    for _, row in recipients_df.iterrows():
        name  = str(row["Name"]).strip()
        email = str(row["Email"]).strip()
        try:
            msg = build_message(name, meeting_date, subject, body, president_name, secretary_name)
            msg["From"]  = f"MUNA GEORGIA <{sender_email}>"
            msg["To"]    = email
            server.sendmail(sender_email, email, msg.as_string())
            results["sent"].append(email)
        except Exception as e:
            results["failed"].append({"email": email, "reason": str(e)})

    server.quit()
    return results


def safe_pdf_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    normalized = unicodedata.normalize("NFKD", text)
    return normalized


def create_minutes_pdf(
    meeting_date: str,
    subject: str,
    body: str,
    president_name: str,
    secretary_name: str,
) -> bytes:
    if FPDF is None:
        raise RuntimeError("FPDF is not installed. Please add fpdf to requirements.txt.")

    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(13, 27, 42)
    pdf.cell(0, 10, safe_pdf_text("MUNA GEORGIA Meeting Minutes"), ln=1, align="C")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, safe_pdf_text(f"Date: {meeting_date}"), ln=1)
    pdf.cell(0, 7, safe_pdf_text(f"Subject: {subject}"), ln=1)
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 11)
    for line in body.splitlines():
        pdf.multi_cell(0, 7, safe_pdf_text(line))
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, safe_pdf_text("Approved Signatures"), ln=1)
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, safe_pdf_text(f"President: {president_name}"), ln=1)
    pdf.cell(0, 7, safe_pdf_text("Signature: ____________________________"), ln=1)
    pdf.ln(5)
    pdf.cell(0, 7, safe_pdf_text(f"Secretary: {secretary_name}"), ln=1)
    pdf.cell(0, 7, safe_pdf_text("Signature: ____________________________"), ln=1)
    pdf.ln(10)

    if logo_path.exists():
        try:
            pdf.image(str(logo_path), x=pdf.get_x(), w=32)
        except Exception:
            pass

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, safe_pdf_text("MUNA GEORGIA"), ln=1)

    return pdf.output(dest="S").encode("latin-1", "replace")


def load_local_secrets() -> dict:
    """Load local Streamlit secrets for local development fallback."""
    if tomllib is None:
        return {}

    merged = {}
    for candidate in (Path('.streamlit/secrets.toml'), Path('secrets.toml')):
        if candidate.exists():
            try:
                with candidate.open('rb') as f:
                    data = tomllib.load(f)
                for key, value in data.items():
                    if value is None:
                        continue
                    value_str = str(value).strip()
                    if value_str:
                        merged[key] = value_str
            except Exception:
                continue
    return merged


# ──────────────────────────────────────────────
#  MASTHEAD
# ──────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div class="masthead-left">
    <div class="masthead-title">MUNA GEORGIA Minutes Mailer</div>
    <div class="masthead-sub">Member Meeting Minutes Distribution System</div>
  </div>
  <div class="masthead-badge">📋</div>
</div>
""", unsafe_allow_html=True)

if logo_path.exists():
    st.image(str(logo_path), width=100, caption="Georgia Chapter ")


# ──────────────────────────────────────────────
#  SIDEBAR – SMTP credentials (stored in secrets
#  on Streamlit Community Cloud)
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Sender Configuration")
    st.caption(
        "On Streamlit Community Cloud, store these in **Settings → Secrets** "
        "as `SENDER_EMAIL` and `APP_PASSWORD` to avoid entering them each time."
    )

    local_secrets = load_local_secrets()
    default_email = st.secrets.get("SENDER_EMAIL", "") if hasattr(st, "secrets") else ""
    default_pw    = st.secrets.get("APP_PASSWORD",  "") if hasattr(st, "secrets") else ""

    def is_placeholder(value: str) -> bool:
        value = str(value).strip()
        return not value or value.lower().startswith("your-") or value.startswith("xxxx")

    if is_placeholder(default_email):
        default_email = local_secrets.get("SENDER_EMAIL", "")
    if is_placeholder(default_pw):
        default_pw = local_secrets.get("APP_PASSWORD", "")

    sender_email = st.text_input(
        "Sender Gmail Address",
        value=default_email,
        placeholder="yourname@gmail.com",
    )
    app_password = st.text_input(
        "Gmail App Password",
        value=default_pw,
        type="password",
        placeholder="xxxx xxxx xxxx xxxx",
        help="Generate at myaccount.google.com → Security → App Passwords",
    )
    st.markdown("---")
    st.caption(" **Tip:** Enable 2-Step Verification on your Google account, then create a 16-character App Password dedicated to this app.")


# ──────────────────────────────────────────────
#  STEP 1 – Upload recipient list
# ──────────────────────────────────────────────
st.markdown('<div class="section-label">Step 1 — Recipient List</div>', unsafe_allow_html=True)

with st.container():
    uploaded_file = st.file_uploader(
        "Upload Member Excel File  (.xlsx)",
        type=["xlsx"],
        help="Must contain at least a **Name** column and an **Email** column. All other columns are ignored.",
    )

recipients_df = None
if uploaded_file:
    try:
        recipients_df = load_recipients(uploaded_file)
        count = len(recipients_df)

        pills = "".join(f'<span class="pill">{row["Name"]}</span>' for _, row in recipients_df.iterrows())
        st.markdown(
            f'<div class="card">'
            f'<span style="font-size:0.8rem;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;">'
            f'✅ &nbsp;{count} recipient{"s" if count != 1 else ""} loaded</span>'
            f'<div class="recipient-grid">{pills}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Could not read file: {e}")
else:
    st.info("Upload your members Excel file to continue. The file must have **Name** and **Email** columns.")


# ──────────────────────────────────────────────
#  STEP 2 – Compose & Send
# ──────────────────────────────────────────────
st.markdown('<div class="section-label">Step 2 — Compose Minutes</div>', unsafe_allow_html=True)

with st.form("minutes_form", clear_on_submit=False):
    col1, col2 = st.columns([1, 2])

    with col1:
        meeting_date = st.date_input("Meeting Date", value=date.today())

    with col2:
        subject_line = st.text_input(
            "Email Subject Line",
            value=f"MUNA GEORGIA Member Meeting Minutes – {meeting_date.strftime('%d %B %Y')}",
        )

    col3, col4 = st.columns(2)
    with col3:
        president_name = st.text_input(
            "President Name",
            value="",
            placeholder="e.g. Nora Ahmed",
        )
    with col4:
        secretary_name = st.text_input(
            "Secretary Name",
            value="",
            placeholder="e.g. Leyla Khatun",
        )

    st.markdown("**Minutes & Action Items**")
    minutes_text = st.text_area(
        label="minutes_body",
        label_visibility="collapsed",
        placeholder=(
            "Meeting Summary\n"
            "───────────────\n"
            "1. Topics discussed…\n\n"
            "Key Decisions\n"
            "─────────────\n"
            "• …\n\n"
            "Action Items\n"
            "────────────\n"
            "[ ] Owner — Task — Due date\n"
        ),
    )

    send_button = st.form_submit_button("  ✉  Distribute to All Members  ", use_container_width=False)


# ──────────────────────────────────────────────
#  SEND LOGIC
# ──────────────────────────────────────────────
if send_button:
    errors = []
    if not sender_email:
        errors.append("Sender email is required (set in sidebar or Secrets).")
    if not app_password:
        errors.append("Gmail App Password is required (set in sidebar or Secrets).")
    if recipients_df is None:
        errors.append("Please upload a recipient Excel file in Step 1.")
    if not minutes_text.strip():
        errors.append("The minutes body cannot be empty.")
    if not president_name.strip():
        errors.append("President name is required for the signature section.")
    if not secretary_name.strip():
        errors.append("Secretary name is required for the signature section.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        total = len(recipients_df)
        progress_bar = st.progress(0, text="Preparing to send…")

        def send_with_progress():
            results = {"sent": [], "failed": []}
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
                server.ehlo()
                server.starttls()
                server.login(sender_email, app_password)
            except Exception as e:
                return {"error": str(e), "sent": [], "failed": []}

            for i, (_, row) in enumerate(recipients_df.iterrows()):
                name  = str(row["Name"]).strip()
                email = str(row["Email"]).strip()
                pct = int((i / total) * 100)
                progress_bar.progress(pct, text=f"Sending to {name}…  ({i}/{total})")
                try:
                    msg = build_message(
                        name,
                        str(meeting_date),
                        subject_line,
                        minutes_text,
                        president_name,
                        secretary_name,
                    )
                    msg["From"] = f"MUNA GEORGIA <{sender_email}>"
                    msg["To"]   = email
                    server.sendmail(sender_email, email, msg.as_string())
                    results["sent"].append(email)
                except Exception as e:
                    results["failed"].append({"email": email, "reason": str(e)})

            server.quit()
            progress_bar.progress(100, text="Done.")
            return results

        result = send_with_progress()

        if "error" in result:
            st.markdown(
                f'<div class="result-banner error">⚠ SMTP connection failed: {result["error"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            sent_count   = len(result["sent"])
            failed_count = len(result["failed"])

            if sent_count:
                st.markdown(
                    f'<div class="result-banner success">✔ Successfully dispatched to {sent_count} member{"s" if sent_count != 1 else ""}.</div>',
                    unsafe_allow_html=True,
                )
                st.balloons()

            if failed_count:
                st.warning(f"⚠ {failed_count} delivery failure(s):")
                for f in result["failed"]:
                    st.caption(f"• {f['email']} — {f['reason']}")

if recipients_df is not None and minutes_text.strip() and president_name.strip() and secretary_name.strip():
    try:
        pdf_bytes = create_minutes_pdf(
            meeting_date=str(meeting_date),
            subject=subject_line,
            body=minutes_text,
            president_name=president_name,
            secretary_name=secretary_name,
        )
        st.download_button(
            "Download Signed Minutes PDF",
            pdf_bytes,
            file_name=f"MUNA_GEORGIA_Member_Meeting_Minutes_{meeting_date}.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Could not generate PDF: {e}")

# ──────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.8rem;">
    All rights reserved MUNA GEORGIA | <a href="https://www.sazidshovon.tech" target="_blank" style="color: var(--gold); text-decoration: none;">Sazid Shovon</a>
</div>
""", unsafe_allow_html=True)