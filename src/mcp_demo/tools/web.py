from typing import Dict, Any, List, Optional
import logging
import asyncio
import aiohttp
import feedparser
from bs4 import BeautifulSoup
from collections import defaultdict
from math import log
import string
from urllib.parse import quote_plus
from mcp.server.fastmcp import FastMCP
from mcp_demo.utils.http import make_http_request

# --- Crawler Helper Functions ---
async def fetch_content(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                return await response.text()
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return ""

def clean_content(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        return " ".join(soup.get_text().split())
    except Exception as e:
        logging.error(f"Error cleaning HTML: {e}")
        return ""

# --- Search Engine ---
def normalize(text):
    table = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    return text.translate(table).lower()

class SearchEngine:
    def __init__(self):
        self._index = defaultdict(lambda: defaultdict(int))
        self._documents = {}
        self._titles = {}
        self.k1 = 1.5
        self.b = 0.75

    def index(self, url, content, title=""):
        self._documents[url] = content
        self._titles[url] = title
        for word in normalize(content).split():
            self._index[word][url] += 1
        return True

    @property
    def number_of_documents(self):
        return len(self._documents)

    @property
    def avdl(self):
        if not self._documents:
            return 0
        return sum(len(d) for d in self._documents.values()) / len(self._documents)

    def idf(self, kw):
        N = self.number_of_documents
        n_kw = len(self._index[kw])
        if n_kw == 0:
            return 0
        return log((N - n_kw + 0.5) / (n_kw + 0.5) + 1)

    def bm25(self, kw):
        result = {}
        idf_score = self.idf(kw)
        avdl = self.avdl
        if avdl == 0:
            return {}
        for url, freq in self._index[kw].items():
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * len(self._documents[url]) / avdl)
            result[url] = idf_score * numerator / denominator
        return result

    def search(self, query, top_n=5):
        keywords = normalize(query).split()
        url_scores = defaultdict(float)
        for kw in keywords:
            for url, score in self.bm25(kw).items():
                url_scores[url] += score
        
        top = sorted(url_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [{
            "url": url,
            "title": self._titles.get(url, url),
            "snippet": self._documents[url][:200] + "...",
            "score": score
        } for url, score in top]

# Create a singleton instance
_search_engine = SearchEngine()

def register_web_tools(mcp: FastMCP) -> None:
    """Register web-related tools."""
    
    @mcp.tool()
    def web_search(
        query: str,
        max_results: Optional[int] = 5
    ) -> Dict[str, Any]:
        """
        Search the web using DuckDuckGo and return relevant results.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            Dictionary containing search results or error message
        """
        try:
            # Ensure max_results is within reasonable bounds
            max_results = min(max(1, max_results or 5), 10)
            
            # Construct DuckDuckGo API URL
            encoded_query = quote_plus(query)
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
            
            # Make the request
            response = make_http_request(url)
            
            if response.get("error"):
                return response
                
            # Extract and format results from the proper response structure
            content = response.get("content", {})
            results = []
            
            # Add the instant answer if available
            abstract = content.get("AbstractText")
            if abstract:
                results.append({
                    "title": "Top Result",
                    "snippet": abstract,
                    "url": content.get("AbstractURL", "")
                })
                
            # Add related topics
            related = content.get("RelatedTopics", [])
            for topic in related[:max_results - len(results)]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("FirstURL", "").split("/")[-1].replace("_", " "),
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", "")
                    })
            
            return {
                "error": False,
                "data": {
                    "results": results,
                    "count": len(results),
                    "query": query
                }
            }
            
        except Exception as e:
            logging.error("Error in web_search: %s", str(e))
            return {
                "error": True,
                "message": f"Failed to perform web search: {str(e)}"
            }
    
    @mcp.tool()
    def index_document(
        url: str, 
        content: str,
        title: Optional[str] = ""
    ) -> Dict[str, Any]:
        """
        Index a document in the local search engine.
        
        Args:
            url: URL or unique identifier for the document
            content: Text content of the document
            title: Title of the document (optional)
            
        Returns:
            Status of the indexing operation
        """
        try:
            _search_engine.index(url, content, title)
            return {
                "error": False,
                "message": f"Document indexed successfully: {url}"
            }
        except Exception as e:
            logging.error(f"Error indexing document: {e}")
            return {
                "error": True,
                "message": f"Failed to index document: {str(e)}"
            }
    
    @mcp.tool()
    def index_rss_feed(feed_url: str) -> Dict[str, Any]:
        """
        Crawl and index an RSS feed in the local search engine.
        
        Args:
            feed_url: URL of the RSS feed to crawl and index
            
        Returns:
            Status of the operation and number of documents indexed
        """
        try:
            # This has to be synchronous because MCP tools don't support async
            feed = feedparser.parse(feed_url)
            indexed = 0
            
            for entry in feed.entries:
                url = entry.link
                # Use a synchronous HTTP request for content
                response = make_http_request(url)
                if not response.get("error"):
                    content = clean_content(str(response.get("content", "")))
                    title = entry.get("title", "")
                    _search_engine.index(url, content, title)
                    indexed += 1
            
            return {
                "error": False,
                "message": f"Indexed {indexed} documents from {feed_url}",
                "data": {
                    "indexed_count": indexed,
                    "feed_url": feed_url
                }
            }
        except Exception as e:
            logging.error(f"Error indexing RSS feed: {e}")
            return {
                "error": True,
                "message": f"Failed to index RSS feed: {str(e)}"
            }
    
    @mcp.tool()
    def local_search(
        query: str,
        max_results: Optional[int] = 5
    ) -> Dict[str, Any]:
        """
        Search the local index for documents matching the query.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            Dictionary containing search results
        """
        try:
            max_results = min(max(1, max_results or 5), 10)
            results = _search_engine.search(query, max_results)
            
            return {
                "error": False,
                "data": {
                    "results": results,
                    "count": len(results),
                    "query": query,
                    "total_documents": _search_engine.number_of_documents
                }
            }
        except Exception as e:
            logging.error(f"Error performing local search: {e}")
            return {
                "error": True,
                "message": f"Failed to perform local search: {str(e)}"
            } 