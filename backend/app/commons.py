from fastapi import HTTPException


def return_http_400_response(message):
    raise HTTPException(status_code=400, detail=message)


def return_http_404_response(message):
    raise HTTPException(status_code=404, detail=message)


def return_http_403_response(message):
    raise HTTPException(status_code=403, detail=message)
