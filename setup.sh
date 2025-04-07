python -m venv .venv

if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
    source .venv/bin/activate
elif [ "$(uname)" == "CYGWIN" ] || [ "$(uname)" == "MINGW" ] || [ "$(uname)" == "MSYS" ]; then
    .venv\Scripts\activate
fi

pip install -r requirements.txt