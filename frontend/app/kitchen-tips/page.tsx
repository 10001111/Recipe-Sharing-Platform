'use client';

import Link from 'next/link';

export default function KitchenTipsPage() {
  const tips = [
    {
      category: 'Cooking Basics',
      tips: [
        'Always preheat your oven before baking',
        'Use a sharp knife - it\'s safer than a dull one',
        'Taste as you cook, not just at the end',
        'Read the entire recipe before you start',
        'Mise en place - prep all ingredients before cooking',
      ],
    },
    {
      category: 'Ingredient Tips',
      tips: [
        'Store herbs in water like flowers to keep them fresh',
        'Bring eggs to room temperature for better baking',
        'Use salt to enhance flavors, not just for saltiness',
        'Toast spices before using to release their oils',
        'Don\'t overcrowd the pan when sautéing',
      ],
    },
    {
      category: 'Time Savers',
      tips: [
        'Prep vegetables in advance and store in containers',
        'Cook grains in large batches and freeze portions',
        'Use a slow cooker for hands-off cooking',
        'Make double batches and freeze half',
        'Clean as you cook to save time later',
      ],
    },
    {
      category: 'Kitchen Equipment',
      tips: [
        'Invest in a good chef\'s knife - it\'s worth it',
        'Use a digital thermometer for perfect doneness',
        'A microplane is great for zesting and grating',
        'Parchment paper prevents sticking and makes cleanup easy',
        'Kitchen shears are versatile and underrated',
      ],
    },
    {
      category: 'Food Safety',
      tips: [
        'Wash hands frequently while cooking',
        'Use separate cutting boards for raw meat and vegetables',
        'Cook meat to proper internal temperatures',
        'Don\'t leave perishables at room temperature for more than 2 hours',
        'When in doubt, throw it out',
      ],
    },
    {
      category: 'Baking Tips',
      tips: [
        'Measure flour by weight, not volume, for accuracy',
        'Don\'t overmix batter - it makes baked goods tough',
        'Let ingredients come to room temperature before baking',
        'Use an oven thermometer to verify your oven temperature',
        'Rotate pans halfway through baking for even cooking',
      ],
    },
  ];

  return (
    <main className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem 1rem' }}>
      <div style={{ marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#333' }}>
          Kitchen Tips & Tricks
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#666', lineHeight: '1.6' }}>
          Discover helpful tips, techniques, and tricks to improve your cooking skills and make your time in the kitchen more enjoyable.
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '2rem',
        marginBottom: '3rem'
      }}>
        {tips.map((section, index) => (
          <div 
            key={index}
            style={{
              background: 'white',
              padding: '2rem',
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            }}
          >
            <h2 style={{ 
              fontSize: '1.5rem', 
              fontWeight: 'bold', 
              marginBottom: '1.5rem',
              color: '#333',
              borderBottom: '2px solid #e5e5e5',
              paddingBottom: '0.75rem'
            }}>
              {section.category}
            </h2>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
              {section.tips.map((tip, tipIndex) => (
                <li 
                  key={tipIndex}
                  style={{
                    padding: '0.75rem 0',
                    borderBottom: tipIndex < section.tips.length - 1 ? '1px solid #f0f0f0' : 'none',
                    fontSize: '0.95rem',
                    lineHeight: '1.6',
                    color: '#333',
                    paddingLeft: '1.5rem',
                    position: 'relative',
                  }}
                >
                  <span style={{
                    position: 'absolute',
                    left: 0,
                    color: '#0066cc',
                    fontWeight: 'bold',
                  }}>•</span>
                  {tip}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Additional Resources */}
      <div style={{
        background: '#f8f9fa',
        padding: '2rem',
        borderRadius: '8px',
        border: '1px solid #e5e5e5',
      }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#333' }}>
          More Resources
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <Link href="/kitchen-tips/equipment" style={{ color: '#0066cc', textDecoration: 'none' }}>
            <div style={{ padding: '1rem', background: 'white', borderRadius: '4px', border: '1px solid #e5e5e5' }}>
              <strong>Equipment Guide</strong>
              <p style={{ margin: '0.5rem 0 0', fontSize: '0.9rem', color: '#666' }}>
                Essential kitchen tools and equipment
              </p>
            </div>
          </Link>
          <Link href="/kitchen-tips/techniques" style={{ color: '#0066cc', textDecoration: 'none' }}>
            <div style={{ padding: '1rem', background: 'white', borderRadius: '4px', border: '1px solid #e5e5e5' }}>
              <strong>Cooking Techniques</strong>
              <p style={{ margin: '0.5rem 0 0', fontSize: '0.9rem', color: '#666' }}>
                Master fundamental cooking methods
              </p>
            </div>
          </Link>
          <Link href="/kitchen-tips/substitutions" style={{ color: '#0066cc', textDecoration: 'none' }}>
            <div style={{ padding: '1rem', background: 'white', borderRadius: '4px', border: '1px solid #e5e5e5' }}>
              <strong>Ingredient Substitutions</strong>
              <p style={{ margin: '0.5rem 0 0', fontSize: '0.9rem', color: '#666' }}>
                Smart swaps for common ingredients
              </p>
            </div>
          </Link>
        </div>
      </div>
    </main>
  );
}

