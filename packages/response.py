import json
status_codes = {
    
    200: "OK",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    405: "Method Not Allowed",
    429: "Too Many Requests",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    504: "Gateway Timeout"
}


def response_handler(code,content,type):

    response=(f"HTTP/1.1 {code} {status_codes.get(code)}\r\n"
              f"Content-Type: {type}\r\n"
              f"Content-Length: {len(content)}\r\n"
               "\r\n"
              f"{content}")
    return response