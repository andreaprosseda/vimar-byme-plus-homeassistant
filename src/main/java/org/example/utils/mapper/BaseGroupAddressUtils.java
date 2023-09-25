package org.example.utils.mapper;

import org.example.model.vimar.Dpt;
import org.example.model.vimar.GroupAddress;

public class BaseGroupAddressUtils {

    public static boolean is(GroupAddress groupAddress, String value) {
        String name = getName(groupAddress);
        if (name == null) return false;
        return name.equals(value);
    }

    private static String getName(GroupAddress groupAddress) {
        if (groupAddress == null) return null;
        Dpt dptx = groupAddress.getDptx();
        if (dptx == null) return null;
        return dptx.getName();
    }

}
