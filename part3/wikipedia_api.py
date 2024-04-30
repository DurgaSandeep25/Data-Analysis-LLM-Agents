# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

from typing import Optional, Type
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

import wikipedia

class WikipediaSearchInput(BaseModel):
    query: str = Field(description="should be a query to search in the wikipedia")


class WikipediaSearchTool(BaseTool):
    name = "wikipedia_search"
    description = "useful for when you need to answer questions about facts, location or current events"
    args_schema: Type[BaseModel] = WikipediaSearchInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        # retriever = WikipediaRetriever(top_k_results=1)
        # docs = retriever.get_relevant_documents(query=query)
        try:
            
            search_results = wikipedia.search(query)

            # Get the page title from the search results
            
            res = ""
            for i in range(min(5, len(search_results))):
                page_title = search_results[i]

                # Get the Wikipedia page
                page = wikipedia.page(page_title)
                res += " ".join(page.content.split(" ")[:50])
        except:
            res = "Error fetching data through wikipedia, lets try another tool"
        return res

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")