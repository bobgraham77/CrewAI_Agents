import streamlit as st
import os
from utils import rnd_id
from crewai_tools import CodeInterpreterTool,ScrapeElementFromWebsiteTool,TXTSearchTool,SeleniumScrapingTool,PGSearchTool,PDFSearchTool,MDXSearchTool,JSONSearchTool,GithubSearchTool,EXASearchTool,DOCXSearchTool,CSVSearchTool,ScrapeWebsiteTool, FileReadTool, DirectorySearchTool, DirectoryReadTool, CodeDocsSearchTool, YoutubeVideoSearchTool,SerperDevTool,YoutubeChannelSearchTool,WebsiteSearchTool
from custom_tools import CustomApiTool,CustomFileWriteTool,CustomCodeInterpreterTool
from langchain_community.tools import YahooFinanceNewsTool
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, Union, List

class MyTool(ABC):
    def __init__(self, tool_id, name, description, parameters, **kwargs):
        self.tool_id = tool_id or rnd_id()
        self.name = name
        self.description = description
        self.parameters = kwargs
        self.parameters_metadata = parameters

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, **kwargs):
        self.parameters.update(kwargs)

    def get_parameter_names(self):
        return list(self.parameters_metadata.keys())

    def is_parameter_mandatory(self, param_name):
        return self.parameters_metadata.get(param_name, {}).get('mandatory', False)

    def is_valid(self,show_warning=False):
        for param_name, metadata in self.parameters_metadata.items():
            if metadata['mandatory'] and not self.parameters.get(param_name):
                if show_warning:
                    st.warning(f"Parameter '{param_name}' is mandatory for tool '{self.name}'")
                return False
        return True

    @abstractmethod
    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        """Create and return a tool instance."""
        pass

class MyScrapeWebsiteTool(MyTool):
    def __init__(self, tool_id=None, website_url=None):
        parameters = {
            'website_url': {'mandatory': False}
        }
        super().__init__(tool_id, 'ScrapeWebsiteTool', "A tool that can be used to read website content.", parameters, website_url=website_url)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return ScrapeWebsiteTool(self.parameters.get('website_url') if self.parameters.get('website_url') else None)

class MyFileReadTool(MyTool):
    def __init__(self, tool_id=None, file_path=None):
        parameters = {
            'file_path': {'mandatory': False}
        }
        super().__init__(tool_id, 'FileReadTool', "A tool that can be used to read a file's content.", parameters, file_path=file_path)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return FileReadTool(self.parameters.get('file_path') if self.parameters.get('file_path') else None)

class MyDirectorySearchTool(MyTool):
    def __init__(self, tool_id=None, directory=None):
        parameters = {
            'directory': {'mandatory': False}
        }
        super().__init__(tool_id, 'DirectorySearchTool', "A tool that can be used to semantic search a query from a directory's content.", parameters, directory_path=directory)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return DirectorySearchTool(self.parameters.get('directory') if self.parameters.get('directory') else None)

class MyDirectoryReadTool(MyTool):
    def __init__(self, tool_id=None, directory_contents=None):
        parameters = {
            'directory_contents': {'mandatory': True}
        }
        super().__init__(tool_id, 'DirectoryReadTool', "Use the tool to list the contents of the specified directory", parameters, directory_contents=directory_contents)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return DirectoryReadTool(self.parameters.get('directory_contents'))

class MyCodeDocsSearchTool(MyTool):
    def __init__(self, tool_id=None, code_docs=None):
        parameters = {
            'code_docs': {'mandatory': False}
        }
        super().__init__(tool_id, 'CodeDocsSearchTool', "A tool that can be used to search through code documentation.", parameters, code_docs=code_docs)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return CodeDocsSearchTool(self.parameters.get('code_docs') if self.parameters.get('code_docs') else None)

class MyYoutubeVideoSearchTool(MyTool):
    def __init__(self, tool_id=None, youtube_video_url=None):
        parameters = {
            'youtube_video_url': {'mandatory': False}
        }
        super().__init__(tool_id, 'YoutubeVideoSearchTool', "A tool that can be used to semantic search a query from a Youtube Video content.", parameters, youtube_video_url=youtube_video_url)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return YoutubeVideoSearchTool(self.parameters.get('youtube_video_url') if self.parameters.get('youtube_video_url') else None)

