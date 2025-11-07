from .list_serializer import MascotaListSerializer
from .detail_serializer import MascotaDetailSerializer
from .create_update_serializer import MacotaCreateUpdateSerializer
from .liked_serializer import LikeModelSerializer


__all__ = [
    "MascotaListSerializer",
    "MascotaDetailSerializer",
    "MacotaCreateUpdateSerializer",
    "LikeModelSerializer",
]
