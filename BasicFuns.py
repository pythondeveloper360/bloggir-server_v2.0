from random import shuffle


def idGenerator(_range:int=10):
    alpha = [*[chr(i) for i in range(ord('a'), ord('z')+1)], *[chr(i)
                                                               for i in range(ord('A'), ord('Z')+1)], *[str(i) for i in range(1, 11)]]
    shuffle(alpha)
    return ''.join(alpha[0:int(_range)])