class MySerperDevTool(MyTool):
    def __init__(self, tool_id=None, SERPER_API_KEY: Optional[str] = None):
        parameters = {
            'SERPER_API_KEY': SERPER_API_KEY
        }
        super().__init__(tool_id, 'SerperDevTool', "A tool that can be used to search the internet with a search_query", parameters)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        api_key = self.parameters.get('SERPER_API_KEY')
        if api_key:
            os.environ['SERPER_API_KEY'] = api_key
        return SerperDevTool()

class MyYoutubeChannelSearchTool(MyTool):
    def __init__(self, tool_id=None, youtube_channel_handle=None):
        parameters = {
            'youtube_channel_handle': {'mandatory': False}
        }
        super().__init__(tool_id, 'YoutubeChannelSearchTool', "A tool that can be used to semantic search a query from a Youtube Channels content. Channel can be added as @channel", parameters, youtube_channel_handle=youtube_channel_handle)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return YoutubeChannelSearchTool(self.parameters.get('youtube_channel_handle') if self.parameters.get('youtube_channel_handle') else None)

class MyWebsiteSearchTool(MyTool):
    def __init__(self, tool_id=None, website=None):
        parameters = {
            'website': {'mandatory': False}
        }
        super().__init__(tool_id, 'WebsiteSearchTool', "A tool that can be used to semantic search a query from a specific URL content.", parameters, website=website)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return WebsiteSearchTool(self.parameters.get('website') if self.parameters.get('website') else None)

class MyCSVSearchTool(MyTool):
    def __init__(self, tool_id=None, csv=None):
        parameters = {
            'csv': {'mandatory': False}
        }
        super().__init__(tool_id, 'CSVSearchTool', "A tool that can be used to semantic search a query from a CSV's content.", parameters, csv=csv)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return CSVSearchTool(csv=self.parameters.get('csv') if self.parameters.get('csv') else None)

class MyDocxSearchTool(MyTool):
    def __init__(self, tool_id=None, docx=None):
        parameters = {
            'docx': {'mandatory': False}
        }
        super().__init__(tool_id, 'DOCXSearchTool', "A tool that can be used to semantic search a query from a DOCX's content.", parameters, docx=docx)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return DOCXSearchTool(docx=self.parameters.get('docx') if self.parameters.get('docx') else None)

class MyEXASearchTool(MyTool):
    def __init__(self, tool_id=None, EXA_API_KEY: Optional[str] = None):
        parameters = {
            'EXA_API_KEY': EXA_API_KEY
        }
        super().__init__(tool_id, 'EXASearchTool', "A tool that can be used to search the internet from a search_query", parameters)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        api_key = self.parameters.get('EXA_API_KEY')
        if api_key:
            os.environ['EXA_API_KEY'] = api_key
        return EXASearchTool()

class MyGithubSearchTool(MyTool):
    def __init__(self, tool_id=None, github_repo=None, gh_token=None, content_types=None):
        parameters = {
            'github_repo': github_repo,
            'gh_token': gh_token,
            'content_types': content_types
        }
        super().__init__(tool_id, 'GithubSearchTool', "A tool that can be used to semantic search a query from a Github repository's content. Valid content_types: code,repo,pr,issue (comma separated)", parameters)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        content_types_str = self.parameters.get('content_types', '')
        content_types_list = content_types_str.split(',') if content_types_str else None
        
        return GithubSearchTool(
            github_repo=self.parameters.get('github_repo'),
            gh_token=self.parameters.get('gh_token'),
            content_types=content_types_list
        )

class MyJSONSearchTool(MyTool):
    def __init__(self, tool_id=None, json_path=None):
        parameters = {
            'json_path': {'mandatory': False}
        }
        super().__init__(tool_id, 'JSONSearchTool', "A tool that can be used to semantic search a query from a JSON's content.", parameters, json_path=json_path)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return JSONSearchTool(json_path=self.parameters.get('json_path') if self.parameters.get('json_path') else None)

