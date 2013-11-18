from flask import Flask
from os import getcwd
from os.path import dirname, realpath


PWD = getcwd()
MODULE_PATH = dirname(realpath(__file__))

app = Flask(__name__)


@app.route("/")
def main():
    result = """
        Executed from: {0}<br />
        Path for GUI module: {1}
    """.format(PWD, MODULE_PATH)
    return result

if __name__ == "__main__":
    app.run()
