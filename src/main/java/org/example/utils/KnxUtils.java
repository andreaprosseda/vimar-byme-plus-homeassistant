package org.example.utils;

import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class KnxUtils {

    // business logic taken from https://knxer.net/?p=49

    /*
        HEX TO GROUP ADDRESS CONVERSION
        a. 0x1073
        b. remove 0x -> 1073
        c. convert each digit in binary         ->      0001 0000 0111 0010
        d. take main(H) middle(M) and sub(U)    ->      HHHH HMMM UUUU UUUU
            H = 00010
            M = 000
            Y = 01110011
        d. convert H, M, Y in decimal
            H = 2
            M = 0
            Y = 115
        e. merge 2/0/115
     */
    public static String getKnxGroupAddress(String hex) {
        String hexValue = getHexValue(hex);
        if (hexValue == null) return null;
        String result = convertDigitsInBinary(hexValue);

        String h = result.substring(0, 5);
        String m = result.substring(5, 8);
        String u = result.substring(8);

        String address = fromBinaryToDecimal(h) + "/" + fromBinaryToDecimal(m) + "/" + fromBinaryToDecimal(u);
        if (address.equals("0/0/0")) return "1/0/0";    /* 0/0/0 is reserved */
        return address;
    }

    /*
        HEX TO PHYSICAL ADDRESS CONVERSION
        a. 0x1073
        b. remove 0x -> 1073
        c. convert each digit in binary         ->      0001 0000 0111 0010
        d. take main(A) middle(L) and sub(M)    ->      AAAA LLLL MMMM MMMM
            A = 0010
            L = 0000
            M = 01110011
        d. convert A, L, M in decimal
            A = 2
            L = 0
            M = 115
        e. merge 2/0/115
     */
    public static String getKnxPhysicalAddress(String hex) {
        String hexValue = getHexValue(hex);
        if (hexValue == null) return null;
        String result = convertDigitsInBinary(hexValue);

        String a = result.substring(0, 4);
        String l = result.substring(4, 8);
        String m = result.substring(8);

        return fromBinaryToDecimal(a) + "." + fromBinaryToDecimal(l) + "." + fromBinaryToDecimal(m);
    }

    private static String convertDigitsInBinary(String hexValue) {
        String digit1 = hexValue.substring(0,1);
        String digit1Binary = fromHexToBinary(digit1);

        String digit2 = hexValue.substring(1,2);
        String digit2Binary = fromHexToBinary(digit2);

        String digit3 = hexValue.substring(2,3);
        String digit3Binary = fromHexToBinary(digit3);

        String digit4 = hexValue.substring(3,4);
        String digit4Binary = fromHexToBinary(digit4);

        return digit1Binary + digit2Binary + digit3Binary + digit4Binary;
    }

    private static String getHexValue(String hex) {
        if (hex == null) return null;
        return hex.replace("0x", "");
    }

    public static String fromHexToBinary(String value) {
        String decimalValue = fromHexToDecimal(value);
        String binaryValue = fromDecimalToBinary(decimalValue);
        return fillHexWithZero(binaryValue);
    }

    public static String fromHexToDecimal(String value) {
        return String.valueOf(Integer.parseInt(value, 16));
    }

    public static String fromDecimalToBinary(String value) {
        return Integer.toBinaryString(Integer.parseInt(value));
    }

    public static String fromBinaryToDecimal(String value) {
        return String.valueOf(Integer.parseInt(value, 2));
    }

    private static String fillHexWithZero(String binaryValue) {
        int hexLength = 4;
        String padding = repeatZero(hexLength-binaryValue.length());
        return padding + binaryValue;
    }

    private static String repeatZero(int times) {
        return IntStream
                .range(0, times)
                .mapToObj(i -> "0")
                .collect(Collectors.joining(""));
    }

    public static void main(String[] args) {
        assertGroupAddress("0x1073", "2/0/115");
        assertGroupAddress("0x190F", "3/1/15");
        assertGroupAddress("0x78FF", "15/0/255");
        assertGroupAddress("0x0000", "1/0/0");
        assertGroupAddress("0xFFFF", "31/7/255");
        assertGroupAddress("0x0C81", "1/4/129");

        assertPhysicalAddress("0x1073", "1.0.115");
        assertPhysicalAddress("0x190F", "1.9.15");
        assertPhysicalAddress("0x78FF", "7.8.255");
        assertPhysicalAddress("0x0000", "0.0.0");
        assertPhysicalAddress("0xFFFF", "15.15.255");
        assertPhysicalAddress("0x0C81", "0.12.129");
    }

    private static void assertGroupAddress(String input, String expected) {
        String address = getKnxGroupAddress(input);
        boolean result = address != null && address.equals(expected);
        System.out.println("GROUP ADDRESS" + ":\t\t[" + result + "]" + "\t\tINPUT: " + input + "\t\tACTUAL: " + address + "   \t\tEXPECTED: " + expected);
    }

    private static void assertPhysicalAddress(String input, String expected) {
        String address = getKnxPhysicalAddress(input);
        boolean result = address != null && address.equals(expected);
        System.out.println("PHYSICAL ADDRESS" + ":\t\t[" + result + "]" + "\t\tINPUT: " + input + "\t\tACTUAL: " + address + "   \t\tEXPECTED: " + expected);
    }

}