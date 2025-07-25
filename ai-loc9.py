from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from plyer import gps
from geopy.distance import geodesic
import random

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
    

    # ... (나머지 홀 좌표 유지)
}

class GolfDistanceApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # 홀 선택 스피너
        self.hole_spinner = Spinner(
            text='1',
            values=[str(i) for i in range(1, 19)]
        )
        
        # 거리 계산 버튼
        self.calc_button = Button(
            text='위치 측정 및 거리 계산',
            on_press=self.calculate_distance
        )
        
        # 결과 표시 레이블
        self.result_label = Label(text='결과가 여기에 표시됩니다.')
        
        self.layout.add_widget(self.hole_spinner)
        self.layout.add_widget(self.calc_button)
        self.layout.add_widget(self.result_label)
        
        return self.layout

    def calculate_distance(self, instance):
        hole_number = int(self.hole_spinner.text)
        
        # Android 권한 요청 (Kivy 방식)
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.ACCESS_FINE_LOCATION])
        
        # GPS 초기화
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
            self.result_label.text = "GPS 측정 중..."
        except Exception as e:
            self.result_label.text = f"GPS 오류: {str(e)}"
            self.use_dummy_gps(hole_number)

    def on_location(self, **kwargs):
        # 실제 GPS 위치 획득
        lat = kwargs['lat']
        lon = kwargs['lon']
        self.process_location(lat, lon)

    def use_dummy_gps(self, hole_number):
        # 테스트용 더미 좌표 생성
        lat = -27.536 + random.uniform(-0.001, 0.001)
        lon = 152.945 + random.uniform(-0.001, 0.001)
        self.process_location(lat, lon, is_dummy=True)

    def process_location(self, lat, lon, is_dummy=False):
        hole_number = int(self.hole_spinner.text)
        target_pos = HOLE_COORDS.get(hole_number)
        
        if not target_pos:
            self.result_label.text = "유효하지 않은 홀 번호"
            return
        
        distance = geodesic((lat, lon), target_pos).meters
        result_text = f"[홀 {hole_number}까지 거리]\n{distance:.2f} 미터"
        
        if is_dummy:
            result_text += "\n(테스트용 더미 좌표 사용 중)"
            
        self.result_label.text = result_text

if __name__ == '__main__':
    GolfDistanceApp().run()