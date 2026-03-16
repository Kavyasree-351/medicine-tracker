import streamlit as st
import json
import os
from datetime import datetime, date
from pathlib import Path

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedMate",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main {
        background: #F7F4EF;
    }

    .stApp {
        background: #F7F4EF;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hero header */
    .hero {
        background: linear-gradient(135deg, #2D6A4F 0%, #40916C 50%, #52B788 100%);
        border-radius: 24px;
        padding: 32px 28px 24px;
        margin-bottom: 28px;
        color: white;
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: '💊';
        position: absolute;
        right: 24px;
        top: 20px;
        font-size: 56px;
        opacity: 0.3;
    }

    .hero h1 {
        font-family: 'Nunito', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 4px 0;
        color: white;
    }

    .hero p {
        margin: 0;
        opacity: 0.85;
        font-size: 0.95rem;
    }

    /* Cards */
    .med-card {
        background: white;
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 12px;
        border-left: 5px solid #52B788;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: transform 0.2s;
    }

    .med-card:hover {
        transform: translateY(-2px);
    }

    .med-card.taken {
        border-left-color: #B7E4C7;
        opacity: 0.65;
    }

    .med-card.missed {
        border-left-color: #E63946;
    }

    .med-card.low-stock {
        border-left-color: #F4A261;
    }

    .med-name {
        font-family: 'Nunito', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #1B4332;
        margin-bottom: 4px;
    }

    .med-detail {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 2px;
    }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 6px;
    }

    .badge-green { background: #D8F3DC; color: #1B4332; }
    .badge-red { background: #FFE5E5; color: #C1121F; }
    .badge-orange { background: #FFF0DB; color: #BB4D00; }
    .badge-blue { background: #DBF0FF; color: #004B87; }

    .section-title {
        font-family: 'Nunito', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        color: #1B4332;
        margin: 24px 0 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .stat-row {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
    }

    .stat-box {
        flex: 1;
        background: white;
        border-radius: 14px;
        padding: 16px 14px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .stat-num {
        font-family: 'Nunito', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: #2D6A4F;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #888;
        margin-top: 2px;
    }

    .profile-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 2px solid transparent;
    }

    .profile-active {
        background: #2D6A4F;
        color: white;
    }

    .profile-inactive {
        background: white;
        color: #2D6A4F;
        border-color: #2D6A4F;
    }

    .refill-alert {
        background: #FFF3CD;
        border: 1px solid #F4A261;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        color: #7B3F00;
    }

    /* Form styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1.5px solid #D4E6DC !important;
    }

    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Nunito', sans-serif !important;
    }

    .stButton > button[kind="primary"] {
        background: #2D6A4F !important;
        border: none !important;
        color: white !important;
    }

    .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: #999;
    }

    .empty-state .emoji {
        font-size: 3rem;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ─── DATA STORAGE ─────────────────────────────────────────────────────────────
DATA_FILE = "medmate_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "profiles": ["Me"],
        "medicines": {},
        "logs": {}
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_today():
    return date.today().isoformat()

def get_log_key(profile, med_name):
    return f"{profile}_{med_name}_{get_today()}"

# ─── INIT ─────────────────────────────────────────────────────────────────────
data = load_data()

if "active_profile" not in st.session_state:
    st.session_state.active_profile = data["profiles"][0] if data["profiles"] else "Me"

if "view" not in st.session_state:
    st.session_state.view = "home"

today = get_today()
profile = st.session_state.active_profile

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def get_profile_meds(profile):
    return data["medicines"].get(profile, [])

def get_log(profile, med_name):
    key = get_log_key(profile, med_name)
    return data["logs"].get(key, None)

def set_log(profile, med_name, status):
    key = get_log_key(profile, med_name)
    data["logs"][key] = {"status": status, "time": datetime.now().strftime("%H:%M")}
    save_data(data)

def add_medicine(profile, name, dosage, times, stock, refill_at):
    if profile not in data["medicines"]:
        data["medicines"][profile] = []
    data["medicines"][profile].append({
        "name": name,
        "dosage": dosage,
        "times": times,
        "stock": stock,
        "refill_at": refill_at,
        "added": get_today()
    })
    save_data(data)

def update_stock(profile, med_name, new_stock):
    meds = data["medicines"].get(profile, [])
    for med in meds:
        if med["name"] == med_name:
            med["stock"] = new_stock
    save_data(data)

def delete_medicine(profile, med_name):
    meds = data["medicines"].get(profile, [])
    data["medicines"][profile] = [m for m in meds if m["name"] != med_name]
    save_data(data)

# ─── STATS ────────────────────────────────────────────────────────────────────
meds = get_profile_meds(profile)
total = len(meds)
taken_today = sum(1 for m in meds if get_log(profile, m["name"]) and get_log(profile, m["name"])["status"] == "taken")
missed_today = sum(1 for m in meds if get_log(profile, m["name"]) and get_log(profile, m["name"])["status"] == "missed")
low_stock = [m for m in meds if m["stock"] <= m["refill_at"]]
pending = total - taken_today - missed_today

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <h1>MedMate 💊</h1>
    <p>Hello, <b>{profile}</b>! Today is {datetime.now().strftime("%A, %B %d")}.</p>
</div>
""", unsafe_allow_html=True)

# ─── PROFILE SWITCHER ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">👤 Who\'s this for?</div>', unsafe_allow_html=True)

profile_html = ""
for p in data["profiles"]:
    cls = "profile-active" if p == profile else "profile-inactive"
    profile_html += f'<span class="profile-pill {cls}">{p}</span>'
st.markdown(profile_html, unsafe_allow_html=True)

col_p1, col_p2 = st.columns([3, 1])
with col_p1:
    selected = st.selectbox("Switch profile", data["profiles"], index=data["profiles"].index(profile), label_visibility="collapsed")
    if selected != profile:
        st.session_state.active_profile = selected
        st.rerun()
with col_p2:
    if st.button("➕ Add", use_container_width=True):
        st.session_state.view = "add_profile"

if st.session_state.view == "add_profile":
    new_profile = st.text_input("New profile name (e.g. Mum, Dad)")
    if st.button("Create profile", type="primary"):
        if new_profile and new_profile not in data["profiles"]:
            data["profiles"].append(new_profile)
            save_data(data)
            st.session_state.active_profile = new_profile
            st.session_state.view = "home"
            st.rerun()

# ─── STATS ROW ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
    <div class="stat-box">
        <div class="stat-num" style="color:#2D6A4F">{taken_today}</div>
        <div class="stat-label">Taken today</div>
    </div>
    <div class="stat-box">
        <div class="stat-num" style="color:#888">{pending}</div>
        <div class="stat-label">Pending</div>
    </div>
    <div class="stat-box">
        <div class="stat-num" style="color:#E63946">{missed_today}</div>
        <div class="stat-label">Missed</div>
    </div>
    <div class="stat-box">
        <div class="stat-num" style="color:#F4A261">{len(low_stock)}</div>
        <div class="stat-label">Low stock</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── REFILL ALERTS ────────────────────────────────────────────────────────────
if low_stock:
    st.markdown('<div class="section-title">⚠️ Refill Soon</div>', unsafe_allow_html=True)
    for med in low_stock:
        st.markdown(f"""
        <div class="refill-alert">
            ⚠️ <b>{med['name']}</b> — only <b>{med['stock']} pills</b> left. Time to refill!
        </div>
        """, unsafe_allow_html=True)

# ─── TODAY'S MEDICINES ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">💊 Today\'s Medicines</div>', unsafe_allow_html=True)

if not meds:
    st.markdown("""
    <div class="empty-state">
        <div class="emoji">💊</div>
        <div>No medicines added yet.<br>Add your first medicine below!</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for med in meds:
        log = get_log(profile, med["name"])
        status = log["status"] if log else "pending"
        card_class = "taken" if status == "taken" else "missed" if status == "missed" else ""
        if med["stock"] <= med["refill_at"] and status == "pending":
            card_class = "low-stock"

        badge = ""
        if status == "taken":
            badge = f'<span class="badge badge-green">✓ Taken at {log["time"]}</span>'
        elif status == "missed":
            badge = '<span class="badge badge-red">✗ Missed</span>'
        else:
            badge = '<span class="badge badge-blue">⏳ Pending</span>'

        if med["stock"] <= med["refill_at"]:
            badge += f'<span class="badge badge-orange">⚠️ Low stock: {med["stock"]}</span>'

        times_str = ", ".join(med["times"]) if isinstance(med["times"], list) else med["times"]

        st.markdown(f"""
        <div class="med-card {card_class}">
            <div class="med-name">{med['name']}</div>
            <div class="med-detail">💊 {med['dosage']}</div>
            <div class="med-detail">🕐 {times_str}</div>
            <div class="med-detail">📦 Stock: {med['stock']} pills</div>
            {badge}
        </div>
        """, unsafe_allow_html=True)

        if status == "pending":
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if st.button(f"✅ Taken", key=f"taken_{med['name']}", use_container_width=True):
                    set_log(profile, med["name"], "taken")
                    new_stock = max(0, med["stock"] - 1)
                    update_stock(profile, med["name"], new_stock)
                    st.rerun()
            with col2:
                if st.button(f"❌ Missed", key=f"missed_{med['name']}", use_container_width=True):
                    set_log(profile, med["name"], "missed")
                    st.rerun()
            with col3:
                if st.button("🗑️", key=f"del_{med['name']}", use_container_width=True):
                    delete_medicine(profile, med["name"])
                    st.rerun()
        else:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"↩️ Undo", key=f"undo_{med['name']}", use_container_width=True):
                    key = get_log_key(profile, med["name"])
                    if key in data["logs"]:
                        del data["logs"][key]
                    save_data(data)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del2_{med['name']}", use_container_width=True):
                    delete_medicine(profile, med["name"])
                    st.rerun()

# ─── ADD MEDICINE ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">➕ Add Medicine</div>', unsafe_allow_html=True)

with st.expander("Add a new medicine", expanded=False):
    with st.form("add_med_form"):
        med_name = st.text_input("Medicine name", placeholder="e.g. Paracetamol")
        dosage = st.text_input("Dosage", placeholder="e.g. 500mg, 1 tablet")

        st.write("When to take it:")
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            morning = st.checkbox("Morning")
        with col_t2:
            afternoon = st.checkbox("Afternoon")
        with col_t3:
            night = st.checkbox("Night")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            stock = st.number_input("Current stock (pills)", min_value=0, value=30)
        with col_s2:
            refill_at = st.number_input("Refill alert when below", min_value=1, value=5)

        submitted = st.form_submit_button("Add Medicine", type="primary", use_container_width=True)

        if submitted:
            if not med_name:
                st.error("Please enter a medicine name!")
            else:
                times = []
                if morning: times.append("Morning")
                if afternoon: times.append("Afternoon")
                if night: times.append("Night")
                if not times:
                    times = ["As needed"]
                add_medicine(profile, med_name, dosage or "As prescribed", times, stock, refill_at)
                st.success(f"✅ {med_name} added!")
                st.rerun()

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#aaa; font-size:0.8rem; padding: 8px 0;">
    MedMate 💊 · Never miss a dose · Built with Streamlit
</div>
""", unsafe_allow_html=True)
