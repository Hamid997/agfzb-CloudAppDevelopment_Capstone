from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document
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
        posted_review = Document(
            review_id=dict["review"]["review_id"],
            name=dict["review"]["name"],
            dealership=dict["review"]["dealership"],
            review=dict["review"]["review"],
            purchase=dict["review"]["purchase"],
            purchase_date=dict["review"]["purchase_date"],
            car_make=dict["review"]["car_make"],
            car_model=dict["review"]["car_model"],
            car_year=dict["review"]["car_year"]
        )
        uuid = service.get_uuids(count=1).get_result()
        thisUuid = uuid["uuids"][0]
        response = service.put_document(
            db="reviews",
            doc_id=thisUuid,
            document=posted_review).get_result()
        return formResponse(200, response)
    except ApiException as ae:
        errorBody = {"error": ae.message}
        if ("reason" in ae.http_response.json()):
            errorBody["reason"] = ae.http_response.json()["reason"]
        return formResponse(int(ae.code), errorBody)
    except:
        return formResponse(500, {"error": "Something went wrong on the server"})