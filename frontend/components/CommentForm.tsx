'use client';

import { useState } from 'react';

interface CommentFormProps {
  onSubmit: (text: string) => void;
}

export default function CommentForm({ onSubmit }: CommentFormProps) {
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setSubmitting(true);
    try {
      await onSubmit(text.trim());
      setText('');
    } catch (error) {
      console.error('Error submitting comment:', error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Write a comment..."
        className="form-textarea"
        rows={3}
        maxLength={1000}
        required
      />
      <div style={{ marginTop: '0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '0.85rem', color: '#666' }}>
          {text.length}/1000 characters
        </span>
        <button 
          type="submit" 
          className="btn-primary"
          disabled={submitting || !text.trim()}
        >
          {submitting ? 'Posting...' : 'Post Comment'}
        </button>
      </div>
    </form>
  );
}

