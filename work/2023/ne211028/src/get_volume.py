from pydub import AudioSegment
import math
import time

def write_message(sound):
    if sound >= 60:
        print("基準値以上の音声を感知しました")

def get_audio_volume_transitions(m4a_file, interval=1):
    try:
        # M4Aファイルを読み込みます
        audio = AudioSegment.from_file(m4a_file, format="m4a")

        # サンプリング間隔（秒）を指定します
        sample_interval = interval * 1000  # ミリ秒単位に変換

        for t in range(0, len(audio), sample_interval):
            # 指定した時間刻みでの音声データを切り出します
            segment = audio[t:t + sample_interval]

            # 音量を取得します
            rms = segment.rms
            # 音量をデシベル単位に変換します
            volume_db = 20 * math.log10(rms)

            # 音量と時間（秒）を出力します
            print(f"時間: {t / 1000:.2f}秒, 音量（デシベル単位）: {volume_db:.2f} dB")
            #音量が基準を超えているか判定
            write_message(volume_db)

            # 次のサンプリングまで待機します
            time.sleep(interval)
    
    except KeyboardInterrupt:
        # Ctrl+Cが押された場合、プログラムを終了します
        pass

if __name__ == "__main__":
    m4a_file = "sensorlog_20230908.m4a"  # 分析したいM4Aファイルへのパスを指定してください
    interval = 1  # サンプリング間隔（秒）を設定します
    get_audio_volume_transitions(m4a_file, interval)
