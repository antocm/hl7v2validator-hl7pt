from flask import (
    render_template,
    redirect,
    request,
    jsonify,
    send_from_directory,
    abort,
    session,
    g,
)
from flask_babel import gettext, get_locale
import os
from hl7validator.api import hl7validatorapi, from_hl7_to_df, highlight_message, build_tree_structure
from hl7validator import app
from hl7validator.__version__ import __version__

# Version is now managed centrally in __version__.py and pyproject.toml
VERSION = __version__


@app.before_request
def before_request():
    """Store current language in g for templates"""
    g.current_lang = str(get_locale())


@app.route("/set_language/<language>")
def set_language(language):
    """Allow users to manually select language"""
    if language in app.config['LANGUAGES']:
        session['language'] = language
    # Redirect to the referrer or home page
    return redirect(request.referrer or '/')


@app.route("/docs", methods=["GET"])
def redirection():
    return redirect("/apidocs")


@app.route("/", methods=["GET", "POST"])
@app.route("/<lang>", methods=["GET", "POST"])
@app.route("/hl7validator", methods=["GET", "POST"])
@app.route("/<lang>/hl7validator", methods=["GET", "POST"])
def home(lang=None):
    # Set language from URL if provided
    if lang and lang in app.config['LANGUAGES']:
        session['language'] = lang

    parsed_message = None
    tree_structure = None
    if request.method == "POST":
        req = request.form.get("options")
        msg = request.form.get("msg")
        validation_level = request.form.get("validation_level", "tolerant")
        if not msg:
            return render_template("hl7validatorhome.html", version=VERSION)
        elif req == "hl7v2":
            validation = hl7validatorapi(request.form.get("msg"), validation_level=validation_level)
            print(validation)
            if validation["hl7version"]:
                parsed_message, validation = highlight_message(msg, validation)
                tree_structure, validation = build_tree_structure(msg, validation)
            details = sorted(validation["details"], key=lambda d: list(d.values())[0])
            warnings = validation.get("warnings", [])

            # Translate validation message
            status_message = gettext(validation["message"])

            return render_template(
                "hl7validatorhome.html",
                title=status_message,
                msg=msg,
                result=details,
                warnings=warnings,
                version=VERSION,
                hl7version=validation["hl7version"],
                parsed=parsed_message,
                tree=tree_structure,
            )

        elif req == "converter":
            return send_from_directory(
                os.getcwd(), from_hl7_to_df(request.form.get("msg")), as_attachment=True
            )
    else:
        return render_template("hl7validatorhome.html", version=VERSION)


@app.route("/api/hl7/v1/validate/", methods=["POST"])
def hl7v2validatorapi():
    """
    file: docs/v2.yml
    """

    data = request.json["data"]
    validation_level = request.json.get("validation_level", "tolerant")

    return jsonify(hl7validatorapi(data, validation_level=validation_level))


@app.route("/api/hl7/v1/convert/", methods=["POST"])
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
