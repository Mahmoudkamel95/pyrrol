import streamlit as st
import pandas as pd

st.title("📊 مفردات المرتب")

# 🟢 الاستحقاقات
url_est7qaq = "https://docs.google.com/spreadsheets/d/1ku7qkt_cnfM722rS7r4mzPipVIYxFRS6cVlI0HBTxnY/export?format=csv&gid=0"

# 🔴 الاستقطاعات
url_est2ta3 = "https://docs.google.com/spreadsheets/d/1ku7qkt_cnfM722rS7r4mzPipVIYxFRS6cVlI0HBTxnY/export?format=csv&gid=535952387"

df_est7qaq = pd.read_csv(url_est7qaq)
df_est2ta3 = pd.read_csv(url_est2ta3)

emp_id = st.text_input("ادخل ID الموظف")
search = st.button("🔍 بحث")

if search:
    if emp_id:

        # 🔍 فلترة الموظف
        emp7 = df_est7qaq[df_est7qaq["id hr"].astype(str) == emp_id]
        emp2 = df_est2ta3[df_est2ta3["id hr"].astype(str) == emp_id]

        if emp7.empty and emp2.empty:
            st.error("❌ الموظف غير موجود")
        else:
            st.success("✅ تم العثور على الموظف")

            # 👤 الاسم والدرجة (من الاستحقاقات)
            name = emp7["الإسم"].iloc[0] if "الإسم" in emp7.columns else "-"
            grade = emp7["الدرجه"].iloc[0] if "الدرجه" in emp7.columns else "-"

            st.markdown(f"### 👤 الإسم: {name}")
            st.markdown(f"### 🎓 الدرجة: {grade}")

            # 🔥 الأعمدة غير الحسابية
            basic_cols = [
                "id hr",
                "الرقــــم القـــــــومى",
                "محافظة العمل"
                
            ]

            # 🟢 الاستحقاقات
            data7 = emp7.drop(columns=basic_cols, errors='ignore').T
            data7.columns = ["القيمة"]

            # 🔴 الاستقطاعات
            data2 = emp2.drop(columns=basic_cols, errors='ignore').T
            data2.columns = ["القيمة"]

            # 🔥 تنظيف الداتا (أهم جزء)
            def clean(df):
                df["القيمة"] = pd.to_numeric(
                    df["القيمة"].astype(str).str.replace(",", ""),
                    errors="coerce"
                )
                df = df[df["القيمة"].notna()]
                df = df[df["القيمة"] != 0]
                df = df[~df.index.str.contains("اجمالي|إجمالي", case=False)]
                return df

            data7 = clean(data7)
            data2 = clean(data2)

            # 📊 عرض جنب بعض
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🟢 الاستحقاقات")
                st.dataframe(data7)

            with col2:
                st.subheader("🔴 الاستقطاعات")
                st.dataframe(data2)

    else:
        st.warning("⚠️ من فضلك ادخل ID الموظف")
