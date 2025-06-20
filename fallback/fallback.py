import re

#fallback for location
def fallback_location(user_prompt, entities):
    location = entities.get("loc","")

    if not location:
        loc = re.search(r"(?:no|actually|i moved to|i have relocated|i changed)\s+([a-zA-Z\s-]+)",user_prompt,re.IGNORECASE)
        if loc:
            location = loc.group(2).strip()
        return location

#fallback for name
def fallback_name_update(user_prompt, entities):
    name = entities.get("person", "")

    # Regex fallback if NER missed
    if not name:
        match = re.search(r"(?:no my name is|i am|i'm|it's|this is|call me|name is|updated my name to|"
            r"changed my name to|my real name is|people call me|my name is|i want to change my name to)\s+([a-zA-Z\s'-]+)",
            user_prompt, re.IGNORECASE
        )
        if match:
            name = match.group(1).strip()

    # Final fallback: if input is just a name
    if not name and re.fullmatch(r"[a-zA-Z\s'-]{2,}", user_prompt.strip()):
        name = user_prompt.strip()

    return name

common_colors = {
    "red", "blue", "green", "yellow", "purple", "black", "white",
    "orange", "pink", "brown", "gray", "grey", "gold", "silver",
    "maroon", "navy", "teal", "violet", "indigo", "beige", "cyan"
}

#fallback for color
def fallback_color(user_prompt, entities, common_colors):
    color = entities.get("color", "")
    if not color:
        for c in common_colors:
            if re.search(rf"\b{re.escape(c)}\b", user_prompt, re.IGNORECASE):
                color = c
                break
    return color
