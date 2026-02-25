import streamlit as st

st.title("About App")


col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class="about-card">
            <h4 style="color:#c8102e; margin-top:0;">🎯 Tujuan Aplikasi</h4>
            <p style="color:#374151; font-size:0.9rem; line-height:1.7;">
            Aplikasi ini dirancang untuk membantu Butik emas 
            menemukan <strong>pola pembelian tersembunyi</strong> dalam data transaksi emas batangan,
            sehingga dapat digunakan untuk strategi bundling produk, rekomendasi pelanggan,
            dan perencanaan stok yang lebih efisien.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-card">
            <h4 style="color:#c8102e; margin-top:0;">⚙️ Fitur Utama</h4>
            <ul style="color:#374151; font-size:0.9rem; line-height:2;">
                <li>Upload data transaksi CSV atau Excel</li>
                <li>Preprocessing & normalisasi otomatis</li>
                <li>Analisis FP-Growth tanpa library eksternal</li>
                <li>Hasil dalam bahasa Indonesia</li>
                <li>Unduh laporan PDF </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="about-card">
            <h4 style="color:#c8102e; margin-top:0;">🧠 Algoritma FP-Growth</h4>
            <p style="color:#374151; font-size:0.9rem; line-height:1.7;">
            <strong>FP-Growth (Frequent Pattern Growth)</strong> adalah algoritma data mining
            yang menemukan frequent itemsets secara efisien menggunakan struktur data
            <em>FP-Tree</em>, tanpa perlu menghasilkan candidate itemsets seperti Apriori.
            </p>
            <p style="color:#374151; font-size:0.9rem; line-height:1.7;">
            Keunggulan utama: hanya memerlukan <strong>2 kali scan database</strong>,
            sehingga jauh lebih cepat pada dataset besar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-card">
            <h4 style="color:#c8102e; margin-top:0;">📐 Rumus Metrik</h4>
            <ul style="color:#374151; font-size:0.88rem; line-height:2.2;">
                <li><b>Support</b> = freq(A∪B) / N</li>
                <li><b>Confidence</b> = freq(A∪B) / freq(A)</li>
                <li><b>Lift</b> = Confidence / Support(B)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
