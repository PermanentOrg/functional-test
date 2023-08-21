import { webcrypto as crypto } from "crypto";

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
