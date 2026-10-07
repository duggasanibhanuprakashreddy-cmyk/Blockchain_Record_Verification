import streamlit as st
from hashing import generate_hash
from blockchain import Blockchain
from storage import save_blockchain, load_blockchain


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BlockVerify",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# THEME
# ============================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

dark = st.session_state.theme == "dark"


if dark:
    BG = "#050816"
    CARD = "#0d1528"
    CARD2 = "#111c33"
    BORDER = "#263957"
    TEXT = "#f8fafc"
    MUTED = "#94a3b8"
    ACCENT = "#38bdf8"
else:
    BG = "#f5f8fc"
    CARD = "#ffffff"
    CARD2 = "#eef5fc"
    BORDER = "#d7e2ee"
    TEXT = "#0f172a"
    MUTED = "#475569"
    ACCENT = "#0284c7"


# ============================================================
# CSS ONLY
# ============================================================

st.markdown(
    f"""
    <style>

    /* MAIN */

    .stApp {{
        background: {BG};
    }}

    .main .block-container {{
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    /* SIDEBAR */

    section[data-testid="stSidebar"] {{
        background: {CARD};
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT};
    }}

    /* HEADINGS */

    h1, h2, h3, h4 {{
        color: {TEXT} !important;
    }}

    /* NORMAL TEXT */

    p {{
        color: {MUTED};
    }}

    /* METRICS */

    div[data-testid="stMetric"] {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 18px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {MUTED};
    }}

    div[data-testid="stMetricValue"] {{
        color: {TEXT};
    }}

    /* BUTTON */

    .stButton > button {{
        width: 100%;
        min-height: 44px;
        border-radius: 10px;
        border: 1px solid {BORDER};
        background: {CARD2};
        color: {TEXT};
        font-weight: 700;
    }}

    .stButton > button:hover {{
        border-color: {ACCENT};
        color: {ACCENT};
    }}

    /* INPUT */

    input {{
        color: {TEXT} !important;
    }}

    /* CODE */

    code {{
        word-break: break-all;
    }}

    /* EXPANDERS */

    div[data-testid="stExpander"] {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
    }}

    /* HERO */

    .hero {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 25px;
    }}

    .hero-title {{
        font-size: 42px;
        font-weight: 900;
        color: {TEXT};
    }}

    .hero-title span {{
        color: {ACCENT};
    }}

    .hero-subtitle {{
        font-size: 20px;
        color: {MUTED};
        margin-top: 5px;
    }}

    /* FEATURE */

    .feature {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 20px;
        min-height: 150px;
    }}

    .feature:hover {{
        border-color: {ACCENT};
    }}

    /* FOOTER */

    .footer {{
        text-align: center;
        color: {MUTED};
        padding-top: 30px;
        margin-top: 40px;
        border-top: 1px solid {BORDER};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD BLOCKCHAIN
# ============================================================

if "blockchain" not in st.session_state:

    saved_data = load_blockchain()

    if saved_data:
        st.session_state.blockchain = Blockchain.from_data(saved_data)
    else:
        st.session_state.blockchain = Blockchain()


blockchain = st.session_state.blockchain


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # BRANDING
    st.title("⚡ BlockVerify")

    st.caption("Secure Record Verification")

    st.divider()

    # NAVIGATION
    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "➕ Add Record",
            "🔍 Verify Record",
            "📜 Records",
            "⛓️ Blockchain",
            "🛡️ Integrity"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    # THEME

    if dark:

        if st.button("☀️ Light Mode"):
            st.session_state.theme = "light"
            st.rerun()

    else:

        if st.button("🌙 Dark Mode"):
            st.session_state.theme = "dark"
            st.rerun()

    st.divider()

    # STATUS

    total_records = max(
        0,
        len(blockchain.chain) - 1
    )

    valid = blockchain.is_chain_valid()

    if valid:
        st.success("🟢 SYSTEM SECURE")
    else:
        st.error("🔴 SYSTEM COMPROMISED")

    st.metric(
        "Stored Records",
        total_records
    )

    st.divider()

    st.caption("SECURITY STACK")

    st.write("⚡ SHA-256")
    st.write("⛓️ Blockchain")
    st.write("🐍 Python")
    st.write("🖥️ Streamlit")
    st.write("📄 JSON Storage")


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    total_blocks = len(blockchain.chain)

    total_records = max(
        0,
        total_blocks - 1
    )

    valid = blockchain.is_chain_valid()


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        '<div class="hero">',
        unsafe_allow_html=True
    )

    st.markdown(
        "⚡",
        help="BlockVerify"
    )

    st.markdown(
        """
        <div class="hero-title">
        Block<span>Verify</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader(
        "Blockchain-Based Tamper-Proof Record Verification"
    )

    st.write(
        "Secure digital records using cryptographic hashing "
        "and blockchain technology. Detect unauthorized "
        "modifications by comparing record fingerprints."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    if valid:

        st.success(
            "🟢 SYSTEM SECURE — Blockchain integrity has been verified successfully."
        )

    else:

        st.error(
            "🔴 SECURITY ALERT — Blockchain integrity may be compromised."
        )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "⛓️ Total Blocks",
            total_blocks
        )

    with col2:

        st.metric(
            "📄 Records",
            total_records
        )

    with col3:

        st.metric(
            "🔐 Hash Algorithm",
            "SHA-256"
        )

    with col4:

        st.metric(
            "🛡️ Status",
            "VALID" if valid else "INVALID"
        )


    st.divider()


    # --------------------------------------------------------
    # BLOCKCHAIN FLOW
    # --------------------------------------------------------

    st.header("⛓️ Blockchain Flow")

    cols = st.columns(
        len(blockchain.chain)
        if len(blockchain.chain) <= 6
        else 6
    )

    display_blocks = blockchain.chain[:6]

    for i, block in enumerate(display_blocks):

        with cols[i]:

            st.info(
                f"**BLOCK {block.index}**\n\n"
                f"{block.record_id}"
            )

    if len(blockchain.chain) > 6:

        st.caption(
            f"+ {len(blockchain.chain) - 6} more blocks"
        )


    st.divider()


    # --------------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------------

    st.header("⚡ How BlockVerify Works")

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            '<div class="feature">',
            unsafe_allow_html=True
        )

        st.subheader("📄 Record")

        st.write(
            "Enter the digital record details."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            '<div class="feature">',
            unsafe_allow_html=True
        )

        st.subheader("🔐 Hash")

        st.write(
            "Generate a unique SHA-256 fingerprint."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            '<div class="feature">',
            unsafe_allow_html=True
        )

        st.subheader("⛓️ Blockchain")

        st.write(
            "Store the fingerprint inside a linked block."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            '<div class="feature">',
            unsafe_allow_html=True
        )

        st.subheader("🛡️ Verify")

        st.write(
            "Compare hashes to detect tampering."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    st.divider()


    # --------------------------------------------------------
    # SECURITY PRINCIPLE
    # --------------------------------------------------------

    st.header("🎯 Security Principle")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            "✅ Same record → Same hash → VERIFIED"
        )

    with col2:

        st.error(
            "❌ Modified record → Different hash → TAMPERED"
        )


    st.markdown(
        '<div class="footer">'
        '⚡ BlockVerify • Blockchain Record Verification System'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# ADD RECORD
# ============================================================

elif page == "➕ Add Record":

    st.header("➕ Add New Record")

    st.write(
        "Create a secure digital fingerprint and store "
        "the record inside the blockchain."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        record_id = st.text_input(
            "Record ID",
            placeholder="Example: R25EH043"
        )

        student_name = st.text_input(
            "Student Name",
            placeholder="Example: Bhanuprakash Reddy"
        )

    with col2:

        course = st.text_input(
            "Course",
            placeholder="Example: B.Tech AI & DS"
        )

        cgpa = st.text_input(
            "CGPA",
            placeholder="Example: 8.3"
        )

    st.divider()

    if st.button(
        "⚡ Secure & Add Record",
        use_container_width=True
    ):

        if not all([
            record_id,
            student_name,
            course,
            cgpa
        ]):

            st.error(
                "⚠️ Please fill in all fields."
            )

        else:

            record_exists = any(
                block.record_id == record_id
                for block in blockchain.chain
            )

            if record_exists:

                st.warning(
                    "⚠️ Record ID already exists."
                )

            else:

                record_data = (
                    student_name
                    + "|"
                    + course
                    + "|"
                    + cgpa
                )

                record_hash = generate_hash(
                    record_data
                )

                blockchain.add_block(
                    record_id,
                    record_hash
                )

                save_blockchain(
                    blockchain
                )

                st.success(
                    "✅ Record securely added to blockchain!"
                )

                st.subheader(
                    "🔐 Record Fingerprint"
                )

                st.code(
                    record_hash
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Block Number",
                        len(blockchain.chain) - 1
                    )

                with col2:

                    st.metric(
                        "Hash Algorithm",
                        "SHA-256"
                    )


# ============================================================
# VERIFY RECORD
# ============================================================

elif page == "🔍 Verify Record":

    st.header("🔍 Verify Record")

    st.write(
        "Enter the record details. BlockVerify will generate "
        "a new SHA-256 hash and compare it with the stored hash."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        record_id = st.text_input(
            "Record ID",
            placeholder="Example: R25EH043"
        )

        student_name = st.text_input(
            "Student Name",
            placeholder="Example: Bhanuprakash Reddy"
        )

    with col2:

        course = st.text_input(
            "Course",
            placeholder="Example: B.Tech AI & DS"
        )

        cgpa = st.text_input(
            "CGPA",
            placeholder="Example: 8.3"
        )

    st.divider()

    if st.button(
        "🔍 Verify Record",
        use_container_width=True
    ):

        if not all([
            record_id,
            student_name,
            course,
            cgpa
        ]):

            st.error(
                "⚠️ Please fill in all fields."
            )

        else:

            record_data = (
                student_name
                + "|"
                + course
                + "|"
                + cgpa
            )

            generated_hash = generate_hash(
                record_data
            )

            found_record = None

            for block in blockchain.chain:

                if block.record_id == record_id:

                    found_record = block

                    break


            if found_record is None:

                st.warning(
                    "⚠️ Record not found in blockchain."
                )

            else:

                stored_hash = found_record.record_hash

                st.subheader(
                    "🔐 Cryptographic Hash Comparison"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        "### 🔒 Stored Hash"
                    )

                    st.code(
                        stored_hash
                    )

                with col2:

                    st.markdown(
                        "### 🧪 Generated Hash"
                    )

                    st.code(
                        generated_hash
                    )

                st.divider()

                if stored_hash == generated_hash:

                    st.success(
                        "🟢 RECORD VERIFIED"
                    )

                    st.info(
                        "HASH MATCH — The record appears unchanged."
                    )

                else:

                    st.error(
                        "🔴 RECORD TAMPERED"
                    )

                    st.warning(
                        "HASH MISMATCH — The record data has changed."
                    )


# ============================================================
# RECORDS
# ============================================================

elif page == "📜 Records":

    st.header("📜 Stored Records")

    st.write(
        "Records currently registered in the blockchain."
    )

    st.divider()

    records = [
        block
        for block in blockchain.chain
        if block.record_id != "GENESIS"
    ]

    if not records:

        st.info(
            "No records have been added yet."
        )

    else:

        for block in records:

            with st.expander(
                f"📄 {block.record_id}  •  Block {block.index}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Block:** {block.index}"
                    )

                    st.write(
                        f"**Timestamp:** {block.timestamp}"
                    )

                with col2:

                    st.write(
                        "**Record Hash:**"
                    )

                    st.code(
                        block.record_hash
                    )


# ============================================================
# BLOCKCHAIN
# ============================================================

elif page == "⛓️ Blockchain":

    st.header("⛓️ Blockchain Explorer")

    st.write(
        "Explore every block and its cryptographic connections."
    )

    st.divider()

    for block in blockchain.chain:

        with st.expander(
            f"🔗 Block {block.index} | Record: {block.record_id}"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Block Index:** {block.index}"
                )

                st.write(
                    f"**Record ID:** {block.record_id}"
                )

                st.write(
                    f"**Timestamp:** {block.timestamp}"
                )

                st.write(
                    "**Record Hash:**"
                )

                st.code(
                    block.record_hash
                )

            with col2:

                st.write(
                    "**Previous Block Hash:**"
                )

                st.code(
                    block.previous_hash
                )

                st.write(
                    "**Current Block Hash:**"
                )

                st.code(
                    block.current_hash
                )


# ============================================================
# INTEGRITY
# ============================================================

elif page == "🛡️ Integrity":

    st.header("🛡️ Blockchain Integrity")

    st.write(
        "Check whether the blockchain structure and "
        "block hashes are valid."
    )

    st.divider()

    valid = blockchain.is_chain_valid()

    if valid:

        st.success(
            "🟢 BLOCKCHAIN IS VALID"
        )

        st.write(
            "All blocks passed the integrity check."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Blockchain Status",
                "SECURE"
            )

        with col2:

            st.metric(
                "Blocks Checked",
                len(blockchain.chain)
            )

        st.info(
            "Every block's current hash matches its "
            "calculated hash and each block correctly "
            "references the previous block."
        )

    else:

        st.error(
            "🔴 BLOCKCHAIN INTEGRITY COMPROMISED"
        )

        st.write(
            "One or more blocks may have been modified."
        )

        st.metric(
            "Blockchain Status",
            "COMPROMISED"
        )