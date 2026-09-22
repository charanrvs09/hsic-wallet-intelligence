from pathlib import Path
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="HSIC Wallet Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"


NAVIGATION = {
    "▦  Dashboard": "Dashboard",
    "↔  Portfolio & Migration": "Portfolio & Migration",
    "◫  Customer Segmentation": "Customer Segmentation",
    "◎  Opportunity Explorer": "Opportunity Explorer",
    "◒  Recovery Simulator": "Recovery Simulator",
}


SEGMENT_COLORS = {
    "HSIC-First Adopters": "#7BCB63",
    "Active HSIC Growers": "#1D4ED8",
    "Wallet Migrators": "#F2B84B",
}


CAMPAIGN_COLORS = {
    "HSIC Champions": "#71C562",
    "Growing HSIC Users": "#2563EB",
    "High-Value Dormant": "#E05B55",
    "High-Value Silent Decliners": "#E58B43",
    "Dormant Reactivation": "#8B5CF6",
    "Silent Decliners": "#D8A52B",
    "High-Value Low-SoW": "#2AA7A1",
    "General Growth": "#8A94A6",
}


PLOT_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
    "responsive": True,
}


st.markdown(
    """
    <style>
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        height: 0rem;
        background: transparent;
    }

    .stApp {
        background: #F7F8F5;
        color: #111827;
    }

    .block-container {
        max-width: 1540px;
        padding-top: 1.6rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #F1F8ED 0%,
                #F7FAF5 100%
            );
        border-right: 1px solid #E4E8E0;
        width: 240px !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.4rem;
    }

    section[data-testid="stSidebar"] * {
        color: #26322A;
    }

    div[role="radiogroup"] {
        gap: 0.25rem;
    }

    div[role="radiogroup"] label {
        padding: 0.72rem 0.72rem;
        border-radius: 14px;
        transition: all 0.18s ease;
    }

    div[role="radiogroup"] label:hover {
        background: #E8F3E2;
    }

    div[role="radiogroup"] label:has(input:checked) {
        background: #B8F58F;
    }

    div[role="radiogroup"] label:has(input:checked) p {
        color: #17231A !important;
        font-weight: 700 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E3E7E0 !important;
        border-radius: 20px !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 18px rgba(30, 41, 35, 0.035);
    }

    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 1.35rem;
        padding-left: 0.2rem;
    }

    .brand-mark {
        width: 35px;
        height: 35px;
        border-radius: 11px;
        background: #071A43;
        color: #B8F58F;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 900;
    }

    .brand-name {
        font-size: 1.05rem;
        line-height: 1.05rem;
        font-weight: 800;
        color: #111827;
    }

    .brand-sub {
        color: #66726A;
        font-size: 0.67rem;
        margin-top: 0.2rem;
    }

    .sidebar-label {
        font-size: 0.68rem;
        font-weight: 700;
        color: #8A948D;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding-left: 0.55rem;
        margin-bottom: 0.25rem;
    }

    .sidebar-scope {
        padding: 0.9rem 0.8rem;
        margin-top: 0.9rem;
        background: rgba(255, 255, 255, 0.56);
        border: 1px solid #DCE6D7;
        border-radius: 16px;
    }

    .sidebar-scope-title {
        font-size: 0.73rem;
        font-weight: 800;
        color: #26322A;
        margin-bottom: 0.55rem;
    }

    .sidebar-scope-item {
        font-size: 0.72rem;
        color: #68746C;
        line-height: 1.55rem;
    }

    .sidebar-footer-card {
        margin-top: 1.4rem;
        padding: 1.05rem;
        background: #071A43;
        border-radius: 19px;
        color: white;
    }

    .sidebar-footer-card b {
        color: white;
        font-size: 0.78rem;
    }

    .sidebar-footer-card span {
        display: block;
        color: #C8D0E0;
        margin-top: 0.45rem;
        font-size: 0.68rem;
        line-height: 1.1rem;
    }

    .page-top {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 1.35rem;
    }

    .page-title {
        font-size: 1.82rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.04rem;
        margin: 0;
    }

    .page-subtitle {
        color: #737F77;
        font-size: 0.82rem;
        margin-top: 0.3rem;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.57rem 0.85rem;
        background: white;
        border: 1px solid #E3E7E0;
        border-radius: 999px;
        font-size: 0.72rem;
        color: #536057;
        box-shadow: 0 2px 8px rgba(30, 41, 35, 0.03);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 100%;
        background: #72CF63;
        box-shadow: 0 0 0 4px #E5F7E1;
    }

    .featured-card {
        height: 152px;
        padding: 1.25rem 1.28rem;
        border-radius: 20px;
        background:
            radial-gradient(
                circle at 88% 15%,
                rgba(183, 245, 143, 0.2),
                transparent 22%
            ),
            linear-gradient(
                135deg,
                #071A43 0%,
                #0A225A 100%
            );
        color: white;
        box-shadow: 0 8px 24px rgba(7, 26, 67, 0.13);
    }

    .featured-label {
        color: #CFD8EB;
        font-size: 0.73rem;
        font-weight: 650;
    }

    .featured-value {
        color: white;
        font-size: 2rem;
        line-height: 2.15rem;
        font-weight: 800;
        margin-top: 0.9rem;
        letter-spacing: -0.05rem;
    }

    .featured-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #CFD8EB;
        font-size: 0.68rem;
        margin-top: 0.8rem;
    }

    .featured-chip {
        background: #B8F58F;
        color: #173019;
        border-radius: 999px;
        padding: 0.26rem 0.55rem;
        font-size: 0.65rem;
        font-weight: 800;
    }

    .kpi-card {
        height: 152px;
        padding: 1.15rem 1.15rem;
        background: #FFFFFF;
        border: 1px solid #E0E5DD;
        border-radius: 20px;
        box-shadow: 0 4px 18px rgba(30, 41, 35, 0.035);
    }

    .kpi-icon {
        width: 31px;
        height: 31px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F0F8EB;
        color: #274528;
        font-size: 0.85rem;
        margin-bottom: 0.65rem;
    }

    .kpi-label {
        color: #79837C;
        font-size: 0.71rem;
        font-weight: 650;
    }

    .kpi-value {
        color: #151A17;
        font-size: 1.55rem;
        font-weight: 800;
        margin-top: 0.28rem;
        letter-spacing: -0.04rem;
    }

    .kpi-delta {
        display: inline-block;
        margin-top: 0.42rem;
        padding: 0.18rem 0.43rem;
        border-radius: 999px;
        font-size: 0.61rem;
        font-weight: 800;
    }

    .delta-positive {
        color: #3A7C2E;
        background: #E1F7D8;
    }

    .delta-negative {
        color: #B53D3A;
        background: #FDE3E2;
    }

    .delta-neutral {
        color: #5F6D64;
        background: #EEF1ED;
    }

    .section-title {
        font-size: 1.02rem;
        font-weight: 800;
        color: #17201A;
        margin-top: 0.35rem;
        margin-bottom: 0.15rem;
    }

    .section-subtitle {
        color: #88928B;
        font-size: 0.7rem;
        margin-bottom: 0.8rem;
    }

    .mini-card {
        padding: 0.95rem;
        background: #FAFBF9;
        border: 1px solid #E7EAE5;
        border-radius: 15px;
        margin-bottom: 0.55rem;
    }

    .mini-label {
        color: #7A857E;
        font-size: 0.67rem;
        font-weight: 650;
    }

    .mini-value {
        color: #17201A;
        font-size: 1.02rem;
        font-weight: 800;
        margin-top: 0.2rem;
    }

    .insight-card {
        padding: 1.05rem;
        background: #F4FBEF;
        border: 1px solid #DAECD0;
        border-radius: 16px;
        color: #26322A;
    }

    .insight-card b {
        color: #19351B;
        font-size: 0.8rem;
    }

    .insight-card p {
        color: #627065;
        font-size: 0.71rem;
        line-height: 1.15rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    .alert-card {
        padding: 1.05rem;
        background: #FFF9EE;
        border: 1px solid #F3E3B9;
        border-radius: 16px;
        color: #3B3425;
    }

    .alert-card b {
        font-size: 0.8rem;
    }

    .alert-card p {
        color: #776B50;
        font-size: 0.71rem;
        line-height: 1.15rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    .strategy-card {
        padding: 1.15rem 1.25rem;
        background:
            linear-gradient(
                135deg,
                #071A43 0%,
                #0B2B72 100%
            );
        color: white;
        border-radius: 18px;
        margin-top: 0.65rem;
    }

    .strategy-card .eyebrow {
        color: #B8F58F;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
    }

    .strategy-card h4 {
        color: white;
        font-size: 0.95rem;
        margin-top: 0.45rem;
        margin-bottom: 0.25rem;
    }

    .strategy-card p {
        color: #D0D8E6;
        font-size: 0.72rem;
        line-height: 1.15rem;
        margin-bottom: 0;
    }

    .segment-card {
        min-height: 178px;
        background: white;
        border: 1px solid #E2E7DF;
        border-radius: 19px;
        padding: 1.15rem;
        box-shadow: 0 4px 18px rgba(30, 41, 35, 0.03);
    }

    .segment-chip {
        display: inline-block;
        padding: 0.25rem 0.52rem;
        border-radius: 999px;
        background: #F0F5ED;
        color: #556258;
        font-size: 0.62rem;
        font-weight: 800;
    }

    .segment-card h3 {
        font-size: 0.95rem;
        margin-top: 0.75rem;
        margin-bottom: 0.12rem;
        color: #17201A;
    }

    .segment-card .segment-count {
        color: #89928C;
        font-size: 0.68rem;
    }

    .segment-card .segment-number {
        font-size: 1.45rem;
        font-weight: 800;
        color: #152018;
        margin-top: 0.72rem;
    }

    .flag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.55rem;
        margin-bottom: 0.8rem;
    }

    .flag-on {
        display: inline-block;
        padding: 0.28rem 0.55rem;
        border-radius: 999px;
        background: #FDE7E5;
        color: #B74440;
        font-size: 0.65rem;
        font-weight: 750;
    }

    .flag-off {
        display: inline-block;
        padding: 0.28rem 0.55rem;
        border-radius: 999px;
        background: #EAF6E5;
        color: #417A35;
        font-size: 0.65rem;
        font-weight: 750;
    }

    .soft-note {
        padding: 0.85rem 1rem;
        border-radius: 14px;
        background: #F9FAF8;
        border: 1px solid #E7EAE5;
        color: #707B73;
        font-size: 0.7rem;
        line-height: 1.1rem;
    }

    div[data-baseweb="select"] > div {
        border-radius: 13px !important;
        border-color: #E0E5DD !important;
        background: white !important;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 13px !important;
        border: 1px solid #E0E5DD !important;
        background: white !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E9E2;
        border-radius: 15px;
        overflow: hidden;
    }

    .stButton button {
        border-radius: 12px;
        background: #B8F58F;
        border: 0;
        color: #183018;
        font-weight: 800;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .featured-card,
        .kpi-card {
            height: auto;
            min-height: 135px;
        }
    }

    .account-panel {
        background: #FFFFFF;
        border: 1px solid #E1E6DE;
        border-radius: 16px;
        padding: 0.7rem 0.8rem;
        box-shadow: 0 3px 12px rgba(30, 41, 35, 0.035);
    }

    .account-topline {
        color: #97A198;
        font-size: 0.58rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.42rem;
    }

    .account-row {
        display: flex;
        align-items: center;
        gap: 0.58rem;
    }

    .account-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #071A43;
        color: #B8F58F;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.68rem;
        font-weight: 900;
        flex-shrink: 0;
    }

    .account-name {
        color: #17201A;
        font-size: 0.72rem;
        font-weight: 800;
        line-height: 1rem;
    }

    .account-role {
        color: #7D8980;
        font-size: 0.6rem;
        line-height: 0.86rem;
    }

    .account-email {
        color: #A0A8A2;
        font-size: 0.54rem;
        line-height: 0.82rem;
    }

    div[data-testid="stToggle"] {
        margin-top: -0.15rem;
    }

    div[data-testid="stToggle"] label p {
        color: #6F7A72;
        font-size: 0.66rem;
        font-weight: 700;
    }

    div[data-testid="stForm"] {
        border: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 46px;
        border: 0;
        border-radius: 13px;
        background: #071A43;
        color: #FFFFFF;
        font-weight: 800;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: #0B2B72;
        color: #FFFFFF;
        border: 0;
    }

    .login-brand-card {
        min-height: 470px;
        padding: 2.2rem 2.25rem;
        border-radius: 26px;
        background:
            radial-gradient(
                circle at 86% 16%,
                rgba(184, 245, 143, 0.22),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #071A43 0%,
                #0B2B72 100%
            );
        box-shadow: 0 16px 44px rgba(7, 26, 67, 0.13);
    }

    .login-logo {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: #B8F58F;
        color: #071A43;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 900;
        margin-bottom: 3rem;
    }

    .login-brand-card h1 {
        color: #FFFFFF;
        font-size: 2.25rem;
        line-height: 2.5rem;
        letter-spacing: -0.055rem;
        margin: 0 0 0.9rem 0;
    }

    .login-brand-card p {
        max-width: 440px;
        color: #CFD8E8;
        font-size: 0.86rem;
        line-height: 1.42rem;
        margin-bottom: 2.15rem;
    }

    .login-feature {
        color: #DBE3EF;
        font-size: 0.74rem;
        margin-top: 0.8rem;
    }

    .login-feature {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-top: 1rem;
    color: #E4EAF4;
    font-size: 0.82rem;
    line-height: 1.2rem;
}

.login-feature span {
    min-width: 32px;
    height: 32px;
    border-radius: 9px;
    background: rgba(184, 245, 143, 0.14);
    color: #B8F58F;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.69rem;
    font-weight: 800;
}

    .login-feature span {
        display: inline-block;
        width: 24px;
        color: #B8F58F;
        font-weight: 900;
    }

    .login-form-wrap {
        padding: 3.6rem 1.2rem 1rem 1.2rem;
    }

    .login-title {
        color: #111827;
        font-size: 1.75rem;
        font-weight: 850;
        letter-spacing: -0.035rem;
        margin-bottom: 0.22rem;
    }

    .login-subtitle {
        color: #7A857E;
        font-size: 0.78rem;
        margin-bottom: 1.35rem;
    }

    .login-security {
        margin-top: 0.9rem;
        color: #929B94;
        font-size: 0.64rem;
        line-height: 1rem;
    }


    .auth-demo-note {
        margin-top: 0.85rem;
        padding: 0.78rem 0.9rem;
        border: 1px solid #DDE8D7;
        background: #F5FAF2;
        border-radius: 13px;
        color: #68756B;
        font-size: 0.65rem;
        line-height: 1rem;
    }

    .auth-demo-note strong {
        color: #2F5131;
    }

    .auth-mode-label {
        margin-top: 1rem;
        margin-bottom: 0.45rem;
        color: #8C968F;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }

    div[data-testid="stTabs"] button {
        font-size: 0.75rem;
        font-weight: 800;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #071A43;
    }

    </style>
    """,
    unsafe_allow_html=True,
)



