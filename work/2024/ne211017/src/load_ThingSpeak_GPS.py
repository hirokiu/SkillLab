import requests
import json

# ThingSpeakのチャネルIDとAPIキー
channel_id = 2647524
read_api_key = 'OQ3VNW85200SUQOI'

# ThingSpeakからデータを取得
url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}'
response = requests.get(url)
data = json.loads(response.text)

# データ処理
feeds = data['feeds']
if feeds:
    lat = [float(feed['field1']) for feed in feeds if feed['field1']]
    lon = [float(feed['field2']) for feed in feeds if feed['field2']]
    alt = [float(feed['field3']) for feed in feeds if feed['field3']]

    # Googleマップ用HTMLの生成
    markers = ', '.join([f'{{lat: {lat[i]}, lng: {lon[i]}}}' for i in range(len(lat))])

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Maps with Path</title>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBvkPF6EEmP43PjI5pyTaL2y2wQ-kC6Ccg"></script>
        <script>
            function initMap() {{
                var map = new google.maps.Map(document.getElementById('map'), {{
                    zoom: 15,
                    center: {{lat: {lat[-1]}, lng: {lon[-1]}}}  <!-- 最新の位置でマップの中心を設定 -->
                }});

                var pathCoordinates = [
                    {markers}
                ];

                var path = new google.maps.Polyline({{
                    path: pathCoordinates,
                    geodesic: true,
                    strokeColor: '#FF0000',
                    strokeOpacity: 1.0,
                    strokeWeight: 2
                }});

                path.setMap(map);

                var marker = new google.maps.Marker({{
                    position: pathCoordinates[pathCoordinates.length - 1],
                    map: map,
                    title: 'Latest Position'
                }});

                var infoWindow = new google.maps.InfoWindow({{
                    content: 'Altitude: {alt[-1]} meters'
                }});

                marker.addListener('click', function() {{
                    infoWindow.open(map, marker);
                }});
            }}
        </script>
    </head>
    <body onload="initMap()">
        <div id="map" style="height: 500px; width: 100%;"></div>
    </body>
    </html>
    '''

    # HTMLファイルに書き込み
    with open('map.html', 'w') as f:
        f.write(html_content)
else:
    print("No data found.")

