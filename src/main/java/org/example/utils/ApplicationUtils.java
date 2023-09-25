package org.example.utils;

import org.example.model.vimar.Application;
import org.example.model.vimar.Group;

public class ApplicationUtils {

    public static Group getMainGroup(Application application) {
        if (application == null) return null;
        return application
                .getGroups()
                .stream()
                .findFirst()
                .orElse(null);
    }

}
