from django import template
import random
register = template.Library()


@register.filter(name='default_user')
def default_user(value):
    if value == '':
        return value + "8080"
    else:
        value += 'aaaaa'
        return encode_string(value)


def encode_string(value):
    encode = ''
    pattern = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9','0']
    size = len(pattern)
    print(size)
    for i in range(0, len(value)-1):
        encode += value[i]
        for j in range(1, 5):
            encode += random.choice(pattern)
    return encode


