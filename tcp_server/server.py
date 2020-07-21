import socket
import re

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
server_sock.bind(('', 1111))
server_sock.listen(999)


def check_reg_expression_to_response(final_string):
    matched = re.match(
        b"[\d][\d][\d][\d] [A-Z\da-z][A-Z\da-z]"
        b" ([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]."
        b"[\d][\d][\d] [0][0][\r][\n]",
        final_string)
    return bool(matched)


def check_reg_expression_to_write(write_string):
    matched = re.match(
        b"[\d][\d][\d][\d] [A-Z\da-z][A-Z\da-z]"
        b" ([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]."
        b"[\d][\d][\d] [A-Z\da-z][A-Z\da-z][\r][\n]",
        write_string)
    return bool(matched)


def write_to_file(data_name):
    decoded_string_to_write = data_name.decode('utf-8')
    string_slice_to_write = f"спортсмен, нагрудный номер " \
                            f"{decoded_string_to_write[0:4]} прошёл отсечку " \
                            f"{decoded_string_to_write[5:7]} " \
                            f"в {decoded_string_to_write[8:23]} " \
                            f"\n"
    with open("output_log.txt", "a") as file:
        file.write(string_slice_to_write)


def encode_string_slice(data_bytes):
    if check_reg_expression_to_response(data_bytes):
        decoded_string = data_bytes.decode('utf-8')
        string_slice = f"спортсмен, нагрудный номер {decoded_string[0:4]} " \
                       f"прошёл отсечку {decoded_string[5:7]} " \
                       f"в {decoded_string[8:18]} \r" \
                       f"\n"
        return string_slice.encode(encoding='utf-8')


while True:
    client_sock, client_addr = server_sock.accept()
    print('Connected by', client_addr)

    while True:
        data = client_sock.recv(1024)
        if not data:
            break

        if check_reg_expression_to_response(data):
            write_to_file(data)
            client_sock.sendall(encode_string_slice(data))
        elif check_reg_expression_to_write(data):
            write_to_file(data)
            client_sock.sendall('Запись добавлена в лог.\r\n'.encode(encoding='utf-8'))
        else:
            client_sock.sendall('wrong request\r\n'.encode(encoding='utf-8'))
    client_sock.close()
