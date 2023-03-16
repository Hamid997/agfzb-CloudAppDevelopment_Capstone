from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException


def formResponse(statusCode, body):
    return {
        "statusCode": statusCode,
        "headers": {"Content-Type": "application/json"},
        "body": body
    }


def main(dict):
    secret = {
    "COUCH_URL": "https://df79c38b-74bb-431a-a111-d92b6a208d4e-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "XvNXa6UjlKYLgkTl_QqokptibIA_zR2D4GopvbNewRNu",
    "COUCH_USERNAME": "df79c38b-74bb-431a-a111-d92b6a208d4e-bluemix"
    }
    authenticator = IAMAuthenticator(
        secret["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secret["COUCH_URL"])

    try:
        selector = {"dealership": {"$eq": int(dict["dealerId"])}}
        response = service.post_find(
            db="reviews",
            selector=selector
        ).get_result()
        if (len(response["docs"]) == 0):
            return formResponse(404, response)
        else:
            return formResponse(200, response)
    except ApiException as ae:
        errorBody = {"error": ae.message}
        if ("reason" in ae.http_response.json()):
            errorBody["reason"] = ae.http_response.json()["reason"]
        return formResponse(int(ae.code), errorBody)
    except:
        return formResponse(500, {"error": "Something went wrong on the server"})