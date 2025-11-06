from flask import jsonify

def success_response(data=None, message="成功しました", status=200):
    response = {
        "success" : True,
        "message" : message,
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status

def erorr_resoponse(message="エラーが発生しました", erorr=None, status=500):
    response = {
        "success" : False,
        "message" : message,
    }
    if erorr is not None:
        response["error"] = str(erorr)
        return jsonify(response), status