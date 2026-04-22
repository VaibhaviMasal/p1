import sqlite3
import sys
import os

# Ensure we can import app
sys.path.append(os.getcwd())
try:
    from app import app
    from flask import render_template
except ImportError:
    print("Could not import app.py. Make sure you are in the right directory.")
    sys.exit(1)

def check_data_and_render():
    print("--- CHECKING DATABASE DATA ---")
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        
        # Check raw feedback
        feedbacks = conn.execute("SELECT * FROM feedback").fetchall()
        print(f"Total Feedback Rows: {len(feedbacks)}")
        
        # Check Subject Stats
        subject_stats = conn.execute('''
            SELECT subject, AVG(rating) AS avg_rating
            FROM feedback
            GROUP BY subject
        ''').fetchall()
        print("\nSubject Stats:")
        for s in subject_stats:
            print(f"  {s['subject']}: {s['avg_rating']}")

        # Check Rating Distribution
        rating_counts = conn.execute('''
            SELECT rating, COUNT(*) as count 
            FROM feedback 
            GROUP BY rating
        ''').fetchall()
        
        rating_dist = {i: 0 for i in range(1, 6)}
        for r in rating_counts:
            # Replicating app.py logic exactly (checking my previous fix)
            try:
                rating_dist[int(r['rating'])] = r['count']
            except ValueError:
                print(f"  WARNING: Invalid rating value found: {r['rating']}")

        print("\nRating Distribution:")
        print(rating_dist)
        
        conn.close()

        print("\n--- CHECKING RENDERED TEMPLATE JS ---")
        with app.test_request_context('/dashboard'):
            # Mock session
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['admin'] = True
            
            # Render
            rendered = render_template(
                'dashboard.html',
                feedbacks=feedbacks,
                total=len(feedbacks),
                average=0, # Not important for this check
                subject_stats=subject_stats,
                rating_dist=rating_dist
            )
            
            # Extract script tag content roughly
            import re
            match = re.search(r'<script>(.*?)</script>', rendered, re.DOTALL)
            if match:
                print(match.group(1))
            else:
                print("Could not find <script> block in rendered template.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Redirect stdout to a file with utf-8 encoding
    sys.stdout = open('debug_output_utf8.txt', 'w', encoding='utf-8')
    check_data_and_render()
    sys.stdout.close()
