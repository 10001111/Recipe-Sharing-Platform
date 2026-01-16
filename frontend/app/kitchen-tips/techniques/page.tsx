'use client';

import Link from 'next/link';

export default function TechniquesPage() {
  const techniques = [
    {
      name: 'Sautéing',
      description: 'Cooking food quickly in a small amount of fat over high heat. Keep ingredients moving in the pan.',
      tips: [
        'Heat the pan before adding oil',
        'Don\'t overcrowd the pan',
        'Use high heat and keep ingredients moving',
      ],
    },
    {
      name: 'Roasting',
      description: 'Cooking food in an oven using dry heat. Great for vegetables, meats, and whole meals.',
      tips: [
        'Preheat your oven',
        'Use high heat (400-450°F) for crispy results',
        'Don\'t overcrowd the pan',
        'Rotate halfway through cooking',
      ],
    },
    {
      name: 'Braising',
      description: 'Cooking food slowly in liquid at low heat. Perfect for tough cuts of meat.',
      tips: [
        'Sear meat first for better flavor',
        'Use enough liquid to cover halfway',
        'Cook low and slow',
        'Check liquid level periodically',
      ],
    },
    {
      name: 'Poaching',
      description: 'Cooking food gently in liquid just below boiling point. Great for eggs and delicate proteins.',
      tips: [
        'Use enough liquid to fully submerge',
        'Keep temperature just below boiling',
        'Add a splash of vinegar for eggs',
        'Don\'t let liquid come to a full boil',
      ],
    },
    {
      name: 'Steaming',
      description: 'Cooking food with steam from boiling water. Preserves nutrients and keeps food moist.',
      tips: [
        'Don\'t let water touch the food',
        'Keep water at a steady boil',
        'Don\'t overcook - check frequently',
        'Season food before steaming',
      ],
    },
    {
      name: 'Grilling',
      description: 'Cooking food over direct heat. Creates great flavor and char marks.',
      tips: [
        'Preheat the grill thoroughly',
        'Oil the grates to prevent sticking',
        'Don\'t move food too early',
        'Let meat rest after grilling',
      ],
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
          Cooking Techniques
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#666', lineHeight: '1.6' }}>
          Master these fundamental cooking methods to expand your culinary skills and confidence in the kitchen.
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
        gap: '2rem'
      }}>
        {techniques.map((technique, index) => (
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
              marginBottom: '0.75rem',
              color: '#333',
            }}>
              {technique.name}
            </h2>
            <p style={{ 
              color: '#666', 
              lineHeight: '1.6', 
              marginBottom: '1.5rem',
              fontSize: '0.95rem',
            }}>
              {technique.description}
            </p>
            <div>
              <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.75rem', color: '#333' }}>
                Tips:
              </h3>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {technique.tips.map((tip, tipIndex) => (
                  <li 
                    key={tipIndex}
                    style={{
                      padding: '0.5rem 0',
                      paddingLeft: '1.5rem',
                      position: 'relative',
                      fontSize: '0.9rem',
                      color: '#666',
                      lineHeight: '1.6',
                    }}
                  >
                    <span style={{
                      position: 'absolute',
                      left: 0,
                      color: '#0066cc',
                      fontWeight: 'bold',
                    }}>✓</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}

