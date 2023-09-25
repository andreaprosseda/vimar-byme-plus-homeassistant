package org.example.mapper;

import org.example.enums.DptValue;
import org.example.model.knx.Light;
import org.example.model.vimar.Application;
import org.example.model.vimar.Group;
import org.example.utils.ApplicationUtils;
import org.example.utils.mapper.LightGroupAddressUtils;

import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public class LightMapper extends BaseMapper {

    public static Light from(Application application) {
        if (application == null) return null;
        Group group = ApplicationUtils.getMainGroup(application);
        return from(application.getLabel(), group);
    }

    public static Light from(String name, Group group) {
        Light light = new Light();
        light.setName(name);
        light.setAddress(getAddress(group, DptValue.ON_OFF));
        light.setStateAddress(getAddress(group, DptValue.ON_OFF_STATE));
        return light;
    }

}
