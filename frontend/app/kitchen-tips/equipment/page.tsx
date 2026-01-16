'use client';

import Link from 'next/link';

export default function EquipmentPage() {
  const equipment = [
    {
      name: 'Chef\'s Knife',
      description: 'An 8-inch chef\'s knife is the most versatile tool in your kitchen. Invest in a quality one.',
      essential: true,
    },
    {
      name: 'Cutting Board',
      description: 'Use separate boards for raw meat and vegetables. Wood or plastic both work well.',
      essential: true,
    },
    {
      name: 'Digital Thermometer',
      description: 'Essential for cooking meat safely and achieving perfect doneness.',
      essential: true,
    },
    {
      name: 'Microplane Grater',
      description: 'Perfect for zesting citrus, grating garlic, ginger, and hard cheeses.',
      essential: false,
    },
    {
      name: 'Kitchen Shears',
      description: 'Great for cutting herbs, trimming meat, and opening packages.',
      essential: false,
    },
    {
      name: 'Parchment Paper',
      description: 'Prevents sticking, makes cleanup easy, and is reusable.',
      essential: false,
    },
    {
      name: 'Silicone Spatula',
      description: 'Heat-resistant and perfect for scraping bowls and stirring.',
      essential: true,
    },
    {
      name: 'Measuring Cups & Spoons',
      description: 'Accurate measurements are crucial for baking success.',
      essential: true,
    },
    {
      name: 'Mixing Bowls',
      description: 'A set of nested bowls in various sizes is indispensable.',
      essential: true,
    },
    {
      name: 'Sheet Pans',
      description: 'Versatile for roasting, baking cookies, and sheet pan dinners.',
      essential: true,
    },
  ];

  return (
    <main className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem 1rem' }}>
      <div style={{ marginBottom: '2rem' }}>
        <Link href="/kitchen-tips" style={{ color: '#0066cc', textDecoration: 'none', fontSize: '0.9rem' }}>
          ← Back to Kitchen Tips
        </Link>
      </div>

      <div style={{ marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#333' }}>
          Essential Kitchen Equipment
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#666', lineHeight: '1.6' }}>
          Build your kitchen with these essential tools. Start with the basics and expand as you grow your cooking skills.
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '1.5rem'
      }}>
        {equipment.map((item, index) => (
          <div 
            key={index}
            style={{
              background: 'white',
              padding: '1.5rem',
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              borderLeft: item.essential ? '4px solid #0066cc' : '4px solid #e5e5e5',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#333', margin: 0 }}>
                {item.name}
              </h3>
              {item.essential && (
                <span style={{
                  background: '#0066cc',
                  color: 'white',
                  fontSize: '0.75rem',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '4px',
                  fontWeight: '500',
                }}>
                  Essential
                </span>
              )}
            </div>
            <p style={{ color: '#666', lineHeight: '1.6', margin: 0 }}>
              {item.description}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}

