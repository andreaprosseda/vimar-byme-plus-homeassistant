package org.example.mapper;

import org.example.enums.DptValue;
import org.example.model.knx.Climate;
import org.example.model.vimar.Application;
import org.example.model.vimar.Group;
import org.example.utils.ApplicationUtils;

import java.util.ArrayList;
import java.util.Arrays;

public class ClimateMapper extends BaseMapper {

    public static Climate from(Application application) {
        if (application == null) return null;
        Group group = ApplicationUtils.getMainGroup(application);
        return from(application.getLabel(), group);
    }

    public static Climate from(String name, Group group) {
        Climate climate = new Climate();
        climate.setName(name);
        climate.setTemperatureAddress(getAddress(group, DptValue.TEMPERATURE));
        climate.setTargetTemperatureAddress(getAddress(group, DptValue.TARGET_TEMPERATURE));
        climate.setTargetTemperatureStateAddress(getAddress(group, DptValue.TARGET_TEMPERATURE_STATE));
        climate.setMinTemp(16);
        climate.setMaxTemp(30);
        climate.setControllerModeAddress(getAddress(group, DptValue.CONTROLLER_MODE));
        climate.setControllerModeStateAddress(getAddress(group, DptValue.CONTROLLER_MODE_STATE));
        climate.getControllerModes().addAll(Arrays.asList("Auto", "Heat", "Cool", "Off"));
        return climate;
    }

}