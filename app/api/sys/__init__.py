from fastapi import APIRouter
from app.api.sys.user import router as user_router
from app.api.sys.label import router as label_router
from app.api.sys.knowledge import router as knowledge_router
from app.api.sys.collect import router as collect_router
from app.api.sys.library import router as library_router
from app.api.sys.auth import router as auth_router


router = APIRouter(prefix='/sys')
router.include_router(user_router, prefix='/user', tags=['用户管理'])
router.include_router(label_router, prefix='/label', tags=['标签管理'])
router.include_router(knowledge_router, prefix='/knowledge', tags=['知识管理'])
router.include_router(collect_router, prefix='/collect', tags=['收藏管理'])
router.include_router(library_router, prefix='/library', tags=['知识库管理'])
router.include_router(auth_router, prefix='/auth', tags=['认证管理'])
