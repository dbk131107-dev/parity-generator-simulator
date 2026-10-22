import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mô Phỏng Parity Generator & Checker - Đỗ Bảo Khang",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Mô Phỏng Mạch Tạo & Kiểm Tra Chẵn Lẻ (Parity Generator & Checker)")
st.markdown("**Môn học:** Điện Tử Số | **Giáo trình:** G.K. Kharate (Mục 4.9 – 4.11, tr. 233–241) | **Người trình bày:** Đỗ Bảo Khang")
st.divider()

tab1, tab2, tab3 = st.tabs([
    "🔌 1. Mô Phỏng Truyền Tin & Cổng XOR (3-bit / 4-bit)",
    "🔲 2. Mô Phỏng Vi Mạch MSI IC 74180 (8-bit)",
    "📊 3. Bảng Giá Trị Hàm & Bìa Karnaugh Động"
])

# ==========================================
# TAB 1: MÔ PHỎNG HỆ THỐNG GENERATOR & CHECKER
# ==========================================
with tab1:
    st.subheader("Mô phỏng toàn trình: Bộ Phát (Generator) ➔ Kênh Truyền Nhiễu ➔ Bộ Thu (Checker)")

    col_cfg1, col_cfg2 = st.columns([1, 2])
    with col_cfg1:
        bit_mode = st.radio("Số bit dữ liệu đầu vào:", [3, 4], index=1, horizontal=True)
        parity_type = st.radio("Chuẩn Parity hệ thống:", ["Parity Chẵn (Even)", "Parity Lẻ (Odd)"], horizontal=True)

    with col_cfg2:
        st.info(
            "💡 **Hướng dẫn:** Bật/tắt các công tắc bit dữ liệu ở **Bộ Phát**, sau đó thử bấm vào các công tắc **Gây nhiễu lật bit** ở giữa để xem **Bộ Thu** phát hiện lỗi (1 bit lỗi) hay bị đánh lừa (2 bit lỗi cùng lúc)!"
        )

    col_tx, col_ch, col_rx = st.columns(3)

    # 1. BỘ PHÁT
    with col_tx:
        st.markdown("### 1️⃣ Bộ Phát (Parity Generator)")
        a = int(st.toggle("Bit A (MSB)", value=True))
        b = int(st.toggle("Bit B", value=False))
        c = int(st.toggle("Bit C", value=True))
        d = int(st.toggle("Bit D (LSB)", value=False)) if bit_mode == 4 else 0

        data_bits = [a, b, c] if bit_mode == 3 else [a, b, c, d]
        ones_tx = sum(data_bits)
        xor_tx = 0
        for bit in data_bits:
            xor_tx ^= bit

        if "Chẵn" in parity_type:
            p_bit = xor_tx
            eq_str = " ⊕ ".join([str(x) for x in data_bits]) + f" = {p_bit}"
            p_label = "Pe"
        else:
            p_bit = 1 - xor_tx
            eq_str = "(" + " ⊕ ".join([str(x) for x in data_bits]) + f")' = {p_bit}"
            p_label = "Po"

        tx_frame = "".join(map(str, data_bits)) + str(p_bit)
        st.metric(label=f"Bit Parity tạo ra ({p_label})", value=str(p_bit))
        st.code(f"Số bit 1 trong dữ liệu: {ones_tx}\nPhương trình: {p_label} = {eq_str}\nKhung truyền đi: {tx_frame}", language="text")

    # 2. KÊNH TRUYỀN & TẠO NHIỄU
    with col_ch:
        st.markdown("### 2️⃣ Kênh Truyền (Giả Lập Nhiễu)")
        st.caption("Bật công tắc bất kỳ dưới đây để giả lập nhiễu làm lật bit đó trên đường dây:")
        flip_a = int(st.checkbox("⚡ Lật Bit A", value=False))
        flip_b = int(st.checkbox("⚡ Lật Bit B", value=False))
        flip_c = int(st.checkbox("⚡ Lật Bit C", value=False))
        flip_d = int(st.checkbox("⚡ Lật Bit D", value=False)) if bit_mode == 4 else 0
        flip_p = int(st.checkbox(f"⚡ Lật Bit Parity ({p_label})", value=False))

        flips = [flip_a, flip_b, flip_c, flip_p] if bit_mode == 3 else [flip_a, flip_b, flip_c, flip_d, flip_p]
        num_errors = sum(flips)

        if num_errors == 0:
            st.success("Đường truyền sạch: **0 bit bị lỗi**")
        elif num_errors % 2 == 1:
            st.error(f"Đường truyền nhiễu: **{num_errors} bit bị lật (Số lẻ lỗi)**")
        else:
            st.warning(f"Đường truyền nhiễu: **{num_errors} bit bị lật (Số chẵn lỗi - Điểm mù!)**")

    # 3. BỘ THU
    with col_rx:
        st.markdown("### 3️⃣ Bộ Thu (Parity Checker)")
        ra = a ^ flip_a
        rb = b ^ flip_b
        rc = c ^ flip_c
        rd = (d ^ flip_d) if bit_mode == 4 else 0
        rp = p_bit ^ flip_p

        rx_bits = [ra, rb, rc, rp] if bit_mode == 3 else [ra, rb, rc, rd, rp]
        rx_ones = sum(rx_bits)
        xor_rx = 0
        for bit in rx_bits:
            xor_rx ^= bit

        if "Chẵn" in parity_type:
            e_bit = xor_rx
            e_label = "Ee"
            e_eq = " ⊕ ".join(map(str, rx_bits)) + f" = {e_bit}"
        else:
            e_bit = 1 - xor_rx
            e_label = "Eo"
            e_eq = "(" + " ⊕ ".join(map(str, rx_bits)) + f")' = {e_bit}"

        rx_frame = "".join(map(str, rx_bits))
        st.metric(label=f"Ngõ ra báo lỗi ({e_label})", value=f"{e_bit} ({'BÁO LỖI' if e_bit == 1 else 'HỢP LỆ'})")
        st.code(f"Khung nhận được: {rx_frame}\nTổng số bit 1 nhận được: {rx_ones} ({'Chẵn' if rx_ones % 2 == 0 else 'Lẻ'})\nPhương trình: {e_label} = {e_eq}", language="text")

        if e_bit == 0 and num_errors == 0:
            st.success("✅ **KẾT LUẬN:** E = 0. Dữ liệu nhận được chính xác 100%!")
        elif e_bit == 1:
            st.error(f"🚨 **KẾT LUẬN:** E = 1. Mạch Parity Checker đã **PHÁT HIỆN ĐƯỢC LỖI** (do có {num_errors} bit bị lật)!")
        elif e_bit == 0 and num_errors > 0:
            st.warning(f"⚠️ **ĐIỂM MÙ PARITY:** Có tới **{num_errors} bit bị lật** nhưng tổng số bit 1 vẫn giữ tính {'Chẵn' if 'Chẵn' in parity_type else 'Lẻ'}, nên E = 0 (Mạch bị đánh lừa!).")

