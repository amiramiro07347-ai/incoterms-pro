import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="Incoterms Expert", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .expert-card {
        padding: 25px; border-radius: 15px; 
        background: white; border-left: 10px solid #1E3A8A;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-title { color: #1E3A8A; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>⚖️ مستشار قواعد Incoterms 2020</h1>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔍 معايير اختيار القاعدة")
    role = st.radio("دورك في العملية:", ["مصدّر (بائع)", "مستورد (مشتري)"])
    objective = st.selectbox("هدفك الأساسي:", [
        "تقليل المسؤولية والمخاطر لأقصى حد",
        "التحكم في تكاليف الشحن الدولي",
        "تسهيل الإجراءات للمشتري (خدمة كاملة)"
    ])
    transport = st.selectbox("وسيلة النقل المستخدمة:", ["بحري فقط", "بري/جوي/متعدد الوسائط"])

with col2:
    st.subheader("💡 التوصية القانونية")
    
    # منطق الاختيار
    if objective == "تقليل المسؤولية والمخاطر لأقصى حد" and role == "مصدّر (بائع)":
        rec, risk = "EXW (Ex Works)", "منخفض جداً (تنتهي مسؤوليتك عند باب مصنعك)"
    elif objective == "التحكم في تكاليف الشحن الدولي" and role == "مستورد (مشتري)":
        rec, risk = "FOB (Free On Board)", "متوسط (تبدأ مسؤوليتك من لحظة شحن البضاعة)"
    elif objective == "تسهيل الإجراءات للمشتري (خدمة كاملة)":
        rec, risk = "DDP (Delivered Duty Paid)", "عالٍ جداً (تتحمل كل شيء حتى الرسوم الجمركية)"
    else:
        rec, risk = "CIF (Cost, Insurance & Freight)", "متوازن (تدفع الشحن والتأمين لكن المخاطر تنتقل مبكراً)"

    st.markdown(f"""
        <div class="expert-card">
            <h2 style='color:#1E3A8A;'>القاعدة الأنسب: {rec}</h2>
            <p><b>مستوى مخاطرة البائع:</b> {risk}</p>
            <p style='color: #555;'>هذه القاعدة تضمن لك تحقيق هدفك بناءً على معطيات النقل والمسؤولية المختارة.</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("#### 💰 مثال تطبيقي في التسعير:")
    unit_price = st.number_input("سعر السلعة الأصلي ($):", value=1000)
    if "EXW" in rec: total = unit_price
    elif "FOB" in rec: total = unit_price + 200
    elif "CIF" in rec: total = unit_price + 550
    else: total = unit_price + 850
    
    st.success(f"السعر النهائي وفق قاعدة {rec} هو: **{total:,.2f} $**")
