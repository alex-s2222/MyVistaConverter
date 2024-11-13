from typing import Protocol, Self
import pdfplumber


class ConvertFile:
    def __init__(self: Self, file_path: str):
        self.file_path: str = file_path
        self.__content: str = ''

    async def convert(self: Self):
        html :list = []

        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                p = Page(page=page)
                page = await p.convert()
                html.extend(page)

        self.__content = '\n'.join(html)

    @property
    def content(self: Self):
        return self.__content


class Page(ConvertFile):
    def __init__(self, page: pdfplumber.page) -> None:
        self.page_text :str = page.extract_text()
        self.tables :list = page.extract_tables()
        self.lines :list = []

    async def convert(self):
        page :list = []

        for line in self.page_text.split('\n'):
            if line:
                html_file = f'\t\t<div> {line} </div>'
                page.append(html_file)
        
        for table in self.tables:
            if table:
                page.append('\t\t<table>')
                for row in table:
                    if row: 
                        page.append('\t\t\t<tr>')
                        for element in row:
                            page.append(f'\t\t\t\t<td>{element}</td>')
                        page.append('\t\t\t</tr>')
                page.append('\t\t</table>')

        return page


class Header:
    def __init__(self: Self, content: str) -> None:
        self.__content = content

    @property
    def content(self: Self):
        begData = ['<html>','\t<head>']
        endData = ['\t</head>','\t<body>\n']
        result: str = ''

        result += '\n'.join(begData)
        result += self.__content + '\n' if self.__content else ''
        result += '\n'.join(endData)
            
        return result



class Footer:
    def __init__(self: Self, content: str) -> None:
        self.__content = content

    @property
    def content(self: Self):
        data = ['\t</body>','</html>']
        return '\n'.join(data)


class Html:
    def __init__(self: Self, head: Header, body: ConvertFile, foot: Footer) -> None:
        self.head = head.content
        self.body = body.content
        self.foot = foot.content

    def get_all_content(self: Self):
        return self.head + self.body + self.foot





