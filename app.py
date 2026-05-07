import streamlit as st
import os
import uuid
from PyPDF2 import PdfReader
from docx import Document

# ---------------------- 页面配置 ----------------------
st.set_page_config(page_title="私人AI知识库", page_icon="📄", layout="wide")
st.title("📄 私人AI知识库 · 网页版")
st.markdown("### 每个人只能看到自己上传的文件，隐私安全")

# ---------------------- 独立用户ID（自动生成，互不干扰） ----------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

user_folder = f"user_files_{st.session_state.user_id}"
os.makedirs(user_folder, exist_ok=True)

# ---------------------- 上传文件 ----------------------
st.subheader("1. 上传你的 PDF / Word 文件")
uploaded_file = st.file_uploader("选择文件", type=["pdf", "docx"])

if uploaded_file is not None:
    file_path = os.path.join(user_folder, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 1. 先定义变量，接收上传结果
uploaded = st.file_uploader("上传你的 PDF / Word 文件", type=["pdf", "docx"])

# 2. 再判断变量是否存在，然后使用
if uploaded is not None:
    st.success(f"✅ 文件已保存: {uploaded.name}")

# ---------------------- 显示当前用户的文件 ----------------------
st.subheader("2. 你自己的文件列表（别人看不到）")
files = os.listdir(user_folder)
if files:
    for f in files:
        st.write(f"📄 {f}")
else:
    st.info("你还没有上传文件")

# ---------------------- 读取文件内容 ----------------------
def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

# ---------------------- 提问 ----------------------
st.subheader("3. 向你的文件提问")
question = st.text_input("输入你的问题")
if st.button("开始回答") and question and files:
    all_text = ""
    for f in files:
        p = os.path.join(user_folder, f)
        try:
            if f.endswith(".pdf"):
                all_text += read_pdf(p)
            elif f.endswith(".docx"):
                all_text += read_docx(p)
        except:
            pass
    
    st.markdown("### 📌 AI 根据你的文件回答：")
    st.write("文件内容：")
    st.success(all_text[:2000] + "..." if len(all_text) > 2000 else all_text)
    st.info(f"问题：{question}")
    st.success("✅ 已读取你的文件，可用于AI回答（离线版）")

# ---------------------- 说明 ----------------------
st.markdown("---")
st.markdown("""
### ✅ 产品特点
- 🌐 网页版，别人打开就能用
- 🔒 每个人独立空间，只能看自己的文件
- 📶 可离线运行
- 📄 支持 PDF / Word
- 🎯 学生、办公、项目组都能用
""")
