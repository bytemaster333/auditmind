from fpdf import FPDF
import pandas as pd
import re
import unicodedata

# Unicode ve emoji karakterlerini temizler
def remove_unicode_and_emojis(text):
    if not isinstance(text, str):
        return ""
    # Emojileri temizle
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # yüz ifadeleri
        u"\U0001F300-\U0001F5FF"  # semboller
        u"\U0001F680-\U0001F6FF"  # ulaşım
        u"\U0001F1E0-\U0001F1FF"  # ülke bayrakları
        u"\U00002700-\U000027BF"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    # Geriye kalan Unicode'ları kaldır
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text

def generate_pdf_report(address, analysis, score, level, attack, behavior, imports):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Tüm metinleri temizle
    clean_analysis = remove_unicode_and_emojis(analysis)
    clean_attack = remove_unicode_and_emojis(attack)
    clean_behavior = remove_unicode_and_emojis(behavior)
    clean_imports = remove_unicode_and_emojis(imports)
    clean_level = remove_unicode_and_emojis(level)
    clean_address = remove_unicode_and_emojis(address)

    # Başlık
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, "Smart Contract Audit Report", ln=True, align='C')
    pdf.ln(10)

    # Ana içerik
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Address: {clean_address}", ln=True)
    pdf.cell(0, 10, f"Risk Score: {score}/100 - {clean_level}", ln=True)
    pdf.ln(8)

    pdf.multi_cell(0, 10, f"Contract Analysis:\n{clean_analysis}\n")
    pdf.ln(2)
    pdf.multi_cell(0, 10, f"Attack Vector:\n{clean_attack}\n")
    pdf.ln(2)
    pdf.multi_cell(0, 10, f"Token Behavior:\n{clean_behavior}\n")
    pdf.ln(2)
    pdf.multi_cell(0, 10, f"Import Risk:\n{clean_imports}\n")

    # Dosya yolu
    path = f"report_{clean_address[:12]}.pdf"
    pdf.output(path)
    return path

def generate_csv_report(address, score, level, behavior):
    df = pd.DataFrame([{
        "Address": address,
        "Risk Score": score,
        "Risk Level": level,
        "Token Behavior": behavior
    }])
    path = f"report_{address[:12]}.csv"
    df.to_csv(path, index=False)
    return path
