import streamlit as st
import requests

st.set_page_config(page_title="Forex Signal AI", page_icon="📈", layout="centered")

st.markdown("<h2 style='text-align: center; color: #4CAF50;'>📈 Forex Market Analyzer</h2>", unsafe_allow_html=True)
st.write("---")

symbol = st.selectbox("আপনার অ্যাসেট বেছে নিন:", ["XAUUSD (Gold)", "EURUSD", "GBPUSD"])

def analyze_forex(asset):
    ticker = "GC=F" if "XAUUSD" in asset else asset.split()[0] + "=X"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=5m"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(url, headers=headers).json()
        prices = res['chart']['result'][0]['indicators']['quote'][0]['close']
        prices = [p for p in prices if p is not None]
        
        current_price = round(prices[-1], 2)
        sma_20 = round(sum(prices[-20:]) / 20, 2)
        support = round(min(prices[-20:]), 2)
        resistance = round(max(prices[-20:]), 2)
        
        return current_price, sma_20, support, resistance
    except:
        return None, None, None, None

if st.button("🚀 মার্কেট অ্যানালাইসিস করুন", use_container_width=True):
    with st.spinner('লাইভ মার্কেট ডাটা অ্যানালাইসিস করা হচ্ছে...'):
        price, sma, support, resistance = analyze_forex(symbol)
        
        if price is None:
            st.error("মার্কেট ডাটা পেতে সমস্যা হচ্ছে, আবার চেষ্টা করুন।")
        else:
            st.write(f"### 📍 বর্তমান প্রাইস: **{price}**")
            
            if price > sma:
                tp_line = round(price + (resistance - price) * 0.8 + 1.5, 2)
                sl_line = round(support - 0.5, 2)
                
                st.success("🟢 **সিগন্যাল: BUY (মার্কেট উপরে যাওয়ার সম্ভাবনা বেশি)**")
                st.markdown(f"🟢 **টাকা তুলে ফেলার লাইন (Take Profit): {tp_line}**")
                st.markdown(f"🔴 **লস কাটার লাইন (Stop Loss): {sl_line}**")
            else:
                tp_line = round(price - (price - support) * 0.8 - 1.5, 2)
                sl_line = round(resistance + 0.5, 2)
                
                st.error("🔴 **সিগন্যাল: SELL (মার্কেট নিচে যাওয়ার সম্ভাবনা বেশি)**")
                st.markdown(f"🟢 **টাকা তুলে ফেলার লাইন (Take Profit): {tp_line}**")
                st.markdown(f"🔴 **লস কাটার লাইন (Stop Loss): {sl_line}**")

            st.info(f"💡 পরামর্শ: মার্কেট {tp_line} এ গেলে প্রফিটে বন্ধ হবে, এবং {sl_line} এ নামলে লস থামিয়ে ট্রেড বন্ধ হবে।")
      
