'use client';

import Link from 'next/link';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer-delish">
      <div className="footer-delish-container">
        <div className="footer-delish-content">
          <div className="footer-delish-section">
            <h3 className="footer-delish-title">Recipe Sharing</h3>
            <p className="footer-delish-description">
              Discover, share, and rate amazing recipes from our community of passionate cooks.
            </p>
            <div className="footer-delish-social">
              <a href="#" aria-label="Facebook">f</a>
              <a href="#" aria-label="Instagram">📷</a>
              <a href="#" aria-label="Twitter">t</a>
              <a href="#" aria-label="Pinterest">p</a>
            </div>
          </div>

          <div className="footer-delish-section">
            <h4 className="footer-delish-title">Recipes</h4>
            <ul className="footer-delish-links">
              <li>
                <Link href="/recipes">All Recipes</Link>
              </li>
              <li>
                <Link href="/recipes?category=breakfast">Breakfast</Link>
              </li>
              <li>
                <Link href="/recipes?category=lunch">Lunch</Link>
              </li>
              <li>
                <Link href="/recipes?category=dinner">Dinner</Link>
              </li>
              <li>
                <Link href="/recipes?category=dessert">Dessert</Link>
              </li>
            </ul>
          </div>

          <div className="footer-delish-section">
            <h4 className="footer-delish-title">Kitchen Tips</h4>
            <ul className="footer-delish-links">
              <li>
                <Link href="/kitchen-tips">Cooking Tips</Link>
              </li>
              <li>
                <Link href="/kitchen-tips/equipment">Equipment</Link>
              </li>
              <li>
                <Link href="/kitchen-tips/techniques">Techniques</Link>
              </li>
              <li>
                <Link href="/kitchen-tips/substitutions">Substitutions</Link>
              </li>
            </ul>
          </div>

          <div className="footer-delish-section">
            <h4 className="footer-delish-title">About</h4>
            <ul className="footer-delish-links">
              <li>
                <Link href="/about">About Us</Link>
              </li>
              <li>
                <Link href="/contact">Contact</Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="footer-delish-bottom">
          <p className="footer-delish-copyright">
            © {currentYear} Recipe Sharing Platform. All rights reserved.
          </p>
          <div className="footer-delish-legal">
            <Link href="/privacy">Privacy Notice</Link>
            <Link href="/terms">Terms of Use</Link>
            <Link href="/privacy/ca">CA Notice at Collection</Link>
            <Link href="/privacy/opt-out">Your Privacy Choices</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
