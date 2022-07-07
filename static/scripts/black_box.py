def send_list(image: bytes):
    a = image.find(b'\x00')
    return [1, 2, 3, a]
