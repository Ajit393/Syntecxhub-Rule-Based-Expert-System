"""
knowledge_base.py
=================

The PC/Laptop troubleshooting knowledge for the
rule-based expert system.

This file contains only domain knowledge:
    - symptoms/problems the user can report
    - rules connecting problems to possible causes
    - intermediate facts used for multi-step inference
    - final conclusions shown to the user

The inference logic itself is handled by engine.py.

This is an educational troubleshooting system.
It does not perform professional hardware diagnosis.
"""

from engine import Rule


# ---------------------------------------------------------------------------
# Symptoms/problems the user can report
# (internal fact name -> label shown to the user)
# ---------------------------------------------------------------------------

SYMPTOMS: dict[str, str] = {

    # Power
    "laptop_not_turning_on": "Laptop does not turn on",
    "charger_connected": "Charger is connected",
    "charging_light_off": "Charging light is off",

    # Display
    "laptop_turns_on": "Laptop turns on",
    "screen_black": "Screen is black",
    "fans_running": "Fans are running",
    "external_monitor_works": "External monitor works",

    # Overheating
    "laptop_gets_hot": "Laptop gets very hot",
    "fan_noise_high": "Fan noise is very high",

    # Performance
    "laptop_slow": "Laptop is running slowly",
    "many_background_apps": "Many applications are running in background",
    "disk_usage_high": "Disk usage is very high",

    # Network
    "wifi_not_working": "Wi-Fi is not working",
    "other_devices_have_wifi": "Other devices have working Wi-Fi",

    # Battery
    "battery_drains_quickly": "Battery drains quickly",

    # Keyboard
    "keyboard_not_working": "Keyboard is not working",
    "external_keyboard_works": "External keyboard works",

    # Storage
    "storage_almost_full": "Storage is almost full",
}


# ---------------------------------------------------------------------------
# Rules
#
# Some rules create intermediate facts.
# Other rules use those intermediate facts to create final conclusions.
#
# This allows multi-step forward chaining.
# ---------------------------------------------------------------------------

RULES: list[Rule] = [

    # =======================================================================
    # POWER
    # =======================================================================

    Rule(
        name="R1",
        conditions=frozenset({
            "laptop_not_turning_on",
            "charger_connected",
            "charging_light_off"
        }),
        conclusion="possible_power_or_charger_issue",
        explanation=(
            "The laptop does not turn on, the charger is connected, "
            "and the charging light is off. This may indicate a "
            "charger or power supply problem."
        ),
    ),

    # =======================================================================
    # DISPLAY - MULTI-STEP INFERENCE
    # =======================================================================

    # Step 1:
    # screen_black -> display_problem

    Rule(
        name="R2",
        conditions=frozenset({
            "screen_black"
        }),
        conclusion="display_problem",
        explanation=(
            "A black screen indicates a possible display-related problem."
        ),
    ),

    # Step 2:
    # display_problem + external_monitor_works
    # -> possible_internal_display_issue

    Rule(
        name="R3",
        conditions=frozenset({
            "display_problem",
            "external_monitor_works"
        }),
        conclusion="possible_internal_display_issue",
        explanation=(
            "The internal screen is black while an external monitor works. "
            "This suggests a possible internal display or display-cable issue."
        ),
    ),

    # Another display rule

    Rule(
        name="R4",
        conditions=frozenset({
            "laptop_turns_on",
            "screen_black",
            "fans_running"
        }),
        conclusion="possible_display_issue",
        explanation=(
            "The laptop appears to be running because the fans are active, "
            "but the screen remains black. This suggests a possible display issue."
        ),
    ),

    # =======================================================================
    # OVERHEATING
    # =======================================================================

    Rule(
        name="R5",
        conditions=frozenset({
            "laptop_gets_hot",
            "fan_noise_high"
        }),
        conclusion="possible_overheating_issue",
        explanation=(
            "High temperature combined with unusually loud fan noise "
            "suggests a possible overheating problem."
        ),
    ),

    # =======================================================================
    # PERFORMANCE
    # =======================================================================

    Rule(
        name="R6",
        conditions=frozenset({
            "laptop_slow",
            "many_background_apps"
        }),
        conclusion="possible_background_process_issue",
        explanation=(
            "A slow laptop with many background applications may be "
            "affected by excessive background processes."
        ),
    ),

    Rule(
        name="R7",
        conditions=frozenset({
            "laptop_slow",
            "disk_usage_high"
        }),
        conclusion="possible_storage_performance_issue",
        explanation=(
            "High disk usage combined with slow performance may indicate "
            "a storage or disk-performance problem."
        ),
    ),

    # =======================================================================
    # NETWORK
    # =======================================================================

    Rule(
        name="R8",
        conditions=frozenset({
            "wifi_not_working",
            "other_devices_have_wifi"
        }),
        conclusion="possible_laptop_network_issue",
        explanation=(
            "Wi-Fi works on other devices but not on the laptop. "
            "This suggests a possible laptop-specific network issue."
        ),
    ),

    # =======================================================================
    # BATTERY
    # =======================================================================

    Rule(
        name="R9",
        conditions=frozenset({
            "battery_drains_quickly",
            "laptop_gets_hot"
        }),
        conclusion="possible_battery_or_power_management_issue",
        explanation=(
            "Rapid battery drain combined with high temperature may "
            "indicate a possible battery or power-management issue."
        ),
    ),

    # =======================================================================
    # KEYBOARD
    # =======================================================================

    Rule(
        name="R10",
        conditions=frozenset({
            "keyboard_not_working",
            "external_keyboard_works"
        }),
        conclusion="possible_internal_keyboard_issue",
        explanation=(
            "The external keyboard works while the laptop keyboard does not. "
            "This suggests a possible internal keyboard issue."
        ),
    ),

    # =======================================================================
    # STORAGE
    # =======================================================================

    Rule(
        name="R11",
        conditions=frozenset({
            "storage_almost_full",
            "laptop_slow"
        }),
        conclusion="possible_low_storage_issue",
        explanation=(
            "Very low free storage combined with slow performance "
            "may contribute to system slowdown."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Final conclusions
#
# These are the results that should be displayed to the user.
# ---------------------------------------------------------------------------

FINAL_DIAGNOSES: dict[str, str] = {

    "possible_power_or_charger_issue":
        "Possible Charger / Power Supply Issue",

    "possible_internal_display_issue":
        "Possible Internal Display Issue",

    "possible_display_issue":
        "Possible Display Issue",

    "possible_overheating_issue":
        "Possible Overheating Issue",

    "possible_background_process_issue":
        "Possible Background Process Issue",

    "possible_storage_performance_issue":
        "Possible Storage Performance Issue",

    "possible_laptop_network_issue":
        "Possible Laptop Network Issue",

    "possible_battery_or_power_management_issue":
        "Possible Battery / Power Management Issue",

    "possible_internal_keyboard_issue":
        "Possible Internal Keyboard Issue",

    "possible_low_storage_issue":
        "Possible Low Storage Issue",
}


# ---------------------------------------------------------------------------
# Intermediate facts
#
# These are NOT directly selected by the user.
# They are generated by the inference engine and can be used
# by another rule.
# ---------------------------------------------------------------------------

INTERMEDIATE_FACTS: dict[str, str] = {

    "display_problem":
        "Display problem (intermediate)",
}


# ---------------------------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------------------------

DISCLAIMER = (
    "This is an educational rule-based troubleshooting system. "
    "It does not provide professional hardware diagnosis. "
    "The suggested causes are based only on the rules programmed "
    "into the system."
)