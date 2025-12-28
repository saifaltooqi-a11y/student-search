import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="نظام الشهادات", layout="centered")

st.title("🎓 نظام استخراج الشهادات")
st.write("أدخل الرقم المدني للحصول على شهادتك")

# خانة البحث
civil_id = st.text_input("الرقم المدني:", placeholder="اكتب الرقم هنا...")

if civil_id:
    try:
        # فتح الملف
        doc = fitz.open("data.pdf")
        found = False
        
        # البحث في الصفحات
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # نبحث عن النص بطريقة بسيطة وسريعة
            if civil_id in page.get_text():
                st.success(f"تم العثور على الشهادة!")
                
                # تحويل الصفحة لصورة لعرضها فوراً
                pix = page.get_pixmap(dpi=100) # تقليل الجودة قليلاً للسرعة
                st.image(pix.tobytes(), use_container_width=True)
                
                # زر التحميل
                pdf_bytes = doc.convert_to_pdf(from_page=page_num, to_page=page_num)
                st.download_button(
                    label="📥 تحميل الشهادة (PDF)",
                    data=pdf_bytes,
                    file_name=f"Certificate_{civil_id}.pdf",
                    mime="application/pdf"
                )
                found = True
                break
        
        if not found:
            st.warning("الرقم المدني غير موجود في النظام.")
            
    except Exception as e:
        st.error("تأكد من وجود ملف data.pdf في المستودع.")
