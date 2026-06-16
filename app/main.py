import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from scraper import scrape_job
from company_research import CompanyResearch

def create_streamlit_app(llm, portfolio, research, clean_text):
    st.title("📧 Cold Mail Generator")

    url_input = st.text_input(
        "Enter a URL:",
        value="https://jobs.weekday.works/nykaa-nykaa---software-development-engineer-ii---java-technologies?utm_source=chatgpt.com&tab=overview"
    )
    sender_name = st.text_input(
        "Your Name",
        value="Mohan"
    )

    company_name = st.text_input(
        "Your Company",
        value="AtliQ"
    )

    designation = st.text_input(
        "Your Designation",
        value="Business Development Executive"
    )
    uploaded_file = st.file_uploader(
        "Upload Portfolio CSV",
        type=["csv"]
    )
    tone = st.selectbox(
        "Email Style",
        [
            "Professional",
            "Technical",
            "Executive"
        ]
    )

    submit_button = st.button("Submit")

    if submit_button:
        try:
            data = clean_text(scrape_job(url_input))

            if uploaded_file:
                portfolio = Portfolio(
                    uploaded_file
                )

            portfolio.load_portfolio()

            jobs = llm.extract_jobs(data)
            if not jobs:
                st.error("No valid job posting found.")
                return

            for job in jobs:

                skills = job.get("skills", [])

                links = []

                if skills:
                    links = portfolio.query_links(skills)


                company_info = research.get_company_info(
                    job.get("company_name", "")
                )
                emails = llm.write_mail(
                    job,
                    links,
                    sender_name,
                    company_name,
                    designation,
                    company_info,
                    tone
                )
                st.subheader("Company Research")
                st.write(company_info)

                st.subheader("Job Summary")
                st.json(job)
                st.subheader("Generated Cold Email")
                st.markdown(emails)
                st.download_button(
                    label="Download Email",
                    data=emails,
                    file_name="cold_email.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    research = CompanyResearch()

    st.set_page_config(
        layout="wide",
        page_title="Cold Email Generator",
        page_icon="📧"
    )

    create_streamlit_app(
        chain,
        portfolio,
        research,
        clean_text
    )