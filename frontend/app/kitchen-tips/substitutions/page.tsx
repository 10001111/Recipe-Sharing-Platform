'use client';

import Link from 'next/link';

export default function SubstitutionsPage() {
  const substitutions = [
    {
      ingredient: 'Butter',
      substitutes: [
        { name: 'Margarine', ratio: '1:1', notes: 'Works well in most recipes' },
        { name: 'Vegetable Oil', ratio: '3/4 cup oil = 1 cup butter', notes: 'For baking, reduce liquid slightly' },
        { name: 'Applesauce', ratio: '1/2 cup = 1 cup butter', notes: 'Great for reducing fat in baked goods' },
      ],
    },
    {
      ingredient: 'Eggs',
      substitutes: [
        { name: 'Flax Egg', ratio: '1 tbsp ground flax + 3 tbsp water = 1 egg', notes: 'Let sit 5 minutes to gel' },
        { name: 'Applesauce', ratio: '1/4 cup = 1 egg', notes: 'Works well in baked goods' },
        { name: 'Banana', ratio: '1/2 mashed banana = 1 egg', notes: 'Adds sweetness and moisture' },
      ],
    },
    {
      ingredient: 'All-Purpose Flour',
      substitutes: [
        { name: 'Whole Wheat Flour', ratio: '1:1', notes: 'May need more liquid' },
        { name: 'Almond Flour', ratio: '1/4 cup = 1 cup AP flour', notes: 'Add extra egg for binding' },
        { name: 'Coconut Flour', ratio: '1/4 cup = 1 cup AP flour', notes: 'Very absorbent, use sparingly' },
      ],
    },
    {
      ingredient: 'Sugar',
      substitutes: [
        { name: 'Honey', ratio: '3/4 cup = 1 cup sugar', notes: 'Reduce liquid by 1/4 cup' },
        { name: 'Maple Syrup', ratio: '3/4 cup = 1 cup sugar', notes: 'Reduce liquid by 3 tbsp' },
        { name: 'Stevia', ratio: '1 tsp = 1 cup sugar', notes: 'Much sweeter, adjust to taste' },
      ],
    },
    {
      ingredient: 'Heavy Cream',
      substitutes: [
        { name: 'Half & Half + Butter', ratio: '3/4 cup half & half + 1/4 cup butter', notes: 'Melt butter first' },
        { name: 'Milk + Cornstarch', ratio: '1 cup milk + 2 tbsp cornstarch', notes: 'Heat to thicken' },
        { name: 'Coconut Cream', ratio: '1:1', notes: 'Great for dairy-free options' },
      ],
    },
    {
      ingredient: 'Sour Cream',
      substitutes: [
        { name: 'Greek Yogurt', ratio: '1:1', notes: 'Similar tangy flavor' },
        { name: 'Buttermilk', ratio: '1:1', notes: 'Thinner consistency' },
        { name: 'Cream Cheese + Milk', ratio: '3/4 cup cream cheese + 1/4 cup milk', notes: 'Mix until smooth' },
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
          Ingredient Substitutions
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#666', lineHeight: '1.6' }}>
          Don't have a specific ingredient? Use these smart substitutions to keep cooking without a trip to the store.
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '2rem'
      }}>
        {substitutions.map((item, index) => (
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
              paddingBottom: '0.75rem',
            }}>
              {item.ingredient}
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {item.substitutes.map((sub, subIndex) => (
                <div 
                  key={subIndex}
                  style={{
                    padding: '1rem',
                    background: '#f8f9fa',
                    borderRadius: '4px',
                    border: '1px solid #e5e5e5',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                    <strong style={{ color: '#333', fontSize: '1rem' }}>{sub.name}</strong>
                    <span style={{ 
                      color: '#0066cc', 
                      fontSize: '0.85rem', 
                      fontWeight: '500',
                      whiteSpace: 'nowrap',
                      marginLeft: '1rem',
                    }}>
                      {sub.ratio}
                    </span>
                  </div>
                  <p style={{ color: '#666', fontSize: '0.9rem', margin: 0, fontStyle: 'italic' }}>
                    {sub.notes}
                  </p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}

