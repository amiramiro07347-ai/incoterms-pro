import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Inco-Smart Advisor", layout="wide")

# تصميم الواجهة وتنسيق الألوان
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1E3A8A; color: white; }
    .info-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #1E3A8A; }
    .welcome-text { text-align: center; color: #1E3A8A; }
    .footer-text { text-align: center; font-size: 14px; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# نظام القوائم (الصفحات)
tabs = st.tabs(["🏠 الواجهة الترحيبية", "⚙️ إدخال البيانات", "📊 عرض النتائج"])

# --- الصفحة الأولى: الواجهة الترحيبية ---
with tabs[0]:
    st.markdown("<h1 class='welcome-text'>مساعد الاستشارة الذكي لقواعد Incoterms</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
    <p style='text-align: center; font-size: 18px;'>
    مرحبًا بكم في منصتنا الذكية المصممة لتبسيط قرارات التجارة الدولية، حيث نساعدكم على اختيار القاعدة الأنسب 
    وتحليل المخاطر والتكاليف بدقة واحترافية عالية.
    </p>
    <hr>
    <div style='text-align: center;'>
        <h4>إعداد الطلبة:</h4>
        <p><b>لك آية - سهيل عطالي</b></p>
        <h4>تحت إشراف الأستاذة الفاضلة:</h4>
        <p><b>بن شريف كريمة</b></p>
        <hr>
        <p>جامعة محمد خيضر - بسكرة</p>
        <p>كلية العلوم الاقتصادية والتسيير وعلوم التجارة</p>
        <p>تخصص: لوجستيك - ماستر 1</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

# --- الصفحة الثانية: إدخال المعلومات ---
with tabs[1]:
    st.header("📋 مدخلات العملية اللوجستية")
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input("📍 نقطة الانطلاق (مثال: الصين)", "الصين")
        destination = st.text_input("🏁 نقطة الوصول (مثال: الجزائر)", "الجزائر")
        base_price = st.number_input("💰 سعر السلعة الأصلي ($)", min_value=0, value=5000)
        incoterm = st.selectbox("⚖️ اختر قاعدة Incoterm:", ["EXW", "FOB", "CIF", "DDP"])
    
    with col2:
        transport_mode = st.selectbox("🚢 وسيلة النقل:", ["بحري", "جوي", "بري"])
        estimated_days = st.number_input("⏳ الوقت المتوقع للرحلة (أيام)", min_value=1, value=30)
        risk_factor = st.slider("⚠️ مستوى الخطورة المتوقع (%)", 0, 100, 20)

    st.write("---")
    if st.button("عرض النتائج التفصيلية"):
        st.session_state['data_ready'] = True
        st.balloons()

# --- الصفحة الثالثة: النتائج ---
with tabs[2]:
    if 'data_ready' in st.session_state:
        st.header("📊 التقرير التحليلي النهائي")
        
        # حسابات افتراضية للنتائج
        shipping_cost = 500 if transport_mode == "بحري" else 1200
        carbon_footprint = estimated_days * 0.5 # معادلة رمزية للبصمة الكربونية
        total_cost = base_price + shipping_cost + (base_price * 0.1 if incoterm == "DDP" else 0)

        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("التكلفة الإجمالية", f"{total_cost} $")
        col_res2.metric("البصمة الكربونية", f"{carbon_footprint} CO2e")
        col_res3.metric("مستوى الأمان", f"{100 - risk_factor}%")

        st.markdown(f"""
        <div class='info-card'>
        <h3>تفاصيل الرحلة:</h3>
        <ul>
            <li><b>المسار:</b> من {origin} إلى {destination}</li>
            <li><b>القاعدة المستخدمة:</b> {incoterm}</li>
            <li><b>تحليل المخاطر:</b> مستوى الخطورة {risk_factor}% - ينصح بتأمين إضافي إذا تجاوزت 50%.</li>
            <li><b>الوقت المتوقع:</b> {estimated_days} يوم عمل.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("⭐ تقييم المنصة")
        rating = st.select_slider("قيم تجربتك:", options=[1, 2, 3, 4, 5])
        st.write(f"شكراً لتقييمك: {rating} نجوم")
        
        st.write("---")
        st.markdown("<h4 style='text-align: center;'>شكراً لزيارتكم!</h4>", unsafe_allow_html=True)
        
        # زر تحميل التقرير (محاكاة)
        report_data = f"تقرير رحلة {origin}-{destination}\nالقاعدة: {incoterm}\nالتكلفة: {total_cost}"
        st.download_button(label="📥 تحميل التقرير (PDF/Text)", data=report_data, file_name="logistics_report.txt")
    else:
        st.warning("يرجى إدخال البيانات في الصفحة الثانية أولاً.")
