import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Triangle Center Explorer", layout="wide")

st.title("📐 任意實數 - 三角形四心幾何探索器")
st.write("現在你可以手動輸入任何大小的實數（正數、負數、小數）來設定頂點座標，圖表將完全不受限制。")

# --- 側邊欄：自由輸入任何實數 ---
st.sidebar.header("📍 頂點座標輸入 (支援任意實數)")

st.sidebar.subheader("頂點 A")
ax = st.sidebar.number_input("A(x)", value=0.0, step=1.0, format="%.2f")
ay = st.sidebar.number_input("A(y)", value=6.0, step=1.0, format="%.2f")

st.sidebar.subheader("頂點 B")
bx = st.sidebar.number_input("B(x)", value=-6.0, step=1.0, format="%.2f")
by = st.sidebar.number_input("B(y)", value=-3.0, step=1.0, format="%.2f")

st.sidebar.subheader("頂點 C")
cx = st.sidebar.number_input("C(x)", value=6.0, step=1.0, format="%.2f")
cy = st.sidebar.number_input("C(y)", value=-3.0, step=1.0, format="%.2f")

A = np.array([ax, ay])
B = np.array([bx, by])
C = np.array([cx, cy])

# --- 功能勾選選單 ---
st.sidebar.header("🎯 選擇要顯示的幾何中心")
selected_centers = st.sidebar.multiselect(
    "可以選擇多個：",
    ["Centroid (重心中線)", "Circumcenter (外心外接圓)", "Incenter (內心內切圓)", "Orthocenter (垂心高線)"],
    default=["Orthocenter (垂心高線)"]
)

# 新增圖表縮放控制
st.sidebar.header("⚙️ 圖表視窗設定")
auto_scale = st.sidebar.checkbox("自動根據座標縮放視窗", value=True)