class MyMDXSearchTool(MyTool):
    def __init__(self, tool_id=None, mdx=None):
        parameters = {
            'mdx': {'mandatory': False}
        }
        super().__init__(tool_id, 'MDXSearchTool', "A tool that can be used to semantic search a query from a MDX's content.", parameters, mdx=mdx)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return MDXSearchTool(mdx=self.parameters.get('mdx') if self.parameters.get('mdx') else None)

class MyPDFSearchTool(MyTool):
    def __init__(self, tool_id=None, pdf=None):
        parameters = {
            'pdf': {'mandatory': False}
        }
        super().__init__(tool_id, 'PDFSearchTool', "A tool that can be used to semantic search a query from a PDF's content.", parameters, pdf=pdf)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return PDFSearchTool(self.parameters.get('pdf') if self.parameters.get('pdf') else None)

class MyPGSearchTool(MyTool):
    def __init__(self, tool_id=None, db_uri=None, table_name: str = ''):
        parameters = {
            'db_uri': {'mandatory': True},
            'table_name': {'mandatory': False, 'default': ''}
        }
        super().__init__(tool_id, 'PGSearchTool', "A tool that can be used to semantic search a query from a database table's content.", parameters)
        if db_uri:
            self.parameters['db_uri'] = db_uri
        if table_name:
            self.parameters['table_name'] = table_name

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        db_uri = self.parameters.get('db_uri')
        if not db_uri:
            raise ValueError("db_uri is required")
        table_name = self.parameters.get('table_name', '')
        return PGSearchTool(db_uri=db_uri, table_name=table_name)

class MySeleniumScrapingTool(MyTool):
    def __init__(self, tool_id=None, website_url=None, cookie=None, wait_time=None):
        parameters = {
            'website_url': {'mandatory': True},
            'cookie': {'mandatory': False},
            'wait_time': {'mandatory': False}
        }
        super().__init__(
            tool_id, 
            'SeleniumScrapingTool', 
            "A tool that can be used to scrape websites with Selenium. Useful for dynamic websites that require JavaScript.", 
            parameters,
            website_url=website_url, 
            cookie=cookie, 
            wait_time=wait_time
        )

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        cookie_str = self.parameters.get('cookie', '')
        cookie_dict = {}
        if cookie_str:
            try:
                cookie_items = cookie_str.split(',')
                for item in cookie_items:
                    k, v = item.strip('{}').split(':')
                    cookie_dict[k.strip()] = v.strip()
            except Exception:
                pass

        return SeleniumScrapingTool(
            website_url=self.parameters.get('website_url'),
            cookie=cookie_dict if cookie_dict else None,
            wait_time=self.parameters.get('wait_time')
        )

class MyTXTSearchTool(MyTool):
    def __init__(self, tool_id=None, txt=None):
        parameters = {
            'txt': {'mandatory': False}
        }
        super().__init__(tool_id, 'TXTSearchTool', "A tool that can be used to semantic search a query from a TXT's content.", parameters, txt=txt)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return TXTSearchTool(self.parameters.get('txt'))

class MyScrapeElementFromWebsiteTool(MyTool):
    def __init__(self, tool_id=None, website_url=None, css_element=None, cookie=None):
        parameters = {
            'website_url': website_url,
            'css_element': css_element,
            'cookie': cookie
        }
        super().__init__(
            tool_id,
            'ScrapeElementFromWebsiteTool',
            "A tool that can be used to read a specific part of website content. CSS elements are separated by comma, cookies in format {key:value},{key:value}",
            parameters
        )

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        css_element_str = self.parameters.get('css_element', '')
        css_elements = css_element_str.split(',') if css_element_str else None

        cookie_str = self.parameters.get('cookie', '')
        cookie_dict = {}
        if cookie_str:
            try:
                cookie_items = cookie_str.split(',')
                for item in cookie_items:
                    k, v = item.strip('{}').split(':')
                    cookie_dict[k.strip()] = v.strip()
            except Exception:
                pass

        return ScrapeElementFromWebsiteTool(
            website_url=self.parameters.get('website_url'),
            css_element=css_elements,
            cookie=cookie_dict if cookie_dict else None
        )

class MyYahooFinanceNewsTool(MyTool):
    def __init__(self, tool_id=None):
        parameters = {}
        super().__init__(tool_id, 'YahooFinanceNewsTool', "A tool that can be used to search Yahoo Finance News.", parameters)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return YahooFinanceNewsTool()

