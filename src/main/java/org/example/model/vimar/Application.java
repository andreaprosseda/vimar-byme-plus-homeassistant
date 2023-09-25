package org.example.model.vimar;

import jakarta.xml.bind.annotation.XmlAttribute;
import jakarta.xml.bind.annotation.XmlElement;
import jakarta.xml.bind.annotation.XmlElementWrapper;
import jakarta.xml.bind.annotation.XmlRootElement;
import org.example.enums.Category;

import java.util.ArrayList;
import java.util.List;

public class Application {

    private String id;
    private String label;
    private String category_id;
    private List<Group> groups;

    @XmlAttribute
    public String getId() {
        return id;
    }

    public void setId(String id) { this.id = id; }

    @XmlAttribute
    public String getLabel() { return label; }

    public void setLabel(String label) { this.label = label; }

    @XmlAttribute(name = "category_id")
    public String getCategoryId() { return category_id; }

    public void setCategoryId(String category_id) { this.category_id = category_id; }

    @XmlElementWrapper(name = "groups")
    @XmlElement(name = "group")
    public List<Group> getGroups() {
        if (groups == null) groups = new ArrayList<>();
        return groups;
    }

    public boolean hasCategory(Category category) {
        if (category == null) return false;
        if (getCategoryId() == null) return false;
        return getCategoryId().equals(category.getId());
    }

    @Override
    public String toString() {
        return "Application{" +
                "id='" + id + '\'' +
                ", category_id='" + category_id + '\'' +
                ", groups=" + groups +
                '}';
    }

}
