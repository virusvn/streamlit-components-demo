from typing import List, Dict
import logging
import json
import time
import urllib.request
import streamlit as st

# Get an instance of a logger
logger = logging.getLogger(__name__)

JSON_URL = "https://raw.githubusercontent.com/virusvn/streamlit-components-demo/master/streamlit_apps.json"


def st_log(func):
    def log_func(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time() - start
        st.text("Log: the function `%s` tooks %0.4f seconds" % (func.__name__, end))
        return res

    return log_func


def main():
    mode = st.sidebar.selectbox("Show me", ["Streamlit's components", "About"])
    if mode == "About":
        return about()

    components()


@st_log
def components():

    apps = get_apps(JSON_URL)  # type: Dict[str, str]
    logger.info(apps)
    app_names = []

    for name, _ in apps.items():
        app_names.append(name)

    run_app = st.sidebar.selectbox("Select the component", app_names)

    # Fetch the content
    python_code = get_file_content_as_string(apps[run_app])

    # Run the child app
    if python_code is not None:
        try:
            st.header("Result")
            exec(python_code)
            st.header("Source code")
            st.markdown("Link: [Github](%s)" % apps[run_app])
            st.code(python_code)
        except Exception as e:
            st.write("Error occurred when execute [{0}]".format(run_app))
            st.error(str(e))
            logger.error(e)


def about():
    content = get_file_content_as_string(
        "https://raw.githubusercontent.com/virusvn/streamlit-components-demo/master/README.md"
    )
    st.markdown(content)


@st_log
@st.cache
def get_apps(url: str) -> Dict[str, str]:
    json_obj = fetch_json(url)
    apps = {}
    for item in json_obj:
        if item["url"] is not None and item["url"].endswith(".py"):
            # can overwrite if same name
            apps[item["name"]] = item["url"]

    return apps


@st_log
@st.cache
def fetch_json(url: str):
    data = urllib.request.urlopen(url).read()
    output = json.loads(data)
    return output


@st_log
@st.cache
def get_file_content_as_string(url: str):
    data = urllib.request.urlopen(url).read()
    return data.decode("utf-8")


if __name__ == "__main__":
    main()
