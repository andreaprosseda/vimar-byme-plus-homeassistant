package org.example.model.knx;

import java.util.ArrayList;
import java.util.List;

public class KnxYaml {

    private List<Light> lights;
    private List<Cover> covers;
    private List<Climate> climates;

    public List<Light> getLights() {
        if (lights == null) lights = new ArrayList<>();
        return lights;
    }

    public List<Cover> getCovers() {
        if (covers == null) covers = new ArrayList<>();
        return covers;
    }

    public List<Climate> getClimates() {
        if (climates == null) climates = new ArrayList<>();
        return climates;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("knx: \n\n");

        if (!lights.isEmpty()) {
            sb.append("  light:\n");
            lights.forEach(light -> sb.append(light.toString()));
        }

        if (!covers.isEmpty()) {
            sb.append("  cover:\n");
            covers.forEach(cover -> sb.append(cover.toString()));
        }

        if (!climates.isEmpty()) {
            sb.append("  climate:\n");
            climates.forEach(climate -> sb.append(climate.toString()));
        }

        return sb.toString();
    }

}
