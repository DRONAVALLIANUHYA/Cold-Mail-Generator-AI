import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()


class Chain:

    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):

        prompt_extract = PromptTemplate.from_template(
            """
### JOB PAGE CONTENT

{page_data}

### INSTRUCTION

Extract the PRIMARY job posting from the page.

Ignore:
- menus
- navigation bars
- advertisements
- footers
- competitions
- hackathons
- scholarships
- unrelated content

Return ONLY valid JSON in this format:

[
    {{
        "company_name": "",
        "role": "",
        "experience": "",
        "skills": [],
        "responsibilities": "",
        "description": ""
    }}
]

Do not return explanations.
Do not return markdown.
Return only JSON.
"""
        )

        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke(
            {"page_data": cleaned_text}
        )

        try:
            json_parser = JsonOutputParser()
            parsed = json_parser.parse(res.content)

        except OutputParserException:
            raise OutputParserException(
                f"Unable to parse jobs.\n\nLLM Output:\n{res.content}"
            )

        return parsed if isinstance(parsed, list) else [parsed]

    def research_company(self, company_name):

        prompt = PromptTemplate.from_template(
            """
            Tell me about {company_name}.

            Give:
            - What the company does
            - Main products/services
            - Technology/business focus

            Keep it under 100 words.
            """
        )

        chain = prompt | self.llm

        res = chain.invoke(
            {
                "company_name": company_name
            }
        )

        return res.content

    def write_mail(
            self,
            job,
            links,
            sender_name,
            company_name,
            designation,
            company_info,
            tone
    ):

        prompt_email = PromptTemplate.from_template(
            """
            ### TARGET COMPANY
    
            {target_company}
    
            ### COMPANY RESEARCH
    
            {company_info}
    
            ### JOB DETAILS
    
            {job_description}
    
            ### RELEVANT PORTFOLIO PROJECTS
    
            {link_list}
    
            ### SENDER INFORMATION
    
            Name: {sender_name}
            Designation: {designation}
            Company: {sender_company}
    
            ### INSTRUCTION
    
            Generate ONE highly personalized cold email.
    
            Email Style:
            {tone}
    
            Guidelines:
    
            If tone is Professional:
            - Use a formal consulting tone.
            - Focus on relationship building.
            - Highlight relevant experience and capabilities.
    
            If tone is Technical:
            - Focus on architecture, engineering expertise,
              scalability, cloud technologies and system design.
            - Mention technical strengths and relevant projects.
    
            If tone is Executive:
            - Focus on business outcomes.
            - Emphasize ROI, efficiency, cost optimization,
              scalability and digital transformation.
    
            Requirements:
    
            - Create a compelling subject line.
            - Mention the target company.
            - Reference the job role.
            - Incorporate relevant skills and responsibilities.
            - Use relevant portfolio projects where appropriate.
            - Explain how {sender_company} can help.
            - Keep the email concise (200-250 words maximum).
            - End with a clear call-to-action.
    
            Format:
    
            Subject: <subject line>
    
            <email body>
    
            Best Regards,
            {sender_name}
            {designation}
            {sender_company}
    
            Return only the final email.
            """
        )

        chain_email = prompt_email | self.llm

        res = chain_email.invoke(
            {
                "target_company": job.get(
                    "company_name",
                    "Hiring Team"
                ),
                "company_research": company_info,
                "job_description": str(job),
                "link_list": links,
                "company_info": company_info,
                "sender_name": sender_name,
                "designation": designation,
                "sender_company": company_name,
                "tone": tone
            }
        )

        return res.content