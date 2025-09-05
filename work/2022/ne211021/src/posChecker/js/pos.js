//OS変数
let os;
//サーバリクエスト
const xhr = new XMLHttpRequest();
const api_key = 'NF95Y2TXZGKSCG11';
window.addEventListener("DOMContentLoaded", format);

// 初期化
function format() {
    os = detectOSSimply();

    if (os == "iphone") {
        // Safari対応
        document.querySelector("#permit").addEventListener("click", permitDeviceMotionForSafari);
        document.querySelector("#permit").addEventListener("click", permitDeviceOrientationForSafari);

        window.addEventListener(
            "deviceorientation", gyroHandler, true
        );

    } else if (os == "android") {
        window.addEventListener(
            "deviceorientationabsolute", gyroHandler, true
        );

    } else {
        window.alert("スマートフォンからアクセスしてください");
    }
}

// ジャイロスコープと地磁気をセンサーから取得
function gyroHandler(event) {
    let beta = event.beta;
    let gamma = event.gamma;

    if (os == "iphone") {
        // webkitCompasssHeading値を採用
        degrees = event.webkitCompassHeading;

    } else {
        // deviceorientationabsoluteイベントのalphaを補正
        degrees = compassHeading(alpha, beta, gamma);
    }
    document.querySelector("#TB").innerHTML = beta;
    document.querySelector("#LR").innerHTML = gamma;

    //アラート表示
    if (beta > Math.abs(175) && gamma < Math.abs(20)) window.alert("顔に落としちゃうぞ！");
    else if (beta < Math.abs(20) && gamma > Math.abs(89.5)) window.alert("横になりながら使ってるね？");
    else if (beta < Math.abs(20) && gamma < Math.abs(20)) window.alert("首痛うなるよー");

    //文字の読みやすさ変更
    var obj = document.getElementById('text');
    obj.style.fontSize = (beta - 20) + 'px';
    if((40 < beta && beta < 60) && gamma < Math.abs(20)){
        obj.style.background = '#CCCF9A';
    }else{
        obj.style.background = 'white';
    }
}

//android補正
function compassHeading(alpha, beta, gamma) {
    var degtorad = Math.PI / 180; // Degree-to-Radian conversion

    var _x = beta ? beta * degtorad : 0; // beta value
    var _y = gamma ? gamma * degtorad : 0; // gamma value
    var _z = alpha ? alpha * degtorad : 0; // alpha value

    var cX = Math.cos(_x);
    var cY = Math.cos(_y);
    var cZ = Math.cos(_z);
    var sX = Math.sin(_x);
    var sY = Math.sin(_y);
    var sZ = Math.sin(_z);

    // Calculate Vx and Vy components
    var Vx = -cZ * sY - sZ * sX * cY;
    var Vy = -sZ * sY + cZ * sX * cY;

    // Calculate compass heading
    var compassHeading = Math.atan(Vx / Vy);

    // Convert compass heading to use whole unit circle
    if (Vy < 0) {
        compassHeading += Math.PI;
    } else if (Vx < 0) {
        compassHeading += 2 * Math.PI;
    }
}