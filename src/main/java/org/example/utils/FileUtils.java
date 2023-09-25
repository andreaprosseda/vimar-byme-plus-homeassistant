package org.example.utils;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.logging.Level;
import java.util.logging.Logger;

public class FileUtils {

    private static final Logger logger = Logger.getLogger(FileUtils.class.getName());

    public static void create(String content, String path) {
        try {
            Files.writeString(Path.of(path), content);
        } catch (IOException e) {
            logger.log(Level.SEVERE, e.getMessage());
        }
    }

    public static void open(String path) {
        try {
            File file = new File(path);
            if (file.exists()) {
                Desktop desktop = Desktop.getDesktop();
                desktop.open(file);
            }
        } catch (Exception e) {
            logger.log(Level.SEVERE, e.getMessage());
        }
    }

    public static String getFolder(String filePath) {
        int index = filePath.lastIndexOf("/");
        if (index < 0) return null;
        return filePath.substring(0, index);
    }
}
