import rtmidi
import time

# MIDIポートを開く
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    port_number = 1  # 使用するポート番号を設定（0から始まる）
    if port_number < len(available_ports):
        midiout.open_port(port_number)
    else:
        print(f"指定したポート番号 {port_number} は利用できません。利用可能なポート: {available_ports}")
        exit(1)
else:
    print("利用可能なMIDIポートが見つかりません。")
    exit(1)

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
    colourspec = [0x00, color]  # カラーパレットを使用
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

# 文字列をスクロール表示
scroll_text("Hello World!", color=5, speed=10, loop=1)

# スクロールを60秒間表示
time.sleep(60)

# スクロールを停止
print("スクロール停止中...")
stop_sysex_message = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D, 0x07, 0xF7]  # 停止コマンド
midiout.send_message(stop_sysex_message)

# ポートを閉じる
midiout.close_port()
