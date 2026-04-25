import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="Inco-Smart Advisor", layout="wide")

# تصميم الواجهة وتنسيق الألوان
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1E3A8A; color: white; }
    .info-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #1E3A8A; margin-bottom: 20px; }
    .result-card { padding: 20px; border-radius: 15px; background: #f0f4ff; border-right: 5px solid #1E3A8A; }
    .welcome-text { text-align: center; color: #1E3A8A; font-weight: bold; }
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
        <p style='font-size: 20px;'><b>اللك آية - سهيل عطالي</b></p>
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
        st.subheader("📍 تفاصيل الرحلة")
        origin = st.text_input("نقطة الانطلاق (مثال: الصين)", "الصين")
        destination = st.text_input("نقطة الوصول (مثال: الجزائر)", "الجزائر")
        role = st.radio("حدد دورك في العملية:", ["مصدّر (بائع)", "مستورد (مشتري)"])
        base_price = st.number_input("💰 سعر السلعة الأصلي ($)", min_value=0, value=5000)
        
    with col2:
        st.subheader("🚢 تفاصيل اللوجستيك")
        incoterm = st.selectbox("⚖️ اختر قاعدة Incoterm المراد تحليلها:", ["EXW", "FOB", "CIF", "DDP"])
        transport_mode = st.selectbox("وسيلة النقل:", ["بحري", "جوي", "بري"])
        estimated_days = st.number_input("⏳ الوقت المتوقع للرحلة (أيام)", min_value=1, value=30)
        risk_factor = st.slider("⚠️ مستوى الخطورة المتوقع (%)", 0, 100, 20)

    st.write("---")
    if st.button("عرض التقرير والنتائج"):
        st.session_state['data_ready'] = True
        st.balloons()

# --- الصفحة الثالثة: النتائج ---
with tabs[2]:
    if 'data_ready' in st.session_state:
        st.header("📊 التقرير التحليلي النهائي")
        
        explanations = {
            "EXW": "المشتري يتحمل كافة التكاليف والمخاطر من باب مصنع البائع.",
            "FOB": "البائع يسلم البضاعة على ظهر السفينة، ومن هنا تنتقل المخاطر للمشتري.",
            "CIF": "البائع يدفع تكاليف الشحن والتأمين حتى ميناء الوصول، لكن المخاطر تنتقل عند الشحن.",
            "DDP": "البائع يتحمل كل شيء حتى تسليم البضاعة في مخازن المشتري شاملة الرسوم الجمركية."
        }
        
        # منطق التسعير المطور
        shipping_fees = 800 if transport_mode == "بحري" else 1500
        insurance_fee = base_price * 0.05
        customs_fee = base_price * 0.15
        
        if incoterm == "EXW":
            total_cost = base_price
            ship_status, ins_status, cust_status = "على المشتري", "على المشتري", "على المشتري"
        elif incoterm == "FOB":
            total_cost = base_price + 200 
            ship_status, ins_status, cust_status = "على المشتري (من الميناء)", "على المشتري", "على المشتري"
        elif incoterm == "CIF":
            total_cost = base_price + shipping_fees + insurance_fee
            ship_status, ins_status, cust_status = f"مدرج ({shipping_fees} $)", f"مدرج ({insurance_fee} $)", "على المشتري"
        else: # DDP
            total_cost = base_price + shipping_fees + insurance_fee + customs_fee
            ship_status, ins_status, cust_status = f"مدرج ({shipping_fees} $)", f"مدرج ({insurance_fee} $)", f"مدرج ({customs_fee} $)"

        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("التكلفة الإجمالية", f"{total_cost:,.2f} $")
        col_res2.metric("البصمة الكربونية", f"{estimated_days * 0.4} CO2e")
        col_res3.metric("مستوى الأمان", f"{100 - risk_factor}%")

        st.markdown(f"""
        <div class='result-card'>
        <h3>🔍 شرح القاعدة المختارة ({incoterm}):</h3>
        <p>{explanations[incoterm]}</p>
        <hr>
        <h3>💰 تفاصيل عملية التسعير (التحليل المالي):</h3>
        <ul>
            <li><b>السعر الأساسي للسلعة:</b> {base_price:,.2f} $</li>
            <li><b>مصاريف الشحن الدولي:</b> {ship_status}</li>
            <li><b>تأمين البضاعة:</b> {ins_status}</li>
            <li><b>الرسوم الجمركية:</b> {cust_status}</li>
        </ul>
        <p style='color: #1E3A8A; font-weight: bold; font-size: 18px;'>النتيجة النهائية للمصاريف كـ {role}: {total_cost:,.2f} $</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("⭐ تقييمك للمنصة")
        star_rating = st.feedback("stars")
        if star_rating is not None:
            st.success(f"شكراً لتقييمك بـ {star_rating + 1} نجوم!")
        
        st.write("---")
        st.markdown("<h4 style='text-align: center;'>شكراً لزيارتكم!</h4>", unsafe_allow_html=True)
        
        report_text = f"تقرير رحلة {origin}-{destination}\nالقاعدة: {incoterm}\nالتكلفة الإجمالية: {total_cost} $"
        st.download_button("📥 تحميل التقرير التفصيلي", report_text, file_name="Incoterms_Report.txt")
    else:
        st.warning("يرجى إدخال البيانات في الصفحة الثانية أولاً ثم الضغط على 'عرض التقرير'.")
