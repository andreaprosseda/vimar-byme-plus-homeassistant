package org.example.model.vimar;

import jakarta.xml.bind.annotation.XmlElement;
import jakarta.xml.bind.annotation.XmlElementWrapper;
import jakarta.xml.bind.annotation.XmlRootElement;

import java.util.ArrayList;
import java.util.List;

@XmlRootElement(name = "group")
public class Group {
    private List<GroupAddress> groupAddresses;

    @XmlElementWrapper(name = "group_addresses")
    @XmlElement(name = "group_address")
    public List<GroupAddress> getGroupAddresses() {
        if (groupAddresses == null) groupAddresses = new ArrayList<>();
        return groupAddresses;
    }

    @Override
    public String toString() {
        return "Group{" +
                "groupAddresses=" + groupAddresses +
                '}';
    }
}
