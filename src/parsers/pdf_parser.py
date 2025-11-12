"""
PDF parser with table extraction
"""

import logging
from pathlib import Path
from typing import List

from .base_parser import BaseParser
from .models import ParsedDocument, DocumentType, Table
import pdfplumber

logger = logging.getLogger(__name__)


class PDFParser(BaseParser):
    """Parse PDF files with text and table extraction"""
    
    SUPPORTED_EXTENSIONS = ['pdf']
    
    def can_parse(self, file_path: str) -> bool:
        """Check if file is PDF"""
        return self.get_file_extension(file_path) == 'pdf'
    
    def parse(self, file_path: str) -> ParsedDocument:
        """Parse PDF file"""
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
        
        logger.info(f"Parsing PDF file: {file_path}")
        
        try:
            # Try pdfplumber first (better table extraction)
            return self._parse_with_pdfplumber(file_path)
        except Exception as e:
            logger.warning(f"pdfplumber failed, trying pypdf: {e}")
            try:
                return self._parse_with_pypdf(file_path)
            except Exception as e2:
                logger.error(f"All PDF parsing methods failed: {e2}")
                raise
    
    def _parse_with_pdfplumber(self, file_path: str) -> ParsedDocument:
        """Parse PDF using pdfplumber (best for tables)"""
        all_text = []
        all_tables = []
        metadata = {'pages': 0}
        
        with pdfplumber.open(file_path) as pdf:
            metadata['pages'] = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text()
                if text:
                    all_text.append(f"\n--- Page {page_num} ---\n")
                    all_text.append(text)
                
                # Extract tables if enabled
                if self.config.extract_tables:
                    tables = page.extract_tables()
                    if tables:
                        for table_data in tables:
                            if table_data:
                                table = self._convert_table(table_data)
                                all_tables.append(table)
        
        combined_text = "\n".join(all_text)
        
        return self.create_parsed_document(
            file_path=file_path,
            document_type=DocumentType.PDF,
            text=combined_text,
            tables=all_tables,
            metadata=metadata
        )
    
    def _parse_with_pypdf(self, file_path: str) -> ParsedDocument:
        """Parse PDF using pypdf (fallback, text only)"""
        from pypdf import PdfReader
        
        reader = PdfReader(file_path)
        
        all_text = []
        metadata = {
            'pages': len(reader.pages),
            'method': 'pypdf'
        }
        
        # Add PDF metadata if available
        if reader.metadata:
            metadata.update({
                'title': reader.metadata.get('/Title', ''),
                'author': reader.metadata.get('/Author', ''),
                'subject': reader.metadata.get('/Subject', '')
            })
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text:
                all_text.append(f"\n--- Page {page_num} ---\n")
                all_text.append(text)
        
        combined_text = "\n".join(all_text)
        
        return self.create_parsed_document(
            file_path=file_path,
            document_type=DocumentType.PDF,
            text=combined_text,
            metadata=metadata
        )
    
    def _convert_table(self, table_data: List[List]) -> Table:
        """Convert raw table data to Table object"""
        if not table_data:
            return Table()
        
        # First row as headers
        headers = [str(cell) if cell else "" for cell in table_data[0]]
        
        # Rest as rows
        rows = []
        for row_data in table_data[1:]:
            row = [str(cell) if cell else "" for cell in row_data]
            rows.append(row)
        
        return Table(
            headers=headers,
            rows=rows,
            num_rows=len(rows),
            num_columns=len(headers)
        )
