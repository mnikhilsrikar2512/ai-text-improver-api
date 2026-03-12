TEMPLATES = {

    "sick_leave": [
        "I will be taking sick leave today.",
        "I require sick leave today due to illness.",
        "I will be on sick leave today."
    ],

    "family_leave": [
        "I need to take leave today due to a family matter.",
        "I will be unavailable today due to a family commitment.",
        "I need to attend to a family matter today and will be on leave."
    ],

    "meeting_absence": [
        "I will be unable to attend the meeting.",
        "I regret that I cannot attend the meeting.",
        "I will not be able to participate in the meeting."
    ]
}


def get_template(intent):

    return TEMPLATES.get(intent)


def get_template(intent):

    if intent in TEMPLATES:
        return TEMPLATES[intent]

    return None