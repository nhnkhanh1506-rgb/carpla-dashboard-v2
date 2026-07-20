import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import calendar

# ======================
# 1. PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Dashboard DMS - Carpla Service",
    layout="wide"
)

# ======================
# 2. COLORS
# ======================
BG_COLOR = "#EEF3F9"
TEXT_DARK = "#1F2937"
TEXT_MUTED = "#64748B"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#DBE3EE"

PRIMARY_BLUE = "#3B6FD8"
PRIMARY_BLUE_DARK = "#2F5FBE"
PRIMARY_BLUE_LIGHT = "#7FA7E6"

LINE_BLUE = "#8EC5FF"
LINE_BLUE_SOFT = "#A8D3FF"
PCT_TEXT_COLOR = "#DCEEFF"
BAR_LABEL_COLOR = "#FF8A80"

RED_MAIN = "#E45858"
RED_DARK = "#D64545"

DARK_PANEL = "#0B1530"
DARK_GRID = "rgba(255,255,255,0.10)"
WHITE = "#F8FAFC"

# muted formal palette for section 3
MUTED_BAR_COLORS = [
    "#335C99",
    "#426AA4",
    "#5278AF",
    "#6185BA",
    "#7193C4",
    "#80A0CE",
    "#90ADD7",
    "#9FB9DF",
    "#AFC6E7",
    "#BED2EE",
]

# section 4 donut colors
DONUT_MAIN = "#3C64A6"
DONUT_SECOND = "#9CC0DF"

# ======================
# 3. GLOBAL STYLE
# ======================
st.markdown(f"""
<style>
    .stApp {{
        background-color: {BG_COLOR};
    }}

    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1F2937 0%, #111827 100%);
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    h1, h2, h3 {{
        color: {TEXT_DARK};
        font-weight: 800 !important;
    }}

    .hero-box {{
        background: linear-gradient(135deg, #22314D 0%, #2F456D 55%, #496B9E 100%);
        border-radius: 24px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(31, 41, 55, 0.18);
    }}

    .hero-title {{
        font-size: 42px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 8px;
    }}

    .hero-subtitle {{
        font-size: 15px;
        color: #DBEAFE;
    }}

    .card {{
        background: {CARD_BG};
        border-radius: 22px;
        padding: 22px 24px;
        border: 1px solid {CARD_BORDER};
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        min-height: 170px;
    }}

    .card-title {{
        font-size: 15px;
        font-weight: 700;
        color: {TEXT_MUTED};
        margin-bottom: 16px;
    }}

    .card-value {{
        font-size: 48px;
        font-weight: 900;
        color: #0F172A;
        line-height: 1;
        margin-bottom: 18px;
    }}

    .card-badge {{
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: #E8F0FF;
        color: #1D4ED8;
        font-size: 13px;
        font-weight: 700;
    }}

    .section-card {{
        background: {CARD_BG};
        border-radius: 22px;
        padding: 22px 22px 18px 22px;
        border: 1px solid {CARD_BORDER};
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        min-height: 170px;
        margin-bottom: 22px;
    }}

    .progress-title {{
        font-size: 16px;
        font-weight: 800;
        color: {TEXT_DARK};
        margin-bottom: 14px;
    }}

    .progress-sub {{
        font-size: 15px;
        color: #475569;
        margin-bottom: 8px;
        font-weight: 600;
    }}

    .progress-track {{
        position: relative;
        width: 100%;
        height: 10px;
        background: #E5E7EB;
        border-radius: 999px;
        margin-top: 38px;
    }}

    .progress-fill {{
        height: 10px;
        background: linear-gradient(90deg, {RED_DARK}, {RED_MAIN});
        border-radius: 999px;
    }}

    .progress-dot {{
        position: absolute;
        top: -7px;
        width: 24px;
        height: 24px;
        background: {RED_MAIN};
        border: 4px solid white;
        border-radius: 50%;
        transform: translateX(-50%);
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.22);
    }}

    .progress-label {{
        position: absolute;
        top: -34px;
        transform: translateX(-50%);
        font-size: 14px;
        font-weight: 800;
        color: {RED_MAIN};
        white-space: nowrap;
    }}

    .progress-scale {{
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        font-weight: 700;
        color: {TEXT_MUTED};
        margin-top: 10px;
    }}

    .mini-kpi {{
        background: {CARD_BG};
        border-radius: 18px;
        padding: 18px 18px;
        border: 1px solid {CARD_BORDER};
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
        margin-bottom: 14px;
    }}

    .mini-kpi-title {{
        font-size: 13px;
        font-weight: 800;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .mini-kpi-value {{
        font-size: 30px;
        font-weight: 900;
        color: #0F172A;
        margin-bottom: 10px;
    }}

    .mini-kpi-badge {{
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: #ECFEFF;
        color: #0F766E;
        font-size: 12px;
        font-weight: 700;
    }}

    .section-label {{
        font-size: 17px;
        font-weight: 800;
        color: {TEXT_DARK};
        margin-bottom: 12px;
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 18px;
        overflow: hidden;
    }}

    .landing-shell {
        max-width: 980px;
        margin: 3.5rem auto 0 auto;
        padding: 48px 52px;
        background: rgba(255,255,255,0.96);
        border: 1px solid #DBE3EE;
        border-radius: 28px;
        box-shadow: 0 18px 50px rgba(15, 23, 42, 0.10);
        text-align: center;
    }

    .landing-title {
        margin-top: 10px;
        font-size: 38px;
        line-height: 1.15;
        font-weight: 900;
        color: #172554;
    }

    .landing-description {
        max-width: 760px;
        margin: 14px auto 30px auto;
        font-size: 17px;
        line-height: 1.7;
        color: #64748B;
    }

    .landing-filter-title {
        margin-top: 8px;
        margin-bottom: 10px;
        font-size: 16px;
        font-weight: 800;
        color: #334155;
    }

    div.stButton > button {
        min-height: 48px;
        border-radius: 14px;
        font-weight: 800;
    }

</style>
""", unsafe_allow_html=True)

