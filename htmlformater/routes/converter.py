from fastapi import APIRouter, UploadFile, Form, File

from pathlib import Path
import aiofiles
import tempfile



from fastapi.responses import HTMLResponse

from ..schemas.converter import InputFile
from ..service.convert import ConvertFile, Html, Header, Footer 

router = APIRouter()

@router.post('/')
async def converter(file: UploadFile = File(...), option: str = Form(default=False)):
    file_name = file.filename
    file_path = ''

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = temp_dir +'/'+ file_name

        async with aiofiles.open(file_path, mode='wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        body = ConvertFile(file_path)
        await body.convert()


    head = Header(option)
    footer = Footer('')

    html_content = Html(head, body, footer)
    result = html_content.get_all_content()
    
    
    return HTMLResponse(content=result) 
        

# @router.get("/upload", response_class=HTMLResponse)
# async def main():
#     content = """
#     <html>
#         <head>
#             <title>Upload File</title>
#         </head>
#         <body>
#             <h1>Upload a File</h1>
#             <form action="/api/converter/" enctype="multipart/form-data" method="post">
#                 <input name="option" type="text">
#                 <input name="file" type="file">
#                 <input type="submit">
#             </form>
#         </body>
#     </html>
#     """
#     return content