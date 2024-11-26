import rtmidi
import time
import requests
import sys

# OpenWeatherMap API設定
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "7f359a81aab2435659c50f7985f5e074"  # 取得したAPIキーをここに入力
CITY = "Tokyo,jp"

# MIDI設定
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    port_number = 1  # 使用するポート番号を設定（0から始まる）
    if port_number < len(available_ports):
        midiout.open_port(port_number)
        print(f"MIDIポート {available_ports[port_number]} を開きました。")
    else:
        print(f"指定したポート番号 {port_number} は利用できません。利用可能なポート: {available_ports}")
        sys.exit(1)
else:
    print("利用可能なMIDIポートが見つかりません。")
    sys.exit(1)

# 天気状態と対応する色
WEATHER_COLORS = {
    "Clear": 9,    # 晴れ → オレンジ
    "Clouds": 63,  # 曇り → 灰色
    "Rain": 45,    # 雨 → 水色
    "Snow": 15,    # 雪 → 白色
    "Thunderstorm": 12,  # 雷雨 → 紫色
    "Drizzle": 30,  # 霧雨 → 青色
    "Mist": 24,     # 霧 → 薄青色
    # その他の天気条件も必要に応じて追加
}

# 文字列を16進数に変換（ASCIIコード）
def text_to_hex(text):
    return [ord(char) for char in text]

# 文字列をスクロール表示する関数
def scroll_text(text, color=5, speed=10, loop=0):
    """
    Launchpad Mini [MK3]に文字を流す
    :param text: 流す文字列（英数字のみ対応）
    :param color: カラーパレット番号またはRGB指定 (例: 5 = 赤)
    :param speed: スクロール速度 (例: 10)
    :param loop: ループ設定 (0 = ループなし, 1 = ループあり)
    """
    # 色指定（パレットカラー）
    colourspec = [0x00, color]  # パレットカラーを使用
    # colourspec = [0x01, 127, 0, 0]  # RGBカラーの場合（例: 赤）

    # テキストを16進数に変換
    text_hex = text_to_hex(text)

    # SysExメッセージを作成
    sysex_message = (
        [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D, 0x07] +
        [loop, speed] + colourspec + text_hex +
        [0xF7]
    )

    # メッセージを送信
    print(f"送信中: {sysex_message}")
    midiout.send_message(sysex_message)

# 天気情報を取得
def get_weather():
    try:
        response = requests.get(f"{BASE_URL}?q={CITY}&appid={API_KEY}&lang=ja")
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["main"]
            description = data["weather"][0]["description"]
            print(f"現在の天気: {weather} ({description})")
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
        midiout.send_message([0x90, note, color])  # ノートオンメッセージ
        print(f"ノート番号 {note} に色 {color} を設定しました。")
    except Exception as e:
        print(f"MIDIメッセージ送信エラー: {e}")

# ボタンのテスト
def test_buttons():
    for note in range(36, 40):  # ノート番号 36～39 をテスト
        set_button_color(note, 63)  # 灰色で点灯
        time.sleep(0.5)  # 0.5秒間待機
        set_button_color(note, 0)   # 消灯

# Programmer mode に切り替え
def switch_to_programmer_mode():
    sysex_message = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D, 0x00, 0x05, 0xF7]
    try: 
        midiout.send_message(sysex_message)
        print("Programmer mode に切り替えました。")
    except Exception as e: 
        print(f"MIDIメッセージ送信エラー: {e}")

# メイン処理
def main():
    switch_to_programmer_mode()  # Programmer mode に切り替え
    test_buttons()  # ボタンをテスト

    weather = get_weather()
    if weather:
        # 天気に基づく色を設定
        color = WEATHER_COLORS.get(weather, 0)  # デフォルトはオフ
        # 天気の文字列をスクロール表示
        scroll_text(weather, color=color, speed=10, loop=1)
        # 必要に応じて他のボタンにも色を設定
        # 例: ノート番号 36 に色を設定
        set_button_color(36, color)
    else:
        # 天気情報が取得できなかった場合、エラーメッセージを表示
        scroll_text("Error", color=12, speed=10, loop=0)

    # スクロールを60秒間表示
    time.sleep(60)

    # スクロールを停止
    print("スクロール停止中...")
    stop_sysex_message = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D, 0x07, 0xF7]  # 停止コマンド
    midiout.send_message(stop_sysex_message)

    # 全てのボタンを消灯
    for note in range(36, 40):
        set_button_color(note, 0)

    # ポートを閉じる
    midiout.close_port()
    print("MIDIポートを閉じました。")

if __name__ == "__main__":
    main()
