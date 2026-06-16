from langchain_community.utilities import WikipediaAPIWrapper


class CompanyResearch:

    def get_company_info(self, company_name):

        try:
            wiki = WikipediaAPIWrapper()

            result = wiki.run(company_name)

            return result[:1500]

        except:
            return ""