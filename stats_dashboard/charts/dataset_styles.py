def python_to_javascript_name(name: str):
    """
    Converts a Python variable name to a JavaScript name
    e.g. background_color -> backgroundColor
    """
    splitted_name = name.split("_")
    capitalized_name = [splitted_name[0]] + [name.title() for name in splitted_name[1:]]
    return "".join(capitalized_name)


class DatasetStyle:
    def __init__(self, **kwargs):
        self.styles = {}
        for style_name, value in kwargs.items():
            style_name_formatted = python_to_javascript_name(style_name)
            self.styles[style_name_formatted] = value

    def get_dictionary(self):
        return self.styles


default_styles = {
    "border_color": "rgba(255, 127, 80, 0.5)",
    "border_width": 2,
    "hover_background_color": "rgb(255, 127, 80)",
    "hover_border_width": 7,
    "background_color": [
        "rgba(255, 127, 80, 0.2)",
        "rgba(255, 127, 80, 0.3)",
        "rgba(255, 127, 80, 0.4)",
        "rgba(255, 127, 80, 0.5)",
        "rgba(255, 127, 80, 0.6)",
    ],
    "point_background_color": "orange",
    "point_border_width": 8,
}

site_default_style = DatasetStyle(**default_styles)

"""
Some common styles:

background_color,
border_cap_style,
border_color,
border_width,
fill,
hover_background_color,
hover_border_cap_style,
hover_border_color,
hover_border_width,
label,
line_tension,
point_background_color,
point_border_color,
point_border_width,
point_style,
"""
