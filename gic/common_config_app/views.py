from django.shortcuts import render


def generate_response(success, data, message):
    return {
        "success": success,
        "message": message,
        "data": data,
    }
