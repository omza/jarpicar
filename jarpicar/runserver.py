"""
This script runs the jarpicar application using a development server.
"""

#from os import environ
from jarpicar import app

# Main
# --------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', debug=True, threaded=True)

if __name__ == "__main__":
    main()

# EOF
# --------------------------------------------------------------
