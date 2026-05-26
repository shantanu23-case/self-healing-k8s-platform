from flask import Flask
import requests
import time

app = Flask(__name__)

TOKEN = open(
    "/var/run/secrets/kubernetes.io/serviceaccount/token"
).read()

CA = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/strategic-merge-patch+json"
}

@app.route("/heal", methods=["POST"])
def heal():

    url = (
        "https://kubernetes.default.svc"
        "/apis/apps/v1/namespaces/demo/deployments/selfheal-demo"
    )

    payload = {
        "spec": {
            "template": {
                "metadata": {
                    "annotations": {
                        "restart-trigger": str(time.time())
                    }
                }
            }
        }
    }

    r = requests.patch(
        url,
        headers=HEADERS,
        json=payload,
        verify=CA
    )

    return r.text, r.status_code


app.run(host="0.0.0.0", port=5000)