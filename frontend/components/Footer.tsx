'use client';

import Link from 'next/link';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h3 className="footer-title">🍳 Recipe Sharing</h3>
            <p className="footer-description">
              Discover, share, and rate amazing recipes from our community of passionate cooks.
            </p>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">Quick Links</h4>
            <ul className="footer-links">
              <li>
                <Link href="/">Home</Link>
              </li>
              <li>
                <Link href="/recipes">Browse Recipes</Link>
              </li>
              <li>
                <Link href="/recipes/create">Create Recipe</Link>
              </li>
              <li>
                <Link href="/favorites">My Favorites</Link>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">Account</h4>
            <ul className="footer-links">
              <li>
                <Link href="/login">Login</Link>
              </li>
              <li>
                <Link href="/register">Sign Up</Link>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">About</h4>
            <ul className="footer-links">
              <li>
                <Link href="/about">About Us</Link>
              </li>
              <li>
                <Link href="/contact">Contact</Link>
              </li>
              <li>
                <Link href="/privacy">Privacy Policy</Link>
              </li>
              <li>
                <Link href="/terms">Terms of Service</Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="footer-copyright">
            © {currentYear} Recipe Sharing Platform. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}