# ======================
# 4. HELPERS
# ======================
def fmt_m(x):
    return f"{x / 1_000_000:,.2f}M"


def fmt_m0(x):
    return f"{x / 1_000_000:,.0f}M"


def safe_div(a, b):
    return a / b if b else 0


def render_kpi_card(title, value, badge=None):
    badge_html = f'<div class="card-badge">{badge}</div>' if badge else ""
    st.markdown(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            {badge_html}
        </div>
    """, unsafe_allow_html=True)


def render_progress_card(title, actual_text, target_text, rate):
    pct = rate * 100
    pct_show = max(0, min(pct, 100))

    st.markdown(f"""
        <div class="section-card">
            <div class="progress-title">{title}</div>
            <div class="progress-sub">Thực hiện: {actual_text} / {target_text}</div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{pct_show}%;"></div>
                <div class="progress-dot" style="left:{pct_show}%;"></div>
                <div class="progress-label" style="left:{pct_show}%;">{pct:.2f}%</div>
            </div>
            <div class="progress-scale">
                <span>0%</span>
                <span>100%</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_mini_kpi(title, value, badge=None):
    badge_html = f'<div class="mini-kpi-badge">{badge}</div>' if badge else ""
    st.markdown(f"""
        <div class="mini-kpi">
            <div class="mini-kpi-title">{title}</div>
            <div class="mini-kpi-value">{value}</div>
            {badge_html}
        </div>
    """, unsafe_allow_html=True)


# ======================
# 5. FILES + TARGETS
# ======================
WORKSHOP_FILES = {
    "Đà Nẵng": Path("dn1307.xlsx"),
    "Hà Nội - Phạm Văn Đồng": Path("hn_pvd_2026_07.xlsx"),
}

TARGETS = {
    ("Đà Nẵng", 2026, 7): {
        "ro": 488,
        "revenue": 1_105_000_000,
    },
    ("Hà Nội - Phạm Văn Đồng", 2026, 7): {
        "ro": 538,
        "revenue": 1_601_000_000,
    },
}

WORKING_DAYS = 25

# ======================
# 6. LOAD DATA
# ======================
@st.cache_data
def load_data():
    all_data = []
    missing_files = []

    for workshop_name, file_path in WORKSHOP_FILES.items():
        if not file_path.exists():
            missing_files.append(str(file_path))
            continue

        df = pd.read_excel(file_path)
        data = df.copy()

        data = data.rename(columns={
            "Số": "ro",
            "Trạng thái": "trang_thai",
            "Ngày hóa đơn": "ngay_hoa_don",
            "Tổng trước thuế": "doanh_thu_truoc_thue",
            "Tổng tiền": "tong_tien_sau_thue",
            "Hãng xe": "hang_xe",
            "Dòng xe": "dong_xe",
            "Khách hàng": "ten_khach_hang",
            "Khách hàng.1": "khach_hang_chi_tra",
            "Bảo hiểm": "bao_hiem_chi_tra"
        })

        required_columns = [
            "ro",
            "trang_thai",
            "ngay_hoa_don",
            "doanh_thu_truoc_thue",
            "tong_tien_sau_thue",
            "hang_xe",
        ]

        missing_columns = [
            col for col in required_columns
            if col not in data.columns
        ]

        if missing_columns:
            st.error(
                f"File {file_path.name} thiếu các cột: "
                + ", ".join(missing_columns)
            )
            st.stop()

        data["xuong"] = workshop_name
        data["ngay_hoa_don"] = pd.to_datetime(
            data["ngay_hoa_don"],
            errors="coerce",
            dayfirst=True
        )

        money_cols = [
            "doanh_thu_truoc_thue",
            "tong_tien_sau_thue",
            "khach_hang_chi_tra",
            "bao_hiem_chi_tra"
        ]

        for col in money_cols:
            if col not in data.columns:
                data[col] = 0
            data[col] = pd.to_numeric(
                data[col],
                errors="coerce"
            ).fillna(0)

        data["trang_thai"] = (
            data["trang_thai"]
            .astype(str)
            .str.strip()
        )

        data["hang_xe"] = (
            data["hang_xe"]
            .fillna("KHÔNG XÁC ĐỊNH")
            .astype(str)
            .str.upper()
            .str.strip()
        )

        data["hang_xe"] = data["hang_xe"].replace({
            "HUYNDAI": "HYUNDAI",
            "HYNDAI": "HYUNDAI",
            "MERCEDES BENZ": "MERCEDES-BENZ",
            "LYNK&CO": "LYNK & CO",
            "LYNK AND CO": "LYNK & CO"
        })

        all_data.append(data)

    if missing_files:
        st.error(
            "Không tìm thấy file dữ liệu: "
            + ", ".join(missing_files)
        )
        st.stop()

    if not all_data:
        st.error("Không có dữ liệu để hiển thị.")
        st.stop()

    return pd.concat(all_data, ignore_index=True)


data_raw = load_data()

# ======================
# 7. HOME PAGE + FILTER
# ======================
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

workshop_options = sorted(data_raw["xuong"].dropna().unique())

if not st.session_state.show_dashboard:
    st.markdown('<div class="landing-shell">', unsafe_allow_html=True)

    logo_path = Path("carpla_services_logo.png")
    if logo_path.exists():
        _, logo_col, _ = st.columns([1, 1.2, 1])
        with logo_col:
            st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown(
            "<div style='font-size:30px;font-weight:900;color:#172554;'>CARPLA SERVICES</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="landing-title">DASHBOARD QUẢN TRỊ DMS</div>
        <div class="landing-description">
            Dashboard tập trung theo dõi hiệu quả hoạt động của các xưởng trong toàn hệ thống
            Carpla Services, bao gồm lượt xe, doanh thu, cơ cấu hãng xe và nguồn thanh toán.
        </div>
        <div class="landing-filter-title">Chọn phạm vi dữ liệu để xem dashboard</div>
        """,
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        home_workshop = st.selectbox(
            "Xưởng",
            workshop_options,
            key="home_workshop"
        )

    home_workshop_data = data_raw[
        data_raw["xuong"] == home_workshop
    ].copy()

    home_year_options = sorted(
        home_workshop_data["ngay_hoa_don"]
        .dropna()
        .dt.year
        .unique(),
        reverse=True
    )

    with f2:
        home_year = st.selectbox(
            "Năm",
            home_year_options,
            key="home_year"
        )

    home_month_options = sorted(
        home_workshop_data.loc[
            home_workshop_data["ngay_hoa_don"].dt.year == home_year,
            "ngay_hoa_don"
        ]
        .dropna()
        .dt.month
        .unique()
    )

    with f3:
        home_month = st.selectbox(
            "Tháng",
            home_month_options,
            format_func=lambda x: f"Tháng {int(x)}",
            key="home_month"
        )

    _, button_col, _ = st.columns([1.2, 1, 1.2])
    with button_col:
        if st.button(
            "XEM DASHBOARD",
            type="primary",
            use_container_width=True
        ):
            st.session_state.selected_workshop = home_workshop
            st.session_state.selected_year = int(home_year)
            st.session_state.selected_month = int(home_month)
            st.session_state.show_dashboard = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

selected_workshop = st.session_state.selected_workshop
year = int(st.session_state.selected_year)
month = int(st.session_state.selected_month)

st.sidebar.markdown("## Bộ lọc đã chọn")
st.sidebar.write(f"**Xưởng:** {selected_workshop}")
st.sidebar.write(f"**Năm:** {year}")
st.sidebar.write(f"**Tháng:** {month}")

if st.sidebar.button("← Quay lại trang chủ", use_container_width=True):
    st.session_state.show_dashboard = False
    st.rerun()

workshop_data = data_raw[
    data_raw["xuong"] == selected_workshop
].copy()

target_info = TARGETS.get(
    (selected_workshop, int(year), int(month))
)

if target_info is None:
    st.warning(
        f"Chưa thiết lập target cho {selected_workshop}, "
        f"tháng {month}/{year}. Dashboard tạm dùng target bằng 0."
    )
    TARGET_RO = 0
    TARGET_REVENUE = 0
else:
    TARGET_RO = target_info["ro"]
    TARGET_REVENUE = target_info["revenue"]

data = workshop_data[
    (workshop_data["ngay_hoa_don"].dt.year == year) &
    (workshop_data["ngay_hoa_don"].dt.month == month)
].copy()

exclude_status = [
    "Báo giá",
    "Hủy",
    "Không thực hiện",
    "Không duyệt",
    "Nháp"
]

data = data[~data["trang_thai"].isin(exclude_status)]
data = data[data["doanh_thu_truoc_thue"] > 0]

# ======================
# 8. KPI TOP
# ======================
actual_ro = data["ro"].nunique()
actual_revenue = data["doanh_thu_truoc_thue"].sum()
total_after_tax = data["tong_tien_sau_thue"].sum()
revenue_per_ro = safe_div(actual_revenue, actual_ro)

ro_rate = safe_div(actual_ro, TARGET_RO)
revenue_rate = safe_div(actual_revenue, TARGET_REVENUE)

# ======================
# 9. HERO
# ======================
st.markdown(f"""
    <div class="hero-box">
        <div class="hero-title">Dashboard DMS - Xưởng {selected_workshop}</div>
        <div class="hero-subtitle">
            Theo dõi hiệu quả hoạt động tháng {month}/{year}: lượt xe, doanh thu, cơ cấu hãng xe và nguồn thanh toán
        </div>
    </div>
""", unsafe_allow_html=True)

# ======================
# 10. TOP KPI CARDS
# ======================
c1, c2, c3, c4 = st.columns(4)

with c1:
    render_kpi_card(
        "Lượt xe / RO",
        f"{actual_ro:,.0f}",
        f"Target: {TARGET_RO:,.0f} | Đạt: {ro_rate:.2%}"
    )

with c2:
    render_kpi_card(
        "Doanh thu trước thuế",
        fmt_m(actual_revenue),
        f"Target: {TARGET_REVENUE / 1_000_000:,.0f}M | Đạt: {revenue_rate:.2%}"
    )

with c3:
    render_kpi_card(
        "Tổng tiền sau thuế",
        fmt_m(total_after_tax)
    )

with c4:
    render_kpi_card(
        "DT trước thuế / RO",
        fmt_m(revenue_per_ro)
    )

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# ======================
# 11. SECTION 1 - TARGET / ACTUAL
# ======================
st.markdown("## 1. Lượt xe và doanh thu: Chỉ tiêu / Thực hiện")

p1, p2 = st.columns(2)

with p1:
    render_progress_card(
        "Lượt xe / RO",
        f"{actual_ro:,.0f}",
        f"{TARGET_RO:,.0f}",
        ro_rate
    )

with p2:
    render_progress_card(
        "Doanh thu trước thuế",
        fmt_m(actual_revenue),
        fmt_m0(TARGET_REVENUE),
        revenue_rate
    )

summary_kpi = pd.DataFrame({
    "Chỉ tiêu": ["Lượt xe / RO", "Doanh thu trước thuế"],
    "Target": [
        f"{TARGET_RO:,.0f}",
        fmt_m0(TARGET_REVENUE)
    ],
    "Thực hiện": [
        f"{actual_ro:,.0f}",
        fmt_m(actual_revenue)
    ],
    "% đạt": [
        f"{ro_rate:.2%}",
        f"{revenue_rate:.2%}"
    ]
})

st.dataframe(summary_kpi, use_container_width=True, hide_index=True)

# ======================
# 12. DAILY DATA
# ======================
st.markdown("## 2. Lượt xe & doanh thu theo ngày")

days_in_month = calendar.monthrange(year, month)[1]
days = list(range(1, days_in_month + 1))

daily = (
    data.dropna(subset=["ngay_hoa_don"])
    .assign(day=lambda x: x["ngay_hoa_don"].dt.day)
    .groupby("day")
    .agg(
        ro=("ro", "nunique"),
        revenue=("doanh_thu_truoc_thue", "sum")
    )
    .reindex(days, fill_value=0)
    .reset_index()
)

daily["revenue_m"] = daily["revenue"] / 1_000_000
daily["cum_ro"] = daily["ro"].cumsum()
daily["cum_revenue"] = daily["revenue"].cumsum()

target_ro_day = TARGET_RO / WORKING_DAYS
target_revenue_day = TARGET_REVENUE / WORKING_DAYS

daily["target_cum_ro"] = [
    target_ro_day * min(d, WORKING_DAYS)
    for d in daily["day"]
]

daily["target_cum_revenue"] = [
    target_revenue_day * min(d, WORKING_DAYS)
    for d in daily["day"]
]

daily["cum_ro_pct"] = daily["cum_ro"] / daily["target_cum_ro"] * 100
daily["cum_revenue_pct"] = daily["cum_revenue"] / daily["target_cum_revenue"] * 100

daily["cum_ro_pct"] = daily["cum_ro_pct"].replace([float("inf"), -float("inf")], 0).fillna(0)
daily["cum_revenue_pct"] = daily["cum_revenue_pct"].replace([float("inf"), -float("inf")], 0).fillna(0)

total_ro = daily["ro"].sum()
total_revenue = daily["revenue"].sum()

actual_ro_avg = total_ro / WORKING_DAYS
actual_revenue_avg = total_revenue / WORKING_DAYS

ro_vs_target = safe_div(total_ro, TARGET_RO) - 1
revenue_vs_target = safe_div(total_revenue, TARGET_REVENUE) - 1
revenue_per_cpus = safe_div(total_revenue, total_ro)

chart_col, side_col = st.columns([4.6, 1.25])

with chart_col:
    # CHART 1 - RO
    fig_ro = make_subplots(specs=[[{"secondary_y": True}]])

    fig_ro.add_trace(
        go.Bar(
            x=daily["day"],
            y=daily["ro"],
            marker=dict(
                color=PRIMARY_BLUE,
                line=dict(color=PRIMARY_BLUE_LIGHT, width=1)
            ),
            name="RO/ngày",
            text=[f"{int(v)}" if v > 0 else "" for v in daily["ro"]],
            textposition="outside",
            textfont=dict(color=BAR_LABEL_COLOR, size=12)
        ),
        secondary_y=False
    )

    fig_ro.add_trace(
        go.Scatter(
            x=daily["day"],
            y=daily["cum_ro_pct"],
            mode="lines+markers+text",
            line=dict(color=LINE_BLUE, width=2.5, dash="dot"),
            marker=dict(
                size=6,
                color=LINE_BLUE_SOFT,
                line=dict(color="#D7EAFE", width=1)
            ),
            text=[f"{v:.0f}%" if v > 0 else "" for v in daily["cum_ro_pct"]],
            textposition="bottom center",
            textfont=dict(size=10, color=PCT_TEXT_COLOR),
            name="% đạt lũy kế"
        ),
        secondary_y=True
    )

    fig_ro.update_layout(
        template="plotly_dark",
        height=370,
        paper_bgcolor=DARK_PANEL,
        plot_bgcolor=DARK_PANEL,
        font=dict(color=WHITE),
        margin=dict(l=30, r=30, t=65, b=40),
        showlegend=False,
        title=dict(
            text=f"CPUS DAILY - {selected_workshop.upper()}",
            x=0.5,
            font=dict(size=19, color=WHITE)
        )
    )

    fig_ro.update_xaxes(
        tickmode="array",
        tickvals=days,
        showgrid=False,
        color="rgba(248,250,252,0.85)",
        linecolor="rgba(255,255,255,0.22)"
    )

    fig_ro.update_yaxes(
        showgrid=True,
        gridcolor=DARK_GRID,
        color="rgba(248,250,252,0.85)",
        zeroline=False,
        secondary_y=False
    )

    fig_ro.update_yaxes(
        range=[0, 300],
        ticksuffix="%",
        showgrid=False,
        color="rgba(248,250,252,0.85)",
        zeroline=False,
        secondary_y=True
    )

    st.plotly_chart(fig_ro, use_container_width=True)

    # CHART 2 - REVENUE
    fig_rev = make_subplots(specs=[[{"secondary_y": True}]])

    fig_rev.add_trace(
        go.Bar(
            x=daily["day"],
            y=daily["revenue_m"],
            marker=dict(
                color=PRIMARY_BLUE,
                line=dict(color=PRIMARY_BLUE_LIGHT, width=1)
            ),
            name="Doanh thu/ngày",
            text=[f"{v:.0f}M" if v > 0 else "" for v in daily["revenue_m"]],
            textposition="outside",
            textfont=dict(color=BAR_LABEL_COLOR, size=12)
        ),
        secondary_y=False
    )

    fig_rev.add_trace(
        go.Scatter(
            x=daily["day"],
            y=daily["cum_revenue_pct"],
            mode="lines+markers+text",
            line=dict(color=LINE_BLUE, width=2.5, dash="dot"),
            marker=dict(
                size=6,
                color=LINE_BLUE_SOFT,
                line=dict(color="#D7EAFE", width=1)
            ),
            text=[f"{v:.0f}%" if v > 0 else "" for v in daily["cum_revenue_pct"]],
            textposition="bottom center",
            textfont=dict(size=10, color=PCT_TEXT_COLOR),
            name="% đạt lũy kế"
        ),
        secondary_y=True
    )

    fig_rev.update_layout(
        template="plotly_dark",
        height=370,
        paper_bgcolor=DARK_PANEL,
        plot_bgcolor=DARK_PANEL,
        font=dict(color=WHITE),
        margin=dict(l=30, r=30, t=65, b=40),
        showlegend=False,
        title=dict(
            text=f"DOANH THU DAILY - {selected_workshop.upper()}",
            x=0.5,
            font=dict(size=19, color=WHITE)
        )
    )

    fig_rev.update_xaxes(
        tickmode="array",
        tickvals=days,
        showgrid=False,
        color="rgba(248,250,252,0.85)",
        linecolor="rgba(255,255,255,0.22)"
    )

    fig_rev.update_yaxes(
        showgrid=True,
        gridcolor=DARK_GRID,
        color="rgba(248,250,252,0.85)",
        zeroline=False,
        secondary_y=False
    )

    fig_rev.update_yaxes(
        range=[0, 300],
        ticksuffix="%",
        showgrid=False,
        color="rgba(248,250,252,0.85)",
        zeroline=False,
        secondary_y=True
    )

    st.plotly_chart(fig_rev, use_container_width=True)

with side_col:
    render_mini_kpi("DT TB/CPUS", fmt_m(revenue_per_cpus))
    render_mini_kpi("CPUS TB/NGÀY", f"{actual_ro_avg:.0f}")
    render_mini_kpi("CPUS TB/NGÀY TARGET", f"{target_ro_day:.0f}")
    render_mini_kpi(
        "CPUS VS TARGET",
        f"{total_ro:,.0f}",
        f"Target: {TARGET_RO:,.0f} | {ro_vs_target:.2%}"
    )
    render_mini_kpi("DT TB/NGÀY", fmt_m(actual_revenue_avg))
    render_mini_kpi("DT TB/NGÀY TARGET", fmt_m(target_revenue_day))
    render_mini_kpi(
        "DOANH THU VS TARGET",
        fmt_m0(total_revenue),
        f"Target: {fmt_m0(TARGET_REVENUE)} | {revenue_vs_target:.2%}"
    )

# ======================
# 13. SECTION 3 - BRAND
# ======================
st.markdown("## 3. Hãng xe")

brand_summary = (
    data.groupby("hang_xe")
    .agg(
        so_ro=("ro", "nunique"),
        doanh_thu=("doanh_thu_truoc_thue", "sum")
    )
    .reset_index()
    .sort_values("doanh_thu", ascending=False)
)

total_ro_brand = brand_summary["so_ro"].sum()
total_revenue_brand = brand_summary["doanh_thu"].sum()

brand_summary["ty_trong_ro"] = brand_summary["so_ro"] / total_ro_brand
brand_summary["ty_trong_doanh_thu"] = brand_summary["doanh_thu"] / total_revenue_brand

brand_display = brand_summary.copy()
brand_display["doanh_thu"] = brand_display["doanh_thu"].map(fmt_m)
brand_display["ty_trong_ro"] = brand_display["ty_trong_ro"].map(lambda x: f"{x:.2%}")
brand_display["ty_trong_doanh_thu"] = brand_display["ty_trong_doanh_thu"].map(lambda x: f"{x:.2%}")

brand_display = brand_display.rename(columns={
    "hang_xe": "Hãng xe",
    "so_ro": "Số RO",
    "doanh_thu": "Doanh thu trước thuế",
    "ty_trong_ro": "Tỷ trọng RO",
    "ty_trong_doanh_thu": "Tỷ trọng doanh thu"
})

total_brand_row = pd.DataFrame({
    "Hãng xe": ["TỔNG"],
    "Số RO": [total_ro_brand],
    "Doanh thu trước thuế": [fmt_m(total_revenue_brand)],
    "Tỷ trọng RO": ["100.00%"],
    "Tỷ trọng doanh thu": ["100.00%"]
})

brand_display = pd.concat([brand_display, total_brand_row], ignore_index=True)

left_brand, right_brand = st.columns([1.35, 1])

with left_brand:
    st.markdown('<div class="section-label">Bảng chi tiết theo hãng xe</div>', unsafe_allow_html=True)
    st.dataframe(brand_display, use_container_width=True, hide_index=True)

with right_brand:
    st.markdown('<div class="section-label">Top hãng xe theo doanh thu</div>', unsafe_allow_html=True)

    brand_chart = brand_summary.head(10).sort_values("doanh_thu", ascending=True).copy()
    brand_chart["doanh_thu_m"] = brand_chart["doanh_thu"] / 1_000_000

    color_list = MUTED_BAR_COLORS[:len(brand_chart)]

    fig_brand = go.Figure()

    fig_brand.add_trace(go.Bar(
        x=brand_chart["doanh_thu_m"],
        y=brand_chart["hang_xe"],
        orientation="h",
        marker=dict(
            color=color_list,
            line=dict(color="#E5ECF6", width=0.5)
        ),
        text=[f"{x:.1f}M" for x in brand_chart["doanh_thu_m"]],
        textposition="outside",
        textfont=dict(color="#667085", size=12),
        hovertemplate="<b>%{y}</b><br>Doanh thu: %{x:.2f}M<extra></extra>"
    ))

    fig_brand.update_layout(
        template="simple_white",
        height=450,
        margin=dict(l=10, r=40, t=10, b=30),
        xaxis_title="Doanh thu trước thuế (M)",
        yaxis_title="",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#475467"),
        showlegend=False
    )

    fig_brand.update_xaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=False,
        title_font=dict(color="#667085"),
        tickfont=dict(color="#667085")
    )

    fig_brand.update_yaxes(
        showgrid=False,
        tickfont=dict(color="#667085")
    )

    st.plotly_chart(fig_brand, use_container_width=True)

# ======================
# 14. SECTION 4 - PAYMENT STRUCTURE
# ======================
st.markdown("## 4. Cơ cấu nguồn thanh toán")

bao_hiem_value = data["bao_hiem_chi_tra"].sum()
khach_hang_value = data["tong_tien_sau_thue"].sum() - bao_hiem_value

payment_structure = pd.DataFrame({
    "Nguồn thanh toán": ["Bảo hiểm chi trả", "Khách hàng chi trả"],
    "Giá trị": [bao_hiem_value, khach_hang_value]
})

total_payment = payment_structure["Giá trị"].sum()
payment_structure["Tỷ trọng"] = payment_structure["Giá trị"].apply(
    lambda value: safe_div(value, total_payment)
)

payment_display = payment_structure.copy()
payment_display["Giá trị"] = payment_display["Giá trị"].map(fmt_m)
payment_display["Tỷ trọng"] = payment_display["Tỷ trọng"].map(lambda x: f"{x:.2%}")

total_payment_row = pd.DataFrame({
    "Nguồn thanh toán": ["TỔNG"],
    "Giá trị": [fmt_m(total_payment)],
    "Tỷ trọng": ["100.00%"]
})

payment_display = pd.concat([payment_display, total_payment_row], ignore_index=True)

left_pay, right_pay = st.columns([1, 1])

with left_pay:
    st.markdown('<div class="section-label">Bảng cơ cấu nguồn thanh toán</div>', unsafe_allow_html=True)
    st.dataframe(payment_display, use_container_width=True, hide_index=True)

with right_pay:
    st.markdown('<div class="section-label">Tỷ trọng nguồn thanh toán</div>', unsafe_allow_html=True)

    fig_payment = go.Figure(data=[go.Pie(
        labels=["Khách hàng chi trả", "Bảo hiểm chi trả"],
        values=[khach_hang_value, bao_hiem_value],
        hole=0.58,
        marker=dict(colors=[DONUT_MAIN, DONUT_SECOND]),
        textinfo="percent",
        textfont=dict(size=15, color="white"),
        domain=dict(
            x=[0.08, 0.78],
            y=[0.10, 0.90]
        ),
        hovertemplate="<b>%{label}</b><br>Giá trị: %{value:,.0f}<br>Tỷ trọng: %{percent}<extra></extra>"
    )])

    fig_payment.update_layout(
        template="simple_white",
        height=410,
        margin=dict(l=10, r=20, t=10, b=10),
        legend=dict(
            orientation="v",
            y=0.5,
            yanchor="middle",
            x=0.82,
            xanchor="left",
            font=dict(color="#475467")
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#475467")
    )

    st.plotly_chart(fig_payment, use_container_width=True)

# ======================
# 15. CHECK TOTAL
# ======================
with st.expander("Kiểm tra đối chiếu tổng"):
    st.write("Tổng doanh thu trước thuế:", fmt_m(actual_revenue))
    st.write("Tổng tiền sau thuế:", fmt_m(total_after_tax))
    st.write("Tổng cơ cấu nguồn thanh toán:", fmt_m(total_payment))
    st.write("Chênh lệch:", fmt_m(total_after_tax - total_payment))

# ======================
# 16. RAW DATA
# ======================
with st.expander("Xem dữ liệu chi tiết"):
    st.dataframe(data, use_container_width=True)