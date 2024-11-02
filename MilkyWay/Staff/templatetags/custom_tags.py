# custom_tags.py
from django import template

register = template.Library()
class MyClass:
    # Định nghĩa biến tĩnh
    static_variable = 0

    def __init__(self, value):
        self.instance_variable = value  # Biến thể hiện

    def increment_static(self):
        MyClass.static_variable += 1

    def get_static_variable(self):
        return MyClass.static_variable
@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def addition(value, arg):
    return int(MyClass.static_variable) + int(value) + int(MyClass.static_variable)