@st.cache_data
def load_data():
    executive = pd.read_csv(
        DATA_DIR / "final_executive_kpis.csv"
    )

    fiscal = pd.read_csv(
        DATA_DIR / "fiscal_year_sow.csv"
    )

    monthly = pd.read_csv(
        DATA_DIR / "monthly_sow.csv"
    )

    payments = pd.read_csv(
        DATA_DIR / "payment_analysis.csv"
    )

    segments = pd.read_csv(
        DATA_DIR / "business_segment_summary.csv"
    )

    campaign_summary = pd.read_csv(
        DATA_DIR / "campaign_segment_summary.csv"
    )

    campaign_value = pd.read_csv(
        DATA_DIR / "campaign_segment_value.csv"
    )

    impact = pd.read_csv(
        DATA_DIR / "final_impact_display.csv"
    )

    customers = pd.read_csv(
        DATA_DIR / "dashboard_customers.csv"
    )

    leakage = pd.read_csv(
        DATA_DIR / "leakage_strategy.csv"
    )

    monthly["Month_Start"] = pd.to_datetime(
        monthly["Month_Start"]
    )

    customers["Primary_Leakage_Method"] = (
        customers["Primary_Leakage_Method"]
        .fillna("No Significant Leakage")
    )

    customers["Top_Category"] = (
        customers["Top_Category"]
        .fillna("Not Available")
        .replace({
            "Large Applicances": "Large Appliances"
        })
    )

    return {
        "executive": executive,
        "fiscal": fiscal,
        "monthly": monthly,
        "payments": payments,
        "segments": segments,
        "campaign_summary": campaign_summary,
        "campaign_value": campaign_value,
        "impact": impact,
        "customers": customers,
        "leakage": leakage,
    }


