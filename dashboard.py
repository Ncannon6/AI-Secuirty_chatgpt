
import streamlit as st
import pandas as pd
from Ai_assitant import analyze_threat
st.set_page_config(page_title="AI Security Copilot", layout="wide")
from rag_system import search_knowledge

st.title("AI Security Copilot")
st.write("Cybersecurity Threat Detection Dashboard")


uploaded_file = st.file_uploader(
    "Upload a security log file",
    type=["txt"]
)

if uploaded_file is not None:
    security_logs = uploaded_file.getvalue().decode("utf-8").splitlines()

    failed_attempts = {}

    for log in security_logs:
        if " - " in log and "LOGIN FAILED" in log:
            ip = log.split(" - ")[0]

            if ip in failed_attempts:
                failed_attempts[ip] += 1
            else:
                failed_attempts[ip] = 1

    results = []

    for ip in failed_attempts:
        attempts = failed_attempts[ip]

        if attempts >= 10:
            severity = "CRITICAL"
        elif attempts >= 5:
            severity = "HIGH"
        elif attempts >= 3:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        results.append({
            "IP Address": ip,
            "Failed Attempts": attempts,
            "Severity": severity
        })

    if results:
        df = pd.DataFrame(results)

        st.subheader("Threat Detection Results")
        st.dataframe(df)

        st.subheader("Failed Login Attempts")
        st.bar_chart(df.set_index("IP Address")["Failed Attempts"])

        st.download_button(
            "Download Incident Report",
            data=df.to_csv(index=False),
            file_name="incident_report.csv",
            mime="text/csv"
        )

        st.subheader("AI Threat Analysis")

        selected_ip = st.selectbox(
            "Select an IP address to analyze",
            df["IP Address"]
        )

        if st.button("Analyze Threat with AI"):
            selected_alert = df[df["IP Address"] == selected_ip].iloc[0]

            with st.spinner("AI is analyzing the threat..."):
                try:
                    analysis = analyze_threat(
                        selected_alert["IP Address"],
                        int(selected_alert["Failed Attempts"]),
                        selected_alert["Severity"]
                    )

                    st.write(analysis)

                    with st.expander("View Retrieved Security Documentation"):
                        source = search_knowledge(
                            "How should an analyst investigate repeated failed logins?"
                        )
                        st.write(source)





                except Exception as error:

                    st.error("AI analysis failed.")

                    st.write("Error type:", type(error).__name__)

                    if isinstance(error, NameError):

                        st.write("Problem:", str(error))

                    else:

                        st.write("HTTP status:", getattr(error, "status_code", "Not available"))



    else:
        st.success("No failed login attempts detected.")
