import streamlit as st
import pandas as pd
import json
import os

# -----------------------------------
# Page config
# -----------------------------------
st.set_page_config(
    page_title="PHinD me if You Can",
    page_icon="🎓",
    layout="wide"
)

# def inject_global_styles():
#     st.markdown("""
#         <style>

#         /* --- Global font enlargement --- */
#         html, body, [class*="css"]  {
#             font-size: 1.05rem;
#         }

#         /* --- Header Title Styling --- */
#         h1 {
#             font-size: 5.3rem !important;
#             font-weight: 700 !important;
#         }

#         h2, h3 {
#             font-weight: 650 !important;
#         }

#         /* --- Metric card styling --- */
#         div[data-testid="metric-container"] {
#             background: #f8f9ff;
#             padding: 1.2rem;
#             border-radius: 12px;
#             border: 1px solid #e5e7eb;
#             box-shadow: 0 2px 6px rgba(0,0,0,0.05);
#             margin-bottom: 1rem;
#         }

#         div[data-testid="metric-container"] > label {
#             font-size: 0.9rem;
#             color: #4F46E5 !important; 
#             font-weight: 600 !important;
#         }

#         div[data-testid="metric-container"] > div {
#             font-size: 2rem !important;
#             font-weight: 700 !important;
#             color: #111 !important;
#         }

#         /* --- Section headers --- */
#         .section-header {
#             font-size: 1.6rem;
#             font-weight: 700;
#             margin-top: 2.5rem;
#             margin-bottom: 1rem;
#             color: #111827;
#         }

#         /* --- Tables --- */
#         table {
#             font-size: 1.05rem;
#         }

#         /* --- Improve chart spacing --- */
#         .element-container {
#             margin-bottom: 1.8rem;
#         }

#         </style>
#     """, unsafe_allow_html=True)

# inject_global_styles()

# -------------------------
# Initialize state
# -------------------------
if "step" not in st.session_state:
    st.session_state.step = "student"   # "student" -> "professor" -> "results"

if "student_profile" not in st.session_state:
    st.session_state.student_profile = {}

if "professor_profile" not in st.session_state:
    st.session_state.professor_profile = {}

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# -------------------------
# UI helpers: header & stepper
# -------------------------
# def render_header():
#     st.markdown(
#         """
# <div style="text-align:center; margin-bottom: 1.5rem;">

#   <div style="font-size:2.5rem; line-height:1; margin-bottom:0.3rem;">
#     🎓
#   </div>

#   <h1 style="margin-bottom:0.2rem;">
#     <span style="color:#4F46E5;">P</span>
#     <span style="color:#4F46E5;">h</span>in
#     <span style="color:#4F46E5;">D</span> me if You Can
#   </h1>

#   <p style="font-size:1.1rem; color:#555;">
#     Find your perfect PhD advisor match
#   </p>

# </div>
#         """,
#         unsafe_allow_html=True,
#     )

def render_header():
    st.markdown(
        """
<div style="text-align:center; margin-bottom: 1.5rem;">

  <div style="font-size:2.5rem; line-height:1; margin-bottom:0.3rem;">
    🎓
  </div>

  <h1 style="margin-bottom:0.2rem;">
    <span style="color:#4F46E5;">P</span><span style="color:#4F46E5;">h</span>in<span style="color:#4F46E5;">D</span> me if You Can
  </h1>

  <p style="font-size:1.1rem; color:#555;">
    Find your perfect PhD advisor match
  </p>

</div>
        """,
        unsafe_allow_html=True,
    )


# def render_header():
#     st.markdown(
#         """
# <div style="text-align:center; margin-bottom: 1.5rem;">

# <h1 style="margin-bottom:0.2rem; position:relative; display:inline-block;">

# <span style="position:absolute; top:-2.2rem; left:52%; transform:translateX(-50%); font-size:2.3rem; line-height:1;">🎓</span>

# <span style="color:#4F46E5;">P</span><span style="color:#4F46E5;">h</span>in<span style="color:#4F46E5;">D</span> me if You Can
# </h1>

# <p style="font-size:1.1rem; color:#555; margin-top:0.3rem;">
# Find your perfect PhD advisor match
# </p>

# </div>
#         """,
#         unsafe_allow_html=True,
#     )