class MyCustomApiTool(MyTool):
    def __init__(self, tool_id=None, base_url=None, headers=None, query_params=None):
        parameters = {
            'base_url': base_url,
            'headers': headers,
            'query_params': query_params
        }
        super().__init__(tool_id, 'CustomApiTool', "A tool that can be used to make API calls with customizable parameters.", parameters)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        headers_str = self.parameters.get('headers')
        headers_dict = None
        if headers_str:
            try:
                headers_dict = eval(headers_str)
            except Exception:
                pass

        query_params_str = self.parameters.get('query_params')
        query_params_dict = None
        if query_params_str:
            try:
                query_params_dict = eval(query_params_str)
            except Exception:
                pass

        return CustomApiTool(
            base_url=self.parameters.get('base_url'),
            headers=headers_dict,
            query_params=query_params_dict
        )

class MyCustomFileWriteTool(MyTool):
    def __init__(self, tool_id=None, base_folder: str = 'workspace', filename=None):
        parameters = {
            'base_folder': base_folder,
            'filename': filename
        }
        super().__init__(tool_id, 'CustomFileWriteTool', "A tool that can be used to write a file to a specific folder.", parameters)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        base_folder = self.parameters.get('base_folder', 'workspace')
        return CustomFileWriteTool(
            base_folder=base_folder,
            filename=self.parameters.get('filename')
        )

class MyCodeInterpreterTool(MyTool):
    def __init__(self, tool_id=None):
        parameters = {}
        super().__init__(tool_id, 'CodeInterpreterTool', "This tool is used to give the Agent the ability to run code (Python3) from the code generated by the Agent itself. The code is executed in a sandboxed environment, so it is safe to run any code. Docker required.", parameters)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return CodeInterpreterTool()

class MyCustomCodeInterpreterTool(MyTool):
    def __init__(self, tool_id=None,workspace_dir=None):
        parameters = {
            'workspace_dir': workspace_dir
        }
        super().__init__(tool_id, 'CustomCodeInterpreterTool', "This tool is used to give the Agent the ability to run code (Python3) from the code generated by the Agent itself. The code is executed in a sandboxed environment, so it is safe to run any code. Worskpace folder is shared. Docker required.", parameters, workspace_dir=workspace_dir)

    def create_tool(self, config: Optional[Dict[str, Any]] = None) -> Any:
        return CustomCodeInterpreterTool(workspace_dir=self.parameters.get('workspace_dir') if self.parameters.get('workspace_dir') else "workspace")

# Register all tools here
TOOL_CLASSES = {
    'SerperDevTool': MySerperDevTool,
    'WebsiteSearchTool': MyWebsiteSearchTool,
    'ScrapeWebsiteTool': MyScrapeWebsiteTool,
    'SeleniumScrapingTool': MySeleniumScrapingTool,
    'ScrapeElementFromWebsiteTool': MyScrapeElementFromWebsiteTool,
    'CustomApiTool': MyCustomApiTool,
    'CodeInterpreterTool': MyCodeInterpreterTool,
    'CustomCodeInterpreterTool': MyCustomCodeInterpreterTool,
    'FileReadTool': MyFileReadTool,
    'CustomFileWriteTool': MyCustomFileWriteTool,
    'DirectorySearchTool': MyDirectorySearchTool,
    'DirectoryReadTool': MyDirectoryReadTool,

    'YoutubeVideoSearchTool': MyYoutubeVideoSearchTool,
    'YoutubeChannelSearchTool' :MyYoutubeChannelSearchTool,
    'GithubSearchTool': MyGithubSearchTool,
    'CodeDocsSearchTool': MyCodeDocsSearchTool,
    'YahooFinanceNewsTool': MyYahooFinanceNewsTool,

    'TXTSearchTool': MyTXTSearchTool,
    'CSVSearchTool': MyCSVSearchTool,
    'DOCXSearchTool': MyDocxSearchTool, 
    'EXASearchTool': MyEXASearchTool,
    'JSONSearchTool': MyJSONSearchTool,
    'MDXSearchTool': MyMDXSearchTool,
    'PDFSearchTool': MyPDFSearchTool,
    'PGSearchTool': MyPGSearchTool    
}