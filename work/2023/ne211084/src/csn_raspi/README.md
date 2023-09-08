csn_raspi
=========
# for WitMotion
BWT901CL(WitMotion)センサーから加速度を取得し、STA/LTA法で地震を検知するプログラムです。

## output files
### data/csn.log
- 連続波形のデータを記録したファイル
  - 時刻（UNIXTIME+ミリ秒）, x, y, z
- syslogを使用してrotate
  - rotationは，1時間 or 25MBを超えたら
  - csn_log_%Y%m%d-%H%M-%s で保存
    - 年月日-時分-UNIXTIME
  - 終了時刻がファイル名

### earthquakes/XX-unixtime.milisec.csv
- 地震をトリガーした場合に作成されるファイル
- デバイスID_トリガー時刻.csv
- トリガーした時刻の前10秒 + 後ろ60秒分のデータ

## install
[Raspberry Pi設定手順](https://hackmd.io/@hrku/BJSOcmmq_)
