from app.routers.auth.docs import auth_docs
from app.routers.user.docs import user_docs

router_docs = {
    "name": "article-backend",
    "description": "API методы",
}

docs_tags = [
    auth_docs,
    user_docs,
    user_docs,
]