# --- 幾何計算函式 ---
def get_line_equation(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if abs(x2 - x1) < 1e-9:
        return None, x1
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return m, c

def get_perpendicular_line(point, base_m, base_c, is_vertical_base, base_x_if_vert):
    xp, yp = point
    if is_vertical_base: 
        return 0.0, yp
    if abs(base_m) < 1e-9: 
        return None, xp
    m_perp = -1.0 / base_m
    c_perp = yp - m_perp * xp
    return m_perp, c_perp

def find_intersection(m1, c1, m2, c2):
    if m1 is None and m2 is None: return None
    if m1 is None: return np.array([c1, m2 * c1 + c2])
    if m2 is None: return np.array([c2, m1 * c2 + c1])
    if abs(m1 - m2) < 1e-9: return None
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    return np.array([x, y])

def format_eq(m, c, prefix):
    if m is None: return f"**{prefix}**: $x = {c:.2f}$"
    if abs(m) < 1e-9: return f"**{prefix}**: $y = {c:.2f}$"
    return f"**{prefix}**: $y = {m:.2f}x {'+' if c>=0 else '-'} {abs(c):.2f}$"

# --- 邏輯驗證與繪圖 ---
D = A[0]*(B[1] - C[1]) + B[0]*(C[1] - A[1]) + C[0]*(A[1] - B[1])

if abs(D) < 1e-9:
    st.error("❌ 警告：這三個點共線，無法結合成一個封閉的三角形！請修改座標數字。")
else:
    a_len = np.linalg.norm(B - C)
    b_len = np.linalg.norm(A - C)
    c_len = np.linalg.norm(A - B)
    
    col1, col2 = st.columns([3, 2])
    
    fig, ax_plt = plt.subplots(figsize=(7, 7))
    tx = [A[0], B[0], C[0], A[0]]
    ty = [A[1], B[1], C[1], A[1]]
    ax_plt.plot(tx, ty, 'k-', linewidth=2, label='Triangle Framework')
    ax_plt.scatter([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='black', zorder=5)
    ax_plt.text(A[0], A[1], f' A({A[0]:.1f}, {A[1]:.1f})', fontsize=11, va='bottom')
    ax_plt.text(B[0], B[1], f' B({B[0]:.1f}, {B[1]:.1f})', fontsize=11, va='top', ha='right')
    ax_plt.text(C[0], C[1], f' C({C[0]:.1f}, {C[1]:.1f})', fontsize=11, va='top', ha='left')
    
    with col2:
        st.subheader("📊 幾何數據與直線方程式")
        
        # 1. 重心 (Centroid)
        if "Centroid (重心中線)" in selected_centers:
            centroid = (A + B + C) / 3
            mid_BC = (B + C) / 2
            mid_AC = (A + C) / 2
            mid_AB = (A + B) / 2
            
            ax_plt.plot([A[0], mid_BC[0]], [A[1], mid_BC[1]], 'r:', alpha=0.7)
            ax_plt.plot([B[0], mid_AC[0]], [B[1], mid_AC[1]], 'r:', alpha=0.7)
            ax_plt.plot([C[0], mid_AB[0]], [C[1], mid_AB[1]], 'r:', alpha=0.7)
            ax_plt.scatter(centroid[0], centroid[1], color='red', s=120, zorder=6, label='Centroid (G)')
            
            m_mA, c_mA = get_line_equation(A, mid_BC)
            st.write("#### 🔴 重心 (Centroid G):")
            st.write(f"座標位置: `({centroid[0]:.2f}, {centroid[1]:.2f})`")
            st.write(format_eq(m_mA, c_mA, "中線 AD (from A)"))
            st.write("---")

        # 2. 外心 (Circumcenter)
        if "Circumcenter (外心外接圓)" in selected_centers:
            m_BC, c_BC = get_line_equation(B, C)
            mid_BC = (B + C) / 2
            m_pBC, c_pBC = get_perpendicular_line(mid_BC, m_BC, c_BC, m_BC is None, B[0])
            
            m_AC, c_AC = get_line_equation(A, C)
            mid_AC = (A + C) / 2
            m_pAC, c_pAC = get_perpendicular_line(mid_AC, m_AC, c_AC, m_AC is None, A[0])
            
            circumcenter = find_intersection(m_pBC, c_pBC, m_pAC, c_pAC)
            r_circum = np.linalg.norm(circumcenter - A)
            
            circle = plt.Circle(circumcenter, r_circum, color='blue', fill=False, linestyle='-.', alpha=0.5, linewidth=1.5)
            ax_plt.add_patch(circle)
            ax_plt.scatter(circumcenter[0], circumcenter[1], color='blue', s=120, zorder=6, label='Circumcenter (O)')
            
            st.write("#### 🔵 外心 (Circumcenter O):")
            st.write(f"座標位置: `({circumcenter[0]:.2f}, {circumcenter[1]:.2f})`, 半徑 R = `{r_circum:.2f}`")
            st.write(format_eq(m_pBC, c_pBC, "BC 中垂線"))
            st.write("---")

        # 3. 內心 (Incenter)
        if "Incenter (內心內切圓)" in selected_centers:
            incenter = (a_len * A + b_len * B + c_len * C) / (a_len + b_len + c_len)
            s = (a_len + b_len + c_len) / 2
            area = np.sqrt(s * (s - a_len) * (s - b_len) * (s - c_len))
            r_in = area / s
            
            incircle = plt.Circle(incenter, r_in, color='green', fill=False, linestyle=':', alpha=0.6, linewidth=1.5)
            ax_plt.add_patch(incircle)
            ax_plt.scatter(incenter[0], incenter[1], color='green', s=120, zorder=6, label='Incenter (I)')
            
            st.write("#### 🟢 內心 (Incenter I):")
            st.write(f"座標位置: `({incenter[0]:.2f}, {incenter[1]:.2f})`, 內切圓半徑 r = `{r_in:.2f}`")
            st.write("---")

        # 4. 垂心 (Orthocenter)
        if "Orthocenter (垂心高線)" in selected_centers:
            m_BC, c_BC = get_line_equation(B, C)
            m_hA, c_hA = get_perpendicular_line(A, m_BC, c_BC, m_BC is None, B[0])
            
            m_AC, c_AC = get_line_equation(A, C)
            m_hB, c_hB = get_perpendicular_line(B, m_AC, c_AC, m_AC is None, A[0])
            
            m_AB, c_AB = get_line_equation(A, B)
            m_hC, c_hC = get_perpendicular_line(C, m_AB, c_AB, m_AB is None, A[0])
            
            orthocenter = find_intersection(m_hA, c_hA, m_hB, c_hB)
            
            ax_plt.plot([A[0], orthocenter[0]], [A[1], orthocenter[1]], 'purple', linestyle='--', alpha=0.6)
            ax_plt.plot([B[0], orthocenter[0]], [B[1], orthocenter[1]], 'purple', linestyle='--', alpha=0.6)
            ax_plt.plot([C[0], orthocenter[0]], [C[1], orthocenter[1]], 'purple', linestyle='--', alpha=0.6)
            ax_plt.scatter(orthocenter[0], orthocenter[1], color='purple', s=120, zorder=6, label='Orthocenter (H)')
            
            st.write("#### 🟣 垂心 (Orthocenter H):")
            st.write(f"座標位置: `({orthocenter[0]:.2f}, {orthocenter[1]:.2f})`")
            st.write(format_eq(m_hA, c_hA, "高線 (from A)"))
            st.write(format_eq(m_hB, c_hB, "高線 (from B)"))
            st.write(format_eq(m_hC, c_hC, "高線 (from C)"))
            st.write("---")

    with col1:
        ax_plt.set_aspect('equal', 'box')
        
        # 視窗範圍控制控制邏輯
        if not auto_scale:
            ax_plt.set_xlim(-15, 15)
            ax_plt.set_ylim(-15, 15)
            
        ax_plt.axhline(0, color='gray', linewidth=0.5)
        ax_plt.axvline(0, color='gray', linewidth=0.5)
        ax_plt.grid(True, linestyle=':', alpha=0.5)
        ax_plt.legend(loc='lower left')
        st.pyplot(fig)
