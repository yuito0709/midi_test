import rtmidi
import time

# Launchpad MiniのMIDIポート名を設定
OUTPUT_PORT_NAME = 'Launchpad Mini MK3 LPMiniMK3 MIDI In'

# Launchpadの8x8ドットマトリックスに表示するパターン
# 0: 消灯, 1: 赤, 2: 緑, 3: 青
pattern = [
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
]

# カラーパレットの定義 (MIDIのVelocity値)
COLOR_PALETTE = {
    0: 0,    # 消灯
    1: 5,    # 赤
    2: 21,   # 緑
    3: 45,   # 青
}

def set_pad_color(output, x, y, color):
    """
    特定のパッドの色を設定
    :param output: MIDI出力ポート
    :param x: X座標 (0-7)
    :param y: Y座標 (0-7)
    :param color: 色 (0: 消灯, 1: 赤, 2: 緑, 3: 青)
    """
    note = x + y * 10  # Launchpadのパッドノート番号計算
    velocity = COLOR_PALETTE.get(color, 0)  # デフォルトで消灯
    msg = [0x90, note, velocity]  # Note Onメッセージ
    output.send_message(msg)

def display_pattern(output, pattern):
    """
    8x8パターンをLaunchpadに表示
    :param output: MIDI出力ポート
    :param pattern: 表示するパターン (8x8リスト)
    """
    for y, row in enumerate(pattern):
        for x, color in enumerate(row):
            set_pad_color(output, x, y, color)

def switch_to_programmer_mode(output):
    """
    Launchpad MiniをProgrammer Modeに切り替えるSysExメッセージを送信
    """
    # Programmer Modeに切り替えるSysExメッセージ
    sys_ex_message = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D, 0x0E, 0xF7]
    output.send_message(sys_ex_message)
    print("Switched to Programmer Mode")

def main():
    # MIDI出力ポートを開く
    midi_out = rtmidi.MidiOut()
    available_ports = midi_out.get_ports()
    
    # 適切なポート名を選択
    if len(available_ports) > 0:
        output_port = available_ports[0]  # 最初のポートを選択
        midi_out.open_port(0)  # ポートを開く
    else:
        print("No available MIDI output ports.")
        sys.exit()

    # Programmer Modeに切り替え
    switch_to_programmer_mode(midi_out)

    # ドット絵パターンを表示
    display_pattern(midi_out, pattern)
    print("Pattern displayed. Press Ctrl+C to exit.")

    time.sleep(10)  # 10秒間表示して終了

    # MIDIポートを閉じる
    midi_out.close_port()

if __name__ == '__main__':
    main()
