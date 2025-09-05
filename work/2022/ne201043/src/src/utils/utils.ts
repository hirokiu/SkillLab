// ゼロ埋め
const fillZero = (input: string | number) => `00${input}`.slice(-2);

// 日付フォーマット
export const formatDate = (date: Date) =>
  `${date.getFullYear()}/${date.getMonth()}/${date.getDate()}`;

//　時間フォーマット
export const formatTime = (date: Date) =>
  `${fillZero(date.getHours())}:${fillZero(date.getMinutes())}:${fillZero(
    date.getSeconds(),
  )}`;
