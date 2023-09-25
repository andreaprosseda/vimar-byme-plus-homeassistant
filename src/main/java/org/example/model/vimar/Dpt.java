package org.example.model.vimar;

import jakarta.xml.bind.annotation.XmlAttribute;

public class Dpt {
    private String id;

    private String name;

    @XmlAttribute
    public String getId() {
        return id;
    }

    public void setId(String id) { this.id = id; }

    @XmlAttribute
    public String getName() {
        return name;
    }

    public void setName(String name) { this.name = name; }

    @Override
    public String toString() {
        return "Dpt{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                '}';
    }


}
