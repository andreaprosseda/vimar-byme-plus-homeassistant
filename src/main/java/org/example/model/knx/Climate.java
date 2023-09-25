package org.example.model.knx;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Climate {
    private String name;
    private String temperatureAddress;
    private String targetTemperatureAddress;
    private String targetTemperatureStateAddress;
    private String controllerModeAddress;
    private String controllerModeStateAddress;
    private int minTemp;
    private int maxTemp;
    private List<String> controllerModes;

    public String getName() { return name; }

    public void setName(String name) { this.name = name; }

    public String getTemperatureAddress() {
        return temperatureAddress;
    }

    public void setTemperatureAddress(String temperatureAddress) {
        this.temperatureAddress = temperatureAddress;
    }

    public String getTargetTemperatureAddress() {
        return targetTemperatureAddress;
    }

    public void setTargetTemperatureAddress(String targetTemperatureAddress) { this.targetTemperatureAddress = targetTemperatureAddress; }

    public String getTargetTemperatureStateAddress() {
        return targetTemperatureStateAddress;
    }

    public void setTargetTemperatureStateAddress(String targetTemperatureStateAddress) { this.targetTemperatureStateAddress = targetTemperatureStateAddress; }

    public String getControllerModeAddress() {
        return controllerModeAddress;
    }

    public void setControllerModeAddress(String controllerModeAddress) { this.controllerModeAddress = controllerModeAddress; }

    public String getControllerModeStateAddress() {
        return controllerModeStateAddress;
    }

    public void setControllerModeStateAddress(String controllerModeStateAddress) { this.controllerModeStateAddress = controllerModeStateAddress; }

    public int getMinTemp() {
        return minTemp;
    }

    public void setMinTemp(int minTemp) {
        this.minTemp = minTemp;
    }

    public int getMaxTemp() {
        return maxTemp;
    }

    public void setMaxTemp(int maxTemp) {
        this.maxTemp = maxTemp;
    }

    public List<String> getControllerModes() {
        if (controllerModes == null) controllerModes = new ArrayList<>();
        return controllerModes;
    }

    @Override
    public String toString() {
        return
                "    - name: '" + getName() + "'\n" +
                "      temperature_address: '" + getTemperatureAddress() + "'\n" +
                "      target_temperature_address: '" + getTargetTemperatureAddress() + "'\n" +
                "      target_temperature_state_address: '" + getTargetTemperatureStateAddress() + "'\n" +
                "      controller_mode_address: '" + getControllerModeAddress() + "'\n" +
                "      controller_mode_state_address: '" + getControllerModeStateAddress() + "'\n" +
                "      min_temp: " + getMinTemp() + "\n" +
                "      max_temp: " + getMaxTemp() + "\n" +
                "      controller_modes: [" + getControllerModes().stream().map(val -> "'" + val + "'").collect(Collectors.joining(", ")) + "]\n" +
                "\n";
    }

}
