from rest_framework import serializers

from common.utils import characters


def validate_number(number: str):
    if len(number) != 11:
        raise ValueError('invalid number length')
    
    if number[:2] != "09":
        raise ValueError('invalid number')
    
    try:
        int(number)
    except:
        raise ValueError('invalid number character')
    

def validate_landline_number(landline_number: str):
    if len(landline_number) < 5:
        raise ValueError('invalid number length')
    
    try:
        int(landline_number)
    except:
        raise ValueError('invalid number character')
    

def validate_name(name: str):
    valid_chars = characters.NAME_CHARS

    validate(name.lower(), valid_chars)
        
def validate_description(description: str):
    valid_chars = characters.DESCRIPTION_CHARS

    validate(description.lower(), valid_chars)
        

def validate_username(username: str):
    valid_chars = characters.USERNAME_CHARS

    validate(username.lower(), valid_chars)

def validate_choice_se(field_name, field_value):
    if field_value.key != field_name:
        raise serializers.ValidationError({field_name:f'{field_name} with id={field_value.id} not found'})

def validate_integer(value):
    """validate a string that have integer"""
    if type(value) != str:
        raise ValueError('invalid integer')
    try:
        int(value)
    except:
        raise ValueError('invalid integer')

def validate(string: str, valid_chars):

    for c in string:
        if c not in valid_chars:
            raise ValueError('invalid character: '+c)
            

def validate_se(field_name, field_value, validate_func):
    """validate with serializer exception"""

    try:
        validate_func(field_value)
    except ValueError as e:
        raise serializers.ValidationError({field_name: str(e)})