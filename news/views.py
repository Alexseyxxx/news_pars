#до
# import requests
# from django.conf import settings
# from django.core.cache import cache
# from django.utils import timezone
# from rest_framework import generics, permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Article
# from .serializers import ArticleSerializer
# from datetime import timedelta


# NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"  # or everything endpoint

# class UpdateArticlesView(APIView):
#     permission_classes = [permissions.IsAuthenticated]  # optional: only for authenticated users

#     def post(self, request):
#         cache_key = "newsapi_update_result"
#         cached = cache.get(cache_key)
#         if cached:
#             return Response({"detail": "Already updated (cached)", "result": cached})

#         api_key = settings.NEWSAPI_KEY if hasattr(settings, "NEWSAPI_KEY") else None
#         if not api_key:
#             api_key = settings.NEWSAPI_KEY if hasattr(settings, "NEWSAPI_KEY") else None
#         if not api_key:
#             return Response({"detail": "NEWSAPI_KEY not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         params = {"apiKey": api_key, "language": "en", "pageSize": 100}
#         resp = requests.get(NEWSAPI_URL, params=params, timeout=10)
#         if resp.status_code != 200:
#             return Response({"detail": "NewsAPI error", "status": resp.status_code}, status=status.HTTP_502_BAD_GATEWAY)

#         data = resp.json()
#         new_articles = []
#         for item in data.get("articles", []):
#             url = item.get("url")
#             if not url:
#                 continue
#             if Article.objects.filter(url=url).exists():
#                 continue
#             art = Article.objects.create(
#                 source_id=(item.get("source") or {}).get("id"),
#                 source_name=(item.get("source") or {}).get("name") or "",
#                 author=item.get("author"),
#                 title=item.get("title") or "",
#                 description=item.get("description"),
#                 url=url,
#                 url_to_image=item.get("urlToImage"),
#                 published_at=item.get("publishedAt") or None,
#                 content=item.get("content"),
#             )
#             new_articles.append(art.pk)

#         result = {"created": len(new_articles)}
#         cache.set(cache_key, result, 30 * 60)  # 30 minutes
#         return Response(result, status=status.HTTP_201_CREATED)

# class ArticleListView(generics.ListAPIView):
#     serializer_class = ArticleSerializer
#     permission_classes = [permissions.AllowAny]
#     queryset = Article.objects.all()

#     def list(self, request, *args, **kwargs):
#         # caching per querystring
#         cache_key = "articles_list:" + request.get_full_path()
#         cached = cache.get(cache_key)
#         if cached:
#             return Response(cached)

#         qs = self.get_queryset()
#         fresh = request.query_params.get("fresh")
#         title_contains = request.query_params.get("title_contains")
#         if fresh and fresh.lower() in ("1", "true", "yes"):
#             since = timezone.now() - timedelta(hours=24)
#             qs = qs.filter(published_at__gte=since)
#         if title_contains:
#             qs = qs.filter(title__icontains=title_contains)

#         page = self.paginate_queryset(qs)
#         serializer = self.get_serializer(page, many=True)
#         data = self.get_paginated_response(serializer.data).data if page is not None else serializer.data
#         cache.set(cache_key, data, 10 * 60)  # cache 10 minutes
#         return Response(data)

import requests
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"

class UpdateArticlesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        api_key = getattr(settings, "NEWSAPI_KEY", None)
        if not api_key:
            return Response({"detail": "NEWSAPI_KEY not configured"}, status=500)

        try:
            data = requests.get(
                NEWSAPI_URL,
                params={"apiKey": api_key, "language": "en", "pageSize": 100},
                timeout=10,
            ).json().get("articles", [])
        except requests.RequestException as e:
            return Response({"detail": f"NewsAPI request failed: {e}"}, status=502)

        existing_urls = set(Article.objects.values_list("url", flat=True))
        articles_to_create = [
            Article(
                source_id=(item.get("source") or {}).get("id"),
                source_name=(item.get("source") or {}).get("name", ""),
                author=item.get("author"),
                title=item.get("title", ""),
                description=item.get("description"),
                url=item["url"],
                url_to_image=item.get("urlToImage"),
                published_at=item.get("publishedAt"),
                content=item.get("content"),
            )
            for item in data
            if item.get("url") and item["url"] not in existing_urls
        ]

        Article.objects.bulk_create(articles_to_create)
        return Response({"created": len(articles_to_create)}, status=201)


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Article.objects.all()
        params = self.request.query_params

        if params.get("fresh") in ("1", "true", "yes"):
            qs = qs.filter(published_at__gte=timezone.now() - timedelta(hours=24))

        if title := params.get("title_contains"):
            qs = qs.filter(title__icontains=title)

        return qs
