---
layout: default
permalink: /
title: blog
nav: true
nav_order: 1
pagination:
  enabled: true
  collection: posts
  permalink: /page/:num/
  per_page: 5
  sort_field: date
  sort_reverse: true
  trail:
    before: 1 # The number of links before the current page
    after: 3 # The number of links after the current page
---

<div class="post">

{% assign blog_name_size = site.blog_name | size %}
{% assign blog_description_size = site.blog_description | size %}

{% if blog_name_size > 0 or blog_description_size > 0 %}

  <div class="header-bar">
    <h1>{{ site.blog_name }}</h1>
    <h2>{{ site.blog_description }}</h2>
  </div>
  {% endif %}


{% assign featured_posts = site.posts | where: "featured", "true" %}
{% if featured_posts.size > 0 %}
<div class="featured-posts-section">
<h4 style="margin-bottom: 1rem; font-weight: 300;">Featured Posts</h4>
<ul class="post-list">
{% for post in featured_posts %}
  {% if post.external_source == blank %}
    {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
  {% else %}
    {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
  {% endif %}
  
  <li>
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <p class="post-meta" style="margin: 0;">
        {{ read_time }} min read &nbsp; &middot; &nbsp;
        {{ post.date | date: '%B %d, %Y' }}
        {% if post.external_source %}
        &nbsp; &middot; &nbsp; {{ post.external_source }}
        {% endif %}
      </p>
      <i class="fa-solid fa-thumbtack fa-xs" style="color: var(--global-theme-color);"></i>
    </div>
    <h3>
      <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
    <p>{{ post.description }}</p>
  </li>
{% endfor %}
</ul>
</div>
<hr style="margin: 2rem 0;">

{% endif %}

{% if site.display_tags or site.display_categories %}
<div class="tags-categories-section">
<h4 style="margin-bottom: 1rem; font-weight: 300;">Browse by Topic</h4>
<div class="tag-category-list">
  <ul class="p-0 m-0">
    {% for tag in site.display_tags %}
      <li>
        <i class="fa-solid fa-hashtag fa-sm"></i> <a href="{{ tag | slugify | prepend: '/blog/tag/' | relative_url }}">{{ tag }}</a>
      </li>
      {% unless forloop.last %}
        <p>&bull;</p>
      {% endunless %}
    {% endfor %}
    {% if site.display_categories.size > 0 and site.display_tags.size > 0 %}
      <p>&bull;</p>
    {% endif %}
    {% for category in site.display_categories %}
      <li>
        <i class="fa-solid fa-tag fa-sm"></i> <a href="{{ category | slugify | prepend: '/blog/category/' | relative_url }}">{{ category }}</a>
      </li>
      {% unless forloop.last %}
        <p>&bull;</p>
      {% endunless %}
    {% endfor %}
  </ul>
</div>
</div>
<hr style="margin: 2rem 0;">
{% endif %}

  <!-- Blog Post Tabs -->
  <div class="blog-tabs">
    <ul class="nav nav-tabs" id="blogTabs" role="tablist">
      <li class="nav-item" role="presentation">
        <a class="nav-link active" id="latest-tab" data-toggle="tab" href="#latest" role="tab" aria-controls="latest" aria-selected="true">Latest</a>
      </li>
      <li class="nav-item" role="presentation">
        <a class="nav-link" id="popular-tab" data-toggle="tab" href="#popular" role="tab" aria-controls="popular" aria-selected="false">Popular</a>
      </li>
    </ul>
    
    <div class="tab-content" id="blogTabContent">
      <!-- Latest Posts Tab -->
      <div class="tab-pane fade show active" id="latest" role="tabpanel" aria-labelledby="latest-tab">
        <ul class="post-list">

    {% if page.pagination.enabled %}
      {% assign postlist = paginator.posts %}
    {% else %}
      {% assign postlist = site.posts %}
    {% endif %}

    {% for post in postlist %}

    {% if post.external_source == blank %}
      {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
    {% else %}
      {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
    {% endif %}
    {% assign year = post.date | date: "%Y" %}
    {% assign tags = post.tags | join: "" %}
    {% assign categories = post.categories | join: "" %}

    <li>

{% if post.thumbnail %}

<div class="row">
          <div class="col-sm-9">
{% endif %}
      <p class="post-meta">
        {{ read_time }} min read &nbsp; &middot; &nbsp;
        {{ post.date | date: '%B %d, ' }}<a href="{{ year | prepend: '/blog/' | prepend: site.baseurl}}">{{ year }}</a>
        {% if post.external_source %}
        &nbsp; &middot; &nbsp; {{ post.external_source }}
        {% endif %}
      </p>
        <h3>
        {% if post.redirect == blank %}
          <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
        {% elsif post.redirect contains '://' %}
          <a class="post-title" href="{{ post.redirect }}" target="_blank">{{ post.title }}</a>
          <svg width="2rem" height="2rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
            <path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        {% else %}
          <a class="post-title" href="{{ post.redirect | relative_url }}">{{ post.title }}</a>
        {% endif %}
      </h3>
      <p>{{ post.description }}</p>

{% if post.thumbnail %}

</div>

  <div class="col-sm-3">
    <img class="card-img" src="{{post.thumbnail | relative_url}}" style="object-fit: cover; height: 90%" alt="image">
  </div>
</div>
{% endif %}
    </li>

    {% endfor %}

        </ul>
        
        {% if page.pagination.enabled %}
        {% include pagination.liquid %}
        {% endif %}
      </div>
      
      <!-- Popular Posts Tab -->
      <div class="tab-pane fade" id="popular" role="tabpanel" aria-labelledby="popular-tab">
        <ul class="post-list">
        {% comment %} Sort by rank (1 = highest), then by date for same rank or no rank {% endcomment %}
        {% assign ranked_posts = '' | split: '' %}
        {% assign unranked_posts = '' | split: '' %}
        
        {% comment %} Separate ranked and unranked posts {% endcomment %}
        {% for post in site.posts %}
          {% if post.rank %}
            {% assign ranked_posts = ranked_posts | push: post %}
          {% else %}
            {% assign unranked_posts = unranked_posts | push: post %}
          {% endif %}
        {% endfor %}
        
        {% comment %} Sort ranked posts by rank (ascending), then by date (descending) {% endcomment %}
        {% assign sorted_ranked = ranked_posts | sort: 'rank' | sort: 'date' | reverse | group_by: 'rank' %}
        {% assign popular_posts = '' | split: '' %}
        {% for rank_group in sorted_ranked %}
          {% assign group_posts = rank_group.items | sort: 'date' | reverse %}
          {% for post in group_posts %}
            {% assign popular_posts = popular_posts | push: post %}
          {% endfor %}
        {% endfor %}
        
        {% comment %} Add unranked posts at the end, sorted by date {% endcomment %}
        {% assign sorted_unranked = unranked_posts | sort: 'date' | reverse %}
        {% for post in sorted_unranked %}
          {% assign popular_posts = popular_posts | push: post %}
        {% endfor %}
        
        {% for post in popular_posts limit: 10 %}
        {% if post.external_source == blank %}
          {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
        {% else %}
          {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
        {% endif %}
        {% assign year = post.date | date: "%Y" %}
        {% assign tags = post.tags | join: "" %}
        {% assign categories = post.categories | join: "" %}

        <li>
        {% if post.thumbnail %}
        <div class="row">
          <div class="col-sm-9">
        {% endif %}
        <p class="post-meta">
        {{ read_time }} min read &nbsp; &middot; &nbsp;
        {{ post.date | date: '%B %d, ' }}<a href="{{ year | prepend: '/blog/' | prepend: site.baseurl}}">{{ year }}</a>
        {% if post.external_source %}
        &nbsp; &middot; &nbsp; {{ post.external_source }}
        {% endif %}
        </p>
        <h3>
        {% if post.redirect == blank %}
          <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
        {% elsif post.redirect contains '://' %}
          <a class="post-title" href="{{ post.redirect }}" target="_blank">{{ post.title }}</a>
          <svg width="2rem" height="2rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
            <path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        {% else %}
          <a class="post-title" href="{{ post.redirect | relative_url }}">{{ post.title }}</a>
        {% endif %}
        </h3>
        <p>{{ post.description }}</p>

        {% if post.thumbnail %}
        </div>
        <div class="col-sm-3">
        <img class="card-img" src="{{post.thumbnail | relative_url}}" style="object-fit: cover; height: 90%" alt="image">
        </div>
        </div>
        {% endif %}
        </li>
        {% endfor %}
        </ul>
      </div>
    </div>
  </div>

</div>
