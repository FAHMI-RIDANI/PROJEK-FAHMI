import streamlit as st

st.set_page_config(page_title="FP-Growth Analytics", page_icon="📊", layout="wide")

with st.sidebar:
    st.markdown(
        """
    <div class="sidebar-logo">
        <div style="font-size:2rem;">📊</div>
        <div class="title" style="font-weight:bold; font-size:1.2rem;">FP-Growth Analytics</div>
        <div class="sub" style="font-size:0.8rem; color:gray;">Analisis Pola Pembelian Emas ANTAM</div>
    </div>
    <br>
    """,
        unsafe_allow_html=True,
    )


page_1 = st.Page("views/main_page.py", title="Dashboard Utama", icon="🏠")
page_2 = st.Page("views/about_app.py", title="Tentang Aplikasi", icon="ℹ️")
page_3 = st.Page("views/about_me.py", title="Tentang Pengembang", icon="👤")


pg = st.navigation([page_1, page_2, page_3])


with st.sidebar:
    st.markdown("---")
    st.markdown(
        """
    <div style="font-size:0.75rem; color:#64748b; line-height:1.6;">
        <b style="color:#94a3b8;">Panduan Parameter</b><br>
        🔸 <b>Min Support</b>: Frekuensi kemunculan itemset<br>
        🔸 <b>Min Confidence</b>: Kepercayaan aturan<br>
        🔸 <b>Lift > 1</b>: Asosiasi kuat & positif
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
    <div style="font-size:0.72rem; color:#475569; text-align:center;">
        v2.0 · Built with Streamlit<br>
        © 2025 ANTAM Analytics
    </div>
    """,
        unsafe_allow_html=True,
    )

pg.run()
