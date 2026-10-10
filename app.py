import streamlit as st

from bank import Bank


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MyBank",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.7;
        margin-bottom: 30px;
    }

    .balance-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 20px;
    }

    .balance-label {
        font-size: 15px;
        opacity: 0.7;
    }

    .balance-value {
        font-size: 32px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None


# ============================================================
# LOGIN FUNCTION
# ============================================================

def login_user(account_no, pin):

    user = Bank.find_user(
        account_no,
        pin
    )

    if user:

        st.session_state.logged_in = True
        st.session_state.account = user

        return True

    return False


# ============================================================
# LOGOUT FUNCTION
# ============================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.account = None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏦 MyBank")

if st.session_state.logged_in:

    st.sidebar.success(
        f"Welcome, {st.session_state.account['name']}"
    )

    page = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Deposit Money",
            "Withdraw Money",
            "Account Details",
            "Update Details",
            "Delete Account"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        logout()

        st.rerun()

else:

    page = st.sidebar.radio(
        "Menu",
        [
            "Home",
            "Create Account",
            "Login"
        ]
    )


# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        '<div class="main-title">🏦 Welcome to MyBank</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Simple Python Banking System powered by Streamlit'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            ### 👤 Create Account

            Open a new bank account
            quickly and easily.
            """
        )

    with col2:

        st.success(
            """
            ### 💰 Manage Money

            Deposit and withdraw
            money from your account.
            """
        )

    with col3:

        st.warning(
            """
            ### 🔐 Secure Access

            Access your account using
            your account number and PIN.
            """
        )


# ============================================================
# CREATE ACCOUNT
# ============================================================

elif page == "Create Account":

    st.title("🆕 Create New Account")

    st.write(
        "Enter your information below to create an account."
    )

    with st.form("create_account_form"):

        name = st.text_input(
            "Full Name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        email = st.text_input(
            "Email"
        )

        pin = st.text_input(
            "4-Digit PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

    if submitted:

        if not pin.isdigit():

            st.error(
                "PIN must contain only numbers."
            )

        elif len(pin) != 4:

            st.error(
                "PIN must be exactly 4 digits."
            )

        else:

            success, message, account = Bank.create_account(
                name,
                int(age),
                email,
                int(pin)
            )

            if success:

                st.success(message)

                st.balloons()

                st.subheader(
                    "🎉 Account Created Successfully"
                )

                st.write(
                    f"**Name:** {account['name']}"
                )

                st.write(
                    f"**Email:** {account['email']}"
                )

                st.write(
                    f"**Account Number:** "
                    f"`{account['accountNo.']}`"
                )

                st.write(
                    "**Initial Balance:** ₹0"
                )

                st.info(
                    "⚠️ Please save your account number. "
                    "You will need it to login."
                )

            else:

                st.error(message)


# ============================================================
# LOGIN
# ============================================================

elif page == "Login":

    st.title("🔐 Login")

    st.write(
        "Enter your account number and PIN."
    )

    with st.form("login_form"):

        account_no = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if submitted:

        if not pin.isdigit():

            st.error(
                "PIN must contain only numbers."
            )

        elif login_user(
            account_no.strip(),
            int(pin)
        ):

            st.success(
                "Login successful!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid account number or PIN."
            )


# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    account = st.session_state.account

    st.title("📊 Dashboard")

    st.write(
        f"Welcome back, **{account['name']}**!"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Current Balance",
            f"₹{account['balance']:,.2f}"
        )

    with col2:

        st.metric(
            "Age",
            account["age"]
        )

    with col3:

        st.metric(
            "Account Status",
            "Active"
        )

    st.divider()

    st.subheader("Account Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Name:** {account['name']}"
        )

        st.write(
            f"**Email:** {account['email']}"
        )

    with col2:

        st.write(
            f"**Account Number:** "
            f"`{account['accountNo.']}`"
        )

        st.write(
            f"**Balance:** "
            f"₹{account['balance']:,.2f}"
        )


# ============================================================
# DEPOSIT
# ============================================================

elif page == "Deposit Money":

    st.title("💰 Deposit Money")

    account = st.session_state.account

    st.metric(
        "Current Balance",
        f"₹{account['balance']:,.2f}"
    )

    st.divider()

    with st.form("deposit_form"):

        amount = st.number_input(
            "Enter amount",
            min_value=1.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Deposit Money",
            use_container_width=True
        )

    if submitted:

        success, message, balance = Bank.deposit(
            account["accountNo."],
            account["pin"],
            amount
        )

        if success:

            st.session_state.account = Bank.find_user(
                account["accountNo."],
                account["pin"]
            )

            st.success(message)

            st.metric(
                "New Balance",
                f"₹{balance:,.2f}"
            )

        else:

            st.error(message)


# ============================================================
# WITHDRAW
# ============================================================

elif page == "Withdraw Money":

    st.title("💸 Withdraw Money")

    account = st.session_state.account

    st.metric(
        "Available Balance",
        f"₹{account['balance']:,.2f}"
    )

    st.divider()

    with st.form("withdraw_form"):

        amount = st.number_input(
            "Enter amount",
            min_value=1.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Withdraw Money",
            use_container_width=True
        )

    if submitted:

        success, message, balance = Bank.withdraw(
            account["accountNo."],
            account["pin"],
            amount
        )

        if success:

            st.session_state.account = Bank.find_user(
                account["accountNo."],
                account["pin"]
            )

            st.success(message)

            st.metric(
                "New Balance",
                f"₹{balance:,.2f}"
            )

        else:

            st.error(message)


# ============================================================
# ACCOUNT DETAILS
# ============================================================

elif page == "Account Details":

    st.title("👤 Account Details")

    account = st.session_state.account

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Personal Information")

        st.write(
            f"**Name:** {account['name']}"
        )

        st.write(
            f"**Age:** {account['age']}"
        )

        st.write(
            f"**Email:** {account['email']}"
        )

    with col2:

        st.subheader("Bank Information")

        st.write(
            f"**Account Number:** "
            f"`{account['accountNo.']}`"
        )

        st.write(
            "**PIN:** `****`"
        )

        st.write(
            f"**Balance:** "
            f"₹{account['balance']:,.2f}"
        )


# ============================================================
# UPDATE ACCOUNT
# ============================================================

elif page == "Update Details":

    st.title("✏️ Update Account Details")

    account = st.session_state.account

    with st.form("update_form"):

        name = st.text_input(
            "Name",
            value=account["name"]
        )

        email = st.text_input(
            "Email",
            value=account["email"]
        )

        new_pin = st.text_input(
            "New PIN (leave empty to keep current PIN)",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Update Account",
            use_container_width=True
        )

    if submitted:

        pin_value = None

        if new_pin:

            if (
                not new_pin.isdigit()
                or len(new_pin) != 4
            ):

                st.error(
                    "New PIN must contain exactly 4 digits."
                )

                st.stop()

            pin_value = int(new_pin)

        success, message, updated_user = Bank.update_account(
            account["accountNo."],
            account["pin"],
            name,
            email,
            pin_value
        )

        if success:

            st.session_state.account = updated_user

            st.success(message)

            st.rerun()

        else:

            st.error(message)


# ============================================================
# DELETE ACCOUNT
# ============================================================

elif page == "Delete Account":

    st.title("🗑️ Delete Account")

    account = st.session_state.account

    st.warning(
        """
        ⚠️ **Warning**

        Deleting your account is permanent.
        Your account and balance will be deleted.
        This action cannot be undone.
        """
    )

    confirm = st.checkbox(
        "I understand that I want to permanently delete my account."
    )

    if confirm:

        if st.button(
            "Delete My Account",
            type="primary",
            use_container_width=True
        ):

            success, message = Bank.delete_account(
                account["accountNo."],
                account["pin"]
            )

            if success:

                logout()

                st.success(message)

                st.rerun()

            else:

                st.error(message)
