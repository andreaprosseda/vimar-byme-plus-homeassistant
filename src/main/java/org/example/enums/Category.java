package org.example.enums;

public enum Category {
    LIGHT("1", "luci"),
    COVER("2", "tende e tapparelle"),
    CLIMATE("4", "clima"),
    DOOR("9", "accessi e presenze");

    private final String id;
    private final String name;

    private Category(String id, String name) {
        this.id = id;
        this.name = name;
    }

    public String getId() { return id; }

    public String getName() { return name; }

}
