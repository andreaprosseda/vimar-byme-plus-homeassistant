package org.example.model.knx;

public class Cover {

    private String name;
    private String moveLongAddress;
    private String stopAddress;
    private String positionAddress;
    private String positionStateAddress;
    private int travellingTimeDown;
    private int travellingTimeUp;
    private boolean invertUpDown;
    private String deviceClass;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getMoveLongAddress() {
        return moveLongAddress;
    }

    public void setMoveLongAddress(String moveLongAddress) {
        this.moveLongAddress = moveLongAddress;
    }

    public String getStopAddress() {
        return stopAddress;
    }

    public void setStopAddress(String stopAddress) {
        this.stopAddress = stopAddress;
    }

    public String getPositionAddress() {
        return positionAddress;
    }

    public void setPositionAddress(String positionAddress) {
        this.positionAddress = positionAddress;
    }

    public String getPositionStateAddress() {
        return positionStateAddress;
    }

    public void setPositionStateAddress(String positionStateAddress) {
        this.positionStateAddress = positionStateAddress;
    }

    public int getTravellingTimeDown() {
        return travellingTimeDown;
    }

    public void setTravellingTimeDown(int travellingTimeDown) {
        this.travellingTimeDown = travellingTimeDown;
    }

    public int getTravellingTimeUp() {
        return travellingTimeUp;
    }

    public void setTravellingTimeUp(int travellingTimeUp) {
        this.travellingTimeUp = travellingTimeUp;
    }

    public String getDeviceClass() { return deviceClass; }

    public void setDeviceClass(String deviceClass) { this.deviceClass = deviceClass; }

    public boolean isInvertUpDown() { return invertUpDown; }

    public void setInvertUpDown(boolean invertUpDown) { this.invertUpDown = invertUpDown; }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("    - name: '" + getName() + "'\n");
        if(getMoveLongAddress() != null)        sb.append("      move_long_address: '" + getMoveLongAddress() + "'\n");
        if(getStopAddress() != null)            sb.append("      stop_address: '" + getStopAddress() + "'\n");
        if(getPositionAddress() != null)        sb.append("      position_address: '" + getPositionAddress() + "'\n");
        if(getPositionStateAddress() != null)   sb.append("      position_state_address: '" + getPositionStateAddress() + "'\n");
        if(isInvertUpDown())                    sb.append("      invert_updown: true");
        if(getDeviceClass() != null)            sb.append("      device_class: '" + getDeviceClass() + "'\n");
        sb.append("\n");
        return sb.toString();
    }

}
