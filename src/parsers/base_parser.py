from abc import ABC, abstractmethod 
from pathlib import Path 
from typing import Optional 
import logging
from .models import ParsedDocument, ParserConfig, DocumentType

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Base class for all document parsers"""
    
    def __init__(self, config: Optional[ParserConfig] = None):
        self.config = config or ParserConfig()
    
    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the file"""
        pass
    
    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument:
        """Parse the document and return structured data"""
        pass
    
    def validate_file(self, file_path: str) -> bool:
        """Validate file exists and size is acceptable"""
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return False
        
        if not path.is_file():
            logger.error(f"Not a file: {file_path}")
            return False
        
        # Check file size
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            logger.error(f"File too large: {size_mb:.2f}MB (max: {self.config.max_file_size_mb}MB)")
            return False
        
        return True
    
    def get_file_extension(self, file_path: str) -> str:
        """Get file extension in lowercase"""
        return Path(file_path).suffix.lower().lstrip('.')
    
    def create_parsed_document(
        self,
        file_path: str,
        document_type: DocumentType,
        text: str = "",
        tables: list = None,
        metadata: dict = None
    ) -> ParsedDocument:
        """Helper to create ParsedDocument"""
        return ParsedDocument(
            file_path=file_path,
            document_type=document_type,
            text=text,
            tables=tables or [],
            metadata=metadata or {}
        )
