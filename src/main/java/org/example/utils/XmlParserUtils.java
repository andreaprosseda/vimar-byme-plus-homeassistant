package org.example.utils;

import jakarta.xml.bind.JAXBContext;
import jakarta.xml.bind.Unmarshaller;
import org.example.model.vimar.Configuration;

import java.io.File;
import java.util.logging.Level;
import java.util.logging.Logger;

public class XmlParserUtils {
    private static final Logger logger = Logger.getLogger(XmlParserUtils.class.getName());

    public static Configuration getConfiguration(String xmlPath) {
        try {
            JAXBContext context = JAXBContext.newInstance(Configuration.class);
            Unmarshaller unmarshaller = context.createUnmarshaller();
            return (Configuration) unmarshaller.unmarshal(new File(xmlPath));
        } catch (Exception e) {
            logger.log(Level.SEVERE, e.getMessage());
            return null;
        }
    }
}
