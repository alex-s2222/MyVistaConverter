from pydantic import BaseModel, FilePath
from enum import Enum


class FileType(str, Enum):
    pear = 'pdf'
    banana = 'word'


class InputFile(BaseModel):
    file: FilePath
    header: str 
    file_type: FileType

