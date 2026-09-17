import streamlit as st
import plotly.express as px
import uuid

from supabase_client import supabase
from ai_analysis import analyze_complaint


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI College Complaint Management System",
    page_icon="🏫",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "role" not in st.session_state:
    st.session_state.role = None

if "full_name" not in st.session_state:
    st.session_state.full_name = None

if "email" not in st.session_state:
    st.session_state.email = None


# =========================================================
# AUTHENTICATION PAGE
# =========================================================

def authentication_page():

    st.title(
        "🏫 AI-Based College Complaint & Maintenance Management System"
    )

    st.write(
        "Smart platform for submitting, analyzing and managing college complaints."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader("🔐 Login")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            key="login_button"
        ):

            if not email or not password:

                st.warning(
                    "⚠️ Please enter email and password."
                )

            else:

                try:

                    result = (
                        supabase.auth.sign_in_with_password(
                            {
                                "email": email,
                                "password": password
                            }
                        )
                    )

                    user = result.user

                    if user:

                        st.session_state.logged_in = True
                        st.session_state.user_id = user.id
                        st.session_state.email = user.email

                        # Get user profile
                        profile_result = (
                            supabase
                            .table("profiles")
                            .select("*")
                            .eq("id", user.id)
                            .execute()
                        )

                        if profile_result.data:

                            profile = profile_result.data[0]

                            st.session_state.full_name = (
                                profile.get(
                                    "full_name",
                                    user.email
                                )
                            )

                            st.session_state.role = (
                                profile.get(
                                    "role",
                                    "student"
                                )
                            )

                        else:

                            st.session_state.full_name = (
                                user.email
                            )

                            st.session_state.role = "student"

                        st.success(
                            "✅ Login successful!"
                        )

                        st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Login failed: {e}"
                    )


    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.subheader(
            "📝 Create Student Account"
        )

        full_name = st.text_input(
            "Full Name",
            key="register_full_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )

        if st.button(
            "Create Account",
            type="primary",
            key="register_button"
        ):

            if not full_name:

                st.warning(
                    "⚠️ Please enter your full name."
                )

            elif not email:

                st.warning(
                    "⚠️ Please enter your email."
                )

            elif not password:

                st.warning(
                    "⚠️ Please enter a password."
                )

            elif len(password) < 6:

                st.error(
                    "❌ Password must contain at least 6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            else:

                try:

                    result = supabase.auth.sign_up(
                        {
                            "email": email,
                            "password": password,
                            "options": {
                                "data": {
                                    "full_name": full_name
                                }
                            }
                        }
                    )

                    if result.user:

                        st.success(
                            "✅ Account created successfully!"
                        )

                        st.info(
                            "Please login using your email and password."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Registration failed: {e}"
                    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def student_dashboard():

    st.title("👨‍🎓 Student Dashboard")

    st.success(
        f"Welcome, {st.session_state.full_name}! 👋"
    )

    st.write(
        f"📧 Email: {st.session_state.email}"
    )

    st.divider()

    menu = st.sidebar.selectbox(
        "📌 Student Menu",
        [
            "🏠 Dashboard",
            "📝 Submit Complaint",
            "🔍 Track Complaint",
            "📋 Complaint History"
        ]
    )


    # =====================================================
    # STUDENT HOME
    # =====================================================

    if menu == "🏠 Dashboard":

        st.header(
            "🏠 Welcome to Student Portal"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                "📝\n\n"
                "**Submit Complaint**\n\n"
                "Report a college problem."
            )

        with col2:

            st.info(
                "🔍\n\n"
                "**Track Complaint**\n\n"
                "Check your complaint status."
            )

        with col3:

            st.info(
                "📋\n\n"
                "**Complaint History**\n\n"
                "View your previous complaints."
            )

        st.divider()

        st.subheader(
            "How the system works"
        )

        st.write(
            """
            1. Submit your complaint.
            2. Upload an image if required.
            3. AI analyzes the complaint.
            4. AI generates a summary.
            5. AI identifies the department.
            6. AI suggests the priority.
            7. Complaint is stored securely.
            8. Admin reviews the complaint.
            9. Admin updates the status.
            10. Student tracks the complaint.
            """
        )


    # =====================================================
    # SUBMIT COMPLAINT
    # =====================================================

    elif menu == "📝 Submit Complaint":

        st.header(
            "📝 Submit a Complaint"
        )

        category = st.selectbox(
            "Complaint Category",
            [
                "Electrical",
                "Plumbing",
                "Classroom",
                "Hostel",
                "Laboratory",
                "Cleanliness",
                "Internet",
                "Furniture",
                "Security",
                "Water Supply",
                "Other"
            ]
        )

        description = st.text_area(
            "Complaint Description",
            placeholder="Describe your problem clearly...",
            height=160
        )

        image = st.file_uploader(
            "📷 Upload Image (Optional)",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        if image:

            st.subheader(
                "🖼️ Image Preview"
            )

            st.image(
                image,
                width=400
            )

        st.divider()

        if st.button(
            "🚀 Submit Complaint",
            type="primary"
        ):

            if not description.strip():

                st.warning(
                    "⚠️ Please enter a complaint description."
                )

            else:

                complaint_id = (
                    "CMP-"
                    + str(uuid.uuid4())[:8].upper()
                )

                image_url = None

                try:

                    # =============================================
                    # IMAGE UPLOAD
                    # =============================================

                    if image:

                        file_extension = (
                            image.name
                            .split(".")[-1]
                            .lower()
                        )

                        file_path = (
                            f"{st.session_state.user_id}/"
                            f"{complaint_id}."
                            f"{file_extension}"
                        )

                        image_bytes = image.getvalue()

                        supabase.storage \
                            .from_("complaint-images") \
                            .upload(
                                file_path,
                                image_bytes,
                                {
                                    "content-type": image.type
                                }
                            )

                        image_url = (
                            supabase.storage
                            .from_("complaint-images")
                            .get_public_url(
                                file_path
                            )
                        )


                    # =============================================
                    # GROQ AI ANALYSIS
                    # =============================================

                    with st.spinner(
                        "🤖 AI is analyzing your complaint..."
                    ):

                        ai_result = analyze_complaint(
                            description
                        )


                    # =============================================
                    # DEFAULT VALUES
                    # =============================================

                    ai_summary = (
                        "AI analysis unavailable."
                    )

                    ai_department = category

                    ai_priority = "Medium"


                    # =============================================
                    # EXTRACT AI RESULT
                    # =============================================

                    for line in ai_result.splitlines():

                        line = line.strip()

                        if line.startswith(
                            "Summary:"
                        ):

                            ai_summary = (
                                line
                                .replace(
                                    "Summary:",
                                    "",
                                    1
                                )
                                .strip()
                            )

                        elif line.startswith(
                            "Department:"
                        ):

                            ai_department = (
                                line
                                .replace(
                                    "Department:",
                                    "",
                                    1
                                )
                                .strip()
                            )

                        elif line.startswith(
                            "Priority:"
                        ):

                            ai_priority = (
                                line
                                .replace(
                                    "Priority:",
                                    "",
                                    1
                                )
                                .strip()
                            )


                    # =============================================
                    # VALIDATE PRIORITY
                    # =============================================

                    valid_priorities = [
                        "Low",
                        "Medium",
                        "High",
                        "Critical"
                    ]

                    if ai_priority not in valid_priorities:

                        ai_priority = "Medium"


                    # =============================================
                    # SAVE COMPLAINT
                    # =============================================

                    (
                        supabase
                        .table("complaints")
                        .insert(
                            {
                                "complaint_id": complaint_id,
                                "student_id": st.session_state.user_id,
                                "category": category,
                                "description": description,
                                "image_url": image_url,
                                "priority": ai_priority,
                                "status": "Pending",
                                "assigned_department": ai_department,
                                "ai_summary": ai_summary
                            }
                        )
                        .execute()
                    )


                    # =============================================
                    # SUCCESS
                    # =============================================

                    st.success(
                        "✅ Complaint submitted successfully!"
                    )

                    st.info(
                        f"🆔 Complaint ID: **{complaint_id}**"
                    )

                    st.warning(
                        "Please save your Complaint ID for tracking."
                    )


                    # =============================================
                    # AI RESULT
                    # =============================================

                    st.divider()

                    st.subheader(
                        "🤖 AI Analysis"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.write(
                            "📝 **Summary**"
                        )

                        st.info(
                            ai_summary
                        )

                    with col2:

                        st.write(
                            "🏢 **Department**"
                        )

                        st.success(
                            ai_department
                        )

                    with col3:

                        st.write(
                            "⚡ **Priority**"
                        )

                        if ai_priority == "Critical":

                            st.error(
                                "🔴 Critical"
                            )

                        elif ai_priority == "High":

                            st.warning(
                                "🟠 High"
                            )

                        elif ai_priority == "Medium":

                            st.info(
                                "🟡 Medium"
                            )

                        else:

                            st.success(
                                "🟢 Low"
                            )


                    if image_url:

                        st.success(
                            "📷 Image uploaded successfully!"
                        )


                except Exception as e:

                    st.error(
                        f"❌ Error submitting complaint: {e}"
                    )


    # =====================================================
    # TRACK COMPLAINT
    # =====================================================

    elif menu == "🔍 Track Complaint":

        st.header(
            "🔍 Track Your Complaint"
        )

        complaint_id = st.text_input(
            "Enter Complaint ID",
            placeholder="Example: CMP-A1B2C3D4"
        )

        if st.button(
            "🔎 Track Complaint",
            type="primary"
        ):

            if not complaint_id:

                st.warning(
                    "⚠️ Please enter Complaint ID."
                )

            else:

                try:

                    result = (
                        supabase
                        .table("complaints")
                        .select("*")
                        .eq(
                            "complaint_id",
                            complaint_id.strip()
                        )
                        .eq(
                            "student_id",
                            st.session_state.user_id
                        )
                        .execute()
                    )

                    complaints = result.data

                    if complaints:

                        complaint = complaints[0]

                        st.success(
                            f"Status: {complaint['status']}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(
                                f"**Complaint ID:** "
                                f"{complaint['complaint_id']}"
                            )

                            st.write(
                                f"**Category:** "
                                f"{complaint['category']}"
                            )

                            st.write(
                                f"**Priority:** "
                                f"{complaint['priority']}"
                            )

                        with col2:

                            department = (
                                complaint.get(
                                    "assigned_department"
                                )
                                or "Not assigned"
                            )

                            st.write(
                                f"**Department:** "
                                f"{department}"
                            )

                            st.write(
                                f"**Status:** "
                                f"{complaint['status']}"
                            )

                        st.divider()

                        st.write(
                            "**Description:**"
                        )

                        st.write(
                            complaint["description"]
                        )

                        if complaint.get(
                            "ai_summary"
                        ):

                            st.subheader(
                                "🤖 AI Summary"
                            )

                            st.info(
                                complaint["ai_summary"]
                            )

                        if complaint.get(
                            "image_url"
                        ):

                            st.subheader(
                                "📷 Complaint Image"
                            )

                            st.image(
                                complaint["image_url"],
                                width=500
                            )

                    else:

                        st.error(
                            "❌ Complaint not found."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Error tracking complaint: {e}"
                    )


    # =====================================================
    # COMPLAINT HISTORY
    # =====================================================

    elif menu == "📋 Complaint History":

        st.header(
            "📋 My Complaint History"
        )

        try:

            result = (
                supabase
                .table("complaints")
                .select("*")
                .eq(
                    "student_id",
                    st.session_state.user_id
                )
                .order(
                    "created_at",
                    desc=True
                )
                .execute()
            )

            complaints = result.data

            if complaints:

                st.success(
                    f"You have submitted "
                    f"{len(complaints)} complaint(s)."
                )

                for complaint in complaints:

                    with st.expander(
                        f"🆔 "
                        f"{complaint['complaint_id']} "
                        f"— "
                        f"{complaint['category']} "
                        f"— "
                        f"{complaint['status']}"
                    ):

                        st.write(
                            f"**Description:** "
                            f"{complaint['description']}"
                        )

                        st.write(
                            f"**Priority:** "
                            f"{complaint['priority']}"
                        )

                        st.write(
                            f"**Status:** "
                            f"{complaint['status']}"
                        )

                        department = (
                            complaint.get(
                                "assigned_department"
                            )
                            or "Not assigned"
                        )

                        st.write(
                            f"**Department:** "
                            f"{department}"
                        )

                        if complaint.get(
                            "ai_summary"
                        ):

                            st.write(
                                "**🤖 AI Summary:**"
                            )

                            st.info(
                                complaint["ai_summary"]
                            )

                        if complaint.get(
                            "image_url"
                        ):

                            st.image(
                                complaint["image_url"],
                                width=400
                            )

            else:

                st.info(
                    "📭 You have not submitted any complaints yet."
                )

        except Exception as e:

            st.error(
                f"❌ Error loading complaints: {e}"
            )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard():

    st.title(
        "👨‍💼 Admin Dashboard"
    )

    st.success(
        f"Welcome, {st.session_state.full_name}! 👋"
    )

    st.divider()


    # =====================================================
    # LOAD COMPLAINTS
    # =====================================================

    try:

        result = (
            supabase
            .table("complaints")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        complaints = result.data

    except Exception as e:

        st.error(
            f"❌ Could not load complaints: {e}"
        )

        complaints = []


    # =====================================================
    # COUNTS
    # =====================================================

    total = len(complaints)

    pending = sum(
        1
        for complaint in complaints
        if complaint.get("status") == "Pending"
    )

    in_progress = sum(
        1
        for complaint in complaints
        if complaint.get("status") == "In Progress"
    )

    resolved = sum(
        1
        for complaint in complaints
        if complaint.get("status") == "Resolved"
    )

    rejected = sum(
        1
        for complaint in complaints
        if complaint.get("status") == "Rejected"
    )


    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Total",
            total
        )

    with col2:

        st.metric(
            "Pending",
            pending
        )

    with col3:

        st.metric(
            "In Progress",
            in_progress
        )

    with col4:

        st.metric(
            "Resolved",
            resolved
        )

    with col5:

        st.metric(
            "Rejected",
            rejected
        )


    # =====================================================
    # ANALYTICS
    # =====================================================

    st.divider()

    st.header(
        "📊 Complaint Analytics"
    )


    if complaints:

        # -------------------------------------------------
        # STATUS COUNTS
        # -------------------------------------------------

        status_counts = {}

        for complaint in complaints:

            status = complaint.get(
                "status",
                "Unknown"
            )

            status_counts[status] = (
                status_counts.get(
                    status,
                    0
                ) + 1
            )


        status_data = {
            "Status": list(
                status_counts.keys()
            ),
            "Complaints": list(
                status_counts.values()
            )
        }


        # -------------------------------------------------
        # PRIORITY COUNTS
        # -------------------------------------------------

        priority_counts = {}

        for complaint in complaints:

            priority = complaint.get(
                "priority",
                "Medium"
            )

            priority_counts[priority] = (
                priority_counts.get(
                    priority,
                    0
                ) + 1
            )


        priority_data = {
            "Priority": list(
                priority_counts.keys()
            ),
            "Complaints": list(
                priority_counts.values()
            )
        }


        # -------------------------------------------------
        # DEPARTMENT COUNTS
        # -------------------------------------------------

        department_counts = {}

        for complaint in complaints:

            department = (
                complaint.get(
                    "assigned_department"
                )
                or "Not Assigned"
            )

            department_counts[department] = (
                department_counts.get(
                    department,
                    0
                ) + 1
            )


        department_data = {
            "Department": list(
                department_counts.keys()
            ),
            "Complaints": list(
                department_counts.values()
            )
        }


        # =================================================
        # STATUS + PRIORITY CHARTS
        # =================================================

        col1, col2 = st.columns(2)


        with col1:

            fig_status = px.pie(
                status_data,
                names="Status",
                values="Complaints",
                title="Complaints by Status"
            )

            st.plotly_chart(
                fig_status,
                use_container_width=True
            )


        with col2:

            fig_priority = px.bar(
                priority_data,
                x="Priority",
                y="Complaints",
                title="Complaints by Priority"
            )

            st.plotly_chart(
                fig_priority,
                use_container_width=True
            )


        # =================================================
        # DEPARTMENT CHART
        # =================================================

        fig_department = px.bar(
            department_data,
            x="Department",
            y="Complaints",
            title="Complaints by Department"
        )

        st.plotly_chart(
            fig_department,
            use_container_width=True
        )


    else:

        st.info(
            "📭 No complaint data available for analytics."
        )


    # =====================================================
    # COMPLAINT MANAGEMENT
    # =====================================================

    st.divider()

    st.header(
        "📋 Complaint Management"
    )


    filter_status = st.selectbox(
        "Filter Complaints",
        [
            "All",
            "Pending",
            "In Progress",
            "Resolved",
            "Rejected"
        ]
    )


    if filter_status == "All":

        filtered_complaints = complaints

    else:

        filtered_complaints = [
            complaint
            for complaint in complaints
            if complaint.get(
                "status"
            ) == filter_status
        ]


    st.write(
        f"Showing **{len(filtered_complaints)}** complaint(s)"
    )


    # =====================================================
    # OPTIONS
    # =====================================================

    departments = [
        "Electrical",
        "Plumbing",
        "Classroom",
        "Hostel",
        "Laboratory",
        "Cleanliness",
        "Internet",
        "Furniture",
        "Security",
        "Water Supply",
        "Other"
    ]


    statuses = [
        "Pending",
        "In Progress",
        "Resolved",
        "Rejected"
    ]


    # =====================================================
    # DISPLAY COMPLAINTS
    # =====================================================

    if filtered_complaints:

        for complaint in filtered_complaints:

            complaint_id = complaint[
                "complaint_id"
            ]


            with st.expander(
                f"🆔 {complaint_id} "
                f"— {complaint['category']} "
                f"— {complaint['status']}"
            ):

                st.write(
                    f"**Student ID:** "
                    f"{complaint['student_id']}"
                )

                st.write(
                    f"**Category:** "
                    f"{complaint['category']}"
                )

                st.write(
                    f"**Description:** "
                    f"{complaint['description']}"
                )


                # =========================================
                # AI ANALYSIS
                # =========================================

                st.subheader(
                    "🤖 AI Analysis"
                )


                if complaint.get(
                    "ai_summary"
                ):

                    st.info(
                        complaint["ai_summary"]
                    )

                else:

                    st.info(
                        "AI summary not available."
                    )


                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        f"**AI Priority:** "
                        f"{complaint['priority']}"
                    )


                with col2:

                    st.write(
                        f"**AI Department:** "
                        f"{complaint.get('assigned_department') or 'Not assigned'}"
                    )


                # =========================================
                # IMAGE
                # =========================================

                if complaint.get(
                    "image_url"
                ):

                    st.subheader(
                        "📷 Complaint Image"
                    )

                    st.image(
                        complaint["image_url"],
                        width=500
                    )


                st.divider()


                # =========================================
                # ADMIN CONTROLS
                # =========================================

                st.subheader(
                    "⚙️ Admin Controls"
                )


                current_department = (
                    complaint.get(
                        "assigned_department"
                    )
                    or complaint.get(
                        "category"
                    )
                )


                if current_department not in departments:

                    current_department = "Other"


                current_status = complaint.get(
                    "status",
                    "Pending"
                )


                if current_status not in statuses:

                    current_status = "Pending"


                col1, col2 = st.columns(2)


                with col1:

                    new_department = st.selectbox(
                        "🏢 Assign Department",
                        departments,
                        index=departments.index(
                            current_department
                        ),
                        key=(
                            f"department_"
                            f"{complaint_id}"
                        )
                    )


                with col2:

                    new_status = st.selectbox(
                        "🔄 Complaint Status",
                        statuses,
                        index=statuses.index(
                            current_status
                        ),
                        key=(
                            f"status_"
                            f"{complaint_id}"
                        )
                    )


                # =========================================
                # SAVE CHANGES
                # =========================================

                if st.button(
                    "💾 Save Changes",
                    key=f"save_{complaint_id}",
                    type="primary"
                ):

                    try:

                        (
                            supabase
                            .table("complaints")
                            .update(
                                {
                                    "assigned_department":
                                        new_department,

                                    "status":
                                        new_status
                                }
                            )
                            .eq(
                                "complaint_id",
                                complaint_id
                            )
                            .execute()
                        )


                        st.success(
                            "✅ Complaint updated successfully!"
                        )


                        st.rerun()


                    except Exception as e:

                        st.error(
                            f"❌ Error updating complaint: {e}"
                        )


    else:

        st.info(
            "📭 No complaints found."
        )


# =========================================================
# LOGOUT
# =========================================================

def logout():

    if st.sidebar.button(
        "🚪 Logout"
    ):

        try:

            supabase.auth.sign_out()

        except Exception:

            pass


        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.role = None
        st.session_state.full_name = None
        st.session_state.email = None

        st.rerun()


# =========================================================
# MAIN APPLICATION
# =========================================================

if not st.session_state.logged_in:

    authentication_page()

else:

    st.sidebar.title(
        "🏫 College Portal"
    )

    st.sidebar.write(
        f"👤 **{st.session_state.full_name}**"
    )

    st.sidebar.write(
        f"Role: **{st.session_state.role}**"
    )

    st.sidebar.divider()

    logout()


    if st.session_state.role == "admin":

        admin_dashboard()

    else:

        student_dashboard()