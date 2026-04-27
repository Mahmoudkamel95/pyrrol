import streamlit as st
import pandas as pd

st.title("📊 مفردات المرتب")

url = "https://docs.google.com/spreadsheets/d/1ku7qkt_cnfM722rS7r4mzPipVIYxFRS6cVlI0HBTxnY/export?format=csv&gid=0"
df = pd.read_csv(url)

emp_id = st.text_input("ادخل ID الموظف")

# 🔥 زرار البحث
search = st.button("🔍 بحث")

if search:
    if emp_id:
        emp_data = df[df["id hr"].astype(str) == emp_id]

        if emp_data.empty:
            st.error("❌ الموظف غير موجود")
        else:
            st.success("✅ تم العثور على الموظف")

            # حذف الأعمدة الأساسية
            basic_cols = ["id hr", "الرقــــم القـــــــومى", "محافظة العمل", "الدرجه"]
            data = emp_data.drop(columns=basic_cols, errors='ignore')

            # تحويل البيانات
            data = data.T
            data.columns = ["القيمة"]

            # حذف القيم الفاضية أو صفر
            data = data[(data["القيمة"] != 0) & (data["القيمة"].notna())]

            st.dataframe(data)
    else:
        st.warning("⚠️ من فضلك ادخل ID الموظف")
