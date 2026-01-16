# Milestone 4.4: Image Handling - Implementation Plan

## Overview

This document outlines the detailed implementation plan for Milestone 4.4: Image Handling features.

## Current State

### What We Have:
- ✅ Vercel Blob Storage integration
- ✅ Basic image upload (`ImageUploadBlob` component)
- ✅ Single image per recipe
- ✅ Basic validation (file type, 5MB limit)

### What We Need:
- ✅ Enhanced image upload validation
- ✅ Image compression/optimization
- ✅ Multiple image support per recipe
- ✅ Default placeholder images

---

## Feature 1: Image Upload Validation ✅

### Current Limitations:
- Only checks file type (image/*)
- Only checks file size (5MB)
- No dimension validation
- No MIME type verification
- No corruption detection

### What We'll Add:

#### 1.1 Enhanced File Type Validation
```typescript
// Validate MIME type matches extension
- Check actual file content (magic bytes)
- Verify MIME type matches file extension
- Support: JPEG, PNG, GIF, WebP
- Reject: PDFs, videos, executables
```

#### 1.2 Dimension Validation
```typescript
// Validate image dimensions
- Min width: 200px
- Max width: 4000px
- Min height: 200px
- Max height: 4000px
- Aspect ratio: Optional validation
```

#### 1.3 File Corruption Detection
```typescript
// Ensure image can be loaded
- Try to load image in browser
- Verify image data is valid
- Check for corrupted files
```

#### 1.4 Size Validation (Enhanced)
```typescript
// Configurable size limits
- Recipe images: Max 5MB
- Step images: Max 2MB
- Avatar images: Max 1MB
```

### Implementation Files:
- `frontend/lib/image-validation.ts` - Validation utilities
- `frontend/components/ImageUploadBlob.tsx` - Enhanced component
- `frontend/app/api/upload-blob/route.ts` - Server-side validation

---

## Feature 2: Image Compression/Optimization ✅

### Current State:
- Images uploaded as-is (no compression)
- No format conversion
- No resizing

### What We'll Add:

#### 2.1 Client-Side Compression
```typescript
// Using browser-image-compression library
- Compress before upload
- Reduce file size by 60-80%
- Maintain quality (configurable)
- Convert to WebP when possible
```

#### 2.2 Format Conversion
```typescript
// Convert to optimal format
- PNG → WebP (if no transparency needed)
- JPEG → WebP (better compression)
- GIF → WebP (animated support)
- Maintain original if WebP not supported
```

#### 2.3 Automatic Resizing
```typescript
// Resize oversized images
- Max width: 1920px
- Max height: 1920px
- Maintain aspect ratio
- Create thumbnails (optional)
```

#### 2.4 Metadata Stripping
```typescript
// Remove EXIF data
- Strip location data (privacy)
- Remove camera info
- Reduce file size
```

### Implementation Files:
- `frontend/lib/image-compression.ts` - Compression utilities
- `frontend/components/ImageUploadBlob.tsx` - Add compression step
- `package.json` - Add `browser-image-compression` dependency

### Dependencies:
```json
{
  "browser-image-compression": "^2.0.2"
}
```

---

## Feature 3: Multiple Image Support ✅

### Current State:
- Recipe model has single `image` field
- Only one image per recipe

### What We'll Add:

#### 3.1 Database Model Changes
```python
# New model: RecipeImage
class RecipeImage(models.Model):
    recipe = models.ForeignKey(
        Recipe, 
        related_name='images',
        on_delete=models.CASCADE
    )
    image_url = models.URLField(
        help_text="URL from Vercel Blob Storage"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Primary/featured image"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for accessibility"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = [['recipe', 'is_primary']]  # Only one primary per recipe
```

#### 3.2 API Changes
```python
# Update RecipeSerializer
- Add images field (nested serializer)
- Support creating multiple images
- Support reordering images
- Support setting primary image
```

#### 3.3 Frontend Components
```typescript
// New component: ImageGallery
- Display multiple images
- Drag-and-drop reordering
- Set primary image
- Delete individual images
- Upload multiple images at once
```

### Implementation Files:
- `apps/recipes/models.py` - Add RecipeImage model
- `apps/recipes/migrations/0004_recipeimage.py` - Migration
- `apps/api/serializers.py` - RecipeImageSerializer
- `apps/api/views.py` - Update RecipeViewSet
- `frontend/components/ImageGallery.tsx` - New component
- `frontend/app/recipes/create/page.tsx` - Update form
- `frontend/app/recipes/[id]/edit/page.tsx` - Update form
- `frontend/app/recipes/[id]/page.tsx` - Display gallery

---

## Feature 4: Default Placeholder Images ✅

### Current State:
- Broken image icon when no image
- Empty space when image missing

### What We'll Add:

#### 4.1 Placeholder System
```typescript
// Placeholder images
- Recipe placeholder (default)
- Category-specific placeholders
- User avatar placeholder
- Step image placeholder
```

#### 4.2 Implementation Strategy
```typescript
// Options:
1. Use placeholder service (placeholder.com)
2. Generate SVG placeholders
3. Use local placeholder images
4. Use emoji-based placeholders
```

#### 4.3 Fallback Handling
```typescript
// Image component with fallback
- Try to load image
- If fails, show placeholder
- Handle broken URLs gracefully
- Show loading state
```

### Implementation Files:
- `frontend/lib/placeholders.ts` - Placeholder utilities
- `frontend/components/RecipeImage.tsx` - Image component with fallback
- `frontend/components/RecipeCard.tsx` - Use placeholder
- `frontend/app/recipes/[id]/page.tsx` - Use placeholder

---

## Implementation Steps

### Phase 1: Validation & Compression (Week 1)
1. ✅ Install compression library
2. ✅ Create validation utilities
3. ✅ Enhance ImageUploadBlob component
4. ✅ Add server-side validation
5. ✅ Test compression and validation

### Phase 2: Multiple Images (Week 2)
1. ✅ Create RecipeImage model
2. ✅ Create migration
3. ✅ Update serializers
4. ✅ Update API views
5. ✅ Create ImageGallery component
6. ✅ Update recipe forms
7. ✅ Update recipe display

### Phase 3: Placeholders (Week 3)
1. ✅ Create placeholder utilities
2. ✅ Create RecipeImage component
3. ✅ Update all image displays
4. ✅ Test fallback handling

### Phase 4: Testing & Polish (Week 4)
1. ✅ Test all features
2. ✅ Performance testing
3. ✅ Mobile testing
4. ✅ Documentation
5. ✅ Bug fixes

---

## Technical Decisions

### Compression Library Choice:
**browser-image-compression** ✅
- Pros: Client-side, no server load, easy to use
- Cons: Browser compatibility, larger bundle size
- Alternative: Server-side with Sharp (more complex)

### Multiple Images Storage:
**Vercel Blob Storage** ✅
- Already integrated
- Each image gets its own URL
- No changes needed to storage

### Placeholder Strategy:
**SVG Placeholders** ✅
- No external dependencies
- Fast loading
- Customizable
- Works offline

---

## Testing Checklist

### Validation:
- [ ] Valid images accepted
- [ ] Invalid files rejected
- [ ] Size limits enforced
- [ ] Dimension limits enforced
- [ ] Corrupted files detected

### Compression:
- [ ] Images compressed before upload
- [ ] Quality maintained
- [ ] File size reduced
- [ ] Format conversion works
- [ ] Resizing works

### Multiple Images:
- [ ] Can upload multiple images
- [ ] Can reorder images
- [ ] Can set primary image
- [ ] Can delete images
- [ ] Gallery displays correctly

### Placeholders:
- [ ] Placeholder shows when no image
- [ ] Placeholder shows on error
- [ ] Category placeholders work
- [ ] Fallback handling works

---

## Performance Targets

- **Image size after compression:** < 500KB (target: 200-300KB)
- **Upload time:** < 3 seconds per image
- **Page load with images:** < 2 seconds
- **Compression ratio:** 60-80% reduction

---

## Dependencies

### New Packages:
```json
{
  "browser-image-compression": "^2.0.2"
}
```

### No Backend Changes Needed:
- Vercel Blob Storage already handles storage
- Django just stores URLs (no changes needed)

---

## Migration Path

### For Existing Recipes:
1. Keep existing single image
2. Migrate to RecipeImage model
3. Set existing image as primary
4. Allow users to add more images

### Backward Compatibility:
- Old `image` field still works
- Gradual migration to `images` relationship
- Support both during transition

---

## Success Criteria

✅ Images are validated before upload  
✅ Images are compressed automatically  
✅ Multiple images per recipe supported  
✅ Placeholders show when no image  
✅ Performance improved (faster loads)  
✅ Storage costs reduced  
✅ User experience enhanced  

---

## Questions & Answers

### Q: Do we need server-side compression?
**A:** No, client-side compression is sufficient for most cases. Server-side can be added later if needed.

### Q: What about image CDN optimization?
**A:** Vercel Blob already includes CDN. We're optimizing before upload.

### Q: Can users upload unlimited images?
**A:** We'll set a limit (e.g., 10 images per recipe) to prevent abuse.

### Q: What about image editing (crop, rotate)?
**A:** Out of scope for Milestone 4.4. Can be added later.

### Q: Do we need image alt text?
**A:** Yes, for accessibility. We'll add it in the RecipeImage model.

---

## Next Steps

1. Review this plan
2. Approve technical decisions
3. Start Phase 1 implementation
4. Test as we go
5. Iterate based on feedback

