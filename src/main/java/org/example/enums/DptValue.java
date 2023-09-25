package org.example.enums;

public enum DptValue {
    ON_OFF("DPTx_OnOff", "On/Off relè"),
    ON_OFF_STATE("DPTx_OnOffInfo", "Stato corrente On/Off"),
    STOP("DPTx_StopStepUpDown", "STOP (con tapparella in movimento)"),
    MOVE_LONG("DPTx_UpDown", "Tutto su / Tutto giù"),
    POSITION("DPTx_ShutterPosition", "Aoertura/Chiusura % tapparelle"),
    POSITION_STATE("DPTx_ShutterPositionInfo", "Stato corrente di apertura delle tapparella"),
    TEMPERATURE("DPTx_AmbientTemperature","Temperatura corrente della stanza"),
    TARGET_TEMPERATURE("DPTx_TemperatureSetpoint1","Set della temperatura da raggiungere"),
    TARGET_TEMPERATURE_STATE("DPTx_TemperatureSetpointInfo1","Verifica della temperatura da raggiungere"),
    CONTROLLER_MODE("DPTx_HvacMode","Set HVAC Mode"),
        CONTROLLER_MODE_STATE("DPTx_HvacModeInfo","Verifica del HVAC Mode");

    private final String id;
    private final String description;

    private DptValue(String id, String description) {
        this.id = id;
        this.description = description;
    }

    public String getId() { return id; }

    public String getDescription() { return description; }

}

