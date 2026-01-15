'use client';

import { Comment } from '@/lib/api';
import { commentApi, api } from '@/lib/api';
import { useState, useEffect } from 'react';

interface CommentListProps {
  comments: Comment[];
  onDelete?: () => void;
}

export default function CommentList({ comments, onDelete }: CommentListProps) {
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);

  useEffect(() => {
    // Get current user ID
    checkCurrentUser();
  }, []);

  const checkCurrentUser = async () => {
    try {
      const { userApi } = await import('@/lib/api');
      const user = await userApi.getCurrent();
      if (user) {
        setCurrentUserId(user.id);
      }
    } catch (error) {
      // User not authenticated
      setCurrentUserId(null);
    }
  };

  const canDeleteComment = (comment: Comment): boolean => {
    // Check if current user is the comment author
    return currentUserId !== null && currentUserId === comment.user.id;
  };

  const handleDelete = async (id: number, comment: Comment) => {
    if (!confirm('Are you sure you want to delete this comment?')) return;

    try {
      setDeletingId(id);
      await commentApi.delete(id);
      if (onDelete) onDelete();
    } catch (error: any) {
      console.error('Error deleting comment:', error);
      if (error.response?.status === 403 || error.response?.status === 401) {
        alert('You can only delete your own comments.');
      } else {
        alert('Failed to delete comment. Please try again.');
      }
    } finally {
      setDeletingId(null);
    }
  };

  if (comments.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
        No comments yet. Be the first to comment!
      </div>
    );
  }

  return (
    <div className="comments-section">
      {comments.map((comment) => {
        const canDelete = canDeleteComment(comment);
        return (
          <div key={comment.id} className="comment">
            <div className="comment-header">
              <span className="comment-author">{comment.user.username}</span>
              <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                <span className="comment-date">
                  {new Date(comment.created_at).toLocaleDateString()}
                </span>
                {canDelete && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(comment.id, comment);
                    }}
                    disabled={deletingId === comment.id}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#dc3545',
                      cursor: 'pointer',
                      fontSize: '0.85rem',
                      padding: '0.25rem 0.5rem'
                    }}
                  >
                    {deletingId === comment.id ? 'Deleting...' : 'Delete'}
                  </button>
                )}
              </div>
            </div>
            <p className="comment-text">{comment.text}</p>
          </div>
        );
      })}
    </div>
  );
}

