from pathlib import Path
import pandas as pd
import chromadb
import uuid


class Portfolio:

    def __init__(self, file_path=None):

        if file_path:
            self.data = pd.read_csv(file_path)

        else:
            self.file_path = (
                    Path(__file__).parent
                    / "resource"
                    / "my_portfolio.csv"
            )

            self.data = pd.read_csv(
                self.file_path
            )

        # Store vector database in project root
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")

        self.collection = self.chroma_client.get_or_create_collection(
            name="portfolio"
        )

    def load_portfolio(self):
        # Load data only once
        if self.collection.count() == 0:

            for _, row in self.data.iterrows():

                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"Links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

            print("Portfolio loaded into ChromaDB.")

    def query_links(self, skills):

        if not skills:
            return []

        if isinstance(skills, list):
            skills = [", ".join(skills)]

        results = self.collection.query(
            query_texts=skills,
            n_results=2
        )

        return results.get("metadatas", [])

    def calculate_match_score(self, skills):

        if not skills:
            return 0

        portfolio_text = " ".join(
            self.data["Techstack"].astype(str).tolist()
        ).lower()

        matched = 0

        for skill in skills:
            if skill.lower() in portfolio_text:
                matched += 1

        return round((matched / len(skills)) * 100)