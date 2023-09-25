package org.example.model.knx;

public class Light {

    private String name;
    private String address;
    private String stateAddress;

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

    @Override
    public String toString() {
        return
                "    - name: '" + getName() + "'\n" +
                "      address: '" + getAddress() + "'\n" +
                "      state_address: '" + getStateAddress() + "'\n" +
                "\n";
    }
}