# ==========================================
# TAB 2: MÔ PHỎNG VI MẠCH IC 74180 (8-BIT)
# ==========================================
with tab2:
    st.subheader("Mô phỏng Vi mạch MSI IC 74180 (8-Bit Odd/Even Parity Generator/Checker)")
    st.markdown("Chọn trạng thái 8 chân dữ liệu `I0 – I7` và 2 chân điều khiển `Even Input`, `Odd Input` (Mục 4.11 trang 239):")

    cols_i = st.columns(8)
    i_bits = []
    default_i = [1, 0, 1, 1, 0, 0, 1, 0]
    for idx in range(8):
        with cols_i[idx]:
            val = int(st.checkbox(f"I{idx}", value=bool(default_i[idx])))
            i_bits.append(val)

    c_ctrl1, c_ctrl2, c_out = st.columns([1, 1, 2])
    with c_ctrl1:
        even_in = st.selectbox("Chân Even Input (Ngõ vào Chẵn):", [1, 0], index=0)
    with c_ctrl2:
        odd_in = st.selectbox("Chân Odd Input (Ngõ vào Lẻ):", [0, 1], index=0)

    sum_ones_8bit = sum(i_bits)
    is_data_even = (sum_ones_8bit % 2 == 0)

    # Logic chuẩn của IC 74180 theo Bảng chân trị trang 239
    if even_in == 1 and odd_in == 1:
        sigma_even, sigma_odd = 0, 0
    elif even_in == 0 and odd_in == 0:
        sigma_even, sigma_odd = 1, 1
    elif even_in == 1 and odd_in == 0:
        sigma_even = 1 if is_data_even else 0
        sigma_odd = 0 if is_data_even else 1
    else:  # even_in == 0 and odd_in == 1
        sigma_even = 0 if is_data_even else 1
        sigma_odd = 1 if is_data_even else 0

    with c_out:
        st.markdown("#### Kết quả ngõ ra IC 74180:")
        m1, m2, m3 = st.columns(3)
        m1.metric("Tổng bit 1 (I0–I7)", f"{sum_ones_8bit} ({'Chẵn' if is_data_even else 'Lẻ'})")
        m2.metric("Ngõ ra Σ Even", str(sigma_even))
        m3.metric("Ngõ ra Σ Odd", str(sigma_odd))

# ==========================================
# TAB 3: BẢNG CHÂN TRỊ & KARNAUGH
# ==========================================
with tab3:
    st.subheader("Bảng Giá Trị Hàm Mạch Tạo Parity 3-Bit & Mạch Kiểm Tra 4-Bit")
    rows = []
    for val in range(8):
        ba = (val >> 2) & 1
        bb = (val >> 1) & 1
        bc = val & 1
        cnt = ba + bb + bc
        pe = ba ^ bb ^ bc
        po = 1 - pe
        rows.append({
            "Số thập phân": val,
            "A": ba, "B": bb, "C": bc,
            "Số lượng bit 1": f"{cnt} ({'Chẵn' if cnt % 2 == 0 else 'Lẻ'})",
            "Parity Chẵn (Pe = A⊕B⊕C)": pe,
            "Parity Lẻ (Po = A⊙B⊙C)": po
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)