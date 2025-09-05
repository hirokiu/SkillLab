import functions_framework
from google.cloud import firestore
import requests

# --- 設定 ---
LINE_NOTIFY_TOKEN = 'MY_LINE_NOTIFY_TOKEN'
LINE_NOTIFY_API_URL = 'https://notify-api.line.me/api/notify'
COLLECTION_NAME = 'angle_data'

# --- 判定ロジックの閾値 ---
X_MIN, X_MAX = -40, -20
Y_MIN, Y_MAX = -60, -40
CONSECUTIVE_COUNT_THRESHOLD = 10

# Firestoreクライアントの初期化
db = firestore.Client()

def send_line_notification(message):
    """LINE Notifyへ通知を送信する関数"""
    try:
        headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
        data = {'message': message}
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"LINE通知エラー: {e}")
        return False

def is_concentration_lapsed(data):
    """集中力が途切れているかを判定する関数"""
    x = data.get('x_angle', 0)
    y = data.get('y_angle', 0)
    return Y_MIN <= y <= Y_MAX and X_MIN <= x <= X_MAX

@functions_framework.cloud_event
def concentration_check(cloud_event):
    """Firestoreへの書き込みをトリガーに実行されるメイン関数"""
    
    docs = db.collection(COLLECTION_NAME).order_by(
        'timestamp', direction=firestore.Query.DESCENDING
    ).limit(CONSECUTIVE_COUNT_THRESHOLD).stream()
    
    recent_data = [doc.to_dict() for doc in docs]
    
    if len(recent_data) < CONSECUTIVE_COUNT_THRESHOLD:
        print(f"データが{CONSECUTIVE_COUNT_THRESHOLD}件未満のため、連続判定をスキップします。")
        return

    consecutive_lapses = 0
    for data in recent_data:
        if is_concentration_lapsed(data):
            consecutive_lapses += 1
        else:
            # 連続が途切れた時点でループを抜ける
            break
            
    # 6. 通知
    if consecutive_lapses == CONSECUTIVE_COUNT_THRESHOLD:
        message = "【警告】集中力が途切れている可能性が非常に高いです。休憩を取りましょう。"
        print(f"通知実行: {message}")
        send_line_notification(message)
        
    elif is_concentration_lapsed(recent_data[0]) and not is_concentration_lapsed(recent_data[1]):
        message = "【注意】集中力が途切れている可能性があります。"
        print(f"通知実行: {message}")
        send_line_notification(message)
    
    else:
        print("通知条件を満たしませんでした。")
        
    return 'OK'