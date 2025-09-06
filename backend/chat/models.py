"""
Chat Models

This module contains models for managing chat sessions, messages,
and conversation history for the AI ChatBot application.
"""

from django.db import models
from django.conf import settings
import uuid


class ChatSession(models.Model):
    """
    Individual chat sessions for users.
    Each session represents a conversation thread.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='chat_sessions'
    )
    
    # Session metadata
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Session context
    subject = models.ForeignKey(
        'content.Subject', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Subject context for this chat session"
    )
    chapter = models.ForeignKey(
        'content.Chapter', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Chapter context for this chat session"
    )
    
    # Session state
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    last_message_at = models.DateTimeField(null=True, blank=True)
    
    # AI agent configuration
    agent_model = models.CharField(max_length=100, default='gpt-3.5-turbo')
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=1000)
    system_prompt = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-last_message_at', '-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title or 'Chat Session'}"
    
    @property
    def messages_count(self):
        """Count of messages in this session."""
        return self.messages.count()
    
    def generate_title(self):
        """Auto-generate title from first user message."""
        first_message = self.messages.filter(
            message_type='USER'
        ).first()
        if first_message:
            content = first_message.content
            # Take first 50 characters and add ellipsis if longer
            self.title = content[:50] + ('...' if len(content) > 50 else '')
            self.save()


class Message(models.Model):
    """
    Individual messages within chat sessions.
    """
    MESSAGE_TYPES = [
        ('USER', 'User Message'),
        ('ASSISTANT', 'Assistant Response'),
        ('SYSTEM', 'System Message'),
        ('ERROR', 'Error Message'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    
    # Message content
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    content_html = models.TextField(blank=True, help_text="Rendered HTML content")
    
    # Message metadata
    token_count = models.IntegerField(default=0)
    character_count = models.IntegerField(default=0)
    
    # AI response metadata
    model_used = models.CharField(max_length=100, blank=True)
    response_time = models.FloatField(null=True, blank=True, help_text="Response time in seconds")
    cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    
    # Context and retrieval
    context_used = models.JSONField(default=list, blank=True, help_text="Retrieved context chunks")
    sources = models.JSONField(default=list, blank=True, help_text="Source documents")
    
    # Message state
    is_edited = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.session.user.email} - {self.message_type} - {self.content[:50]}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate character count and update session."""
        self.character_count = len(self.content)
        super().save(*args, **kwargs)
        
        # Update session's last message time
        self.session.last_message_at = self.created_at
        self.session.save(update_fields=['last_message_at'])


class ConversationMemory(models.Model):
    """
    Long-term memory storage for conversations.
    Stores important information extracted from conversations.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='conversation_memories'
    )
    
    # Memory content
    key = models.CharField(max_length=200, help_text="Memory key/identifier")
    value = models.TextField(help_text="Memory content")
    context = models.TextField(blank=True, help_text="Additional context")
    
    # Memory metadata
    memory_type = models.CharField(
        max_length=50,
        choices=[
            ('PREFERENCE', 'User Preference'),
            ('FACT', 'User Fact'),
            ('GOAL', 'User Goal'),
            ('CONTEXT', 'Context Information'),
            ('LEARNING', 'Learning Progress'),
        ],
        default='FACT'
    )
    confidence = models.FloatField(default=1.0, help_text="Confidence score 0-1")
    importance = models.IntegerField(default=5, help_text="Importance score 1-10")
    
    # Source tracking
    source_session = models.ForeignKey(
        ChatSession, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='extracted_memories'
    )
    source_message = models.ForeignKey(
        Message, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='extracted_memories'
    )
    
    # Memory lifecycle
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    access_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversation_memories'
        unique_together = ['user', 'key']
        ordering = ['-importance', '-updated_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.key}: {self.value[:50]}"


class ChatUsageLog(models.Model):
    """
    Usage tracking for billing and analytics.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='usage_logs'
    )
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='usage_logs'
    )
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='usage_logs'
    )
    
    # Usage metrics
    operation_type = models.CharField(
        max_length=50,
        choices=[
            ('CHAT_QUERY', 'Chat Query'),
            ('DOCUMENT_SEARCH', 'Document Search'),
            ('EMBEDDING_GENERATION', 'Embedding Generation'),
            ('SUMMARIZATION', 'Text Summarization'),
        ],
        default='CHAT_QUERY'
    )
    
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    tokens_total = models.IntegerField(default=0)
    
    # Cost calculation
    cost_input = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    cost_output = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    cost_total = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    
    # Performance metrics
    response_time = models.FloatField(help_text="Response time in seconds")
    model_used = models.CharField(max_length=100)
    
    # Context retrieval
    documents_retrieved = models.IntegerField(default=0)
    chunks_used = models.IntegerField(default=0)
    retrieval_time = models.FloatField(default=0, help_text="Retrieval time in seconds")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_usage_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.operation_type} - {self.tokens_total} tokens"
