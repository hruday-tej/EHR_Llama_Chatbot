import os
from streamlit_interface.streamlit import StreamlitInterface

if __name__ == "__main__":

    os.environ["http_proxy"] = "http://proxe.shands.ufl.edu:3128"
    os.environ["https_proxy"] = "http://proxe.shands.ufl.edu:3128"

    # Verify the environment variables are set
    print("http_proxy:", os.environ.get("http_proxy"))
    print("https_proxy:", os.environ.get("https_proxy"))
    # core_module = Core()
    st = StreamlitInterface()
    st.start_chat()

    # user_query = input("enter the query you want")
    # core_module.core_impl(user_query)
