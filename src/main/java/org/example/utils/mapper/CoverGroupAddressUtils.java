package org.example.utils.mapper;

import org.example.model.vimar.Dpt;
import org.example.model.vimar.GroupAddress;

public class CoverGroupAddressUtils extends BaseGroupAddressUtils {

    public static boolean isMoveLongAddress(GroupAddress groupAddress) {
        return is(groupAddress, "");
    }

    public static boolean isMoveShortAddress(GroupAddress groupAddress) {
        return is(groupAddress, "");
    }

    public static boolean isStopAddress(GroupAddress groupAddress) {
        return is(groupAddress, "DPTx_StopStepUpDown");
    }

    public static boolean isPositionAddress(GroupAddress groupAddress) {
        return is(groupAddress, "");
    }

    public static boolean isPositionStateAddress(GroupAddress groupAddress) {
        return is(groupAddress, "");
    }

}