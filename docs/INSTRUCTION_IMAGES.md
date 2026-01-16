# Instruction Images Feature

## Overview

Authors can now add images to individual instruction steps in their recipes. This feature allows for more visual and engaging recipe instructions, similar to popular recipe websites like Allrecipes.

## How It Works

### For Authors (Create/Edit Recipe)

1. **Step-by-Step Editor**: When creating or editing a recipe, authors use the `InstructionStepEditor` component instead of a plain textarea.

2. **Add Steps**: Click "Add Step" to create a new instruction step.

3. **Add Images**: Each step has an optional image upload field. Authors can:
   - Upload an image for each step
   - See a preview of the uploaded image
   - Remove images if needed

4. **Reorder Steps**: Steps can be moved up or down using the "Move Up" and "Move Down" buttons.

5. **Remove Steps**: Authors can remove individual steps if needed.

### Storage Format

Instructions are stored as JSON in the database:

```json
[
  {
    "text": "Preheat oven to 375°F (190°C)",
    "imageUrl": "https://blob.vercel-storage.com/recipe-steps/step1.jpg"
  },
  {
    "text": "Mix butter and sugars until smooth",
    "imageUrl": null
  },
  {
    "text": "Add eggs and vanilla",
    "imageUrl": "https://blob.vercel-storage.com/recipe-steps/step3.jpg"
  }
]
```

### Display

The `InstructionDisplay` component automatically:
- Parses JSON format instructions
- Falls back to plain text parsing if JSON is not available
- Supports markdown-style images: `![alt](url)` or `[IMAGE:url]`
- Displays images below each step
- Maintains Allrecipes-style layout

## Components

### `InstructionStepEditor`
- **Purpose**: Allows authors to create/edit instruction steps with images
- **Features**:
  - Add/remove steps
  - Reorder steps
  - Upload images per step
  - Step numbering
  - Image preview

### `InstructionDisplay`
- **Purpose**: Displays instructions with images on recipe detail page
- **Features**:
  - Parses JSON format
  - Falls back to plain text
  - Supports markdown images
  - Responsive image display

## Image Storage

### Development
- Images uploaded via FormData to Django backend
- Stored in `media/recipe-steps/` folder

### Production (Vercel)
- Images uploaded to Vercel Blob Storage
- Stored in `recipe-steps/` path
- URLs stored in JSON format

## Migration Path

### Existing Recipes
- Old recipes with plain text instructions continue to work
- `InstructionDisplay` automatically parses plain text
- Authors can edit recipes to add images using the new editor

### New Recipes
- All new recipes use the step-by-step editor
- Instructions stored as JSON with image support

## Usage Examples

### Creating a Recipe with Step Images

1. Fill in recipe details (title, description, etc.)
2. Click "Add Step" for each instruction
3. Enter step text
4. Optionally upload an image for that step
5. Repeat for all steps
6. Submit recipe

### Editing Existing Recipe

1. Open recipe edit page
2. Existing steps load automatically
3. Add images to steps that don't have them
4. Add new steps if needed
5. Save changes

## Technical Details

### Frontend
- **Components**: `InstructionStepEditor`, `InstructionDisplay`
- **Storage**: JSON string in `instructions` field
- **Image Upload**: Uses `uploadToBlob` for Vercel or FormData for local

### Backend
- **Model**: `Recipe.instructions` (TextField)
- **Format**: JSON string or plain text (backward compatible)
- **No schema changes needed**: Uses existing `instructions` field

## Benefits

1. **Visual Instructions**: Images help users understand each step
2. **Better UX**: More engaging recipe pages
3. **Professional Look**: Matches industry-standard recipe sites
4. **Backward Compatible**: Old recipes still work
5. **Flexible**: Supports JSON, plain text, and markdown formats

## Future Enhancements

- Video support for steps
- Step timing information
- Ingredient highlighting per step
- Print-friendly format
- Step notes/tips

