'use client';

import { useState } from 'react';

interface RatingStarsProps {
  currentRating: number;
  onSubmit: (stars: number, reviewText?: string) => void;
  onDelete?: () => void;
  reviewText?: string;
  canDelete?: boolean;
}

export default function RatingStars({ 
  currentRating, 
  onSubmit, 
  onDelete,
  reviewText: initialReviewText = '',
  canDelete = false
}: RatingStarsProps) {
  const [selectedStars, setSelectedStars] = useState(currentRating);
  const [hoveredStar, setHoveredStar] = useState(0);
  const [reviewText, setReviewText] = useState(initialReviewText);
  const [showReviewForm, setShowReviewForm] = useState(false);

  const handleStarClick = (stars: number) => {
    setSelectedStars(stars);
    setShowReviewForm(true);
  };

  const handleSubmit = () => {
    if (selectedStars > 0) {
      onSubmit(selectedStars, reviewText);
      setShowReviewForm(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete your rating?')) return;
    if (onDelete) {
      onDelete();
    }
  };

  return (
    <div>
      <div className="rating-stars">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            className={`star-button ${selectedStars >= star ? 'active' : ''}`}
            onClick={() => handleStarClick(star)}
            onMouseEnter={() => setHoveredStar(star)}
            onMouseLeave={() => setHoveredStar(0)}
          >
            {(hoveredStar >= star || selectedStars >= star) ? '⭐' : '☆'}
          </button>
        ))}
        <span style={{ marginLeft: '1rem', color: '#666' }}>
          {selectedStars > 0 ? `${selectedStars} out of 5 stars` : 'Click to rate'}
        </span>
      </div>

      {currentRating > 0 && canDelete && (
        <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {initialReviewText && (
            <div style={{ flex: 1, padding: '1rem', background: '#f8f9fa', borderRadius: '4px' }}>
              <strong>Your Review:</strong>
              <p style={{ marginTop: '0.5rem', color: '#666' }}>{initialReviewText}</p>
            </div>
          )}
          <button 
            onClick={handleDelete}
            style={{
              background: 'none',
              border: '1px solid #dc3545',
              color: '#dc3545',
              padding: '0.5rem 1rem',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.9rem'
            }}
          >
            Delete Rating
          </button>
        </div>
      )}

      {showReviewForm && (
        <div style={{ marginTop: '1rem' }}>
          <textarea
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            placeholder="Write a review (optional)"
            className="form-textarea"
            rows={4}
            maxLength={1000}
          />
          <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.5rem' }}>
            <button onClick={handleSubmit} className="btn-primary">
              {currentRating > 0 ? 'Update Rating' : 'Submit Rating'}
            </button>
            <button 
              onClick={() => {
                setShowReviewForm(false);
                setReviewText(initialReviewText);
              }}
              className="btn-outline"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

