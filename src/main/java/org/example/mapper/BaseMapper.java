package org.example.mapper;

import org.example.enums.DptValue;
import org.example.model.vimar.Group;
import org.example.model.vimar.GroupAddress;
import org.example.utils.mapper.BaseGroupAddressUtils;

import java.util.function.Predicate;

public class BaseMapper {

//    private static String getKnxAddress(Group group, Predicate<GroupAddress> predicate) {
//        return group
//                .getGroupAddresses()
//                .stream()
//                .filter(predicate)
//                .map(GroupAddress::getKnxAddress)
//                .findFirst()
//                .orElse(null);
//    }

    public static String getKnxAddress(Group group, DptValue value) {
        return group
                .getGroupAddresses()
                .stream()
                .filter(address -> BaseGroupAddressUtils.is(address, value.getId()))
                .map(GroupAddress::getKnxAddress)
                .findFirst()
                .orElse(null);
    }

    public static String getAddress(Group group, DptValue value) {
        return getKnxAddress(group, value);
    }

}
