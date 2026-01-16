import Link from 'next/link';

export default function NotFound() {
  return (
    <main className="container">
      <div style={{ 
        textAlign: 'center', 
        padding: '4rem 2rem',
        minHeight: '60vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <h1 style={{ 
          fontSize: '6rem', 
          fontWeight: '300', 
          marginBottom: '1rem', 
          color: '#333',
          lineHeight: '1'
        }}>
          404
        </h1>
        <h2 style={{ 
          fontSize: '2rem', 
          fontWeight: '400', 
          marginBottom: '1rem', 
          color: '#333'
        }}>
          Page Not Found
        </h2>
        <p style={{ 
          color: '#666', 
          marginBottom: '2rem', 
          fontSize: '1.1rem',
          maxWidth: '500px'
        }}>
          The page you're looking for doesn't exist or has been moved.
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link href="/" className="btn-primary">
            Go Home
          </Link>
          <Link href="/recipes" className="btn-outline">
            Browse Recipes
          </Link>
        </div>
      </div>
    </main>
  );
}

