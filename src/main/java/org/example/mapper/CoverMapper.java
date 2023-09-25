package org.example.mapper;

import org.example.enums.DptValue;
import org.example.model.knx.Cover;
import org.example.model.vimar.Application;
import org.example.model.vimar.Dpt;
import org.example.model.vimar.Group;
import org.example.utils.ApplicationUtils;
import org.example.utils.mapper.BaseGroupAddressUtils;
import org.example.utils.mapper.CoverGroupAddressUtils;
import org.example.utils.mapper.LightGroupAddressUtils;

import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public class CoverMapper extends BaseMapper {

    public static Cover from(Application application) {
        if (application == null) return null;
        Group group = ApplicationUtils.getMainGroup(application);
        return from(application.getLabel(), group);
    }
    public static Cover fromDoor(Application application) {
        if (application == null) return null;
        Group group = ApplicationUtils.getMainGroup(application);
        return fromDoor(application.getLabel(), group);
    }

    public static Cover from(String name, Group group) {
        Cover cover = new Cover();
        cover.setName(name);
        cover.setMoveLongAddress(getAddress(group, DptValue.MOVE_LONG));
        cover.setPositionAddress(getAddress(group, DptValue.POSITION));
        cover.setPositionStateAddress(getAddress(group, DptValue.POSITION_STATE));
        cover.setStopAddress(getAddress(group, DptValue.STOP));
        cover.setTravellingTimeDown(30);
        cover.setTravellingTimeUp(30);
        cover.setInvertUpDown(false);
        cover.setDeviceClass("blind");
        return cover;
    }

    public static Cover fromDoor(String name, Group group) {
        Cover cover = new Cover();
        cover.setName(name);
        cover.setMoveLongAddress(getAddress(group, DptValue.ON_OFF));
        cover.setTravellingTimeDown(1);
        cover.setTravellingTimeUp(0);
        cover.setInvertUpDown(true);
        cover.setDeviceClass("door");
        return cover;
    }

}