def render_stepper():
    step = st.session_state.step
    steps = ["student", "professor", "results"]
    labels = {
        "student": "1. Student Profile",
        "professor": "2. Professor Profile",
        "results": "3. Match Insights",
    }

    cols = st.columns(3)
    for i, s in enumerate(steps):
        active = (s == step)
        with cols[i]:
            bg = "#4F46E5" if active else "#E5E7EB"
            fg = "white" if active else "#111827"
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:0.6rem 0.4rem;
                    border-radius:999px;
                    background-color:{bg};
                    color:{fg};
                    font-size:0.9rem;
                    font-weight:600;
                    margin-bottom:0.5rem;
                ">
                    {labels[s]}
                </div>
                """,
                unsafe_allow_html=True,
            )


# -------------------------
# Sidebar info
# -------------------------
with st.sidebar:
    st.markdown("### About PHinD me if You Can")
    st.write(
        "- Helps prospective PhD students explore advisor fit.\n"
        "- Looks at research alignment, publication patterns, and workstyle signals.\n"
        "- Prototype: uses pre-generated LLM analyses for selected student–advisor pairs."
    )
    st.markdown("---")
    st.caption("Built for Claude for Good 2025 · Student Track")


# -------------------------
# Navigation helpers
# -------------------------
def go_to_professor(student_data: dict):
    st.session_state.student_profile = student_data
    st.session_state.step = "professor"
    st.experimental_rerun()


def _normalize_name(name: str) -> str:
    # "Aidong Zhang" -> "aidongzhang"
    # "Sarah Chen"   -> "sarahchen"
    return "".join(name.strip().lower().split())


def go_to_results(prof_data: dict):
    st.session_state.professor_profile = prof_data
    # 🔹 Run background evaluation (currently a file lookup / placeholder)
    analysis = run_background_evaluation(
        st.session_state.student_profile,
        st.session_state.professor_profile,
    )
    st.session_state.analysis_result = analysis
    st.session_state.step = "results"
    st.experimental_rerun()


# -------------------------
# Placeholder / file-based analysis
# -------------------------
def run_background_evaluation(student: dict, professor: dict) -> dict:
    """
    Look up a pre-generated JSON file for this (student, professor) pair.
    If not found, fall back to some default / mock result.
    """

    student_name = _normalize_name(student.get("name", ""))
    prof_name = _normalize_name(professor.get("name", ""))

    # Option A: use file naming convention
    data_dir = "output_files"
    #filename = f"{student_name}__{prof_name}.json"
    fname_prof_student = f"{prof_name}_{student_name}.json"
    print(fname_prof_student)
    filepath = os.path.join(data_dir, fname_prof_student)
    print(filepath)

    if os.path.exists(filepath):
        print('file paisi')
        with open(filepath, "r") as f:
            result = json.load(f)
        return result

    # Optional: Option B – explicit mapping dictionary instead of filename convention
    # MATCH_DB = {
    #     ("farzana_ahmad", "prof_a"): "data/farzana__prof_a.json",
    #     ("farzana_ahmad", "prof_b"): "data/farzana__prof_b.json",
    # }
    # key = (student_name, prof_name)
    # if key in MATCH_DB:
    #     with open(MATCH_DB[key], "r") as f:
    #         return json.load(f)

    # Fallback if no JSON exists (for safety / testing)
    return {
        "overall_match_score": 80,
        "research_fit_score": 0.5,
        "workstyle_fit_score": 0.5,
        "advising_skill_confidence": 0.5,
        "prof_publications_per_year": {
            "2021": 0,
            "2022": 0,
            "2023": 0,
            "2024": 0,
        },
        "student_publications_per_year": {       
            "2021": 0,
            "2022": 0,
            "2023": 0,
            "2024": 0,
        },
        "top_target_venues": [],
        "narrative_research_fit": "No pre-generated analysis was found for this pair.",
        "narrative_workstyle": "Workstyle information is not available.",
        "narrative_overall": (
            "This is a placeholder result. In the full system, an LLM-generated analysis "
            "would appear here based on Google Scholar and lab website signals."
        ),
    }


# -------------------------
# STEP 1: Student page
# -------------------------
if st.session_state.step == "student":
    render_header()
    render_stepper()
    st.markdown("---")

    st.title("Step 1: Student Profile")
    st.write("Fill out your profile. After you submit, you'll go to the professor page.")

    with st.form("student_profile_form"):
        st.subheader("Basic Information")
        student_name = st.text_input("Full Name *")
        student_email = st.text_input("Email (optional)")

        st.subheader("Academic & Research Profile")
        research_interests = st.text_area(
            "Research Interests *",
            placeholder="Example: ML for physics, generative models, uncertainty quantification...",
        )

        # sop = st.text_area(
        #     "Statement of Purpose (Short Version)",
        #     placeholder="Briefly describe your background and what kind of research excites you.",
        #     height=200,
        # )

        sop_file = st.file_uploader(
            "Upload Statement of Purpose (PDF) *",
            type=["pdf"],
        )

        cv_file = st.file_uploader(
            "Upload CV / Resume (PDF preferred) *",
            type=["pdf", "doc", "docx"],
        )

        professional_skills = st.text_area(
            "Professional / Technical Skills *",
            placeholder="Example: Python, PyTorch, statistics, experimental design, etc.",
        )

        work_life_balance = st.selectbox(
            "How important is work–life balance to you? *",
            [
                "Extremely important – I need clear boundaries and reasonable hours",
                "Important – I can work hard, but I need some balance",
                "Flexible – I can handle intense periods when needed",
                "I am okay with a very intense work environment",
            ],
        )

        advising_style = st.selectbox(
            "Preferred advising style *",
            [
                "Very hands-on (frequent check-ins, detailed guidance)",
                "Regular guidance (weekly/bi-weekly meetings, some independence)",
                "Mostly independent (high autonomy, occasional check-ins)",
                "No strong preference",
            ],
        )

        submitted = st.form_submit_button("Submit and go to Professor page →")

    # if submitted:
    #     if not student_name:
    #         st.error("Please enter your name before submitting.")
    #     else:
    #         student_data = {
    #             "name": student_name,
    #             "email": student_email,
    #             "research_interests": research_interests,
    #             "sop_filename": sop_file.name if sop_file is not None else None,
    #             "professional_skills": professional_skills,
    #             "work_life_balance": work_life_balance,
    #             "advising_style": advising_style,
    #             "cv_filename": cv_file.name if cv_file is not None else None,
    #         }
    #         go_to_professor(student_data)

    if submitted:
        missing = []

        if not student_name.strip():
            missing.append("Full Name")
        if not research_interests.strip():
            missing.append("Research Interests")
        if sop_file is None:
            missing.append("Statement of Purpose (PDF)")
        if cv_file is None:
            missing.append("CV / Resume")
        if not professional_skills.strip():
            missing.append("Professional / Technical Skills")
        # work_life_balance and advising_style always have some selection,
        # so we don't need to check them unless you add a blank option.

        if missing:
            st.error("Please fill in the required fields marked with *: " + ", ".join(missing))
        else:
            student_data = {
                "name": student_name,
                "email": student_email,
                "research_interests": research_interests,
                "sop_filename": sop_file.name if sop_file is not None else None,
                "professional_skills": professional_skills,
                "work_life_balance": work_life_balance,
                "advising_style": advising_style,
                "cv_filename": cv_file.name if cv_file is not None else None,
            }
            go_to_professor(student_data)



# -------------------------
# STEP 2: Professor page
# -------------------------
elif st.session_state.step == "professor":
    render_header()
    render_stepper()
    st.markdown("---")

    st.title("Step 2: Professor Profile")
    st.write("Now provide information about the professor you'd like to analyze or match with.")
    student = st.session_state.student_profile
    with st.expander("View student profile summary"):
        st.write(f"**Name:** {student.get('name', '')}")
        st.write("**Research Interests:**")
        st.write(student.get("research_interests", ""))
        st.write("**Professional Skills:**")
        st.write(student.get("professional_skills", ""))
        st.write("**Work–life balance preference:**")
        st.write(student.get("work_life_balance", ""))
        st.write("**Preferred advising style:**")
        st.write(student.get("advising_style", ""))

        sop_name = student.get("sop_filename")
        if sop_name:
            st.write(f"**SOP Uploaded:** {sop_name}")
        else:
            st.write("**SOP Uploaded:** _None_")

        cv_name = student.get("cv_filename")
        if cv_name:
            st.write(f"**CV Uploaded:** {cv_name}")
        else:
            st.write("**CV Uploaded:** _None_")


    
    # with st.expander("View student profile summary"):
    #     st.write(f"**Name:** {student.get('name', '')}")
    #     st.write("**Research Interests:**")
    #     st.write(student.get("research_interests", ""))
    #     st.write("**Professional Skills:**")
    #     st.write(student.get("professional_skills", ""))
    #     st.write("**Work–life balance preference:**")
    #     st.write(student.get("work_life_balance", ""))
    #     st.write("**Preferred advising style:**")
    #     st.write(student.get("advising_style", ""))
    #     cv_name = student.get("cv_filename")
    #     if cv_name:
    #         st.write(f"**CV Uploaded:** {cv_name}")
    #     else:
    #         st.write("**CV Uploaded:** _None_")

    with st.form("professor_profile_form"):
        st.subheader("Professor Information")
        prof_name = st.text_input("Professor Name *")
        prof_affiliation = st.text_input("Affiliation / Department (optional)")

        gs_link = st.text_input(
            "Google Scholar Profile URL *",
            placeholder="https://scholar.google.com/...",
        )

        lab_link = st.text_input(
            "Lab / Personal Website URL *",
            placeholder="https://...",
        )

        prof_submitted = st.form_submit_button("Analyze match →")

    if prof_submitted:

        missing = []

        if not prof_name.strip():
            missing.append("Professor Name")
        if not gs_link.strip():
            missing.append("Google Scholar Profile URL")
        if not lab_link.strip():
            missing.append("Lab / Personal Website URL")

        if missing:
            st.error("Please fill in the required fields marked with *: " + ", ".join(missing))
        else:
            prof_data = {
                "name": prof_name,
                "affiliation": prof_affiliation,
                "google_scholar": gs_link,
                "lab_website": lab_link,
            }
            go_to_results(prof_data)


# -------------------------
# STEP 3: Results page
# -------------------------
elif st.session_state.step == "results":
    render_header()
    render_stepper()
    st.markdown("---")

    st.title("Step 3: Match Evaluation")

    student = st.session_state.student_profile
    professor = st.session_state.professor_profile
    analysis = st.session_state.analysis_result

    # st.subheader("Overall Match Score")
    # st.metric(
    #     label=f"Match: {student.get('name', 'Student')} ↔ {professor.get('name', 'Professor')}",
    #     value=f"{analysis['overall_match_score']} / 100",
    # )

    st.subheader("Overall Match Score")

    # 🎉 Add celebration icon for strong matches (>= 80)
    match_score = analysis["overall_match_score"]
    celebration = " 🎉" if match_score >= 80 else ""

    st.metric(
        label=f"Match: {student.get('name', 'Student')} ↔ {professor.get('name', 'Professor')}{celebration}",
        value=f"{match_score} / 100",
    )

    if match_score >= 80:
        st.success("🎉 This looks like a very strong advisor–student match!")


    # --- Research & workstyle scores ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Research fit", f"{int(analysis['research_fit_score'] * 100)} / 100")
    with col2:
        st.metric("Workstyle fit", f"{int(analysis['workstyle_fit_score'] * 100)} / 100")
    with col3:
        st.metric(
            "Advising skill (confidence)",
            f"{int(analysis['advising_skill_confidence'] * 100)}%",
        )

    st.markdown("---")

    # --- Professor publication rate ---
    st.subheader("Professor publication rate (last 5 years)")
    prof_pub_df = pd.DataFrame(
        {
            "Year": list(analysis["prof_publications_per_year"].keys()),
            "Publications": list(analysis["prof_publications_per_year"].values()),
        }
    )
    st.table(prof_pub_df)
    st.bar_chart(prof_pub_df.set_index("Year"))

    # --- Student publication rate (if any) ---
    st.subheader("Typical student publication output (last 5 years)")
    stud_pub_df = pd.DataFrame(
        {
            "Year": list(analysis["student_publications_per_year"].keys()),
            "Publications": list(analysis["student_publications_per_year"].values()),
        }
    )
    st.table(stud_pub_df)
    st.bar_chart(stud_pub_df.set_index("Year"))

    # --- Top target conferences ---
    st.subheader("Top target conferences / venues")
    venues_df = pd.DataFrame(analysis["top_target_venues"])
    st.table(venues_df)

    # --- Narrative explanations ---
    st.subheader("Interpretation")
    st.markdown("**Research fit**")
    st.write(analysis["narrative_research_fit"])

    st.markdown("**Workstyle & intensity**")
    st.write(analysis["narrative_workstyle"])

    st.markdown("**Overall recommendation**")
    st.write(analysis["narrative_overall"])

    st.info(
        "These insights are meant to help you ask better questions when talking to potential advisors. "
        "They do not replace your own judgment or conversations."
    )

    # Optional: button to restart
    if st.button("Start over"):
        st.session_state.step = "student"
        st.session_state.student_profile = {}
        st.session_state.professor_profile = {}
        st.session_state.analysis_result = None
        st.experimental_rerun()
