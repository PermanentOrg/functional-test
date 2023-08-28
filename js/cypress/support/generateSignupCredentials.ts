export function generatePassword(length: number): string {
  const lowestPrintableCode = 33;
  const highestPrintableCode = 126 - lowestPrintableCode;
  const array = new Uint32Array(length);
  crypto.getRandomValues(array);
  return Array.from(array)
    .map<string>((n) =>
      String.fromCharCode(lowestPrintableCode + (n % highestPrintableCode)),
    )
    .join("");
}

export function generateNewEmail(baseEmail: string): string {
  const unixTime = Math.floor(new Date().getTime() / 1000);
  return baseEmail.replace("@", `+prmnttstr${unixTime}@`);
}
