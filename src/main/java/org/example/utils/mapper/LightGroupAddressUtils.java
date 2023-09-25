package org.example.utils.mapper;

import org.example.model.vimar.Dpt;
import org.example.model.vimar.GroupAddress;

public class LightGroupAddressUtils extends BaseGroupAddressUtils{

    public static boolean isLightAddress(GroupAddress groupAddress) {
        return is(groupAddress, "DPTx_OnOff");
    }

    public static boolean isLightStateAddress(GroupAddress groupAddress) {
        return is(groupAddress, "DPTx_OnOffInfo");
    }

}
