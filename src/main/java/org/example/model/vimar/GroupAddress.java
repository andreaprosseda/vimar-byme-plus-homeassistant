package org.example.model.vimar;


import jakarta.xml.bind.annotation.XmlAttribute;
import jakarta.xml.bind.annotation.XmlElement;
import org.example.utils.KnxUtils;

public class GroupAddress {
    private Dpt dpt;
    private Dpt dptx;
    private String address;

    @XmlElement
    public Dpt getDpt() {
        return dpt;
    }

    public void setDpt(Dpt dpt) { this.dpt = dpt; }

    @XmlElement
    public Dpt getDptx() {
        return dptx;
    }

    public void setDptx(Dpt dptx) { this.dptx = dptx; }

    @XmlAttribute
    public String getAddress() {
        return address;
    }

    public void setAddress(String address) { this.address = address; }

    public String getKnxAddress() {
        return KnxUtils.getKnxGroupAddress(address);
    }

    @Override
    public String toString() {
        return "GroupAddress{" +
                "dpt=" + getDpt() +
                ", hex_address='" + getAddress() + '\'' +
                ", knx_address='" + getKnxAddress() + '\'' +
                '}';
    }
}
