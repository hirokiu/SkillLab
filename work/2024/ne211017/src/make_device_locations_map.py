import requests

# チャネルごとのリード API キーとチャネル ID
channel_info = [
    {'id': 'YOUR_CHANNEL_ID_1', 'api_key': 'YOUR_READ_API_KEY_1'},
    {'id': 'YOUR_CHANNEL_ID_2', 'api_key': 'YOUR_READ_API_KEY_2'},
    {'id': 'YOUR_CHANNEL_ID_3', 'api_key': 'YOUR_READ_API_KEY_3'},
    {'id': 'YOUR_CHANNEL_ID_4', 'api_key': 'YOUR_READ_API_KEY_4'}
]

# 最新の位置情報を取得する関数
def get_latest_data(channel_id, api_key):
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}&results=1'
    response = requests.get(url)
    data = response.json()
    if 'feeds' in data and len(data['feeds']) > 0:
        latest_feed = data['feeds'][0]
        return {
            'lat': float(latest_feed.get('field1', 0)),
            'lon': float(latest_feed.get('field2', 0)),
            'alt': float(latest_feed.get('field3', 0))
        }
    return None

# 各デバイスのデータを取得
device_data = [get_latest_data(info['id'], info['api_key']) for info in channel_info]

# HTML コンテンツの生成
html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Device Locations</title>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBvkPF6EEmP43PjI5pyTaL2y2wQ-kC6Ccg"></script>
    <script>
        function initMap() {{
            var map = new google.maps.Map(document.getElementById('map'), {{
                zoom: 15,
                center: {{lat: 35.608668, lng: 139.555230}} // 初期位置を設定
            }});

            var locations = [
'''

# 各デバイスの位置情報を HTML に追加
for data in device_data:
    if data:
        html_content += f'{{lat: {data["lat"]}, lng: {data["lon"]}, alt: {data["alt"]}}},\n'

html_content += '''
            ];

            // マーカーを追加
            for (var i = 0; i < locations.length; i++) {{
                var marker = new google.maps.Marker({{
                    position: locations[i],
                    map: map,
                    title: 'Device ' + (i + 1)
                }});
            }}

            // ラインを引く
            var pathCoordinates = locations.map(function(location) {{
                return new google.maps.LatLng(location.lat, location.lng);
            }});
            var path = new google.maps.Polyline({{
                path: pathCoordinates,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
            }});
            path.setMap(map);
        }}
    </script>
</head>
<body onload="initMap()">
    <div id="map" style="height: 100%; width: 100%;"></div>
</body>
</html>
'''

# HTML ファイルに保存
with open('device_locations_map.html', 'w') as file:
    file.write(html_content)

print("HTML ファイルが生成されました: device_locations_map.html")

