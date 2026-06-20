import streamlit as st
from datetime import datetime, timedelta

USERS = {
    "admin": "admin123",
    "manager": "manager123"
}

SESSION_TIMEOUT = 10 # minutes

###login
def login(username, password):

    if USERS.get(username) == password:

        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["expiry"] = (
            datetime.now() +
            timedelta(minutes=SESSION_TIMEOUT)
        )

        return True

    return False


#logout
def logout():

    st.session_state.clear()

#authentication
def is_authenticated():

    if not st.session_state.get("logged_in"):
        return False
    expiry = st.session_state.get("expiry")

    if expiry is None:
        return False

    if datetime.now() > expiry:

        logout()
        return False

    return True