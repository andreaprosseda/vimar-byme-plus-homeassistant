package org.example;

import org.example.enums.Category;
import org.example.mapper.ClimateMapper;
import org.example.mapper.CoverMapper;
import org.example.mapper.LightMapper;
import org.example.model.knx.*;
import org.example.model.vimar.Application;
import org.example.model.vimar.Configuration;
import org.example.utils.FileUtils;
import org.example.utils.XmlParserUtils;

import java.util.List;
import java.util.stream.Collectors;

public class Migrator {
    private static final String XML_PATH = "/Users/andrea/Desktop/vimar_export.xml";
    private static final String YAML_FILENAME = "result.yaml";

    private final Configuration configuration;

    public Migrator(Configuration configuration) {
        this.configuration = configuration;
    }

    private List<Application> getApplications(Category category) {
        return configuration
                .getApplications()
                .stream()
                .filter(application -> application.hasCategory(category))
                .collect(Collectors.toList());
    }

    private KnxYaml createYaml() {
        KnxYaml yaml = new KnxYaml();
        yaml.getLights().addAll(getLights());
        yaml.getCovers().addAll(getCovers());
        yaml.getCovers().addAll(getCoverDoors());
        yaml.getClimates().addAll(getClimates());
        return yaml;
    }

    private List<Light> getLights() {
        return getApplications(Category.LIGHT)
                .stream()
                .map(LightMapper::from)
                .collect(Collectors.toList());
    }

    private List<Cover> getCovers() {
        return getApplications(Category.COVER)
                .stream()
                .map(CoverMapper::from)
                .collect(Collectors.toList());
    }

    private List<Cover> getCoverDoors() {
        return getApplications(Category.DOOR)
                .stream()
                .map(CoverMapper::fromDoor)
                .collect(Collectors.toList());
    }

    private List<Climate> getClimates() {
        return getApplications(Category.CLIMATE)
                .stream()
                .map(ClimateMapper::from)
                .collect(Collectors.toList());
    }

    public static void main(String[] args) {
        Configuration config = XmlParserUtils.getConfiguration(XML_PATH);
        Migrator migrator = new Migrator(config);
        KnxYaml yaml = migrator.createYaml();
        String folder = FileUtils.getFolder(XML_PATH);
        FileUtils.create(yaml.toString(), folder + "/" + YAML_FILENAME);
        FileUtils.open(folder + "/" + YAML_FILENAME);
    }
}