data = load_data()

executive = data["executive"]
fiscal = data["fiscal"]
monthly = data["monthly"]
payments = data["payments"]
segments = data["segments"]
campaign_summary = data["campaign_summary"]
campaign_value = data["campaign_value"]
impact = data["impact"]
customers = data["customers"]
leakage = data["leakage"]


campaigns = campaign_value.merge(
    campaign_summary[
        [
            "Campaign_Segment",
            "Customer_Share_Pct",
        ]
    ],
    on="Campaign_Segment",
    how="left",
)
segment_lookup = segments.set_index(
    "Business_Segment",
    drop=False,
)


def executive_value(kpi_name):
    row = executive.loc[
        executive["KPI"] == kpi_name,
        "Value",
    ]

    if row.empty:
        return "—"

    return str(row.iloc[0])


def format_inr(value):
    if pd.isna(value):
        return "—"

    value = float(value)

    if abs(value) >= 10_000_000:
        return f"₹{value / 10_000_000:.2f} Cr"

    if abs(value) >= 100_000:
        return f"₹{value / 100_000:.2f} L"

    return f"₹{value:,.0f}"


def metric_card(
    label,
    value,
    icon="↗",
    delta=None,
    delta_type="neutral",
):
    delta_html = ""

    if delta is not None:
        delta_html = (
            f'<div class="kpi-delta delta-{delta_type}">'
            f"{delta}</div>"
        )

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def featured_card(
    label,
    value,
    baseline,
    delta,
):
    st.markdown(
        f"""
        <div class="featured-card">
            <div class="featured-label">{label}</div>
            <div class="featured-value">{value}</div>
            <div class="featured-meta">
                <span>Baseline {baseline}</span>
                <span class="featured-chip">{delta}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, subtitle=None):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )

    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="page-top">
            <div>
                <div class="page-title">
                    {html.escape(title)}
                </div>
                <div class="page-subtitle">
                    {html.escape(subtitle)}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_figure(
    fig,
    height=370,
):
    fig.update_layout(
        height=height,
        margin=dict(
            l=15,
            r=15,
            t=55,
            b=18,
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=11,
            color="#667069",
        ),
        title=dict(
            font=dict(
                size=14,
                color="#17201A",
            ),
            x=0.02,
            xanchor="left",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
        ),
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E5E9E2",
        tickfont=dict(
            color="#7D8780",
            size=10,
        ),
        title_font=dict(
            color="#6D776F",
            size=10,
        ),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF0EB",
        zeroline=False,
        linecolor="#E5E9E2",
        tickfont=dict(
            color="#7D8780",
            size=10,
        ),
        title_font=dict(
            color="#6D776F",
            size=10,
        ),
    )

    return fig


def render_segment_card(row):
    st.markdown(
        f"""
        <div class="segment-card">
            <span class="segment-chip">
                {row["Customer_Share_Pct"]:.1f}% of cohort
            </span>
            <h3>{row["Business_Segment"]}</h3>
            <div class="segment-count">
                {int(row["Customers"]):,} customers
            </div>
            <div class="segment-number">
                {
    f"{row['Avg_Recent_SoW']:.2f}%"
    if row["Avg_Recent_SoW"] < 1
    else f"{row['Avg_Recent_SoW']:.1f}%"
}
            </div>
            <div class="mini-label">
                Recent HSIC Share of Wallet
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-mark">◈</div>
            <div>
                <div class="brand-name">HSIC Intelligence</div>
                <div class="brand-sub">
                    Wallet Recovery Platform
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    selected_label = st.radio(
        "Navigation",
        list(NAVIGATION.keys()),
        label_visibility="collapsed",
    )

    page = NAVIGATION[selected_label]

    st.markdown(
        """
        <div class="sidebar-scope">
            <div class="sidebar-scope-title">
                Analysis Scope
            </div>
            <div class="sidebar-scope-item">
                ◷ &nbsp; Aug 2024 – Jul 2026
            </div>
            <div class="sidebar-scope-item">
                ◫ &nbsp; Fiscal Year: Aug – Jul
            </div>
            <div class="sidebar-scope-item">
                ◎ &nbsp; 14,503 modeled customers
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
    """
    <div class="sidebar-footer-card">
        <b>Decision Intelligence</b>
        <span>
            Customer behavior, wallet migration
            and targeted recovery insights.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)




if page == "Dashboard":
    page_header(
        "Dashboard",
        (
            "Portfolio health, silent attrition and "
            "wallet-recovery opportunities at a glance."
        ),
    )

    top_1, top_2, top_3, top_4 = st.columns(
        [1.35, 1, 1, 1]
    )

    with top_1:
        featured_card(
            "Current HSIC Share of Wallet",
            executive_value(
                "FY2026 HSIC Share of Wallet"
            ),
            executive_value(
                "FY2025 HSIC Share of Wallet"
            ),
            executive_value(
                "Fiscal-Year SoW Decline"
            ),
        )

    with top_2:
        metric_card(
            "Silent Attriters",
            executive_value(
                "Silent Attrition Customers"
            ),
            icon="◎",
            delta=executive_value(
                "Silent Attrition Rate"
            )
            + " of cohort",
            delta_type="negative",
        )

    with top_3:
        metric_card(
            "Silent Attrition Wallet",
            executive_value(
                "Silent Attrition Addressable Wallet"
            ),
            icon="₹",
            delta="Recoverable opportunity",
            delta_type="positive",
        )

    with top_4:
        metric_card(
            "Wallet Migrator Opportunity",
            executive_value(
                "Wallet Migrator Addressable Wallet"
            ),
            icon="↗",
            delta=executive_value(
                "Wallet Migrator Customers"
            )
            + " customers",
            delta_type="neutral",
        )

    main_left, main_right = st.columns(
        [2.25, 1]
    )

    with main_left:
        with st.container(border=True):
            section_title(
                "HSIC Share-of-Wallet Trend",
                (
                    "Monthly portfolio trend across the "
                    "full analysis window"
                ),
            )

            monthly_fig = go.Figure()

            monthly_fig.add_trace(
                go.Scatter(
                    x=monthly["Month_Start"],
                    y=monthly["HSIC_SoW"],
                    mode="lines+markers",
                    name="HSIC SoW",
                    line=dict(
                        color="#123C9C",
                        width=3,
                    ),
                    marker=dict(
                        size=6,
                        color="#123C9C",
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(37, 99, 235, 0.06)",
                    hovertemplate=(
                        "%{x|%b %Y}<br>"
                        "HSIC SoW: %{y:.2f}%"
                        "<extra></extra>"
                    ),
                )
            )

            monthly_fig.update_yaxes(
                title="HSIC SoW (%)"
            )

            monthly_fig.update_xaxes(
                title=""
            )

            st.plotly_chart(
                style_figure(
                    monthly_fig,
                    height=355,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )

    with main_right:
        latest_fiscal = (
            fiscal.sort_values("Fiscal_Year")
            .iloc[-1]
        )

        with st.container(border=True):
            section_title(
                "Current Wallet Mix",
                "Latest fiscal year",
            )

            wallet_fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "HSIC",
                            "Non-HSIC",
                        ],
                        values=[
                            latest_fiscal[
                                "HSIC_Net_Sales"
                            ],
                            latest_fiscal[
                                "Non_HSIC_Net_Sales"
                            ],
                        ],
                        hole=0.72,
                        sort=False,
                        marker=dict(
                            colors=[
                                "#071A43",
                                "#B8F58F",
                            ]
                        ),
                        textinfo="none",
                        hovertemplate=(
                            "%{label}<br>"
                            "%{percent}<extra></extra>"
                        ),
                    )
                ]
            )

            wallet_fig.add_annotation(
                x=0.5,
                y=0.5,
                text=(
                    f"<b>"
                    f"{latest_fiscal['HSIC_SoW']:.1f}%"
                    f"</b><br>"
                    f"<span style='font-size:10px'>"
                    f"HSIC SoW"
                    f"</span>"
                ),
                showarrow=False,
                font=dict(
                    size=18,
                    color="#111827",
                ),
            )

            wallet_fig.update_layout(
                height=250,
                margin=dict(
                    l=5,
                    r=5,
                    t=10,
                    b=5,
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    y=-0.02,
                    x=0.5,
                    xanchor="center",
                ),
                paper_bgcolor="white",
            )

            st.plotly_chart(
                wallet_fig,
                width="stretch",
                config=PLOT_CONFIG,
            )

    insight_left, insight_mid, insight_right = st.columns(
        [1.1, 1.1, 1]
    )

    with insight_left:
        st.markdown(
            f"""
            <div class="insight-card">
                <b>MetroMart is growing</b>
                <p>
                    Net sales increased
                    <strong>
                    {executive_value("MetroMart Net Sales Growth")}
                    </strong>,
                    showing customers remain commercially active.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_mid:
        st.markdown(
            f"""
            <div class="alert-card">
                <b>HSIC spend is moving the other way</b>
                <p>
                    HSIC net spend changed
                    <strong>
                    {executive_value("HSIC Net Spend Growth")}
                    </strong>
                    while non-HSIC spend grew
                    <strong>
                    {executive_value("Non-HSIC Spend Growth")}
                    </strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_right:
        st.markdown(
            """
            <div class="strategy-card">
                <div class="eyebrow">Core Insight</div>
                <h4>Payment preference is shifting</h4>
                <p>
                    The customer is still shopping at MetroMart.
                    The wallet — not the shopper — is leaving HSIC.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_title(
        "Behavioral Segments",
        "Three customer patterns emerged from K-Means clustering",
    )

    seg_1, seg_2, seg_3 = st.columns(3)

    ordered_segments = [
        "HSIC-First Adopters",
        "Active HSIC Growers",
        "Wallet Migrators",
    ]


    for column, name in zip(
        [seg_1, seg_2, seg_3],
        ordered_segments,
    ):
        with column:
            if name in segment_lookup.index:
                render_segment_card(
                    segment_lookup.loc[name]
                )

    lower_left, lower_right = st.columns(
        [1.45, 1]
    )

    with lower_left:
        with st.container(border=True):
            section_title(
                "Customer Distribution",
                "Population by behavioral segment",
            )

            segment_fig = px.bar(
                segments.sort_values(
                    "Customers",
                    ascending=True,
                ),
                x="Customers",
                y="Business_Segment",
                orientation="h",
                color="Business_Segment",
                color_discrete_map=SEGMENT_COLORS,
                text="Customers",
            )

            segment_fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_line_width=0,
            )

            segment_fig.update_layout(
                showlegend=False,
            )

            segment_fig.update_xaxes(
                title="Customers"
            )

            segment_fig.update_yaxes(
                title=""
            )

            st.plotly_chart(
                style_figure(
                    segment_fig,
                    height=305,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )

    with lower_right:
        with st.container(border=True):
            section_title(
    "Addressable Wallet by Campaign Segment",
    "Commercial opportunity across actionable customer groups",
)


            top_campaigns = (
                campaigns
                .sort_values(
                    "Addressable_Wallet",
                    ascending=False,
                )
                .head(5)
            )

            campaign_fig = px.bar(
                top_campaigns.sort_values(
                    "Addressable_Wallet"
                ),
                x="Addressable_Wallet",
                y="Campaign_Segment",
                orientation="h",
                color="Campaign_Segment",
                color_discrete_map=CAMPAIGN_COLORS,
            )

            campaign_fig.update_layout(
                showlegend=False
            )

            campaign_fig.update_xaxes(
                title="Addressable Wallet (₹)"
            )

            campaign_fig.update_yaxes(
                title=""
            )

            st.plotly_chart(
                style_figure(
                    campaign_fig,
                    height=305,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )


elif page == "Portfolio & Migration":
    page_header(
        "Portfolio & Migration",
        (
            "Understand why HSIC wallet share declined "
            "despite continued MetroMart growth."
        ),
    )

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        metric_card(
            "FY2025 HSIC SoW",
            executive_value(
                "FY2025 HSIC Share of Wallet"
            ),
            icon="◷",
        )

    with p2:
        metric_card(
            "FY2026 HSIC SoW",
            executive_value(
                "FY2026 HSIC Share of Wallet"
            ),
            icon="◷",
            delta=executive_value(
                "Fiscal-Year SoW Decline"
            ),
            delta_type="negative",
        )

    with p3:
        metric_card(
            "MetroMart Sales Growth",
            executive_value(
                "MetroMart Net Sales Growth"
            ),
            icon="↗",
            delta="Customer spend growing",
            delta_type="positive",
        )

    with p4:
        metric_card(
            "Non-HSIC Spend Growth",
            executive_value(
                "Non-HSIC Spend Growth"
            ),
            icon="↗",
            delta="Wallet leakage",
            delta_type="negative",
        )

    portfolio_left, portfolio_right = st.columns(2)

    with portfolio_left:
        with st.container(border=True):
            section_title(
                "MetroMart Spend Composition",
                "HSIC versus alternative payment spend",
            )

            spend_fig = go.Figure()

            spend_fig.add_bar(
                x=fiscal["Fiscal_Year"],
                y=fiscal["HSIC_Net_Sales"],
                name="HSIC",
                marker_color="#071A43",
            )

            spend_fig.add_bar(
                x=fiscal["Fiscal_Year"],
                y=fiscal["Non_HSIC_Net_Sales"],
                name="Non-HSIC",
                marker_color="#B8F58F",
            )

            spend_fig.update_layout(
                barmode="stack"
            )

            spend_fig.update_yaxes(
                title="Net Sales (₹)"
            )

            spend_fig.update_xaxes(
                title=""
            )

            st.plotly_chart(
                style_figure(
                    spend_fig,
                    height=365,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )

    with portfolio_right:
        with st.container(border=True):
            section_title(
                "HSIC Share of Wallet",
                "Fiscal-year comparison",
            )

            sow_fig = px.bar(
                fiscal,
                x="Fiscal_Year",
                y="HSIC_SoW",
                text="HSIC_SoW",
            )

            sow_fig.update_traces(
                marker_color="#8EDC6A",
                texttemplate="%{text:.2f}%",
                textposition="outside",
                width=0.48,
            )

            sow_fig.update_yaxes(
                title="HSIC SoW (%)"
            )

            sow_fig.update_xaxes(
                title=""
            )

            st.plotly_chart(
                style_figure(
                    sow_fig,
                    height=365,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )

    with st.container(border=True):
        section_title(
            "Where Did the Wallet Move?",
            "Payment-method share: FY2025 versus FY2026",
        )

        payment_fig = px.bar(
            payments,
            x="Payment_Method",
            y="Spend_Share",
            color="Fiscal_Year",
            barmode="group",
            text_auto=".1f",
            color_discrete_sequence=[
                "#071A43",
                "#A7EB7F",
            ],
        )

        payment_fig.update_xaxes(
            title="",
        )

        payment_fig.update_yaxes(
            title="Spend Share (%)",
        )

        st.plotly_chart(
            style_figure(
                payment_fig,
                height=390,
            ),
            width="stretch",
            config=PLOT_CONFIG,
        )

    fy_order = sorted(
        payments["Fiscal_Year"]
        .astype(str)
        .unique()
        .tolist()
    )

    if len(fy_order) >= 2:
        payment_delta = (
            payments.pivot_table(
                index="Payment_Method",
                columns="Fiscal_Year",
                values="Spend_Share",
                aggfunc="sum",
            )
            .reset_index()
        )

        previous_fy = fy_order[-2]
        current_fy = fy_order[-1]

        if (
            previous_fy in payment_delta.columns
            and current_fy in payment_delta.columns
        ):
            payment_delta["Change_pp"] = (
                payment_delta[current_fy]
                - payment_delta[previous_fy]
            )

            payment_delta = (
                payment_delta.sort_values(
                    "Change_pp",
                    ascending=False,
                )
            )

            table_left, table_right = st.columns(
                [1.35, 1]
            )

            with table_left:
                with st.container(border=True):
                    section_title(
                        "Payment Migration Scorecard",
                        "Percentage-point change in payment share",
                    )

                    display_delta = payment_delta[
                        [
                            "Payment_Method",
                            previous_fy,
                            current_fy,
                            "Change_pp",
                        ]
                    ].copy()

                    display_delta.columns = [
                        "Payment Method",
                        previous_fy,
                        current_fy,
                        "Change (pp)",
                    ]

                    st.dataframe(
                        display_delta,
                        hide_index=True,
                        width="stretch",
                        column_config={
                            previous_fy:
                                st.column_config.NumberColumn(
                                    format="%.2f%%"
                                ),
                            current_fy:
                                st.column_config.NumberColumn(
                                    format="%.2f%%"
                                ),
                            "Change (pp)":
                                st.column_config.NumberColumn(
                                    format="%+.2f"
                                ),
                        },
                    )

            with table_right:
                st.markdown(
                    """
                    <div class="insight-card">
                        <b>The competitor is not just another bank.</b>
                        <p>
                            Wallet leakage also moved toward
                            MetroMart Wallet, Cash/UPI and debit.
                            This makes payment convenience and
                            checkout preference important parts
                            of the recovery strategy.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


elif page == "Customer Segmentation":
    page_header(
        "Customer Segmentation",
        (
            "Behavioral clusters reveal who to protect, "
            "grow and win back."
        ),
    )

    st.markdown(
        """
        <div class="soft-note">
            Model:
            <strong>K-Means, K = 3</strong>
            &nbsp; • &nbsp;
            Silhouette Score:
            <strong>0.4282</strong>
            &nbsp; • &nbsp;
            Features include recent SoW, SoW decline,
            spend, recoverable wallet, HSIC recency
            and customer engagement.
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_title(
        "Business Segments",
        "Machine-generated clusters translated into actionable customer groups",
    )

    segment_cols = st.columns(3)

    for column, segment_name in zip(
        segment_cols,
        [
            "HSIC-First Adopters",
            "Active HSIC Growers",
            "Wallet Migrators",
        ],
    ):
        with column:
            if segment_name in segment_lookup.index:
                row = segment_lookup.loc[
                    segment_name
                ]

                render_segment_card(row)

                st.markdown(
                    f"""
                    <div class="mini-card">
                        <div class="mini-label">
                            Addressable Wallet
                        </div>
                        <div class="mini-value">
                            {
                                format_inr(
                                    row[
                                        "Total_Recoverable_Wallet"
                                    ]
                                )
                            }
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    chart_left, chart_right = st.columns(2)

    with chart_left:
        with st.container(border=True):
            section_title(
                "Baseline vs Recent HSIC SoW",
                "How customer payment behavior changed",
            )

            sow_compare = segments.melt(
                id_vars=["Business_Segment"],
                value_vars=[
                    "Avg_Baseline_SoW",
                    "Avg_Recent_SoW",
                ],
                var_name="Period",
                value_name="SoW",
            )

            sow_compare["Period"] = (
                sow_compare["Period"]
                .replace({
                    "Avg_Baseline_SoW":
                        "Baseline",
                    "Avg_Recent_SoW":
                        "Recent",
                })
            )

            sow_segment_fig = px.bar(
                sow_compare,
                x="Business_Segment",
                y="SoW",
                color="Period",
                barmode="group",
                color_discrete_map={
                    "Baseline": "#D9DFD7",
                    "Recent": "#071A43",
                },
            )

            sow_segment_fig.update_xaxes(
                title=""
            )

            sow_segment_fig.update_yaxes(
                title="Average HSIC SoW (%)"
            )

            st.plotly_chart(
                style_figure(
                    sow_segment_fig,
                    height=370,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )

    with chart_right:
        with st.container(border=True):
            section_title(
                "Addressable Wallet by Segment",
                "Potential non-HSIC spend available for recovery",
            )

            wallet_fig = px.bar(
                segments.sort_values(
                    "Total_Recoverable_Wallet",
                    ascending=True,
                ),
                x="Total_Recoverable_Wallet",
                y="Business_Segment",
                orientation="h",
                color="Business_Segment",
                color_discrete_map=SEGMENT_COLORS,
                text="Total_Recoverable_Wallet",
            )

            wallet_fig.update_traces(
                texttemplate="₹%{text:.2s}",
                textposition="outside",
            )

            wallet_fig.update_layout(
                showlegend=False
            )

            wallet_fig.update_xaxes(
                title="Addressable Wallet (₹)"
            )

            wallet_fig.update_yaxes(
                title=""
            )

            st.plotly_chart(
                style_figure(
                    wallet_fig,
                    height=370,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )

    with st.container(border=True):
        section_title(
            "Campaign Micro-Segments",
            "Customer groups designed for campaign execution",
        )

        campaign_fig = px.bar(
            campaigns.sort_values(
                "Customers",
                ascending=True,
            ),
            x="Customers",
            y="Campaign_Segment",
            orientation="h",
            color="Campaign_Segment",
            color_discrete_map=CAMPAIGN_COLORS,
            text="Customers",
        )

        campaign_fig.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
        )

        campaign_fig.update_layout(
            showlegend=False
        )

        campaign_fig.update_xaxes(
            title="Customers"
        )

        campaign_fig.update_yaxes(
            title=""
        )

        st.plotly_chart(
            style_figure(
                campaign_fig,
                height=450,
            ),
            width="stretch",
            config=PLOT_CONFIG,
        )

    section_title(
        "Campaign Opportunity",
        "Commercial value of the action segments",
    )

    campaign_table = campaigns[
        [
            "Campaign_Segment",
            "Customers",
            "Addressable_Wallet",
            "Avg_Recent_SoW",
            "Avg_SoW_Decline",
            "Avg_Opportunity_Score",
        ]
    ].copy()

    st.dataframe(
        campaign_table.sort_values(
            "Avg_Opportunity_Score",
            ascending=False,
        ),
        hide_index=True,
        width="stretch",
        column_config={
            "Campaign_Segment":
                st.column_config.TextColumn(
                    "Campaign Segment"
                ),
            "Customers":
                st.column_config.NumberColumn(
                    "Customers",
                    format="%d",
                ),
            "Addressable_Wallet":
                st.column_config.NumberColumn(
                    "Addressable Wallet",
                    format="₹%.0f",
                ),
            "Avg_Recent_SoW":
                st.column_config.NumberColumn(
                    "Recent SoW",
                    format="%.1f%%",
                ),
            "Avg_SoW_Decline":
                st.column_config.NumberColumn(
                    "SoW Decline",
                    format="%.1f pp",
                ),
            "Avg_Opportunity_Score":
                st.column_config.ProgressColumn(
                    "Opportunity Score",
                    min_value=0,
                    max_value=100,
                    format="%.1f",
                ),
        },
    )


elif page == "Opportunity Explorer":
    page_header(
        "Opportunity Explorer",
        (
            "Turn customer behavior into a specific "
            "HSIC recovery action."
        ),
    )

    section_title(
        "Customer Filters",
        "All customer identifiers are anonymized for dashboard deployment",
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        selected_segment = st.selectbox(
            "Business Segment",
            ["All"]
            + sorted(
                customers[
                    "Business_Segment"
                ]
                .dropna()
                .unique()
                .tolist()
            ),
        )

    with f2:
        selected_campaign = st.selectbox(
            "Campaign Segment",
            ["All"]
            + sorted(
                customers[
                    "Campaign_Segment"
                ]
                .dropna()
                .unique()
                .tolist()
            ),
        )

    with f3:
        selected_tier = st.selectbox(
            "Opportunity Tier",
            [
                "All",
                "Critical",
                "High",
                "Medium",
                "Low",
            ],
        )

    with f4:
        selected_leakage = st.selectbox(
            "Primary Leakage Method",
            ["All"]
            + sorted(
                customers[
                    "Primary_Leakage_Method"
                ]
                .dropna()
                .unique()
                .tolist()
            ),
        )

    search_text = st.text_input(
        "Search Anonymous Customer ID",
        placeholder="Example: HSIC-00042",
    )

    filtered = customers.copy()

    if selected_segment != "All":
        filtered = filtered[
            filtered["Business_Segment"]
            == selected_segment
        ]

    if selected_campaign != "All":
        filtered = filtered[
            filtered["Campaign_Segment"]
            == selected_campaign
        ]

    if selected_tier != "All":
        filtered = filtered[
            filtered["Opportunity_Tier"]
            == selected_tier
        ]

    if selected_leakage != "All":
        filtered = filtered[
            filtered["Primary_Leakage_Method"]
            == selected_leakage
        ]

    if search_text.strip():
        filtered = filtered[
            filtered["Customer_Key"]
            .str.contains(
                search_text.strip(),
                case=False,
                na=False,
            )
        ]

    st.markdown(
        f"""
        <div class="soft-note">
            <strong>{len(filtered):,}</strong>
            customers match the current filters.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning(
            "No customers match the current filters."
        )

    else:
        selected_customer = st.selectbox(
            "Select Customer",
            filtered.sort_values(
                "Opportunity_Score",
                ascending=False,
            )["Customer_Key"].tolist(),
        )

        customer = (
            filtered.loc[
                filtered["Customer_Key"]
                == selected_customer
            ]
            .iloc[0]
        )

        section_title(
            selected_customer,
            (
                f"{customer['Business_Segment']}  •  "
                f"{customer['Campaign_Segment']}  •  "
                f"{customer['Strategic_Priority']}"
            ),
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card(
                "Baseline HSIC SoW",
                f"{customer['Baseline_HSIC_SoW']:.1f}%",
                icon="◷",
            )

        sow_change = float(
            customer["SoW_Change_pp"]
        )

        change_type = (
            "positive"
            if sow_change >= 0
            else "negative"
        )

        with c2:
            metric_card(
                "Recent HSIC SoW",
                f"{customer['Recent_HSIC_SoW']:.1f}%",
                icon="↔",
                delta=f"{sow_change:+.1f} pp",
                delta_type=change_type,
            )

        with c3:
            metric_card(
                "Addressable Wallet",
                format_inr(
                    customer[
                        "Recoverable_Wallet"
                    ]
                ),
                icon="₹",
                delta=customer[
                    "Opportunity_Tier"
                ],
                delta_type="neutral",
            )

        with c4:
            metric_card(
                "Opportunity Score",
                f"{customer['Opportunity_Score']:.1f}",
                icon="◎",
                delta="/ 100",
                delta_type="positive",
            )

        detail_left, detail_mid, detail_right = st.columns(
            [1, 1, 1.15]
        )

        with detail_left:
            with st.container(border=True):
                section_title(
                    "Wallet Behavior"
                )

                st.markdown(
                    f"""
                    <div class="mini-card">
                        <div class="mini-label">
                            Recent MetroMart Spend
                        </div>
                        <div class="mini-value">
                            {
                                format_inr(
                                    customer[
                                        "Recent_Total_Net_Sales"
                                    ]
                                )
                            }
                        </div>
                    </div>

                    <div class="mini-card">
                        <div class="mini-label">
                            Recent HSIC Spend
                        </div>
                        <div class="mini-value">
                            {
                                format_inr(
                                    customer[
                                        "Recent_HSIC_Net_Sales"
                                    ]
                                )
                            }
                        </div>
                    </div>

                    <div class="mini-card">
                        <div class="mini-label">
                            Recent Non-HSIC Spend
                        </div>
                        <div class="mini-value">
                            {
                                format_inr(
                                    customer[
                                        "Recent_Non_HSIC_Net_Sales"
                                    ]
                                )
                            }
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with detail_mid:
            with st.container(border=True):
                section_title(
                    "Behavior Profile"
                )

                st.markdown(
                    f"""
                    <div class="mini-card">
                        <div class="mini-label">
                            Primary Leakage Method
                        </div>
                        <div class="mini-value">
                            {
                                customer[
                                    "Primary_Leakage_Method"
                                ]
                            }
                        </div>
                    </div>

                    <div class="mini-card">
                        <div class="mini-label">
                            Top Category
                        </div>
                        <div class="mini-value">
                            {customer["Top_Category"]}
                        </div>
                    </div>

                    <div class="mini-card">
                        <div class="mini-label">
                            Membership
                        </div>
                        <div class="mini-value">
                            {customer["Membership_Type"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with detail_right:
            with st.container(border=True):
                section_title(
                    "Behavior Flags"
                )

                silent_class = (
                    "flag-on"
                    if customer[
                        "Silent_Attrition_Flag"
                    ] == 1
                    else "flag-off"
                )

                dormant_class = (
                    "flag-on"
                    if customer[
                        "HSIC_Dormant_Flag"
                    ] == 1
                    else "flag-off"
                )

                high_value_class = (
                    "flag-on"
                    if customer[
                        "High_Value_Low_SoW_Flag"
                    ] == 1
                    else "flag-off"
                )

                silent_text = (
                    "Silent Attrition"
                    if customer[
                        "Silent_Attrition_Flag"
                    ] == 1
                    else "No Silent Attrition"
                )

                dormant_text = (
                    "HSIC Dormant"
                    if customer[
                        "HSIC_Dormant_Flag"
                    ] == 1
                    else "HSIC Active"
                )

                high_value_text = (
                    "High-Value Low-SoW"
                    if customer[
                        "High_Value_Low_SoW_Flag"
                    ] == 1
                    else "Standard Value"
                )

                st.markdown(
                    f"""
                    <div class="flag-row">
                        <span class="{silent_class}">
                            {silent_text}
                        </span>
                        <span class="{dormant_class}">
                            {dormant_text}
                        </span>
                        <span class="{high_value_class}">
                            {high_value_text}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                score = float(
                    customer["Opportunity_Score"]
                )

                st.progress(
                    min(
                        max(
                            score / 100,
                            0,
                        ),
                        1,
                    ),
                    text=(
                        f"Opportunity Score: "
                        f"{score:.1f}/100"
                    ),
                )

                st.markdown(
                    f"""
                    <div class="strategy-card">
                        <div class="eyebrow">
                            Recommended Action
                        </div>
                        <h4>
                            {customer["Campaign_Segment"]}
                        </h4>
                        <p>
                            {
                                customer[
                                    "Recommended_Strategy"
                                ]
                            }
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        section_title(
            "Highest-Priority Customers",
            "Top opportunities within the current filtered view",
        )

        priority_table = (
            filtered.sort_values(
                "Opportunity_Score",
                ascending=False,
            )
            [
                [
                    "Customer_Key",
                    "Business_Segment",
                    "Campaign_Segment",
                    "Recent_HSIC_SoW",
                    "Recoverable_Wallet",
                    "Opportunity_Score",
                    "Primary_Leakage_Method",
                ]
            ]
            .head(15)
            .copy()
        )

        st.dataframe(
            priority_table,
            hide_index=True,
            width="stretch",
            column_config={
                "Customer_Key":
                    st.column_config.TextColumn(
                        "Customer"
                    ),
                "Business_Segment":
                    st.column_config.TextColumn(
                        "Business Segment"
                    ),
                "Campaign_Segment":
                    st.column_config.TextColumn(
                        "Campaign Segment"
                    ),
                "Recent_HSIC_SoW":
                    st.column_config.NumberColumn(
                        "Recent SoW",
                        format="%.1f%%",
                    ),
                "Recoverable_Wallet":
                    st.column_config.NumberColumn(
                        "Addressable Wallet",
                        format="₹%.0f",
                    ),
                "Opportunity_Score":
                    st.column_config.ProgressColumn(
                        "Opportunity",
                        min_value=0,
                        max_value=100,
                        format="%.1f",
                    ),
                "Primary_Leakage_Method":
                    st.column_config.TextColumn(
                        "Leakage Method"
                    ),
            },
        )


elif page == "Recovery Simulator":
    page_header(
        "Recovery Simulator",
        (
            "Estimate potential HSIC spend uplift under "
            "different wallet-recovery assumptions."
        ),
    )

    silent_customers = customers[
        customers[
            "Silent_Attrition_Flag"
        ] == 1
    ].copy()

    silent_wallet = (
        silent_customers[
            "Recoverable_Wallet"
        ]
        .sum()
    )

    silent_hsic = (
        silent_customers[
            "Recent_HSIC_Net_Sales"
        ]
        .sum()
    )

    silent_total = (
        silent_customers[
            "Recent_Total_Net_Sales"
        ]
        .sum()
    )

    current_sow = (
        silent_hsic
        / silent_total
        * 100
    )

    slider_left, slider_right = st.columns(
        [1.65, 1]
    )

    with slider_left:
        with st.container(border=True):
            section_title(
                "Wallet Recovery Assumption",
                (
                    "Select the share of addressable "
                    "non-HSIC wallet recovered"
                ),
            )

            recovery_rate = st.slider(
                "Recovery rate",
                min_value=0,
                max_value=30,
                value=10,
                step=1,
                format="%d%%",
                label_visibility="collapsed",
            )

            st.markdown(
                f"""
                <div class="soft-note">
                    Scenario selected:
                    <strong>{recovery_rate}% recovery</strong>
                    of the silent-attrition cohort's
                    addressable wallet.
                </div>
                """,
                unsafe_allow_html=True,
            )

    incremental_hsic = (
        silent_wallet
        * recovery_rate
        / 100
    )

    projected_hsic = (
        silent_hsic
        + incremental_hsic
    )

    projected_sow = (
        projected_hsic
        / silent_total
        * 100
    )

    sow_uplift = (
        projected_sow
        - current_sow
    )

    with slider_right:
        st.markdown(
            """
            <div class="alert-card">
                <b>Scenario — not forecast</b>
                <p>
                    Campaign response was not observed.
                    These values illustrate potential upside
                    and should be validated through controlled
                    testing.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        metric_card(
            "Addressable Wallet",
            format_inr(silent_wallet),
            icon="₹",
        )

    with r2:
        metric_card(
            "Incremental HSIC Spend",
            format_inr(incremental_hsic),
            icon="↗",
            delta=f"{recovery_rate}% recovery",
            delta_type="positive",
        )

    with r3:
        metric_card(
            "Projected HSIC SoW",
            f"{projected_sow:.2f}%",
            icon="◒",
            delta=f"+{sow_uplift:.2f} pp",
            delta_type="positive",
        )

    with r4:
        metric_card(
            "Silent Attrition Cohort",
            f"{len(silent_customers):,}",
            icon="◎",
        )

    sim_left, sim_right = st.columns(
        [1, 1.35]
    )

    with sim_left:
        with st.container(border=True):
            section_title(
                "Projected Share of Wallet",
                "Current versus simulated outcome",
            )

            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=projected_sow,
                    number={
                        "suffix": "%",
                        "font": {
                            "size": 30,
                            "color": "#111827",
                        },
                    },
                    delta={
                        "reference": current_sow,
                        "suffix": " pp",
                        "increasing": {
                            "color": "#5A9D46"
                        },
                    },
                    gauge={
                        "axis": {
                            "range": [0, 35],
                            "tickwidth": 0,
                            "tickcolor": "#E4E8E0",
                        },
                        "bar": {
                            "color": "#071A43"
                        },
                        "bgcolor": "#EEF1EC",
                        "borderwidth": 0,
                        "steps": [
                            {
                                "range": [
                                    0,
                                    current_sow,
                                ],
                                "color": "#EDEFEA",
                            },
                            {
                                "range": [
                                    current_sow,
                                    35,
                                ],
                                "color": "#DFF7D2",
                            },
                        ],
                    },
                )
            )

            gauge.update_layout(
                height=340,
                margin=dict(
                    l=25,
                    r=25,
                    t=40,
                    b=15,
                ),
                paper_bgcolor="white",
            )

            st.plotly_chart(
                gauge,
                width="stretch",
                config=PLOT_CONFIG,
            )

    with sim_right:
        with st.container(border=True):
            section_title(
                "Validated Recovery Scenarios",
                "Incremental HSIC spend under fixed assumptions",
            )

            scenario_fig = px.bar(
                impact,
                x="Scenario",
                y="Incremental_HSIC_Spend_Lakh",
                text="Incremental_HSIC_Spend_Lakh",
            )

            scenario_fig.update_traces(
                marker_color="#A7EB7F",
                texttemplate="₹%{text:.2f} L",
                textposition="outside",
                marker_line_width=0,
            )

            scenario_fig.update_yaxes(
                title="Incremental HSIC Spend (₹ Lakh)"
            )

            scenario_fig.update_xaxes(
                title=""
            )

            st.plotly_chart(
                style_figure(
                    scenario_fig,
                    height=340,
                ),
                width="stretch",
                config=PLOT_CONFIG,
            )

    section_title(
        "Measurement Framework",
        "How HSIC should validate real campaign performance",
    )

    measurement = pd.DataFrame({
        "Measure": [
            "Incremental HSIC Spend",
            "Share-of-Wallet Uplift",
            "Reactivation Rate",
            "Cost per Incremental ₹",
            "Offer Redemption",
            "30/60/90-Day Persistence",
        ],
        "Why It Matters": [
            "Measures actual spend shifted onto HSIC",
            "Tests whether payment preference changed",
            "Tracks dormant-card recovery",
            "Protects campaign economics",
            "Measures offer engagement",
            "Tests whether uplift persists after the offer",
        ],
    })

    st.dataframe(
        measurement,
        hide_index=True,
        width="stretch",
    )