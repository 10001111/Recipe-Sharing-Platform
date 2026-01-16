/**
 * API Route: Upload to Vercel Blob Storage
 * 
 * This route handles image uploads to Vercel Blob Storage
 * Documentation: https://vercel.com/docs/storage/vercel-blob
 */

import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function POST(request: NextRequest) {
  try {
    const BLOB_STORE_TOKEN = process.env.BLOB_READ_WRITE_TOKEN;
    const BLOB_STORE_ID = process.env.BLOB_STORE_ID;

    if (!BLOB_STORE_TOKEN || !BLOB_STORE_ID) {
      return NextResponse.json(
        { error: 'Blob storage not configured. Please set BLOB_READ_WRITE_TOKEN and BLOB_STORE_ID in Vercel environment variables.' },
        { status: 500 }
      );
    }

    const formData = await request.formData();
    const file = formData.get('file') as File;
    const pathname = formData.get('pathname') as string || `recipes/${Date.now()}-${file?.name || 'image'}`;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Enhanced validation: Check MIME type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const fileMimeType = file.type.toLowerCase();
    
    if (!allowedTypes.includes(fileMimeType)) {
      return NextResponse.json(
        { error: `Invalid file type. Allowed types: ${allowedTypes.join(', ')}` },
        { status: 400 }
      );
    }

    // Validate file size (max 5MB for recipes, configurable)
    const maxSizeMB = 5;
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      const actualSizeMB = (file.size / (1024 * 1024)).toFixed(2);
      return NextResponse.json(
        { error: `File size (${actualSizeMB}MB) exceeds maximum (${maxSizeMB}MB)` },
        { status: 400 }
      );
    }

    // Additional validation: Check file extension matches MIME type
    const fileName = file.name.toLowerCase();
    const extension = fileName.substring(fileName.lastIndexOf('.') + 1);
    const mimeToExtension: { [key: string]: string[] } = {
      'image/jpeg': ['jpg', 'jpeg'],
      'image/jpg': ['jpg', 'jpeg'],
      'image/png': ['png'],
      'image/gif': ['gif'],
      'image/webp': ['webp'],
    };
    
    if (mimeToExtension[fileMimeType] && !mimeToExtension[fileMimeType].includes(extension)) {
      return NextResponse.json(
        { error: 'File extension does not match file type' },
        { status: 400 }
      );
    }

    // Convert file to buffer
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // Upload to Vercel Blob Storage using the correct API format
    const blobResponse = await fetch(
      `https://blob.vercel-storage.com/${pathname}`,
      {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${BLOB_STORE_TOKEN}`,
          'Content-Type': file.type,
          'x-content-type': file.type,
        },
        body: buffer,
      }
    );

    if (!blobResponse.ok) {
      const errorText = await blobResponse.text();
      console.error('Blob upload error:', errorText);
      return NextResponse.json(
        { error: `Failed to upload to blob storage: ${errorText}` },
        { status: blobResponse.status }
      );
    }

    const blobData = await blobResponse.json();

    // Construct the public URL
    const publicUrl = `https://${BLOB_STORE_ID}.public.blob.vercel-storage.com/${pathname}`;

    return NextResponse.json({
      url: publicUrl,
      pathname: pathname,
      contentType: file.type,
      size: file.size,
      uploadedAt: Date.now(),
    });
  } catch (error: any) {
    console.error('Upload error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to upload image' },
      { status: 500 }
    );
  }
}
