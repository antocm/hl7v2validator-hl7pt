from flask import (
    render_template,
    redirect,
    request,
    jsonify,
    send_from_directory,
    send_file,
)
import os
from message_validation_logger.api import (
    hl7validatorapi2,
    from_hl7_to_df,
)
from message_validation_logger import app

# http://flask.pocoo.org/docs/1.0/
VERSION = "0.0.1"


@app.route("/docs", methods=["GET"])
def redirection():
    return redirect("/apidocs")


@app.route("/", methods=["GET", "POST"])
@app.route("/hl7validator", methods=["GET", "POST"])
def home():
    if request.method == "POST" and request.form.get("options") == "hl7v2":
        validation = hl7validatorapi2(request.form.get("msg"))
        # print(validation)
        return render_template(
            "hl7validatorhome.html",
            msg=validation["message"],
            result=validation["details"],
            version=VERSION,
        )

    if request.method == "POST" and request.form.get("options") == "converter":
        return send_from_directory(
            os.getcwd(), from_hl7_to_df(request.form.get("msg")), as_attachment=True
        )
    return render_template("hl7validatorhome.html", version=VERSION)


@app.route("/hl7validator/api/v1.0/validate/", methods=["POST"])
def hl7v2validatorapi():
    """
    file: docs/v2.yml
    """
    data = request.json["data"]
    return jsonify(hl7validatorapi2(data))


@app.route("/hl7/api/v1.0/convert/", methods=["POST"])
def from_hl7_to_df_converter():
    """
    file: docs/converter.yml
    """
    data = request.json["data"]
    try:
        return send_from_directory(
            os.getcwd(), from_hl7_to_df(data), as_attachment=True
        )
    except FileNotFoundError:
        abort(404)
