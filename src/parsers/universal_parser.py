"""
Universal Document Parser
Automatically detects format and uses appropriate parser
"""

import logging
from pathlib import Path
from typing import Optional, List

from .base_parser import BaseParser
from .models import ParsedDocument, ParserConfig, DocumentType
from .pdf_parser import PDFParser
from .excel_parser import ExcelParser

logger = logging.getLogger(__name__)


class UniversalParser:
    """
    Universal document parser that handles ANY format
    
    Automatically detects document type and uses the appropriate parser.
    Supports: PDF, Word, Excel, CSV, Text, and more!
    """
    
    def __init__(self, config: Optional[ParserConfig] = None):
        self.config = config or ParserConfig()
        
        # Initialize parsers - PDF and Excel only!
        self.parsers: List[BaseParser] = [
            PDFParser(self.config),
            ExcelParser(self.config)
        ]
        
        logger.info(f"Universal Parser initialized with {len(self.parsers)} parsers (PDF + Excel)")
    
    def parse(self, file_path: str) -> ParsedDocument:
        """
        Parse any document format
        
        Args:
            file_path: Path to the document
            
        Returns:
            ParsedDocument with extracted content
            
        Raises:
            ValueError: If file cannot be parsed
        """
        file_path = str(Path(file_path).resolve())
        
        if not Path(file_path).exists():
            raise ValueError(f"File not found: {file_path}")
        
        logger.info(f"Parsing document: {file_path}")
        
        # Try to find appropriate parser
        for parser in self.parsers:
            if parser.can_parse(file_path):
                try:
                    logger.info(f"Using {parser.__class__.__name__} for {file_path}")
                    return parser.parse(file_path)
                except Exception as e:
                    logger.error(f"{parser.__class__.__name__} failed: {e}")
                    # Try next parser
                    continue
        
        # No parser found
        ext = Path(file_path).suffix
        raise ValueError(
            f"No parser available for file type: {ext}\n"
            f"Supported formats: PDF (.pdf), Excel (.xlsx, .xls), CSV (.csv)"
        )
    
    def detect_format(self, file_path: str) -> DocumentType:
        """Detect document format"""
        ext = Path(file_path).suffix.lower().lstrip('.')
        
        format_map = {
            'pdf': DocumentType.PDF,
            'docx': DocumentType.WORD,
            'doc': DocumentType.WORD,
            'xlsx': DocumentType.EXCEL,
            'xls': DocumentType.EXCEL,
            'csv': DocumentType.CSV,
            'tsv': DocumentType.CSV,
            'txt': DocumentType.TEXT,
            'text': DocumentType.TEXT,
            'md': DocumentType.TEXT,
            'markdown': DocumentType.TEXT
        }
        
        return format_map.get(ext, DocumentType.UNKNOWN)
    
    def can_parse(self, file_path: str) -> bool:
        """Check if file can be parsed"""
        for parser in self.parsers:
            if parser.can_parse(file_path):
                return True
        return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        formats = []
        for parser in self.parsers:
            if hasattr(parser, 'SUPPORTED_EXTENSIONS'):
                formats.extend(parser.SUPPORTED_EXTENSIONS)
        return sorted(set(formats))
    
    def parse_multiple(self, file_paths: List[str]) -> List[ParsedDocument]:
        """
        Parse multiple documents
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of ParsedDocuments
        """
        results = []
        
        for file_path in file_paths:
            try:
                doc = self.parse(file_path)
                results.append(doc)
            except Exception as e:
                logger.error(f"Failed to parse {file_path}: {e}")
                # Create error document
                results.append(ParsedDocument(
                    file_path=file_path,
                    document_type=DocumentType.UNKNOWN,
                    text=f"Error: {e}",
                    metadata={'error': str(e)}
                ))
        
        return results


# Convenience function
def parse_document(
    file_path: str,
    extract_tables: bool = True,
    extract_images: bool = False
) -> ParsedDocument:
    """
    Quick function to parse any document
    
    Usage:
        doc = parse_document("implementation_guide.pdf")
        print(doc.text)
        print(f"Found {len(doc.tables)} tables")
    """
    config = ParserConfig(
        extract_tables=extract_tables,
        extract_images=extract_images
    )
    
    parser = UniversalParser(config)
    return parser.parse(file_path)