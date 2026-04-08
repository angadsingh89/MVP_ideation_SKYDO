from datetime import date, datetime, timedelta
import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="Smart Cashflow MVP", page_icon=":moneybag:", layout="wide")


def theme_css() -> str:
    return """
    <style>
    :root{
      --bg:#F7F5F2;
      --bg-soft:#EFEAE4;
      --text:#1E1E1E;
      --muted:#5C7A7A;
      --line:#E8E6E3;
      --glass:rgba(255,255,255,.68);
      --glass-soft:rgba(255,255,255,.56);
      --primary:#2F6F5E;
      --primary-dark:#285E50;
      --secondary:#5C7A7A;
      --accent:#E6C9A8;
    }
    .stApp{
      color:var(--text);
      background:
        radial-gradient(900px 280px at -8% -10%, rgba(230,201,168,.22), transparent 48%),
        radial-gradient(700px 240px at 102% 0%, rgba(92,122,122,.10), transparent 45%),
        linear-gradient(180deg,#F7F5F2 0%, #F4F1EC 45%, #EFEAE4 100%);
    }
    [data-testid="stHeader"]{background:transparent;}
    [data-testid="stSidebar"]{
      background:linear-gradient(180deg, rgba(239,234,228,.95), rgba(247,245,242,.95));
      border-right:1px solid var(--line);
      backdrop-filter: blur(10px);
    }
    .brand{
      font:600 1.15rem/1.2 Inter,system-ui,sans-serif;
      letter-spacing:.01em;color:var(--text);margin:.1rem 0 .8rem 0;
    }
    .nav-pill{
      border:1px solid transparent;
      border-radius:12px;
      padding:.5rem .7rem;
      margin:.25rem 0;
      font-size:.82rem;
      color:#324544;
      background:rgba(255,255,255,.45);
      transition:all .24s ease;
    }
    .nav-pill:hover{background:rgba(255,255,255,.75);}
    .nav-pill.active{
      color:#1E1E1E;
      border-color:rgba(47,111,94,.18);
      border-left:3px solid var(--primary);
      background:linear-gradient(90deg,rgba(47,111,94,.10),rgba(230,201,168,.18));
      box-shadow:0 8px 20px rgba(47,111,94,.08);
    }
    .topbar{
      display:flex;justify-content:space-between;align-items:center;
      border:1px solid rgba(255,255,255,.7);
      background:var(--glass);
      backdrop-filter:blur(12px);
      border-radius:16px;padding:.65rem .9rem;margin-bottom:1rem;
    }
    .badge{
      padding:.24rem .6rem;border-radius:999px;
      font-size:.74rem;color:#3f4d4d;
      background:rgba(255,255,255,.8);border:1px solid var(--line);
    }
    .btn-primary{
      border:none;border-radius:12px;padding:.52rem .82rem;
      color:white;font-weight:600;font-size:.82rem;
      background:var(--primary);
      box-shadow:0 8px 18px rgba(47,111,94,.16);
      transition:all .25s ease;
    }
    .btn-primary:hover{transform:translateY(-1px);background:var(--primary-dark);}
    .hero{
      position:relative;
      border:1px solid rgba(255,255,255,.75);
      background:var(--glass);
      backdrop-filter: blur(14px);
      border-radius:20px;padding:1.35rem 1.3rem 1.4rem 1.3rem;margin-bottom:1.15rem;
      box-shadow:0 18px 50px rgba(15,23,42,.08);
    }
    .hero:before{
      content:"";
      position:absolute;
      left:16px;right:16px;top:10px;height:3px;border-radius:999px;
      background:linear-gradient(90deg,var(--primary),var(--accent));
      opacity:.8;
    }
    .hero-kicker{
      display:inline-block;border-radius:999px;padding:.22rem .6rem;
      font-size:.72rem;color:#2F6F5E;
      border:1px solid rgba(47,111,94,.20);background:rgba(47,111,94,.10);
      margin-bottom:.6rem;
    }
    .hero-title{
      margin:.1rem 0 .4rem 0;
      font-size:2.35rem;line-height:1.06;font-weight:700;letter-spacing:-.02em;color:#1E1E1E;
    }
    .hero-sub{margin:0;color:#536464;font-size:1rem;max-width:70ch;}
    .card{
      border:1px solid rgba(255,255,255,.75);
      background:var(--glass-soft);
      backdrop-filter: blur(12px);
      border-radius:16px;padding:.9rem 1rem;
      box-shadow:0 12px 30px rgba(15,23,42,.07);
      transition:all .24s ease;
    }
    .card:hover{transform:translateY(-2px);}
    .card.primary{
      background:linear-gradient(125deg, rgba(47,111,94,.18), rgba(220,239,232,.85));
      border-color:rgba(47,111,94,.18);
      box-shadow:0 14px 26px rgba(47,111,94,.10);
    }
    .card.accent{
      background:linear-gradient(125deg, rgba(230,201,168,.35), rgba(255,255,255,.70));
    }
    .label{
      color:var(--muted);font-size:.72rem;letter-spacing:.06em;
      text-transform:uppercase;font-weight:600;
    }
    .value{
      margin:.25rem 0 0 0;color:var(--text);font-size:1.65rem;font-weight:700;
    }
    .section{
      border:1px solid rgba(255,255,255,.75);
      background:var(--glass-soft);
      backdrop-filter: blur(12px);
      border-radius:16px;padding:.95rem 1rem;
      box-shadow:0 12px 30px rgba(15,23,42,.07);
    }
    .section-title{font-size:1.02rem;font-weight:650;color:#0f172a;margin:.1rem 0 .55rem 0;}
    .muted{color:var(--muted);font-size:.84rem;margin-top:.3rem;}
    .risk-chip{
      display:inline-block;padding:.25rem .62rem;border-radius:999px;
      font-size:.75rem;margin:.2rem .3rem .2rem 0;
      background:rgba(230,201,168,.35);color:#7b4f35;border:1px solid rgba(182,130,97,.24);
    }
    .table-wrap{
      border:1px solid rgba(255,255,255,.75);
      border-radius:16px;background:var(--glass-soft);backdrop-filter:blur(12px);
      padding:.35rem .45rem .45rem .45rem;overflow:auto;box-shadow:0 10px 24px rgba(15,23,42,.06);
    }
    .table-wrap table{width:100%;border-collapse:separate;border-spacing:0;font-size:.84rem;color:#0f172a;}
    .table-wrap thead th{
      text-align:left;padding:.62rem .56rem;font-size:.69rem;text-transform:uppercase;letter-spacing:.05em;
      color:#334155;background:rgba(255,255,255,.7);border-bottom:1px solid var(--line);
      position:sticky;top:0;
    }
    .table-wrap tbody td{
      padding:.62rem .56rem;border-bottom:1px solid rgba(148,163,184,.12);white-space:nowrap;font-weight:500;
    }
    .table-wrap tbody tr:hover{background:rgba(255,255,255,.68);}
    .status{
      display:inline-block;padding:.18rem .45rem;border-radius:999px;font-size:.72rem;font-weight:600;
      border:1px solid transparent;
    }
    .status-paid{color:#2f6f5e;background:rgba(47,111,94,.12);border-color:rgba(47,111,94,.20);}
    .status-overdue{color:#9a4f4a;background:rgba(176,112,94,.14);border-color:rgba(176,112,94,.20);}
    .status-partial{color:#8a6435;background:rgba(230,201,168,.34);border-color:rgba(196,158,116,.24);}
    .status-pending{color:#4b6666;background:rgba(92,122,122,.14);border-color:rgba(92,122,122,.20);}
    [data-testid="stExpander"]{
      border:1px solid var(--line);
      border-radius:14px;
      background:rgba(255,255,255,.62);
    }
    [data-testid="stExpander"] details summary{
      color:#1E1E1E !important;
      font-weight:600;
      padding:.4rem .2rem;
    }
    [data-testid="stForm"]{
      background:transparent;
    }
    [data-testid="stForm"] label,
    [data-testid="stForm"] p{
      color:#334155 !important;
    }
    [data-testid="stTextInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stNumberInput"] input{
      background:rgba(255,255,255,.92) !important;
      color:#1E1E1E !important;
      border:1px solid var(--line) !important;
      border-radius:10px !important;
    }
    [data-testid="stDateInput"] button,
    [data-testid="stNumberInput"] button{
      color:#3f4d4d !important;
      background:rgba(255,255,255,.9) !important;
      border:1px solid var(--line) !important;
    }
    [data-testid="stFormSubmitButton"] button{
      background:var(--primary) !important;
      color:white !important;
      border:none !important;
      border-radius:10px !important;
      box-shadow:0 8px 18px rgba(47,111,94,.16) !important;
    }
    [data-testid="stFormSubmitButton"] button:hover{
      background:var(--primary-dark) !important;
    }
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] > div,
    [data-baseweb="textarea"] textarea{
      background:rgba(255,255,255,.92) !important;
      color:#1E1E1E !important;
      border-color:var(--line) !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] div,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea{
      color:#1E1E1E !important;
    }
    [data-baseweb="popover"]{
      background:rgba(255,255,255,.98) !important;
      color:#1E1E1E !important;
    }
    [data-baseweb="menu"]{
      background:rgba(255,255,255,.98) !important;
      color:#1E1E1E !important;
      border:1px solid var(--line) !important;
    }
    [role="option"]{
      color:#1E1E1E !important;
      background:rgba(255,255,255,.98) !important;
    }
    [role="option"][aria-selected="true"]{
      background:rgba(47,111,94,.10) !important;
    }
    [data-testid="stSlider"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stMultiSelect"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stTextInput"] label{
      color:#334155 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]{
      background:var(--primary) !important;
      border-color:var(--primary) !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div{
      background:rgba(47,111,94,.22) !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] p{
      color:#1E1E1E !important;
    }
    @media (max-width: 900px){
      .hero-title{font-size:1.9rem;}
    }
    </style>
    """


