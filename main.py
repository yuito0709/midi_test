import requests
import rtmidi

# OpenWeatherMap API設定
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "7f359a81aab2435659c50f7985f5e074"  # 取得したAPIキー
CITY = "Tokyo,jp"

# MIDI設定
midiout = rtmidi.MidiOut()
ports = midiout.get_ports()

# MIDIポートの選択
if ports:
    midiout.open_port(1)  # 必要に応じてポート番号を変更
else:
    print("MIDIポートが見つかりません。")
    exit()

# 天気状態と対応する色
WEATHER_COLORS = {
    "Clear": 9,   # 晴れ → オレンジ
    "Clouds": 63, # 曇り → 灰色
    "Rain": 45    # 雨 → 水色
}

# Programmer mode に切り替え
def switch_to_programmer_mode():
    sys_ex_message = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D, 0x00, 0x05, 0xF7]
    try: 
        midiout.send_message(sys_ex_message)
        print("Programmer mode に切り替えました。")
    except Exception as e: 
        print(f"MIDIメッセージ送信エラー: {e}")

# 天気情報を取得
def get_weather():
    try:
        response = requests.get(f"{BASE_URL}?q={CITY}&appid={API_KEY}")
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["main"]
            print(f"現在の天気: {weather}")
            return weather
        else:
            print(f"エラー: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"リクエスト中にエラーが発生しました: {e}")
        return None

# ボタンに色を設定
def set_button_color(note, color):
    try:
        midiout.send_message([0x90, note, color])  # ノート番号と色を送信
        print(f"ノート番号 {note} に色 {color} を設定しました。")
    except Exception as e:
        print(f"MIDIメッセージ送信エラー: {e}")

# ボタンのテスト
def test_buttons():
    for note in range(36, 40):  # ノート番号 36～39 をテスト
        set_button_color(note, 63)  # 灰色で点灯
        import time
        time.sleep(1)  # 1秒間待機
        set_button_color(note, 0)   # 消灯

# メイン処理
def main():
    switch_to_programmer_mode()  # Programmer mode に切り替え
    test_buttons()  # ボタンをテスト
    weather = get_weather()
    if weather:
        color = WEATHER_COLORS.get(weather, 0)  # 天気に基づく色を設定
        set_button_color(36, color)  # ノート番号 36 に設定
    midiout.close_port()

if __name__ == "__main__":
    main()
