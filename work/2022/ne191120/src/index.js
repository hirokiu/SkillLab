window.onload = Main;

let measure = false;
let sAlpha;
let sBeta;
let sGamma;
let fAlpha;
let fBeta;
let fGamma;

function Main() {
    let start = document.getElementById("button1");
    let stop = document.getElementById("button2");
    start.addEventListener("click", startPressed);
    stop.addEventListener("click", stopPressed);
}

function startPressed() {
    if (measure == true) {
        alert("計測を終了してください");
    } else {
        measure = true;
        sAlpha = document.getElementById("alpha").textContent;
        sBeta = document.getElementById("beta").textContent;
        sGamma = document.getElementById("gamma").textContent;
        console.log(sAlpha, sBeta, sGamma);
        alert("start!");
    }
}

function stopPressed() {
    if (measure == false) {
        alert("計測が開始されていません");
    } else {
        fAlpha = document.getElementById("alpha").textContent;
        fBeta = document.getElementById("beta").textContent;
        fGamma = document.getElementById("gamma").textContent;
        console.log(fAlpha, fBeta, fGamma);
        alert("stop!!");
        calc(sAlpha, sBeta, sGamma, fAlpha, fBeta, fGamma);
        measure = false;
    }
}

function calc(sAlpha, sBeta, sGamma, fAlpha, fBeta, fGamma) {
    let cAlpha;
    let cBeta;
    let cGamma;
    //alpha
    if (sAlpha => fAlpha) {
        cAlpha = sAlpha - fAlpha;
    } else {
        cAlpha = fAlpha - sAlpha;
    }
    //beta
    if (sBeta => fBeta) {
        cBeta = sBeta - fBeta;
    } else {
        cBeta = fBeta - sBeta;
    }
    //gamma
    if (sGamma => fGamma) {
        cGamma = sGamma - fGamma;
    } else {
        cBGamma = fGamma - sGamma;
    }
    result = document.createElement("p");
    resultArea.appendChild(result);
    result.textContent = "alpha:" + cAlpha + ", beta:" + cBeta + ", gammma:" + cGamma;
    result.classList.add("result");
}
// OS識別用
let os;

// DOM構築完了イベントハンドラ登録
window.addEventListener("DOMContentLoaded", init);

// 初期化
function init() {
    // 簡易的なOS判定
    os = detectOSSimply();
    if (os == "iphone") {
        // safari用。DeviceOrientation APIの使用をユーザに許可して貰う
        document.querySelector("#permit").addEventListener("click", permitDeviceOrientationForSafari);

        window.addEventListener(
            "deviceorientation",
            orientation,
            true
        );
    } else if (os == "android") {
        window.addEventListener(
            "deviceorientationabsolute",
            orientation,
            true
        );
    } else {
        window.alert("スマホでアクセスしてください");
    }
}


// ジャイロスコープと地磁気をセンサーから取得
function orientation(event) {
    let alpha = event.alpha;
    let beta = event.beta;
    let gamma = event.gamma;

    let degrees;
    if (os == "iphone") {
        // webkitCompasssHeading値を採用
        degrees = event.webkitCompassHeading;

    } else {
        // deviceorientationabsoluteイベントのalphaを補正
        degrees = compassHeading(alpha, beta, gamma);
    }
    document.querySelector("#alpha").innerHTML = alpha;
    document.querySelector("#beta").innerHTML = beta;
    document.querySelector("#gamma").innerHTML = gamma;
}

// 端末の傾き補正（Android用）
// https://www.w3.org/TR/orientation-event/
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

    return compassHeading * (180 / Math.PI); // Compass Heading (in degrees)
}

// 簡易OS判定
function detectOSSimply() {
    let ret;
    if (
        navigator.userAgent.indexOf("iPhone") > 0 ||
        navigator.userAgent.indexOf("iPad") > 0 ||
        navigator.userAgent.indexOf("iPod") > 0
    ) {
        // iPad OS13のsafariはデフォルト「Macintosh」なので別途要対応
        ret = "iphone";
    } else if (navigator.userAgent.indexOf("Android") > 0) {
        ret = "android";
    } else {
        ret = "pc";
    }

    return ret;
}

// iPhone + Safariの場合はDeviceOrientation APIの使用許可をユーザに求める
function permitDeviceOrientationForSafari() {
    DeviceOrientationEvent.requestPermission()
        .then(response => {
            if (response === "granted") {
                window.addEventListener(
                    "deviceorientation",
                    detectDirection
                );
            }
        })
        .catch(console.error);
}