package org.example.utils;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class TestUtils {

    public static final Pattern HEX_VALUE = Pattern.compile("[0-9]x[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]");
    public static final Pattern GROUP_ADDRESS = Pattern.compile("([0-9]+/[0-9]+/[0-9]+)");
    public static final Pattern PHYSICAL_ADDRESS = Pattern.compile("([0-9]+\\.[0-9]+\\.[0-9]+)");

    public static String getGroupTest(String line) {
        Matcher hex = HEX_VALUE.matcher(line);
        Matcher address = GROUP_ADDRESS.matcher(line);

        String hexValue = null;
        String addressValue = null;

        if (hex.find()) {
             hexValue = hex.group(0);
        }

        if (address.find()) {
            addressValue = address.group(0);
        }

        if (hexValue == null || addressValue == null) return null;
        return "assertGroupAddress(\"" + hexValue + "\", \"" + addressValue +"\");";
    }

    public static String getPhysicalTest(String line) {
        Matcher hex = HEX_VALUE.matcher(line);
        Matcher address = PHYSICAL_ADDRESS.matcher(line);

        String hexValue = null;
        String addressValue = null;

        if (hex.find()) {
            hexValue = hex.group(0);
        }

        if (address.find()) {
            addressValue = address.group(0);
        }

        if (hexValue == null || addressValue == null) return null;
        return "assertPhysicalAddress(\"" + hexValue + "\", \"" + addressValue +"\");";
    }

    public static void main(String[] args) throws Exception {
        Path path = Paths.get("/Users/andrea/Desktop/log.txt");
        Files
                .lines(path)
                .map(String::trim)
                .filter(GROUP_ADDRESS.asPredicate())
                .map(TestUtils::getGroupTest)
                .filter(Objects::nonNull)
                .distinct()
                .forEach(System.out::println);

        Files
                .lines(path)
                .filter(PHYSICAL_ADDRESS.asPredicate())
                .map(TestUtils::getPhysicalTest)
                .filter(Objects::nonNull)
                .distinct()
                .forEach(System.out::println);


    }


}
