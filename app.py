import streamlit as st
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime


st.set_page_config(page_title="Analisis Pola Pembelian Emas FP-Growth", layout="wide")

st.title("Analisis Pola Pembelian Emas FP-Growth")
st.write(
    """
    ini halaman utama.
    """
)

st.divider()

# Upload Data
st.subheader("Upload Data Transaksi")

import pandas as pd

uploaded_file = st.file_uploader(
    "Upload file transaksi (CSV atau Excel)", type=["csv", "xlsx"]
)

df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File berhasil diupload dan dibaca.")

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")

if df is not None:
    st.subheader("Preview Data Transaksi")
    st.dataframe(df.head(10), width="stretch")

    st.write(f"Jumlah baris: {df.shape[0]} | Jumlah kolom: {df.shape[1]}")

    st.subheader("Pilih Kolom yang Digunakan")

    columns = df.columns.tolist()

    col_transaksi = st.selectbox(
        "Pilih kolom ID Transaksi / No. Faktur",
        options=columns,
        help="Kolom ini digunakan untuk mengelompokkan item dalam satu transaksi.",
    )

    col_item = st.selectbox(
        "Pilih kolom Nama Item / Keterangan",
        options=columns,
        help="Kolom ini berisi nama produk yang dibeli pelanggan.",
    )

    if col_transaksi == col_item:
        st.warning("Kolom transaksi dan kolom item tidak boleh sama.")
    else:
        if df[col_transaksi].isnull().any() or df[col_item].isnull().any():
            st.warning(
                "Terdapat nilai kosong pada kolom yang dipilih. Baris kosong akan diabaikan saat analisis."
            )
        else:
            st.success("Kolom valid dan siap digunakan untuk analisis.")

        st.session_state["df"] = df
        st.session_state["col_transaksi"] = col_transaksi
        st.session_state["col_item"] = col_item

if (
    "df" in st.session_state
    and "col_transaksi" in st.session_state
    and "col_item" in st.session_state
):
    df = st.session_state["df"]
    col_transaksi = st.session_state["col_transaksi"]
    col_item = st.session_state["col_item"]
else:
    st.stop()

st.subheader("Preprocessing Data")

df_clean = df[[col_transaksi, col_item]].copy()

# Hapus baris kosong
df_clean.dropna(inplace=True)

# Normalisasi teks item
df_clean[col_item] = (
    df_clean[col_item]
    .astype(str)
    .str.lower()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

st.write("Data telah dibersihkan dan dinormalisasi.")

total_rows = df_clean.shape[0]
unique_transactions = df_clean[col_transaksi].nunique()
unique_items = df_clean[col_item].nunique()

st.write(f"Total baris setelah pembersihan: **{total_rows}**")
st.write(f"Jumlah transaksi unik: **{unique_transactions}**")
st.write(f"Jumlah item unik: **{unique_items}**")

transactions = (
    df_clean.groupby(col_transaksi)[col_item].apply(list).reset_index(name="items")
)

st.subheader("Contoh Struktur Data Transaksi")

st.dataframe(transactions.head(), width="stretch")

st.session_state["transactions"] = transactions["items"].tolist()


st.divider()

# Parameter Analisis

st.subheader("Parameter Analisis")

st.write("Slider Parameter")

min_support = st.slider(
    "Minimum Support",
    min_value=0.001,
    max_value=0.1,
    value=0.01,
    step=0.001,
    help="Semakin kecil nilai, semakin banyak pola yang mungkin ditemukan.",
)

min_confidence = st.slider(
    "Minimum Confidence",
    min_value=0.1,
    max_value=1.0,
    value=0.3,
    step=0.05,
    help="Menunjukkan seberapa kuat hubungan antar produk.",
)

st.divider()


# Tombol Analisis


def generate_pdf(rules, min_support, min_confidence):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Judul
    elements.append(
        Paragraph("Laporan Analisis Pola Pembelian Pelanggan", styles["Title"])
    )
    elements.append(Spacer(1, 12))

    # Info parameter
    elements.append(
        Paragraph(
            f"Tanggal Analisis: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"],
        )
    )
    elements.append(Paragraph(f"Minimum Support: {min_support}", styles["Normal"]))
    elements.append(
        Paragraph(f"Minimum Confidence: {min_confidence}", styles["Normal"])
    )
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Hasil Aturan Pembelian:", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    rule_items = []

    for _, row in rules.iterrows():
        sentence = (
            f"Jika pelanggan membeli {row['antecedents']}, "
            f"maka pelanggan cenderung membeli {row['consequents']} "
            f"(Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f})."
        )
        rule_items.append(ListItem(Paragraph(sentence, styles["Normal"])))

    if rule_items:
        elements.append(ListFlowable(rule_items, bulletType="bullet"))
    else:
        elements.append(Paragraph("Tidak ditemukan aturan asosiasi.", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer


if st.button("Analisis Pola Pembelian"):

    if "transactions" not in st.session_state:
        st.error("Data transaksi belum siap diproses.")
        st.stop()

    transactions = st.session_state["transactions"]

    st.subheader("4. Proses Analisis FP-Growth")

    with st.spinner("Sedang menjalankan analisis..."):
        # Encoding transaksi
        te = TransactionEncoder()
        te_array = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_array, columns=te.columns_)

        # Jalankan FP-Growth
        frequent_itemsets = fpgrowth(
            df_encoded, min_support=min_support, use_colnames=True
        )

        if frequent_itemsets.empty:
            st.warning("Tidak ditemukan frequent itemsets dengan parameter saat ini.")
            st.stop()

        # Association Rules
        rules = association_rules(
            frequent_itemsets, metric="confidence", min_threshold=min_confidence
        )

        rules = rules[rules["lift"] > 1]

    st.success("Analisis selesai.")

    st.subheader("Hasil Pola Pembelian (Natural Language)")

    if rules.empty:
        st.info("Tidak ditemukan aturan asosiasi dengan parameter yang dipilih.")
    else:
        for _, row in rules.iterrows():
            antecedent = ", ".join(list(row["antecedents"]))
            consequent = ", ".join(list(row["consequents"]))

            st.write(
                f"Jika pelanggan membeli **{antecedent}**, "
                f"maka pelanggan cenderung membeli **{consequent}** "
                f"(Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f})."
            )

    st.subheader("Tabel Detail Association Rules")

    rules_display = rules.copy()
    rules_display["antecedents"] = rules_display["antecedents"].apply(
        lambda x: ", ".join(list(x))
    )
    rules_display["consequents"] = rules_display["consequents"].apply(
        lambda x: ", ".join(list(x))
    )

    st.dataframe(
        rules_display[["antecedents", "consequents", "support", "confidence", "lift"]],
        width="stretch",
    )

    st.session_state["rules"] = rules_display
    st.session_state["min_support"] = min_support
    st.session_state["min_confidence"] = min_confidence

    st.subheader("Unduh Laporan")

    pdf_buffer = generate_pdf(
        st.session_state["rules"],
        st.session_state["min_support"],
        st.session_state["min_confidence"],
    )

    st.download_button(
        label="Download Laporan PDF",
        data=pdf_buffer,
        file_name="laporan_pola_pembelian.pdf",
        mime="application/pdf",
    )
