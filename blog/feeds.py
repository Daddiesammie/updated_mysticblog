from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import BlogPost

class LatestPostsFeed(Feed):
    title = "My Blog Latest Posts"
    link = "/rss/"
    description = "Latest posts from My Blog"

    def items(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:200] + '...' if len(item.content) > 200 else item.content

    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.slug])

    def item_pubdate(self, item):
        return item.published_at

    def item_categories(self, item):
        return [category.name for category in item.categories.all()]