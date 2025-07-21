#
#  Claud coding
#


import streamlit as st
import random
import time
import geocoder
from geopy.distance import geodesic

# Jindalee Golf Course 홀컵 좌표
HOLE_COORDS = {
    1: (-27.53918, 152.945457),
    2: (-27.53658, 152.94362),
    3: (-27.536325, 152.946275),
    4: (-27.535989, 152.943866),
    5: (-27.534852, 152.944261),
    6: (-27.532689, 152.945452),
    7: (-27.534462, 152.944352),
    8: (-27.532874, 152.943498),
    9: (-27.535837, 152.943191),
    10: (-27.53918, 152.945457),
    11: (-27.53658, 152.94362),
    12: (-27.536325, 152.946275),
    13: (-27.535989, 152.943866),
    14: (-27.534852, 152.944261),
    15: (-27.532689, 152.945452),
    16: (-27.534462, 152.944352),
    17: (-27.532874, 152.943498),
    18: (-27.535837, 152.943191)
    
}

class DummyGPS:
    def get_location(self):
        # 테스트용 가상 GPS 좌표 생성
        lat = 37.5665 + random.uniform(-0.001, 0.001)
        lon = 126.9780 + random.uniform(-0.001, 0.001)
        return lat, lon

def main():
    st.markdown("#### Jindalee Golf Course :red[홀 거리] by Kevin")
    st.markdown("현 위치에서 홀컵까지 거리 계산")
    
    # 홀 선택
    hole_number = st.selectbox(
        "홀 번호 선택 (1-18):",
        options=list(range(1, 19)),
        index=0
    )

    gps = DummyGPS()
    
    if st.button("위치 측정 및 거리 계산", type="secondary"):
        # 현재 위치 가져오기 (더미 GPS 사용)
        current_lat, current_lon = gps.get_location()
        st.write(f"현재 위치 - 위도: {current_lat:.6f}, 경도: {current_lon:.6f}")
        
        # 거리 계산
        if hole_number in HOLE_COORDS:
            current_pos = (current_lat, current_lon)
            target_pos = HOLE_COORDS[hole_number]
            distance_m = geodesic(current_pos, target_pos).meters
            
            st.success(
                f"**홀 {hole_number}까지 거리:**\n\n"
                f"- {distance_m:.2f} 미터"
            )
            
            # 진행률 표시
            st.progress(min(1.0, distance_m / 300))
        else:
            st.error("유효하지 않은 홀 번호입니다.")

if __name__ == '__main__':
    main()