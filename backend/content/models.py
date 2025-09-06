"""
Content Management Models

This module contains models for organizing content into categories,
subjects, chapters, and managing document uploads for the AI ChatBot.
"""

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
import uuid
import os


def upload_to_documents(instance, filename):
    """Generate upload path for documents."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('documents', str(instance.chapter.id), filename)


class Category(models.Model):
    """
    Top-level categories for organizing content.
    Examples: Technology, Science, Business, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    
    # SEO and ordering
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_categories'
    )
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def subjects_count(self):
        """Count of active subjects in this category."""
        return self.subjects.filter(is_active=True).count()


class Subject(models.Model):
    """
    Subjects within categories.
    Examples: Under Technology -> Python, JavaScript, AI/ML, etc.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#28a745")
    is_active = models.BooleanField(default=True)
    
    # Learning path
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced'),
            ('EXPERT', 'Expert'),
        ],
        default='BEGINNER'
    )
    estimated_hours = models.PositiveIntegerField(default=10, help_text="Estimated learning hours")
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    # SEO and ordering
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_subjects'
    )
    
    class Meta:
        db_table = 'subjects'
        unique_together = ['category', 'slug']
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    @property
    def chapters_count(self):
        """Count of active chapters in this subject."""
        return self.chapters.filter(is_active=True).count()


class Chapter(models.Model):
    """
    Chapters within subjects containing actual learning content.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="Main chapter content")
    
    # Chapter properties
    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False, help_text="Available to free tier users")
    estimated_minutes = models.PositiveIntegerField(default=30)
    
    # Learning objectives
    objectives = models.JSONField(default=list, blank=True, help_text="List of learning objectives")
    tags = models.JSONField(default=list, blank=True, help_text="Searchable tags")
    
    # SEO and ordering
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_chapters'
    )
    
    class Meta:
        db_table = 'chapters'
        unique_together = ['subject', 'slug']
        ordering = ['subject', 'order', 'title']
    
    def __str__(self):
        return f"{self.subject.name} - {self.title}"
    
    @property
    def documents_count(self):
        """Count of documents in this chapter."""
        return self.documents.filter(is_active=True).count()


class DocumentUpload(models.Model):
    """
    PDF and other document uploads for chapters.
    These documents will be processed for vector embeddings.
    """
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # File details
    file = models.FileField(
        upload_to=upload_to_documents,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'docx'])]
    )
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=10)
    
    # Processing status
    is_active = models.BooleanField(default=True)
    is_processed = models.BooleanField(default=False)
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PROCESSING', 'Processing'),
            ('COMPLETED', 'Completed'),
            ('FAILED', 'Failed'),
        ],
        default='PENDING'
    )
    processing_error = models.TextField(blank=True)
    
    # Document metadata
    page_count = models.PositiveIntegerField(null=True, blank=True)
    word_count = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='uploaded_documents'
    )
    
    class Meta:
        db_table = 'document_uploads'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.chapter.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        """Auto-populate file metadata on save."""
        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)


class DocumentMeta(models.Model):
    """
    Extracted metadata and content from processed documents.
    """
    document = models.OneToOneField(
        DocumentUpload, 
        on_delete=models.CASCADE, 
        related_name='metadata'
    )
    
    # Extracted content
    extracted_text = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    key_topics = models.JSONField(default=list, blank=True)
    
    # Technical metadata
    pdf_metadata = models.JSONField(default=dict, blank=True)
    extraction_method = models.CharField(max_length=50, default='PyPDF2')
    
    # Search and indexing
    search_vector = models.TextField(blank=True, help_text="Preprocessed text for search")
    chunk_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'document_metadata'
    
    def __str__(self):
        return f"Metadata for {self.document.title}"
