package org.example.model.knx;

public class BinarySensor {

    private String name;
    private String address;
    private String stateAddress;
    private Float resetAfter;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getStateAddress() {
        return stateAddress;
    }

    public void setStateAddress(String stateAddress) {
        this.stateAddress = stateAddress;
    }

    public Float getResetAfter() { return resetAfter; }

    public void setResetAfter(Float resetAfter) { this.resetAfter = resetAfter; }

    @Override
    public String toString() {
        return
                "    - name: '" + getName() + "'\n" +
//                "      address: '" + getAddress() + "'\n" +
                "      state_address: '" + getStateAddress() + "'\n" +
                "      reset_after: " + getResetAfter() + "\n" +
                "\n";
    }
}
