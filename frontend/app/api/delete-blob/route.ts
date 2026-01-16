/**
 * API Route: Delete from Vercel Blob Storage
 * 
 * This route handles image deletion from Vercel Blob Storage
 */

import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function DELETE(request: NextRequest) {
  try {
    const BLOB_STORE_TOKEN = process.env.BLOB_READ_WRITE_TOKEN;
    const BLOB_STORE_ID = process.env.BLOB_STORE_ID;

    if (!BLOB_STORE_TOKEN || !BLOB_STORE_ID) {
      return NextResponse.json(
        { error: 'Blob storage not configured' },
        { status: 500 }
      );
    }

    const body = await request.json();
    const { url } = body;

    if (!url) {
      return NextResponse.json(
        { error: 'URL is required' },
        { status: 400 }
      );
    }

    // Extract pathname from URL
    // URL format: https://store-id.public.blob.vercel-storage.com/pathname
    let pathname = '';
    try {
      const urlObj = new URL(url);
      // Remove leading slash from pathname
      pathname = urlObj.pathname.replace(/^\//, '');
    } catch (e) {
      // If URL parsing fails, assume it's already a pathname
      pathname = url.replace(/^https?:\/\/[^\/]+\//, '');
    }

    if (!pathname) {
      return NextResponse.json(
        { error: 'Invalid URL format' },
        { status: 400 }
      );
    }

    // Delete from Vercel Blob Storage
    const blobResponse = await fetch(
      `https://blob.vercel-storage.com/${pathname}`,
      {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${BLOB_STORE_TOKEN}`,
        },
      }
    );

    if (!blobResponse.ok && blobResponse.status !== 404) {
      const errorText = await blobResponse.text();
      console.error('Blob delete error:', errorText);
      return NextResponse.json(
        { error: `Failed to delete from blob storage: ${errorText}` },
        { status: blobResponse.status }
      );
    }

    return NextResponse.json({ success: true });
  } catch (error: any) {
    console.error('Delete error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to delete image' },
      { status: 500 }
    );
  }
}
