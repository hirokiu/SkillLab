//.txtデータの読み込み
String[] lines;

//更新回数
int count = 0;

//眠気限界値
int sleepyMax = 5;     //分

//前回寝た時
int slept = -1;

String past, now;

//イッヌの常動
float act = 0.0;
int actCount = 0;

void setup() {
  size(480, 480);
  textFont(createFont("SansSerif", 10, true));
}

void draw() {
  //更新情報
  lines = loadStrings("cpu_turned.txt");
  count = lines.length;   //.txtの行数

  //前回更新した時刻
  past = lines[count - 2].substring(30, 40);
  //今回更新した時刻
  now = lines[count - 1].substring(30, 40);
  //sleptの初期化
  if (slept == -1) {
    slept = lines.length;
  }

  //眠気メーター
  if (past.equals(now)) {
  } else {
    slept = count;
  }

  background(255);

  //println(count);
  if (count < 2) {
    text("2分程待ってね", 200, 200);
  } else {

    fill(0);
    textSize(10);
    text("前回データ： " + lines[count - 2].substring(0, 40), 20, 20);   //1行目 = 0indexを配慮
    text("前回データ： " + lines[count - 1].substring(0, 40), 20, 40);   //1行目 = 0indexを配慮

    text("前回寝た時間： " + lines[slept - 1].substring(0, 19), 20, 60);

    text("システム起動時間の合計： " + count + "分", 20, 80);
    text("眠気メーター： " + (count - slept) +"分（作業時間） / "+ sleepyMax + "分（限界値）", 20, 100);

    //眠気メーターを割り出す時間
    //println(40 - (count - slept) * 10);

    //眠気メーター
    if ((count - slept) == 0) {
      //元気
      println("元気");
    } else if ((count - slept) == 1) {
      //やや元気
      println("やや元気");
    } else if ((count - slept) == 2) {
      //あまり元気じゃない
      println("あまり元気じゃない");
    } else if ((count - slept) == 3) {
      //元気じゃない
      println("元気じゃない");
    } else if ((count - slept) == 4) {
      //くそ眠い
      println("くそ眠い");
    }
    
    //イッヌのY軸の常動 && イッヌの描画
    if ((count - slept) == 0 || (count - slept) == 1) {     //イッヌ元気 || イッヌやや元気

      actCount++;
      if (actCount >= 0 && actCount<60) {
        act -= 0.15;
      } else if (actCount >= 60 && actCount < 120) {
        act += 0.15;
      } else if (actCount >= 120) {
        actCount = 0;
        act = 0.0;
      }

      //イッヌの描画出力
      innuAct(act, (count - slept));
      
    } else if ((count - slept) == 2 || (count - slept) == 3) {     //イッヌあまり元気じゃない || イッヌ元気じゃない

      actCount++;
      if (actCount >= 0 && actCount<60) {
        act -= 0.05;
      } else if (actCount >= 60 && actCount < 120) {
        act += 0.05;
      } else if (actCount >= 120) {
        actCount = 0;
        act = 0.0;
      }

      //イッヌの描画出力
      innuAct2(act, (count - slept));
      //Zの描画
      fill(0);     //Color Brack
      textSize(30 + act * 2);
      text("Z", 360 + act, 300 + (count - slept) * 2);
      
    } else {

      actCount++;
      if (actCount >= 0 && actCount<60) {
        act -= 0.05;
      } else if (actCount >= 60 && actCount < 120) {
        act += 0.05;
      } else if (actCount >= 120) {
        actCount = 0;
        act = 0.0;
      }

      innuAct3(act, (count - slept));
      
    }
    println(act +","+ actCount +","+ (count - slept));
    
  }
}

void innuAct(float _act, int _sleepy) {     //元気ver.
  fill(255);     //Color White

  rect(80, 255 + _act, 50, 15);     //Tail

  rect(255, 295, 20, 80);     //Left front reg
  rect(155, 295, 20, 80);     //Left back reg

  rect(225, 300, 20, 80);     //Right front reg
  rect(125, 300, 20, 80);     //Right back reg

  rect(120, 260, 160, 60);     //Body

  rect(220, 180 + _act, 100, 105);     //Face contour

  rect(210, 165 + _act, 40, 55);     //Right ear
  rect(300, 165 + _act, 40, 55);     //Left ear
  rect(290, 260 + _act, 55, 25);     //Nose 1

  fill(0);     //Color Black

  rect(245, 225 + _act + _sleepy * 2, 20, 15 - _sleepy * 2);     //Right eye
  rect(285, 225 + _act + _sleepy * 2, 20, 15 - _sleepy * 2);     //Left eye

  rect(310, 260 + _act, 25, 5);     //Nose 2

  fill(255);     //Color White
  rect(247, 227 + _act + _sleepy * 2, 5, 5);     //Right eye 2
  rect(287, 227 + _act + _sleepy * 2, 5, 5);     //Left eye 2
}

void innuAct2(float _act, int _sleepy) {     //眠いver.
  fill(255);     //Color White

  rect(70, 350 + _act, 50, 15);     //Tail

  rect(260, 350, 80, 20);     //Left front reg
  rect(160, 350, 80, 20);     //Left back reg

  rect(120, 310, 160, 60);     //Body

  rect(230, 355, 80, 20);     //Right front reg
  rect(130, 355, 80, 20);     //Right back reg

  rect(220, 240 + _act, 100, 105);     //Face contour

  rect(210, 225 + _act, 40, 55);     //Right ear
  rect(300, 225 + _act, 40, 55);     //Left ear
  rect(290, 320 + _act, 55, 25);     //Nose 1

  fill(0);     //Color Black

  rect(245, 285 + _act + _sleepy * 2, 20, 15 - _sleepy * 2);     //Right eye
  rect(285, 285 + _act + _sleepy * 2, 20, 15 - _sleepy * 2);     //Left eye

  rect(310, 320 + _act, 25, 5);     //Nose 2

  fill(255);     //Color White
  rect(247, 287 + _act + _sleepy * 2, 5, 5);     //Right eye 2
  rect(287, 287 + _act + _sleepy * 2, 5, 5);     //Left eye 2
}

void innuAct3(float _act, int _sleepy) {     //くそ眠いver.
  fill(255);     //Color White

  rect(70, 350, 50, 15);     //Tail

  rect(260, 350, 80, 20);     //Left front reg
  rect(160, 350, 80, 20);     //Left back reg

  rect(120, 310, 160, 60);     //Body

  rect(230, 355, 80, 20);     //Right front reg
  rect(130, 355, 80, 20);     //Right back reg

  rect(220, 240, 100, 105);     //Face contour

  rect(210, 225, 40, 55);     //Right ear
  rect(300, 225, 40, 55);     //Left ear
  rect(290, 320, 55, 25);     //Nose 1

  fill(255);     //Color Black

  rect(245, 285, 20, 15 - _sleepy * 3);     //Right eye
  rect(285, 285, 20, 15 - _sleepy * 3);     //Left eye

  ellipse(275, 195 - _act, 120, 20);     //Angel Ring

  fill(0);     //Color Black
  rect(310, 320, 25, 5);     //Nose 2
}
