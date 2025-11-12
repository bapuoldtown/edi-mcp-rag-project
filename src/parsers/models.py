from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class DocumentType(str, Enum):
    """Supported document types"""
    PDF = "pdf"
    WORD = "word"
    EXCEL = "excel"
    CSV = "csv"
    TEXT = "text"
    HTML = "html"
    UNKNOWN = "unknown"


class TableCell(BaseModel):
    """Single table cell"""
    value: str
    row: int
    column: int


class Table(BaseModel):
    """Extracted table data"""
    headers: List[str] = Field(default_factory=list)
    rows: List[List[str]] = Field(default_factory=list)
    num_rows: int = 0
    num_columns: int = 0
    
    def to_dict(self) -> List[Dict[str, str]]:
        """Convert table to list of dictionaries"""
        if not self.headers or not self.rows:
            return []
        
        result = []
        for row in self.rows:
            row_dict = {}
            for i, header in enumerate(self.headers):
                value = row[i] if i < len(row) else ""
                row_dict[header] = value
            result.append(row_dict)
        return result


class ParsedDocument(BaseModel):
    """Parsed document with extracted content"""
    file_path: str
    document_type: DocumentType
    text: str = ""
    tables: List[Table] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    raw_content: Optional[str] = None
    
    def get_all_text(self) -> str:
        """Get all text including table content"""
        all_text = [self.text]
        
        for table in self.tables:
            # Add table as formatted text
            if table.headers:
                all_text.append("\n\n" + " | ".join(table.headers))
                all_text.append("-" * 50)
            for row in table.rows:
                all_text.append(" | ".join(row))
        
        return "\n".join(all_text)
    
    def has_tables(self) -> bool:
        """Check if document contains tables"""
        return len(self.tables) > 0
    
    def get_table_count(self) -> int:
        """Get number of tables"""
        return len(self.tables)


class ParserConfig(BaseModel):
    """Configuration for parsers"""
    extract_tables: bool = True
    extract_images: bool = False
    ocr_enabled: bool = False
    max_file_size_mb: int = 50
    encoding: str = "utf-8"
