#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import html
import os

def clean_title(title):
    """Clean title for use in filename"""
    # Remove HTML entities
    title = html.unescape(title)
    # Replace special characters with hyphens
    title = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces and multiple hyphens with single hyphens
    title = re.sub(r'[-\s]+', '-', title)
    # Convert to lowercase and strip hyphens from ends
    return title.lower().strip('-')

def clean_content(content):
    """Clean WordPress content and convert to markdown"""
    if not content:
        return ""
    
    # Unescape HTML entities
    content = html.unescape(content)
    
    # Remove WordPress comments
    content = re.sub(r'<!-- wp:.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- /wp:.*?-->', '', content, flags=re.DOTALL)
    
    # Convert WordPress blocks to markdown
    content = re.sub(r'<p>', '', content)
    content = re.sub(r'</p>', '\n\n', content)
    
    # Convert line breaks
    content = re.sub(r'<br\s*/?>', '\n', content)
    
    # Convert links
    content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
    
    # Convert images
    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/?>', r'![\2](\1)', content)
    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*/?>', r'![](\1)', content)
    
    # Remove figure and div wrapper tags
    content = re.sub(r'</?figure[^>]*>', '', content)
    content = re.sub(r'</?div[^>]*>', '', content)
    
    # Convert emphasis
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = content.strip()
    
    return content

def extract_posts_from_xml(xml_file_path):
    """Extract blog posts from WordPress XML export"""
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Define namespaces
    namespaces = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    
    posts = []
    
    for item in root.findall('.//item'):
        # Check if this is a published post (not draft)
        status = item.find('wp:status', namespaces)
        post_type = item.find('wp:post_type', namespaces)
        
        if (status is not None and status.text == 'publish' and 
            post_type is not None and post_type.text == 'post'):
            
            title = item.find('title').text or "Untitled"
            
            # Get post date
            post_date = item.find('wp:post_date', namespaces)
            if post_date is not None and post_date.text:
                try:
                    date_obj = datetime.strptime(post_date.text, '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    date_for_frontmatter = date_obj.strftime('%Y-%m-%d %H:%M:%S %z')
                except:
                    # Fallback if date parsing fails
                    formatted_date = "2020-01-01"
                    date_for_frontmatter = "2020-01-01 00:00:00 +0000"
            else:
                formatted_date = "2020-01-01"
                date_for_frontmatter = "2020-01-01 00:00:00 +0000"
            
            # Get content
            content_elem = item.find('content:encoded', namespaces)
            content = content_elem.text if content_elem is not None else ""
            
            # Get categories/tags
            categories = []
            for category in item.findall('category'):
                if category.text:
                    categories.append(category.text)
            
            posts.append({
                'title': title,
                'date': formatted_date,
                'date_full': date_for_frontmatter,
                'content': content,
                'categories': categories
            })
    
    return posts

def create_jekyll_post(post, posts_dir):
    """Create a Jekyll markdown post file"""
    clean_title_str = clean_title(post['title'])
    filename = f"{post['date']}-{clean_title_str}.md"
    filepath = os.path.join(posts_dir, filename)
    
    # Create Jekyll front matter
    frontmatter = f"""---
layout: post
title: "{post['title']}"
date: {post['date_full']}
categories: {post['categories']}
---

"""
    
    # Clean and format content
    cleaned_content = clean_content(post['content'])
    
    # Write the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + cleaned_content)
    
    return filename

def main():
    xml_file = "/Users/muneebahmaddar/Downloads/contagiousthoughts.WordPress.2025-07-26-2.xml"
    posts_dir = "_posts"
    
    # Create _posts directory if it doesn't exist
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    
    # Extract posts from XML
    posts = extract_posts_from_xml(xml_file)
    
    print(f"Found {len(posts)} published posts")
    
    # Create Jekyll posts
    created_files = []
    for post in posts:
        filename = create_jekyll_post(post, posts_dir)
        created_files.append(filename)
        print(f"Created: {filename}")
    
    print(f"\nSuccessfully created {len(created_files)} blog post files in {posts_dir}/")
    return created_files

if __name__ == "__main__":
    main()