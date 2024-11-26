import rtmidi
import sys

# SysExメッセージの定義
# F0 00 20 29 02 0D 03 <colourspec> F7
# <colourspec> for RGB: 3, LED index, Red, Green, Blue
def create_sysex_message(lighting_type, led_index, *color_data):
    message = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D, 0x03, lighting_type, led_index]
    message.extend(color_data)
    message.append(0xF7)
    return message

# MIDIポートの初期化
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    # 使用するポート番号を設定（0から始まる）
    port_number = 0  # 必要に応じて変更してください
    if port_number < len(available_ports):
        midiout.open_port(port_number)
        print(f"MIDIポート '{available_ports[port_number]}' を開きました。")
    else:
        print(f"指定したポート番号 {port_number} は利用できません。利用可能なポート: {available_ports}")
        sys.exit(1)
else:
    print("利用可能なMIDIポートが見つかりません。Launchpad Mini [MK3] が接続されていることを確認してください。")
    sys.exit(1)

# LEDに色を設定する関数
def set_led_red(led_index):
    lighting_type = 3  # RGBカラー
    red = 127          # 最大値
    green = 0
    blue = 0
    sysex_message = create_sysex_message(lighting_type, led_index, red, green, blue)
    try:
        midiout.send_message(sysex_message)
        print(f"LED {led_index} を赤色に設定しました。")
    except Exception as e:
        print(f"MIDIメッセージ送信エラー: {e}")

# LEDの色を消灯する関数
def clear_led(led_index):
    lighting_type = 3  # RGBカラー
    red = 0
    green = 0
    blue = 0
    sysex_message = create_sysex_message(lighting_type, led_index, red, green, blue)
    try:
        midiout.send_message(sysex_message)
        print(f"LED {led_index} の色を消灯しました。")
    except Exception as e:
        print(f"MIDIメッセージ送信エラー: {e}")

# テスト実行
try:
    button_number = 12
      # テストするボタン番号
    set_led_red(button_number)  # ボタンに赤色を設定

    input("ボタンが赤色に点灯していることを確認してください。終了するにはEnterキーを押してください...")

    clear_led(button_number)  # ボタンの色を消灯

finally:
    midiout.close_port()
    print("MIDIポートを閉じました。")
