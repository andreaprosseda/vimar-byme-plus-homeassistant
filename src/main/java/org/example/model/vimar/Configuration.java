package org.example.model.vimar;

import jakarta.xml.bind.annotation.XmlElement;
import jakarta.xml.bind.annotation.XmlElementWrapper;
import jakarta.xml.bind.annotation.XmlRootElement;

import java.util.ArrayList;
import java.util.List;

@XmlRootElement(name= "byme_configuration")
public class Configuration {

    private List<Application> applications;
    @XmlElementWrapper(name = "applications")
    @XmlElement(name = "application")
    public List<Application> getApplications() {
        if (applications == null) applications = new ArrayList<>();
        return applications;
    }

    @Override
    public String toString() {
        return getApplications().toString();
    }
}