def inr(value: float) -> str:
    return f"Rs {value:,.0f}"


def get_connection():
    return sqlite3.connect("cashflow_streamlit.db")


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            client_name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            amount REAL NOT NULL,
            amount_paid_base REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'pending',
            last_payment_date TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_reference TEXT UNIQUE NOT NULL,
            invoice_number TEXT NOT NULL,
            client_name TEXT NOT NULL,
            payment_date TEXT NOT NULL,
            source_currency TEXT NOT NULL,
            net_amount_base REAL NOT NULL,
            status TEXT NOT NULL,
            delta_amount_base REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def seed_invoices_if_empty():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM invoices")
    count = cur.fetchone()[0]
    if count == 0:
        today = date.today()
        rows = [
            ("INV-1001", "Northwind Retail", str(today - timedelta(days=10)), 250000.0, 250000.0, "paid", str(today - timedelta(days=8)), datetime.utcnow().isoformat()),
            ("INV-1002", "Northwind Retail", str(today + timedelta(days=3)), 180000.0, 99000.0, "partially_paid", str(today - timedelta(days=1)), datetime.utcnow().isoformat()),
            ("INV-2001", "LatePay GmbH", str(today - timedelta(days=15)), 325000.0, 0.0, "pending", None, datetime.utcnow().isoformat()),
            ("INV-1999", "LatePay GmbH", str(today - timedelta(days=60)), 210000.0, 210000.0, "paid", str(today - timedelta(days=40)), datetime.utcnow().isoformat()),
        ]
        cur.executemany(
            """
            INSERT INTO invoices (
                invoice_number, client_name, due_date, amount, amount_paid_base, status, last_payment_date, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
    conn.close()


def seed_payments_if_empty():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM payments")
    count = cur.fetchone()[0]
    if count == 0:
        today = date.today()
        rows = [
            ("PAY-EXACT-001", "INV-1001", "Northwind Retail", str(today - timedelta(days=8)), "USD", 250000.0, "matched", 0.0, datetime.utcnow().isoformat()),
            ("PAY-PARTIAL-001", "INV-1002", "Northwind Retail", str(today - timedelta(days=1)), "USD", 99000.0, "partially_matched", 81000.0, datetime.utcnow().isoformat()),
        ]
        cur.executemany(
            """
            INSERT INTO payments (
                payment_reference, invoice_number, client_name, payment_date, source_currency, net_amount_base, status, delta_amount_base, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
    conn.close()


def load_invoices():
    conn = get_connection()
    invoices = pd.read_sql_query("SELECT * FROM invoices ORDER BY due_date ASC", conn)
    conn.close()
    return invoices


def add_invoice(invoice_number: str, client_name: str, due_date: date, amount: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO invoices (
            invoice_number, client_name, due_date, amount, amount_paid_base, status, last_payment_date, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            invoice_number.strip(),
            client_name.strip(),
            str(due_date),
            float(amount),
            0.0,
            "pending",
            None,
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def load_payments():
    conn = get_connection()
    payments = pd.read_sql_query("SELECT * FROM payments ORDER BY payment_date DESC, id DESC", conn)
    conn.close()
    if payments.empty:
        return pd.DataFrame(
            columns=[
                "id",
                "payment_reference",
                "invoice_number",
                "client_name",
                "payment_date",
                "source_currency",
                "net_amount_base",
                "status",
                "delta_amount_base",
            ]
        )
    return payments


def record_payment(payment_reference: str, invoice_number: str, payment_date: date, source_currency: str, net_amount_base: float):
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(
        """
        SELECT client_name, amount, amount_paid_base FROM invoices WHERE invoice_number = ?
        """,
        (invoice_number,),
    ).fetchone()
    if not row:
        conn.close()
        raise ValueError("Invoice not found.")

    client_name, amount, amount_paid_base = row
    new_paid = float(amount_paid_base) + float(net_amount_base)
    delta = max(float(amount) - new_paid, 0.0)
    if delta <= 1:
        status = "paid"
        match_status = "matched"
    elif new_paid > 0:
        status = "partially_paid"
        match_status = "partially_matched"
    else:
        status = "pending"
        match_status = "unmatched"

    cur.execute(
        """
        UPDATE invoices
        SET amount_paid_base = ?, status = ?, last_payment_date = ?
        WHERE invoice_number = ?
        """,
        (new_paid, status, str(payment_date), invoice_number),
    )
    cur.execute(
        """
        INSERT INTO payments (
            payment_reference, invoice_number, client_name, payment_date, source_currency, net_amount_base, status, delta_amount_base, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payment_reference.strip(),
            invoice_number,
            client_name,
            str(payment_date),
            source_currency,
            float(net_amount_base),
            match_status,
            float(delta),
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def build_reconciliation_from_payments(payments: pd.DataFrame):
    if payments.empty:
        return pd.DataFrame(columns=["payment_id", "invoice_id", "status", "matched_amount_base", "delta_amount_base"])
    return pd.DataFrame(
        {
            "payment_id": payments["id"],
            "invoice_id": payments["invoice_number"],
            "status": payments["status"],
            "matched_amount_base": payments["net_amount_base"],
            "delta_amount_base": payments["delta_amount_base"],
        }
    )


def compute_summary(invoices: pd.DataFrame, payments: pd.DataFrame):
    today = date.today()
    total_received = float(payments["net_amount_base"].sum())
    invoices = invoices.copy()
    invoices["due_date"] = pd.to_datetime(invoices["due_date"])
    invoices["last_payment_date"] = pd.to_datetime(invoices["last_payment_date"], errors="coerce")
    paid = invoices[invoices["status"] == "paid"].dropna(subset=["last_payment_date"]).copy()
    paid["delay"] = (paid["last_payment_date"] - paid["due_date"]).dt.days
    delay_by_client = paid.groupby("client_name")["delay"].mean().to_dict()
    invoices["pending_amount"] = invoices["amount"] - invoices["amount_paid_base"]
    invoices["avg_delay"] = invoices["client_name"].map(delay_by_client).fillna(0).clip(lower=0)
    invoices["predicted_payment_date"] = invoices["due_date"] + pd.to_timedelta(invoices["avg_delay"].astype(int), unit="D")
    expected_7d = float(
        invoices[
            (invoices["pending_amount"] > 0)
            & (invoices["predicted_payment_date"] >= pd.Timestamp(today))
            & (invoices["predicted_payment_date"] <= pd.Timestamp(today + timedelta(days=7)))
        ]["pending_amount"].sum()
    )
    overdue_amount = float(invoices[(invoices["pending_amount"] > 0) & (invoices["due_date"] < pd.Timestamp(today))]["pending_amount"].sum())
    risky_clients = sorted(invoices.loc[invoices["avg_delay"] >= 10, "client_name"].dropna().unique().tolist())
    invoices["status"] = invoices.apply(
        lambda row: "overdue" if row["pending_amount"] > 0 and row["due_date"] < pd.Timestamp(today) else row["status"],
        axis=1,
    )
    return total_received, expected_7d, overdue_amount, risky_clients, invoices


def forex_chart():
    rates = [88.9, 89.4, 89.1, 90.2, 90.8, 91.7, 91.3, 92.1, 92.53]
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue"]
    fig = go.Figure()
    for i in range(len(rates) - 1):
        color = "#2F6F5E" if rates[i + 1] >= rates[i] else "#B0705E"
        fig.add_trace(
            go.Scatter(
                x=[labels[i], labels[i + 1]],
                y=[rates[i], rates[i + 1]],
                mode="lines",
                line=dict(color=color, width=3),
                hovertemplate="USD/INR: %{y}<extra></extra>",
                showlegend=False,
            )
        )
    markers = ["#2F6F5E"] + ["#2F6F5E" if rates[i] >= rates[i - 1] else "#B0705E" for i in range(1, len(rates))]
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=rates,
            mode="markers",
            marker=dict(size=7, color=markers, line=dict(color="white", width=1.4)),
            showlegend=False,
            hovertemplate="USD/INR: %{y}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=rates,
            mode="lines",
            line=dict(color="rgba(60,76,76,.45)", width=1.8),
            fill="tozeroy",
            fillcolor="rgba(92,122,122,.12)",
            showlegend=False,
            hoverinfo="skip",
        )
    )
    y_min = min(rates) - 0.7
    y_max = max(rates) + 0.7
    fig.update_layout(
        margin=dict(l=10, r=10, t=8, b=8),
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.42)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,.24)", range=[y_min, y_max], tickformat=".2f"),
        hovermode="x unified",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})


def status_badge(status: str) -> str:
    cls = {
        "paid": "status-paid",
        "overdue": "status-overdue",
        "partially_paid": "status-partial",
        "partially_matched": "status-partial",
        "pending": "status-pending",
        "matched": "status-paid",
    }.get(status, "status-pending")
    label = status.replace("_", " ")
    return f'<span class="status {cls}">{label}</span>'


def render_table(df: pd.DataFrame):
    formatted = df.copy()
    if "status" in formatted.columns:
        formatted["status"] = formatted["status"].astype(str).map(status_badge)
    st.markdown(f'<div class="table-wrap">{formatted.to_html(index=False, escape=False)}</div>', unsafe_allow_html=True)


def main():
    st.markdown(theme_css(), unsafe_allow_html=True)
    init_db()
    seed_invoices_if_empty()
    seed_payments_if_empty()
    invoices = load_invoices()
    payments = load_payments()
    reconciliation = build_reconciliation_from_payments(payments)
    total_received, expected_7d, overdue_amount, risky_clients, invoices = compute_summary(invoices, payments)

    with st.sidebar:
        st.markdown('<div class="brand">Smart Cashflow MVP</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-pill active">Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-pill">Reconciliation</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-pill">Forecasting</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-pill">Clients</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-pill">Settings</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="topbar"><span class="badge">Live • Export Intelligence</span><button class="btn-primary">Create Invoice</button></div>',
        unsafe_allow_html=True,
    )
    with st.expander("Create Invoice", expanded=False):
        with st.form("create_invoice_form", clear_on_submit=True):
            f1, f2 = st.columns(2)
            invoice_number = f1.text_input("Invoice Number", placeholder="INV-3001")
            client_name = f2.text_input("Client Name", placeholder="Acme Imports")
            f3, f4 = st.columns(2)
            due_date = f3.date_input("Due Date", value=date.today() + timedelta(days=7))
            amount = f4.number_input("Amount (INR)", min_value=1000.0, step=1000.0, value=50000.0)
            submitted = st.form_submit_button("Create Invoice")
            if submitted:
                if not invoice_number.strip() or not client_name.strip():
                    st.error("Invoice number and client name are required.")
                else:
                    try:
                        add_invoice(invoice_number, client_name, due_date, amount)
                        st.success("Invoice created successfully.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Invoice number already exists.")
    with st.expander("Record Payment", expanded=False):
        with st.form("record_payment_form", clear_on_submit=True):
            p1, p2 = st.columns(2)
            payment_reference = p1.text_input("Payment Reference", placeholder="PAY-NEW-001")
            source_currency = p2.selectbox("Source Currency", options=["USD", "EUR", "GBP", "INR"], index=0)
            p3, p4 = st.columns(2)
            invoice_options = invoices["invoice_number"].tolist()
            invoice_number = p3.selectbox("Invoice Number", options=invoice_options if invoice_options else ["No invoices"])
            payment_date = p4.date_input("Payment Date", value=date.today())
            net_amount_base = st.number_input("Net Amount Settled (INR)", min_value=1000.0, step=1000.0, value=50000.0)
            pay_submitted = st.form_submit_button("Record Payment")
            if pay_submitted:
                if not payment_reference.strip() or not invoice_options:
                    st.error("Valid payment reference and invoice are required.")
                else:
                    try:
                        record_payment(payment_reference, invoice_number, payment_date, source_currency, net_amount_base)
                        st.success("Payment recorded and invoice updated.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Payment reference already exists.")
                    except ValueError as exc:
                        st.error(str(exc))
    st.markdown(
        """
        <div class="hero">
          <span class="hero-kicker">Cash Flow Command Center</span>
          <h1 class="hero-title">Know exactly when your export cash lands.</h1>
          <p class="hero-sub">Smarter visibility into your payments and cash flow</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3, gap="small")
    m1.markdown(f'<div class="card primary"><div class="label">Total Received</div><p class="value">{inr(total_received)}</p></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="card accent"><div class="label">Expected Inflow (Next 7d)</div><p class="value">{inr(expected_7d)}</p></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="card"><div class="label">Overdue Amount</div><p class="value">{inr(overdue_amount)}</p></div>', unsafe_allow_html=True)

    st.write("")
    c_left, c_right = st.columns([1.0, 2.1], gap="large")
    with c_left:
        st.markdown(
            """
            <div class="section">
              <div class="label">USD / INR</div>
              <p class="value" style="font-size:2rem;margin-top:.2rem;">92.53</p>
              <p class="muted">+0.84% this week</p>
              <p class="muted">Indicative live trend for settlement planning.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section" style="margin-top:.8rem;"><div class="section-title">Risk Watchlist</div>', unsafe_allow_html=True)
        if risky_clients:
            st.markdown("".join([f'<span class="risk-chip">{name}</span>' for name in risky_clients]), unsafe_allow_html=True)
        else:
            st.markdown('<p class="muted">No risky clients flagged.</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c_right:
        st.markdown('<div class="section"><div class="section-title">Forex Rate Trend</div>', unsafe_allow_html=True)
        forex_chart()
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    with st.expander("What-if Cashflow Simulator", expanded=False):
        s1, s2, s3 = st.columns(3)
        sim_invoice = s1.number_input("Invoice Amount (USD)", min_value=100.0, value=5000.0, step=100.0)
        sim_fx = s2.slider("FX Rate (USD to INR)", min_value=70.0, max_value=100.0, value=92.5, step=0.1)
        sim_fee = s3.slider("Total Fees (%)", min_value=0.0, max_value=5.0, value=1.2, step=0.1)
        sim_delay = st.slider("Predicted Delay (days)", min_value=0, max_value=45, value=8, step=1)
        gross = sim_invoice * sim_fx
        net = gross * (1 - sim_fee / 100)
        c_a, c_b, c_c = st.columns(3)
        c_a.metric("Gross INR", inr(gross))
        c_b.metric("Net INR", inr(net))
        c_c.metric("Predicted Realization Date", str(date.today() + timedelta(days=sim_delay)))

    st.write("")
    f1, f2, f3 = st.columns([1.3, 1.3, 2.4])
    status_filter = f1.multiselect(
        "Filter Status",
        options=sorted(invoices["status"].astype(str).unique().tolist()),
        default=[],
    )
    client_filter = f2.multiselect(
        "Filter Client",
        options=sorted(invoices["client_name"].astype(str).unique().tolist()),
        default=[],
    )
    invoice_search = f3.text_input("Search Invoice", placeholder="Type invoice number...")

    view_invoices = invoices.copy()
    if status_filter:
        view_invoices = view_invoices[view_invoices["status"].isin(status_filter)]
    if client_filter:
        view_invoices = view_invoices[view_invoices["client_name"].isin(client_filter)]
    if invoice_search.strip():
        view_invoices = view_invoices[
            view_invoices["invoice_number"].str.contains(invoice_search.strip(), case=False, na=False)
        ]

    t1, t2 = st.columns(2, gap="large")
    with t1:
        st.markdown('<div class="section-title">Invoices</div>', unsafe_allow_html=True)
        iv = view_invoices[["invoice_number", "client_name", "due_date", "status", "amount_paid_base", "amount"]].copy()
        iv["due_date"] = pd.to_datetime(iv["due_date"]).dt.strftime("%Y-%m-%d")
        iv["amount_paid_base"] = iv["amount_paid_base"].map(inr)
        iv["amount"] = iv["amount"].map(inr)
        render_table(iv)
    with t2:
        st.markdown('<div class="section-title">Payments</div>', unsafe_allow_html=True)
        pv = payments[["payment_reference", "invoice_number", "client_name", "payment_date", "source_currency", "net_amount_base"]].copy()
        pv["payment_date"] = pd.to_datetime(pv["payment_date"]).dt.strftime("%Y-%m-%d")
        pv["net_amount_base"] = pv["net_amount_base"].map(inr)
        render_table(pv)

    st.write("")
    st.markdown('<div class="section-title">Reconciliation Status</div>', unsafe_allow_html=True)
    rv = reconciliation.copy()
    rv["matched_amount_base"] = rv["matched_amount_base"].map(inr)
    rv["delta_amount_base"] = rv["delta_amount_base"].map(inr)
    render_table(rv)


if __name__ == "__main__":
    main()
