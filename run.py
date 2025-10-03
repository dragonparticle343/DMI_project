from flask import render_template
from app.app import create_app

app = create_app(testing=False)

@app.errorhandler(404)
def not_found(error = None):
    return render_template("./error.html")

if __name__ == "__main__":
    app.run(debug=True)