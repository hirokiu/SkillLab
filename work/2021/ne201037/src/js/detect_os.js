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

// iPhone + Safariの場合はDeviceMotion APIの使用許可をユーザに求める
function permitDeviceMotionForSafari() {
    DeviceMotionEvent.requestPermission()
        .then(response => {
            if (response === "granted") {
                window.addEventListener(
                    "devicemotion",
                    motionHandler
                );
            }
        }).catch(console.error);
}
// iPhone + Safariの場合はDeviceOrientation APIの使用許可をユーザに求める
function permitDeviceOrientationForSafari() {
    DeviceOrientationEvent.requestPermission()
        .then(response => {
            if (response === "granted") {
                window.addEventListener(
                    "deviceorientation",
                    orientationHandler
                );
            }
        }).catch(console.error);
}

